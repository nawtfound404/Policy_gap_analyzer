from llm_engine import Phi3PolicyDraftingEngine
from pprint import pprint

engine = Phi3PolicyDraftingEngine()

result = engine.generate_gap_response(
    control_id="RS.MA",
    control_intent="Define incident response roles, escalation paths, and response timelines",
    gap_description=(
        "The policy mentions incident handling but does not define "
        "roles, escalation paths, or response timelines."
    )
)

pprint(result)