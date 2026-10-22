# Urine Analysis Advisory Expert System

A college AI lab prototype for explaining declarative production rules with a reusable forward-chaining engine. Inputs are simulated Siemens Multistix 10 SG style observations. The software does not read a physical strip, diagnose disease, or prescribe medication.

## macOS setup

```bash
cd "/Users/atharva/My Data/TY Stuffs/5th Sem/AI/Lab CA"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pytest -q
streamlit run app.py
```

Open the local URL printed by Streamlit, usually http://localhost:8501.

## Project map

- `app.py`: Streamlit interface and input validation/parsing.
- `knowledge_base/rules.py`: 30 declarative rules with IDs, conditions, conclusions, priority, rationale, and source IDs.
- `engine/inference_engine.py`: reusable forward-chaining engine and working memory.
- `engine/explanation.py`: human-readable explanation trace.
- `knowledge_base/sources.md`: references, mapping, and verification notes.
- `docs/`: report material, algorithm, decision path, rule table, tests, and reflection template.
- `tests/`: pytest coverage for inference and scenarios.

## Viva explanation

The form creates initial facts. The engine checks all rule conditions, fires each matching rule once, and adds derived facts. It repeats until no new fact appears. It handles unknowns explicitly, sorts the trace by priority, and blocks analyte interpretation if the sample is marked unsuitable or the strip was not read at the correct time. Each displayed rule includes its matched facts and source IDs.

Read [the problem definition](docs/problem_definition.md), [architecture](docs/design_and_architecture.md), [rule table](docs/rule_table.md), [source mapping](knowledge_base/sources.md), and [test report](docs/test_report.md) before presenting.

## Safety and data

This is an educational prototype, not a medical device or validated clinical decision-support system. Do not use it for diagnosis or treatment. It collects no patient identifiers and makes no network calls at runtime. Use official product instructions for the exact strip in any real testing context.
