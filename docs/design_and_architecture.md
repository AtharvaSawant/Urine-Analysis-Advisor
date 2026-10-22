# Design and architecture

1. Streamlit form gathers the ten simulated results and two quality flags.
2. The UI validates/parses numbers and creates a dictionary of initial facts, including available count and an abnormal-observation flag.
3. `forward_chain` copies these facts into working memory, scans declarative rules in descending priority, skips analyte rules for unsuitable/mistimed samples, matches all conditions, fires each rule ID at most once, and inserts derived advisory facts.
4. It repeats while any new fact is added, up to a 100-pass safety limit. Since each rule fires once and rule count is finite, cycles cannot repeatedly fire.
5. The explanation formatter emits the ID, category, matched conditions, recommendation, rationale, sources, and priority.
6. Streamlit renders findings, quality warnings, advisory cards, and trace.

## Why forward chaining?
The input consists of known facts (strip results and quality fields) and the system must discover every applicable advisory, including combinations and secondary rules. Forward chaining starts from the available evidence and derives consequences. This fits the workflow better than asking one predefined diagnosis question (backward chaining), and makes the fired-rule trace easy to explain in a viva.

## Conflict and safety behavior
Priority sorts the explanation/action order; no clinical conclusion is resolved by choosing a diagnosis. Rules accumulate independent advisories. Unsuitable or mistimed input blocks analyte interpretation and lets quality/reporting rules fire. Unknown values do not match clinical conditions. Unsupported categorical strings do not match graded rules. This is a deterministic educational policy, not medical conflict resolution.

## Limitations
No external validation or patient evaluation has been performed. Manufacturer chart categories vary by product and locale. The UI uses simulated categories rather than a calibrated device. The knowledge base is intentionally narrow and does not use symptoms, age, pregnancy status, medications, microscopy, culture, or laboratory reference intervals.
