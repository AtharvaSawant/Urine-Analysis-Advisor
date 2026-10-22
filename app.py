import streamlit as st
import pandas as pd
from engine.inference_engine import forward_chain
from engine.explanation import explain
from knowledge_base.rules import RULES

st.set_page_config(page_title="Urine Analysis Advisory Expert System", page_icon="🧪", layout="wide")
st.title("Urine Analysis Advisory Expert System")
st.caption("Educational prototype • simulated Siemens Multistix 10 SG style inputs")
st.warning("Not a diagnostic device. Do not use for self-diagnosis or treatment. Results require interpretation by a qualified healthcare professional; no medication decisions are provided.")

GRADE = ["Unknown", "Negative", "Trace", "+", "++", "+++", "++++"]
BLOOD = ["Unknown", "Negative", "Trace", "Small", "Moderate", "Large"]
LE = ["Unknown", "Negative", "Trace", "Small", "Moderate", "Large"]
NITRITE = ["Unknown", "Negative", "Positive"]
BILIRUBIN = ["Unknown", "Negative", "Small", "Moderate", "Large"]
UROB = ["Unknown", "0.2 mg/dL", "1 mg/dL", "2 mg/dL", "4 mg/dL", "8 mg/dL"]

def urob_value(v):
    if v == "Unknown": return None
    return float(v.split()[0])
def selected(v): return None if v == "Unknown" else v

with st.form("strip"):
    st.subheader("Simulated strip readings")
    a,b,c = st.columns(3)
    with a:
        glucose = st.selectbox("Glucose", GRADE, help="Siemens Multistix chart categories (mg/dL): Negative, 100, 250, 500, 1000, 2000; use qualitative grades here as simulated color-chart categories.")
        protein = st.selectbox("Protein", GRADE, help="Negative, Trace, 30, 100, 300, 2000 mg/dL chart categories.")
        ph = st.selectbox("pH", ["Unknown", "5.0", "6.0", "6.5", "7.0", "7.5", "8.0", "8.5", "9.0"])
        ketones = st.selectbox("Ketones", GRADE, help="Negative, Trace, 5, 15, 40, 80, 160 mg/dL chart categories.")
    with b:
        blood = st.selectbox("Blood", BLOOD, help="Negative, Trace-lysed, Small, Moderate, Large (see manufacturer chart).")
        bilirubin = st.selectbox("Bilirubin", BILIRUBIN, help="Negative, Small, Moderate, Large (mg/dL chart values).")
        urob = st.selectbox("Urobilinogen", UROB, help="Approximate chart positions; use exact bottle chart for a real strip.")
        nitrite = st.selectbox("Nitrite", NITRITE)
    with c:
        leukocytes = st.selectbox("Leucocytes / leukocyte esterase", LE, help="Negative, Trace, Small, Moderate, Large.")
        sg = st.selectbox("Specific gravity", ["Unknown", "1.000", "1.005", "1.010", "1.015", "1.020", "1.025", "1.030"])
        sample_valid = st.selectbox("Sample validity", ["Suitable", "Unsuitable / uncertain"])
        timed = st.selectbox("Read within manufacturer-specified reaction time?", ["Yes", "No"])
    submitted = st.form_submit_button("Generate advisory report", type="primary")

if submitted:
    values = {"glucose":selected(glucose), "protein":selected(protein), "pH":float(ph) if ph!="Unknown" else None, "ketones":selected(ketones), "blood":selected(blood), "bilirubin":selected(bilirubin), "urobilinogen":urob_value(urob), "nitrite":selected(nitrite), "leukocytes":selected(leukocytes), "specific_gravity":float(sg) if sg!="Unknown" else None}
    present = [v for v in values.values() if v is not None]
    abnormal = any(v not in (None,"Negative") for k,v in values.items() if k not in ("pH","specific_gravity","urobilinogen")) or (values["pH"] is not None and not 4.6 <= values["pH"] <= 8.0) or (values["specific_gravity"] is not None and not 1.001 <= values["specific_gravity"] <= 1.035) or (values["urobilinogen"] is not None and values["urobilinogen"] > 1.0)
    facts = {**values, "sample_valid":sample_valid=="Suitable", "timed_correctly":timed=="Yes", "available_count":len(present), "any_abnormal":abnormal}
    result = forward_chain(facts, RULES)
    st.divider(); st.subheader("Submitted findings")
    st.dataframe(pd.DataFrame([{"Parameter":k.replace("_"," ").title(), "Reading":("Unknown / unavailable" if v is None else v)} for k,v in values.items()]), width="stretch", hide_index=True)
    m1,m2,m3 = st.columns(3); m1.metric("Readings available", f"{len(present)} / 10"); m2.metric("Rules fired", len(result.fired_rules)); m3.metric("Quality", "Check required" if sample_valid!="Suitable" or timed!="Yes" else "Reported acceptable")
    st.subheader("Advisory recommendations")
    for fr in result.fired_rules:
        if fr.category not in ("Reporting", "Completeness"):
            st.info(f"**{fr.rule_id} · {fr.category}:** {fr.message}")
    st.subheader("Missing information and quality notes")
    if len(present)<10: st.write(f"{10-len(present)} parameter(s) are unknown. Unknown is not treated as negative.")
    if sample_valid!="Suitable": st.write("Sample marked unsuitable/uncertain; analyte interpretation rules were suppressed.")
    if timed!="Yes": st.write("Reading time was not confirmed; analyte interpretation rules were suppressed.")
    st.subheader("Explanation trace")
    st.dataframe(pd.DataFrame(explain(result)), width="stretch", hide_index=True)
    st.subheader("Source references")
    st.markdown("See the [source and rule mapping](knowledge_base/sources.md) for URLs and supported rule groups.")
    st.caption("No diagnosis, medication, or treatment recommendation is generated. If you have symptoms or concerns, contact a healthcare professional.")
else:
    st.info("Enter simulated strip readings and submit to see the working-memory facts and rule trace.")
with st.expander("About the prototype"):
    st.write("Forward chaining starts with input facts, matches declarative production rules, adds derived advisory facts, and repeats until no new facts appear. The complete rule set is documented in docs/rule_table.md.")
