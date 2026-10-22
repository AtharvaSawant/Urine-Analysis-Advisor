# Problem definition

## Problem and motivation
Urine reagent strips provide several rapid, semiquantitative observations. Reading ten pads and turning them into a consistent, explainable summary is useful as a teaching problem in knowledge representation and inference. The project simulates a rule-based advisory layer; it does not build the strip reader, camera, color calibration, or concentration model.

## Users and stakeholders
Primary users are AI/CSBS students demonstrating expert-system concepts and instructors evaluating knowledge representation. Healthcare professionals are the intended interpreters of real findings, but this prototype is not a clinical tool and is not intended for patient care.

## Scope
Inputs: simulated Multistix 10 SG style values for glucose, protein, pH, ketones, blood, bilirubin, urobilinogen, nitrite, leukocyte esterase, and specific gravity, plus sample validity and reading-time confirmation. Outputs: quality notes, rule trace, and conservative advisory text.

Out of scope: diagnosis, risk scoring, treatment, prescriptions, patient-specific recommendations, image processing, device control, laboratory integration, and clinical validation. No patient identifiers are collected.

## Knowledge acquisition
The rule base maps to manufacturer instructions and public clinical guidance in [sources.md](../knowledge_base/sources.md). The sources define the strip's parameters and limitations and caution that UTI interpretation requires context. A few application rules are conservative software safety decisions (unknown is not negative; invalid/mistimed strips suppress analyte interpretation), not medical thresholds.
