"""Declarative rules. No rule diagnoses a disease or prescribes treatment."""
from engine.inference_engine import Rule

def C(fact, op, value=None):
    d = {"fact": fact, "op": op}
    if value is not None: d["value"] = value
    return d

def R(i, cat, conditions, message, rationale, src, priority=50, conclusions=None):
    return Rule(i, cat, tuple(conditions), tuple(conclusions or ({"fact":"advisory", "value":i},)), message, rationale, tuple(src), priority)

RULES = [
R("Q01","Validity",[C("sample_valid","eq",False)],"Do not interpret this panel; obtain a suitable fresh sample and repeat according to local procedure.","The submitter marked the sample unsuitable.",["S1"],100),
R("Q02","Validity",[C("timed_correctly","eq",False)],"Treat strip results as unreliable and repeat with manufacturer-specified timing.","Siemens instructs users to read each reagent pad at its specified time; timing affects result interpretation.",["S1"],100),
R("Q03","Validity",[C("sample_valid","eq",True),C("timed_correctly","eq",True)],"Sample validity and stated reading time are acceptable for this simulation.","The two quality fields are marked acceptable; this does not validate collection or technique independently.",["S1"],5),
R("Q04","Completeness",[C("available_count","lt",10)],"Some analytes are unavailable; interpret only reported results and consider repeat/completion if clinically needed.","Unknown readings are not treated as negative.",["S1"],80),
R("Q05","Completeness",[C("available_count","eq",0)],"No analyte result is available to interpret.","All analytes are unknown or unavailable.",["S1"],90),
R("G01","Individual findings",[C("glucose","in",["Trace","+","++","+++","++++"])],"Glucose is detected; arrange qualified clinical interpretation.","Dipstick glucose indicates glycosuria but cannot diagnose hyperglycaemia or its cause.",["S1","S3"],60),
R("G02","Individual findings",[C("protein","in",["Trace","+","++","+++","++++"])],"Protein is detected; discuss confirmation and clinical interpretation with a qualified professional.","Dipstick protein is semiquantitative and may be affected by specimen conditions; persistent findings warrant assessment.",["S1","S3"],60),
R("G03","Individual findings",[C("ketones","in",["Trace","+","++","+++","++++"])],"Ketones are detected; seek clinical interpretation in context.","The strip detects acetoacetic acid, not all ketone bodies; trace findings may have limited significance.",["S1"],60),
R("G04","Individual findings",[C("blood","in",["Trace","Small","Moderate","Large","+","++","+++"])],"Blood reaction detected; repeat/confirm and seek clinical interpretation, especially if persistent.","A strip blood reaction is not equivalent to confirmed red cells on microscopy.",["S1","S3"],60),
R("G05","Individual findings",[C("bilirubin","in",["Small","Moderate","Large","+","++","+++"])],"Bilirubin detected; prompt qualified clinical review is appropriate.","Urine bilirubin is not expected on this strip and requires contextual assessment.",["S1","S3"],70),
R("G06","Individual findings",[C("urobilinogen","gt",1.0)],"Urobilinogen is above the selected strip reference level; seek qualified interpretation.","Interpret using the manufacturer chart and local laboratory range; results are not diagnostic by themselves.",["S1"],50),
R("G07","Individual findings",[C("nitrite","eq","Positive")],"Nitrite is detected; discuss with a clinician, particularly if urinary symptoms are present.","Nitrite can support UTI assessment, but dipstick alone does not establish infection.",["S1","S2"],65),
R("G08","Individual findings",[C("leukocytes","in",["Small","Moderate","Large","+","++","+++"])],"Leukocyte esterase detected; seek interpretation in clinical context.","Leukocyte esterase indicates leukocytes, which can occur in infectious and non-infectious conditions.",["S1","S2"],55),
R("G09","Individual findings",[C("pH","gt",8.0)],"pH is above the stated general range; review the value and specimen handling with a professional.","Siemens lists a typical urine pH range and notes specimen bacterial growth can shift pH upward.",["S1"],35),
R("G10","Individual findings",[C("pH","lt",4.6)],"pH is below the stated general range; confirm with the strip chart and local reference.","The manufacturer reference range is used only as a broad educational flag.",["S1"],35),
R("G11","Individual findings",[C("specific_gravity","lt",1.001)],"Specific gravity is below the manufacturer's stated general range; confirm result and seek interpretation.","Specific gravity is a concentration-related measurement and is affected by clinical/specimen context.",["S1"],35),
R("G12","Individual findings",[C("specific_gravity","gt",1.035)],"Specific gravity is above the manufacturer's stated general range; confirm result and seek interpretation.","Specific gravity is a concentration-related measurement and is affected by clinical/specimen context.",["S1"],35),
R("X01","Combined findings",[C("nitrite","eq","Positive"),C("leukocytes","in",["Small","Moderate","Large","+","++","+++"])],"Both nitrite and leukocyte esterase are detected; clinical assessment is appropriate if symptoms exist.","This combination may increase suspicion in symptomatic patients, but symptoms and context are essential.",["S1","S2"],75),
R("X02","Combined findings",[C("nitrite","eq","Positive"),C("blood","in",["Trace","Small","Moderate","Large","+","++","+++"])],"Nitrite and blood are detected; arrange clinical interpretation, especially with urinary symptoms.","Guidance uses symptom context and dipstick combinations; isolated strip results do not diagnose UTI.",["S2"],70),
R("X03","Combined findings",[C("glucose","in",["Trace","+","++","+++","++++"]),C("ketones","in",["Trace","+","++","+++","++++"])],"Both glucose and ketones are detected; seek timely qualified interpretation.","These findings together require context; the app does not infer diabetes or ketoacidosis.",["S1","S3"],85),
R("X04","Combined findings",[C("protein","in",["Trace","+","++","+++","++++"]),C("blood","in",["Trace","Small","Moderate","Large","+","++","+++"])],"Protein and blood reactions are both detected; confirm and discuss with a clinician.","Both are screening findings and require appropriate confirmation.",["S1","S3"],65),
R("X05","Combined findings",[C("bilirubin","in",["Small","Moderate","Large","+","++","+++"]),C("urobilinogen","gt",1.0)],"Bilirubin and elevated urobilinogen are reported; arrange professional interpretation.","The two strip observations do not determine a cause and should be interpreted with other clinical information.",["S1","S3"],65),
R("R01","Repeat testing",[C("blood","in",["Trace","Small","Moderate","Large","+","++","+++"])],"Consider repeat testing or confirmatory urinalysis as directed by a clinician.","A reagent strip blood result alone does not confirm microscopic haematuria.",["S1","S3"],52),
R("R02","Repeat testing",[C("protein","in",["Trace","+","++","+++","++++"])],"If the protein finding persists, follow local clinical/laboratory confirmation guidance.","Dipstick protein is a screening measurement; persistent protein requires assessment.",["S3"],52),
R("R03","Repeat testing",[C("nitrite","eq","Negative"),C("leukocytes","in",["Small","Moderate","Large","+","++","+++"])],"A negative nitrite does not exclude infection; symptoms should guide clinical follow-up.","Nitrite may be negative for some organisms and depends on bladder incubation time.",["S1","S2"],68),
R("S01","Safety",[C("sample_valid","eq",False)],"This educational output is not a diagnosis; consult a qualified healthcare professional.","Quality concerns make clinical interpretation unsafe.",["S4"],100),
R("S02","Safety",[C("any_abnormal","eq",True)],"Do not start or change medication based on this prototype; use qualified care.","Dipstick findings alone are insufficient for diagnosis and treatment decisions.",["S2","S4"],95),
R("S03","Reporting",[C("available_count","ge",1)],"This report summarizes simulated strip readings and does not diagnose disease.","Point-of-care dipstick testing is an aid to assessment, not a standalone diagnosis.",["S1","S2"],10),
]
