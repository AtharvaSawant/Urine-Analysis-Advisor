"""Reusable, data-driven forward chaining engine for the educational prototype."""
from dataclasses import dataclass, field
from typing import Any, Iterable

@dataclass(frozen=True)
class Rule:
    id: str
    category: str
    conditions: tuple[dict[str, Any], ...]
    conclusions: tuple[dict[str, Any], ...]
    message: str
    rationale: str
    source_ids: tuple[str, ...]
    priority: int = 50

@dataclass
class FiredRule:
    rule_id: str
    category: str
    conditions: list[str]
    conclusions: list[dict[str, Any]]
    message: str
    rationale: str
    source_ids: list[str]
    priority: int

@dataclass
class InferenceResult:
    initial_facts: dict[str, Any]
    working_memory: dict[str, Any]
    fired_rules: list[FiredRule] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    iterations: int = 0

OPS = {
    "eq": lambda a,b: a == b,
    "ne": lambda a,b: a != b,
    "in": lambda a,b: a in b,
    "not_in": lambda a,b: a not in b,
    "gt": lambda a,b: float(a) > float(b),
    "ge": lambda a,b: float(a) >= float(b),
    "lt": lambda a,b: float(a) < float(b),
    "le": lambda a,b: float(a) <= float(b),
    "exists": lambda a,b: a is not None,
}

def _match(condition: dict[str, Any], facts: dict[str, Any]) -> bool:
    key, op = condition["fact"], condition["op"]
    if key not in facts:
        return False
    value = facts[key]
    if value is None or value == "Unknown":
        return False
    try:
        return OPS[op](value, condition.get("value"))
    except (TypeError, ValueError, KeyError):
        return False

def _render(c: dict[str, Any]) -> str:
    labels = {"eq":"=", "ne":"≠", "in":"in", "not_in":"not in", "gt":">", "ge":"≥", "lt":"<", "le":"≤", "exists":"is present"}
    return f"{c['fact']} {labels[c['op']]} {c.get('value','')}".strip()

def forward_chain(facts: dict[str, Any], rules: Iterable[Rule], max_iterations: int = 100) -> InferenceResult:
    """Fire each matching rule once; conclusions become facts for later rules."""
    wm = dict(facts)
    result = InferenceResult(dict(facts), wm)
    rules = sorted(rules, key=lambda r: (-r.priority, r.id))
    fired: set[str] = set()
    for iteration in range(max_iterations):
        result.iterations = iteration + 1
        changed = False
        for rule in rules:
            if rule.id in fired:
                continue
            # Invalid or mistimed strips can produce quality advisories, but not analyte interpretation.
            if (wm.get("sample_valid") is False or wm.get("timed_correctly") is False) and rule.category in {"Individual findings", "Combined findings", "Repeat testing"}:
                continue
            if not all(_match(c, wm) for c in rule.conditions):
                continue
            fired.add(rule.id)
            result.fired_rules.append(FiredRule(rule.id, rule.category, [_render(c) for c in rule.conditions], list(rule.conclusions), rule.message, rule.rationale, list(rule.source_ids), rule.priority))
            for item in rule.conclusions:
                key, value = item["fact"], item["value"]
                if key not in wm:
                    wm[key] = value
                    changed = True
                elif isinstance(wm[key], list) and value not in wm[key]:
                    wm[key].append(value)
                    changed = True
        if not changed:
            break
    else:
        result.warnings.append("Inference stopped at the configured iteration limit.")
    result.fired_rules.sort(key=lambda x: (-x.priority, x.rule_id))
    result.working_memory = wm
    return result
