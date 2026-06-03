import json
import time
import sys
import os
import sys, os
from map_manager import load_map_data
from point import Point

#from models.planner_agent import PlannerAgent
from models.risk_aware_planner_agent import RiskAwarePlannerAgent
from decision_layer import DecisionLayer
from models.risk_aware_planner import RiskAwarePlanner
from risk_assessment_agent import RiskAssessmentResult, RiskAssessmentAgent


if __name__ == "__main__":

    # --- Load data ---
    map_data = load_map_data("dataset/smart_home_map.json")
    if not map_data:
        print("Failed to load map data.")
        exit(1)
    print(f"Map loaded. Objects: {len(map_data['objects'])}")

    dataset = load_map_data("dataset/dataset_query_decision_gt.json")
    if not dataset:
        print("Failed to load dataset.")
        exit(1)
    entries = dataset["dataset"]
    print(f"Dataset loaded. Entries: {len(entries)}\n")

    # --- Planner ---
    planner = RiskAwarePlanner(
        map_data,
        execute_threshold=0.30,
        clarify_threshold=0.70,
        hard_ambiguity_ceiling=0.75,  
    )

    results = {"results": []}
    start_time = time.time()
    total = len(entries)

    for index, entry in enumerate(entries, 1):
        entry_start = time.time()
        query = entry["query"]
        print(f"\n[{index}/{total}] {query}")

        # RUN PIPELINE
        out = planner.run(Point(x=0.2, y=4.0), query)

        # Sadece dışa aktarılacak alanları tut
        planner_result = {
            "decision": out["decision"],
            "plan":     out["plan"],
            "answer":   out["answer"],
            "risk": {
                "ambiguity_score":        out["risk"]["ambiguity_score"],
                "hallucination_score":    out["risk"]["hallucination_score"],
                "semantic_conflict_score": out["risk"]["semantic_conflict_score"],
                "overall_risk_score":     out["risk"]["overall_risk_score"],
                "risk_flags":             out["risk"]["risk_flags"],
            },
        }

        entry_elapsed = time.time() - entry_start
        elapsed      = time.time() - start_time
        eta          = (total - index) * (elapsed / index)
        print(f"  → decision={out['decision']}  risk={out['risk']['overall_risk_score']}"
              f"  [{entry_elapsed:.1f}s | ETA {eta:.0f}s]")

        results["results"].append({
            "query":        query,
            "category":     entry.get("category", ""),
            "decision":     entry.get("decision", ""),      # ground truth
            "ground_truth": entry.get("ground_truth", []),
            "result": [
                {
                    "planner": "RiskAwarePlannerAgent",
                    "result":  planner_result,
                }
            ],
        })

    total_time = time.time() - start_time
    print(f"\n{'='*60}")
    print(f"Completed in {total_time:.1f}s  ({total_time/60:.1f} min)")
    print(f"Average per entry: {total_time/total:.1f}s")
    print(f"{'='*60}\n")

    # --- Kaydet ---
    # os.makedirs(os.path.join(BASE_DIR, "results"), exist_ok=True)
    # out_path = os.path.join(BASE_DIR, "results", "risk_aware_results.json")
    out_path = os.path.join("results/risk_aware_results.json")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    print(f"Results saved → {out_path}")
