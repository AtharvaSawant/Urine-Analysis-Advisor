# Test scenarios and report

The scenarios below are implemented in `tests/test_scenarios.py`. Expected rule IDs are asserted there, making the test execution the source of pass/fail truth. The scenario inputs are normalized engine facts rather than medical cases.

| Scenario | Input summary | Expected rules / outcome |
|---|---|---|
| Normal | All ten values available; negative analytes; pH 6.0, SG 1.015; suitable and timed | Q03 and S03. No abnormal analyte or combined rule. |
| Abnormal | Glucose `+`; otherwise normal | G01 and general safety advisory S02. |
| Combined | Glucose `+`, ketones `++`, nitrite positive, leukocytes small | Individual and combined advisories including X01 and X03; no diagnosis. |
| Invalid sample | Glucose `+++`, sample invalid (also separately mistimed) | Quality advisory Q01 or Q02; G01 suppressed. |
| Missing | Every analyte unavailable | Q04 and Q05; unknown is not negative. |
| Edge: duplicate and priority | Invalid sample plus glucose `+` | No duplicate rule IDs; quality rule sorts before lower priority. |
| Edge: unsupported | Glucose value `purple` | No glucose rule match. |

## Automated test result

Executed with `.venv/bin/python -m pytest -q`: **11 passed**. `compileall` completed successfully. Streamlit AppTest initial render passed. A direct server bind was blocked by the execution sandbox socket policy; use the README command in a normal terminal for the live demo. The suite covers fixed-point derivation, one-time firing, unknown handling, priority ordering, normal/abnormal/combined/quality/missing scenarios, unsupported values, and duplicate prevention.

## Discussion

These are software behavior tests, not clinical validation. Passing tests establish that the programmed rules execute as specified; they do not demonstrate diagnostic accuracy or suitability for patient care.
