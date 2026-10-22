# Knowledge sources and rule provenance

The interface models a **Siemens Multistix 10 SG style** dipstick. Color block labels and concentrations can vary by strip/product and locale. This is an educational, simulated mapping; always use the bottle/package insert for a real device. The app does not convert colors to concentrations.

| ID | Source | Used for |
|---|---|---|
| S1 | Siemens Healthineers, *Multistix 10 SG / Multistix 8 SG / Labstix / Uristix reagent strips package insert* (Rev A, 2017), [official IFU PDF](https://doclib.siemens-healthineers.com/rest/v1/view?document-id=401929) | Ten analytes, semiquantitative strip nature, expected values/limitations, nitrite incubation, leukocyte reading time, sample timing/safe interpretation. Rules Q01–Q04, G01–G12, X01, X03–X05, R01–R03, S03. |
| S2 | UK Department of Health and Social Care, *Diagnosis of urinary tract infections: quick reference tools for primary care*, [official guidance](https://www.gov.uk/government/publications/urinary-tract-infection-diagnosis/diagnosis-of-urinary-tract-infections-quick-reference-tools-for-primary-care) | Symptom context required; dipstick combinations support rather than establish assessment; negative results do not fully exclude UTI; follow manufacturer timing. Rules G07–G08, X01–X02, R03, S02–S03. |
| S3 | Royal College of Pathologists of Australasia, *Urine dipstick*, [RCPA Manual](https://www.rcpa.edu.au/Manuals/RCPA-Manual/Pathology-Tests/U/Urine-dipstick) | General limitations and appropriate contextual interpretation of analytes. Rules G01–G05, G08, X03–X05, R01–R02. Page was indexed in search but access returned 403 during authoring; treated as secondary support only. |
| S4 | Siemens package insert, intended professional in-vitro diagnostic use; and DHSC guidance | Scope boundary: this prototype is educational and must not drive diagnosis or treatment. Rules S01–S02. |

## Evidence status and assumptions

- Manufacturer supported: the named strip family covers the ten requested analytes; dipsticks are semiquantitative and have analyte-specific limitations; nitrite detection depends partly on bladder incubation; leukocyte pads have a specified read time. The app gives users categorical simulated values and retains an explicit timing quality field.
- Guidance supported: dipstick findings should be combined with symptoms and clinical context. A negative nitrite does not rule out UTI.
- Conservative educational rules: single abnormal analyte flags advise qualified interpretation; the prototype does not infer disease, urgency level, or treatment. This is an intentionally cautious application design, not a clinically validated decision-support protocol.
- UI grades are chart-like simulated categories. pH and specific gravity choices reflect ranges commonly printed for this strip family. Urobilinogen is displayed as approximate chart positions; exact categories differ by product/chart. For validation, use the actual local package insert.
- Source support does not constitute validation of the rule base. No patient data or external service is used.
