from engine.inference_engine import forward_chain
from knowledge_base.rules import RULES

def run(**overrides):
    base={"glucose":"Negative","protein":"Negative","pH":6.0,"ketones":"Negative","blood":"Negative","bilirubin":"Negative","urobilinogen":0.2,"nitrite":"Negative","leukocytes":"Negative","specific_gravity":1.015,"sample_valid":True,"timed_correctly":True,"available_count":10,"any_abnormal":False}
    base.update(overrides)
    return forward_chain(base,RULES)

def ids(result): return {x.rule_id for x in result.fired_rules}

def test_normal():
    r=run(); assert {"Q03","S03"} <= ids(r); assert not ({"G01","G02","X01"}&ids(r))

def test_abnormal_single():
    r=run(glucose="+",any_abnormal=True); assert {"G01","S02"} <= ids(r)

def test_combination():
    r=run(glucose="+",ketones="++",nitrite="Positive",leukocytes="Small",any_abnormal=True)
    assert {"X01","X03","G07","G08"} <= ids(r)

def test_invalid_or_mistimed_suppresses_interpretation():
    for override in ({"sample_valid":False},{"timed_correctly":False}):
        r=run(glucose="+++",**override)
        assert "Q01" in ids(r) or "Q02" in ids(r)
        assert "G01" not in ids(r)

def test_missing_unknown():
    r=run(glucose=None,protein=None,pH=None,ketones=None,blood=None,bilirubin=None,urobilinogen=None,nitrite=None,leukocytes=None,specific_gravity=None,available_count=0)
    assert {"Q04","Q05"} <= ids(r)

def test_duplicate_prevention_and_conflict_priority():
    # A high-priority quality advisory sorts before lower-priority analyte rules; no duplicates.
    r=run(sample_valid=False,glucose="+")
    got=[x.rule_id for x in r.fired_rules]
    assert len(got)==len(set(got)) and got.index("Q01") < got.index("S03")

def test_unsupported_value_is_not_matched():
    assert "G01" not in ids(run(glucose="purple"))
