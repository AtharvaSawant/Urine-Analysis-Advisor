# Rule table

Conditions use normalized fact names. `Unknown`/`None` never satisfies an analyte condition. Source IDs map to [knowledge_base/sources.md](../knowledge_base/sources.md). Priorities control trace ordering; they are not clinical severity scores.

| ID | Category | IF (all conditions) | THEN advisory |
|---|---|---|---|
| Q01 | Validity | sample_valid eq False | Do not interpret this panel; obtain a suitable fresh sample and repeat according to local procedure. [S1] (priority 100) |
| Q02 | Validity | timed_correctly eq False | Treat strip results as unreliable and repeat with manufacturer-specified timing. [S1] (priority 100) |
| Q03 | Validity | sample_valid eq True AND timed_correctly eq True | Sample validity and stated reading time are acceptable for this simulation. [S1] (priority 5) |
| Q04 | Completeness | available_count lt 10 | Some analytes are unavailable; interpret only reported results and consider repeat/completion if clinically needed. [S1] (priority 80) |
| Q05 | Completeness | available_count eq 0 | No analyte result is available to interpret. [S1] (priority 90) |
| G01 | Individual findings | glucose in ['Trace', '+', '++', '+++', '++++'] | Glucose is detected; arrange qualified clinical interpretation. [S1, S3] (priority 60) |
| G02 | Individual findings | protein in ['Trace', '+', '++', '+++', '++++'] | Protein is detected; discuss confirmation and clinical interpretation with a qualified professional. [S1, S3] (priority 60) |
| G03 | Individual findings | ketones in ['Trace', '+', '++', '+++', '++++'] | Ketones are detected; seek clinical interpretation in context. [S1] (priority 60) |
| G04 | Individual findings | blood in ['Trace', 'Small', 'Moderate', 'Large', '+', '++', '+++'] | Blood reaction detected; repeat/confirm and seek clinical interpretation, especially if persistent. [S1, S3] (priority 60) |
| G05 | Individual findings | bilirubin in ['Small', 'Moderate', 'Large', '+', '++', '+++'] | Bilirubin detected; prompt qualified clinical review is appropriate. [S1, S3] (priority 70) |
| G06 | Individual findings | urobilinogen gt 1.0 | Urobilinogen is above the selected strip reference level; seek qualified interpretation. [S1] (priority 50) |
| G07 | Individual findings | nitrite eq Positive | Nitrite is detected; discuss with a clinician, particularly if urinary symptoms are present. [S1, S2] (priority 65) |
| G08 | Individual findings | leukocytes in ['Small', 'Moderate', 'Large', '+', '++', '+++'] | Leukocyte esterase detected; seek interpretation in clinical context. [S1, S2] (priority 55) |
| G09 | Individual findings | pH gt 8.0 | pH is above the stated general range; review the value and specimen handling with a professional. [S1] (priority 35) |
| G10 | Individual findings | pH lt 4.6 | pH is below the stated general range; confirm with the strip chart and local reference. [S1] (priority 35) |
| G11 | Individual findings | specific_gravity lt 1.001 | Specific gravity is below the manufacturer's stated general range; confirm result and seek interpretation. [S1] (priority 35) |
| G12 | Individual findings | specific_gravity gt 1.035 | Specific gravity is above the manufacturer's stated general range; confirm result and seek interpretation. [S1] (priority 35) |
| X01 | Combined findings | nitrite eq Positive AND leukocytes in ['Small', 'Moderate', 'Large', '+', '++', '+++'] | Both nitrite and leukocyte esterase are detected; clinical assessment is appropriate if symptoms exist. [S1, S2] (priority 75) |
| X02 | Combined findings | nitrite eq Positive AND blood in ['Trace', 'Small', 'Moderate', 'Large', '+', '++', '+++'] | Nitrite and blood are detected; arrange clinical interpretation, especially with urinary symptoms. [S2] (priority 70) |
| X03 | Combined findings | glucose in ['Trace', '+', '++', '+++', '++++'] AND ketones in ['Trace', '+', '++', '+++', '++++'] | Both glucose and ketones are detected; seek timely qualified interpretation. [S1, S3] (priority 85) |
| X04 | Combined findings | protein in ['Trace', '+', '++', '+++', '++++'] AND blood in ['Trace', 'Small', 'Moderate', 'Large', '+', '++', '+++'] | Protein and blood reactions are both detected; confirm and discuss with a clinician. [S1, S3] (priority 65) |
| X05 | Combined findings | bilirubin in ['Small', 'Moderate', 'Large', '+', '++', '+++'] AND urobilinogen gt 1.0 | Bilirubin and elevated urobilinogen are reported; arrange professional interpretation. [S1, S3] (priority 65) |
| R01 | Repeat testing | blood in ['Trace', 'Small', 'Moderate', 'Large', '+', '++', '+++'] | Consider repeat testing or confirmatory urinalysis as directed by a clinician. [S1, S3] (priority 52) |
| R02 | Repeat testing | protein in ['Trace', '+', '++', '+++', '++++'] | If the protein finding persists, follow local clinical/laboratory confirmation guidance. [S3] (priority 52) |
| R03 | Repeat testing | nitrite eq Negative AND leukocytes in ['Small', 'Moderate', 'Large', '+', '++', '+++'] | A negative nitrite does not exclude infection; symptoms should guide clinical follow-up. [S1, S2] (priority 68) |
| S01 | Safety | sample_valid eq False | This educational output is not a diagnosis; consult a qualified healthcare professional. [S4] (priority 100) |
| S02 | Safety | any_abnormal eq True | Do not start or change medication based on this prototype; use qualified care. [S2, S4] (priority 95) |
| S03 | Reporting | available_count ge 1 | This report summarizes simulated strip readings and does not diagnose disease. [S1, S2] (priority 10) |
