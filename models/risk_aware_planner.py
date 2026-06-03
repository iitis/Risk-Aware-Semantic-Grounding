"""
risk_aware_planner.py
---------------------
Top-level pipeline that wires together:
  1. RiskAssessmentAgent  – LLM-based risk scoring (3 dimensions, 0–1 float)
  2. DecisionLayer        – threshold-based gate (execute / clarify / reject)
  3. PlannerAgent         – existing map-aware planner (only called on execute)

Usage
-----
  python risk_aware_planner.py

Evaluation helper
-----------------
  Call `run_evaluation(dataset_path)` to score the pipeline against a JSON
  dataset in the same format as `dataset_query_decision_gt.json`.
"""

import json
from dataclasses import asdict

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from map_manager import load_map_data
from point import Point
# from planner_agent import PlannerAgent          
#from models.planner_agent import PlannerAgent
from models.risk_aware_planner_agent import RiskAwarePlannerAgent

from risk_assessment_agent import RiskAssessmentAgent
from decision_layer import DecisionLayer, DecisionResult


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

class RiskAwarePlanner:
    """
    Orchestrates risk assessment → decision gating → planning.

    Parameters
    ----------
    map_data : dict
        Loaded smart_home_map.json content.
    execute_threshold : float
        overall_risk_score ≤ this → execute (default 0.30).
    clarify_threshold : float
        overall_risk_score ≤ this → clarify, else reject (default 0.70).
    risk_weights : dict | None
        Custom weights for ambiguity / hallucination / semantic_conflict.
    """

    def __init__(
        self,
        map_data: dict,
        execute_threshold: float = 0.30,
        clarify_threshold: float = 0.70,
        risk_weights: dict | None = None,
        hard_ambiguity_ceiling: float = 0.40,
    ):
        self.map_data = map_data
        self.risk_agent = RiskAssessmentAgent(map_data, weights=risk_weights)
        self.decision_layer = DecisionLayer(
            execute_threshold=execute_threshold,
            clarify_threshold=clarify_threshold,
            hard_ambiguity_ceiling=hard_ambiguity_ceiling,
        )
        self.planner = RiskAwarePlannerAgent(map_data)

    def run(self, start: Point, instruction: str) -> dict:
        """
        Execute the full pipeline for one instruction.

        Returns
        -------
        dict with keys:
          - decision      : "execute" | "clarify" | "reject"
          - plan          : list of object IDs (empty if not executed)
          - answer        : robot-facing response string
          - risk          : dict of all risk scores and flags
          - reason        : decision layer explanation
        """
        print("\n" + "="*60)
        print(f"Instruction : {instruction}")
        print(f"Start pos   : ({start.x}, {start.y})")
        print("="*60)

        # Step 1 – Risk Assessment
        risk = self.risk_agent.assess(instruction)

        # Step 2 – Decision Gate
        dec: DecisionResult = self.decision_layer.decide(risk)
        print(f"[DecisionLayer] {dec.decision.upper()} — {dec.reason}")

        # Step 3 – Plan (only if execute)
        plan_output = {"decision": dec.decision, "plan": [], "answer": ""}

        if dec.decision == "execute":
            raw = self.planner.plan(start, instruction)
            # planner.plan() returns a dict with plan/answer/decision keys
            if isinstance(raw, dict):
                plan_output["plan"] = raw.get("plan", [])
                plan_output["answer"] = raw.get("answer", "")
            else:
                plan_output["plan"] = []
                plan_output["answer"] = str(raw)

        elif dec.decision == "clarify":
            plan_output["answer"] = (
                "I need a bit more information before I can proceed. "
                + "; ".join(risk.risk_flags)
            )

        else:  # reject
            plan_output["answer"] = (
                "I'm sorry, I cannot execute this instruction. "
                + "; ".join(risk.risk_flags)
            )

        plan_output["risk"] = {
            "ambiguity_score": risk.ambiguity_score,
            "hallucination_score": risk.hallucination_score,
            "semantic_conflict_score": risk.semantic_conflict_score,
            "overall_risk_score": risk.overall_risk_score,
            "risk_flags": risk.risk_flags,
        }
        plan_output["reason"] = dec.reason

        print(f"[Pipeline]     decision={plan_output['decision']}, "
              f"plan={plan_output['plan']}")
        return plan_output


