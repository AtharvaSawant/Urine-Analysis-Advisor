from engine.inference_engine import Rule, forward_chain

def rule(i, cond, conclusion):
    return Rule(i,"test",(cond,),(conclusion,),"message","reason",("S",),50)

def test_forward_chain_derives_until_fixed_point():
    rules=[rule("R1",{"fact":"x","op":"eq","value":1},{"fact":"y","value":2}), rule("R2",{"fact":"y","op":"eq","value":2},{"fact":"z","value":3})]
    result=forward_chain({"x":1},rules)
    assert result.working_memory["z"] == 3
    assert [r.rule_id for r in result.fired_rules] == ["R1","R2"]

def test_rule_fires_once_even_when_conclusion_already_present():
    r=rule("R1",{"fact":"x","op":"eq","value":1},{"fact":"x","value":1})
    result=forward_chain({"x":1},[r])
    assert len(result.fired_rules)==1

def test_unknown_does_not_match():
    r=rule("R1",{"fact":"x","op":"eq","value":"Positive"},{"fact":"y","value":1})
    assert not forward_chain({"x":"Unknown"},[r]).fired_rules

def test_priority_orders_trace():
    a=rule("A",{"fact":"x","op":"eq","value":1},{"fact":"a","value":1})
    b=Rule("B","test",a.conditions,a.conclusions,"m","r",("S",),90)
    assert [x.rule_id for x in forward_chain({"x":1},[a,b]).fired_rules]==["B","A"]
