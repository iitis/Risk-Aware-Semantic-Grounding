from dataclasses import dataclass
from risk_assessment_agent import RiskAssessmentResult
# from models.risk_assessment_agent import RiskAssessmentResult

@dataclass
class DecisionResult:
    """Output of the Decision Layer."""
    decision: str          # "execute" | "clarify" | "reject"
    risk: RiskAssessmentResult
    reason: str            # human-readable explanation for logging / response


class DecisionLayer:
    """
    Threshold-based decision gate that sits between the Risk Assessment
    Agent and the Planner Agent.

    Thresholds (all configurable)
    ------------------------------
    overall_risk_score ≤ EXECUTE_THRESHOLD          → execute
    EXECUTE_THRESHOLD < score ≤ CLARIFY_THRESHOLD   → clarify
    score > CLARIFY_THRESHOLD                       → reject

    Hard-reject overrides
    ----------------------
    Even if the overall score is low, the instruction is immediately
    rejected when any single-dimension score exceeds its hard ceiling.
    This prevents a low-ambiguity instruction with a complete
    hallucination from slipping through.

    Default values are tuned on the provided evaluation dataset but can
    be overridden at construction time for ablation experiments.
    """

    # Soft thresholds on the aggregate score
    EXECUTE_THRESHOLD: float = 0.30
    CLARIFY_THRESHOLD: float = 0.70

    # Hard per-dimension ceilings (None = disabled)
    HARD_HALLUCINATION_CEILING: float = 0.80
    HARD_CONFLICT_CEILING: float = 0.85
    HARD_AMBIGUITY_CEILING: float = 0.90

    def __init__(
        self,
        execute_threshold: float | None = None,
        clarify_threshold: float | None = None,
        hard_hallucination_ceiling: float | None = None,
        hard_conflict_ceiling: float | None = None,
        hard_ambiguity_ceiling: float | None = None,
    ):
        if execute_threshold is not None:
            self.EXECUTE_THRESHOLD = execute_threshold
        if clarify_threshold is not None:
            self.CLARIFY_THRESHOLD = clarify_threshold
        if hard_hallucination_ceiling is not None:
            self.HARD_HALLUCINATION_CEILING = hard_hallucination_ceiling
        if hard_conflict_ceiling is not None:
            self.HARD_CONFLICT_CEILING = hard_conflict_ceiling
        if hard_ambiguity_ceiling is not None:
            self.HARD_AMBIGUITY_CEILING = hard_ambiguity_ceiling

    def decide(self, risk: RiskAssessmentResult) -> DecisionResult:
        """
        Apply threshold rules and return a DecisionResult.

        Hard-reject overrides are checked first; soft thresholds second.
        """
        # --- Hard-reject overrides ---
        if (
            self.HARD_HALLUCINATION_CEILING is not None
            and risk.hallucination_score > self.HARD_HALLUCINATION_CEILING
        ):
            return DecisionResult(
                decision="reject",
                risk=risk,
                reason=(
                    f"Hard reject: hallucination_score={risk.hallucination_score} "
                    f"exceeds ceiling={self.HARD_HALLUCINATION_CEILING}. "
                    f"Flags: {risk.risk_flags}"
                ),
            )

        if (
            self.HARD_CONFLICT_CEILING is not None
            and risk.semantic_conflict_score > self.HARD_CONFLICT_CEILING
        ):
            return DecisionResult(
                decision="reject",
                risk=risk,
                reason=(
                    f"Hard reject: semantic_conflict_score={risk.semantic_conflict_score} "
                    f"exceeds ceiling={self.HARD_CONFLICT_CEILING}. "
                    f"Flags: {risk.risk_flags}"
                ),
            )

        if (
            self.HARD_AMBIGUITY_CEILING is not None
            and risk.ambiguity_score > self.HARD_AMBIGUITY_CEILING
        ):
            return DecisionResult(
                decision="clarify",
                risk=risk,
                reason=(
                    f"Hard clarify: ambiguity_score={risk.ambiguity_score} "
                    f"exceeds ceiling={self.HARD_AMBIGUITY_CEILING}. "
                    f"Flags: {risk.risk_flags}"
                ),
            )

        # --- Soft threshold on aggregate score ---
        score = risk.overall_risk_score

        if score <= self.EXECUTE_THRESHOLD:
            return DecisionResult(
                decision="execute",
                risk=risk,
                reason=f"Low risk (score={score}). Proceeding to Planner Agent.",
            )

        if score <= self.CLARIFY_THRESHOLD:
            return DecisionResult(
                decision="clarify",
                risk=risk,
                reason=(
                    f"Medium risk (score={score}). "
                    f"Requesting clarification. Flags: {risk.risk_flags}"
                ),
            )

        return DecisionResult(
            decision="reject",
            risk=risk,
            reason=(
                f"High risk (score={score}). "
                f"Instruction rejected. Flags: {risk.risk_flags}"
            ),
        )