# ---------------------------------------------------------------------------
# Evaluation helper
# ---------------------------------------------------------------------------

def run_evaluation(
    dataset_path: str,
    map_data: dict,
    execute_threshold: float = 0.30,
    clarify_threshold: float = 0.70,
) -> dict:
    """
    Score the pipeline against a ground-truth dataset.

    Expected dataset format (list of objects):
    [
      {
        "instruction": "...",
        "start": {"x": 0.2, "y": 4.0},
        "ground_truth_decision": "execute" | "clarify" | "reject"
      },
      ...
    ]

    Returns a summary dict with per-class metrics and overall accuracy.
    """
    with open(dataset_path) as f:
        dataset = json.load(f)

    planner = RiskAwarePlanner(
        map_data,
        execute_threshold=execute_threshold,
        clarify_threshold=clarify_threshold,
    )

    results = []
    correct = 0

    for item in dataset:
        instruction = item["instruction"]
        start = Point(
            x=item.get("start", {}).get("x", 0.0),
            y=item.get("start", {}).get("y", 0.0),
        )
        gt = item.get("ground_truth_decision", "").lower()

        out = planner.run(start, instruction)
        pred = out["decision"]
        is_correct = pred == gt
        if is_correct:
            correct += 1

        results.append({
            "instruction": instruction,
            "ground_truth": gt,
            "predicted": pred,
            "correct": is_correct,
            "overall_risk_score": out["risk"]["overall_risk_score"],
            "risk_flags": out["risk"]["risk_flags"],
        })

    accuracy = correct / len(dataset) if dataset else 0.0

    # Per-class precision / recall
    classes = ["execute", "clarify", "reject"]
    metrics = {}
    for cls in classes:
        tp = sum(1 for r in results if r["ground_truth"] == cls and r["predicted"] == cls)
        fp = sum(1 for r in results if r["ground_truth"] != cls and r["predicted"] == cls)
        fn = sum(1 for r in results if r["ground_truth"] == cls and r["predicted"] != cls)
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall    = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1        = (2 * precision * recall / (precision + recall)
                     if (precision + recall) > 0 else 0.0)
        metrics[cls] = {"precision": round(precision, 3),
                        "recall": round(recall, 3),
                        "f1": round(f1, 3)}

    summary = {
        "total": len(dataset),
        "correct": correct,
        "accuracy": round(accuracy, 3),
        "per_class": metrics,
        "results": results,
    }

    print("\n=== EVALUATION SUMMARY ===")
    print(f"Accuracy : {summary['accuracy']:.1%}  ({correct}/{len(dataset)})")
    for cls, m in metrics.items():
        print(f"  {cls:8s}  P={m['precision']:.3f}  R={m['recall']:.3f}  F1={m['f1']:.3f}")

    return summary


# ---------------------------------------------------------------------------
# Quick test
# ---------------------------------------------------------------------------
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    map_data = load_map_data(os.path.join(BASE_DIR, "dataset", "smart_home_map.json"))

    if not map_data:
        print("Failed to load map data.")
        exit(1)

    planner = RiskAwarePlanner(map_data)

    test_cases = [
        # (instruction, expected_hint)
        ("Visit the refrigerator and then inspect the piano.",           "reject")
        # ("Go to the refrigerator in the bedroom.",                       "reject"),
        # ("Go to the chair.",                                             "clarify"),
        # ("Before heading to the office chair, check the kitchen table.", "execute"),
        # ("Go to the bookshelf in Bedroom 2.",                           "execute"),
    ]

    for instruction, expected in test_cases:
        out = planner.run(Point(x=0.2, y=4.0), instruction)
        status = "✓" if out["decision"] == expected else "✗"
        print(f"\n{status} [{expected} / {out['decision']}] {instruction}")
        print(f"   risk={out['risk']['overall_risk_score']}  flags={out['risk']['risk_flags']}")