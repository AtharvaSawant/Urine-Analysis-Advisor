from .inference_engine import InferenceResult

def explain(result: InferenceResult) -> list[dict]:
    """Return a UI-friendly trace in firing order."""
    return [{"Rule ID": x.rule_id, "Category": x.category, "Matched conditions": "; ".join(x.conditions), "Advisory": x.message, "Why": x.rationale, "Sources": ", ".join(x.source_ids), "Priority": x.priority} for x in result.fired_rules]
