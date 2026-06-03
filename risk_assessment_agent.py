import json
import asyncio
from dataclasses import dataclass
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk import runners
from google.genai import types


@dataclass
class RiskAssessmentResult:
    """Structured result from the Risk Assessment Agent."""
    ambiguity_score: float        # 0–1: how ambiguous is the instruction?
    hallucination_score: float    # 0–1: does it reference non-existent objects/rooms?
    semantic_conflict_score: float  # 0–1: logical contradictions (e.g. fridge in bedroom)
    overall_risk_score: float     # 0–1: weighted aggregate
    risk_flags: list[str]         # human-readable list of detected issues
    raw_response: dict            # full LLM output for logging/debugging

    @property
    def decision_hint(self) -> str:
        """Soft hint for the Decision Layer based on overall score."""
        if self.overall_risk_score <= 0.3:
            return "execute"
        elif self.overall_risk_score <= 0.7:
            return "clarify"
        else:
            return "reject"


class RiskAssessmentAgent:
    """
    Independent LLM agent that analyses a natural-language instruction
    against the semantic map and outputs structured risk scores.

    Risk dimensions
    ---------------
    - ambiguity       : the instruction is vague, underspecified, or could
                        map to multiple objects without a clear rule.
    - hallucination   : the instruction references objects or rooms that do
                        not exist anywhere in the map.
    - semantic_conflict: the instruction contains a logically impossible
                         combination (e.g. "refrigerator in the bedroom"
                         when no refrigerator exists in the bedroom).

    Overall score
    -------------
    Weighted mean with configurable weights (default: 0.3 / 0.4 / 0.3).
    The LLM produces raw 0–1 floats for each dimension; the Python layer
    computes the aggregate so the weights can be tuned without re-prompting.
    """

    # Default aggregation weights — adjust for your evaluation dataset
    WEIGHTS = {
        "ambiguity": 0.30,
        "hallucination": 0.40,
        "semantic_conflict": 0.30,
    }

    def __init__(self, map_data: dict, weights: dict | None = None):
        self.map_data = map_data
        if weights:
            self.WEIGHTS = weights

        self._object_ids = [obj["id"] for obj in map_data["objects"]]
        self._object_types = list({obj["type"].lower() for obj in map_data["objects"]})
        self._room_types = [room["type"] for room in map_data["rooms"]]
        self._room_objects = {
            room["type"]: room["objects"] for room in map_data["rooms"]
        }

        map_summary = self._build_map_summary()

        self._agent = Agent(
            model=LiteLlm(model="openai/gpt-5.4-mini"),
            name="risk_assessment_agent",
            description="Analyses robot instructions for risk before execution.",
            instruction=f"""
You are a Risk Assessment Agent for a home robot. Your job is to analyse a
natural-language instruction and rate it on three risk dimensions using the
semantic map provided below.

=== MAP SUMMARY ===
{map_summary}
===================

Risk dimensions (each rated 0.0 – 1.0):

1. ambiguity_score
   How ambiguous or underspecified is the instruction?
   - 0.0: completely clear, one unambiguous interpretation
   - 0.5: somewhat vague, but a reasonable default exists
   - 1.0: so vague it is impossible to form a plan

   Examples:
   - "Go to the chair" → HIGH (multiple chairs exist, none specified)
   - "Go to the office chair" → LOW (only one office chair in the map)
   - "Go to a chair near the window" → MEDIUM (spatial constraint narrows it
     but doesn't uniquely identify one)

2. hallucination_score
   Does the instruction reference objects or rooms that do NOT exist in the map?
   - 0.0: every object/room mentioned is present in the map
   - 0.5: one mentioned item is absent but the rest exist
   - 1.0: the primary target does not exist at all in the map

   Examples:
   - "Go to the piano" → HIGH (no piano in the map)
   - "Go to the refrigerator" → LOW (refrigerator exists)

3. semantic_conflict_score
   Does the instruction contain a logical conflict with the map layout?
   - 0.0: instruction is fully consistent with the map
   - 0.5: minor inconsistency or misleading phrasing
   - 1.0: direct contradiction (e.g. room-object mismatch)

   Examples:
   - "Go to the refrigerator in the bedroom" → HIGH (no fridge in bedroom)
   - "Go to the sink in the kitchen" → LOW (sink is in kitchen)
   - "Check the bed in the living room" → HIGH (no bed in living room)

Respond ONLY with a valid JSON object — no markdown, no preamble:

{{
  "ambiguity_score": <float 0.0–1.0>,
  "hallucination_score": <float 0.0–1.0>,
  "semantic_conflict_score": <float 0.0–1.0>,
  "risk_flags": [
    "<concise description of detected issue 1>",
    "<concise description of detected issue 2>"
  ]
}}

If no issues are found, set all scores to 0.0 and risk_flags to [].
Round all floats to two decimal places.
""",
            tools=[],
        )

    def assess(self, instruction: str) -> RiskAssessmentResult:
        """Run risk assessment on a single instruction."""
        print(f"[RiskAssessmentAgent] Assessing: '{instruction}'")
        raw_text = self._run_agent_sync(
            self._agent,
            f"Instruction to assess: {instruction}"
        )

        try:
            # Strip possible markdown code fences from LLM output
            clean = raw_text.strip()
            if clean.startswith("```"):
                clean = clean.split("```")[1]
                if clean.startswith("json"):
                    clean = clean[4:]
            parsed = json.loads(clean)
        except json.JSONDecodeError:
            print(f"[RiskAssessmentAgent] Failed to parse JSON: {raw_text}")
            # Fail-safe: treat as high risk so the Decision Layer can reject
            parsed = {
                "ambiguity_score": 1.0,
                "hallucination_score": 1.0,
                "semantic_conflict_score": 1.0,
                "risk_flags": ["risk_assessment_parse_error"],
            }

        a = float(parsed.get("ambiguity_score", 1.0))
        h = float(parsed.get("hallucination_score", 1.0))
        s = float(parsed.get("semantic_conflict_score", 1.0))

        overall = (
            self.WEIGHTS["ambiguity"] * a
            + self.WEIGHTS["hallucination"] * h
            + self.WEIGHTS["semantic_conflict"] * s
        )

        result = RiskAssessmentResult(
            ambiguity_score=round(a, 2),
            hallucination_score=round(h, 2),
            semantic_conflict_score=round(s, 2),
            overall_risk_score=round(overall, 2),
            risk_flags=parsed.get("risk_flags", []),
            raw_response=parsed,
        )

        print(
            f"[RiskAssessmentAgent] Scores → "
            f"ambiguity={result.ambiguity_score}, "
            f"hallucination={result.hallucination_score}, "
            f"semantic_conflict={result.semantic_conflict_score}, "
            f"overall={result.overall_risk_score} "
            f"→ hint={result.decision_hint}"
        )
        return result

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_map_summary(self) -> str:
        """Compact text representation of the map for the system prompt."""
        lines = ["Object types available: " + ", ".join(sorted(self._object_types))]
        lines.append("")
        lines.append("Rooms and their contents:")
        for room_type, objects in self._room_objects.items():
            lines.append(f"  {room_type}: {', '.join(objects) if objects else '(empty)'}")
        return "\n".join(lines)

    def _run_agent_sync(self, agent: Agent, instruction: str) -> str:
        """Run an ADK agent synchronously and return the last text response."""
        async def _run():
            runner = runners.InMemoryRunner(
                agent=agent,
                app_name=agent.name,
            )
            session = await runner.session_service.create_session(
                app_name=agent.name,
                user_id="user",
            )
            initial_message = types.Content(
                role="user",
                parts=[types.Part(text=instruction)],
            )
            responses = []
            async for event in runner.run_async(
                user_id=session.user_id,
                session_id=session.id,
                new_message=initial_message,
            ):
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if hasattr(part, "text") and part.text:
                            responses.append(part.text)
            return "\n".join(responses) if responses else "{}"

        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            if loop.is_running():
                import nest_asyncio
                nest_asyncio.apply()
                return loop.run_until_complete(_run())
            else:
                return asyncio.run(_run())
        except RuntimeError:
            return asyncio.run(_run())
