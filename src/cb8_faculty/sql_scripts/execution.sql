EXEC dbo.PKCheck;

-- Keep initialization explicit. Manual salary is intentionally excluded.
DELETE FROM dbo.CBM008_CB4Instructor;
DELETE FROM dbo.CBM008_BasicInfo_2;
DELETE FROM dbo.FacultyAppointments_2;
DELETE FROM dbo.FacultySupplements_2;


-- Step 0: Create CBM008 Instructor records for the given term.
EXEC dbo.step0_CBM004_Instructor_CBM008_Creation
    @TermCode=:instructor_term,
    @Term_Start_Date=:instructor_start,
    @Term_End_Date=:instructor_end;

-- Step 1: Create CBM008 BasicInfo records for the given term.
EXEC dbo.step1_v2_BasicInfoCreation
    @TermCode=:cbm_term,
    @Term_Start_Date=:term_start,
    @Term_End_Date=:term_end;


-- Step 2: Create CBM008 Salary records for the given term.
EXEC dbo.step2_v2_SalaryCreation
    @TermCode=:cbm_term,
    @Term_Start_Date=:term_start,
    @Term_End_Date=:term_end;

-- Step 3: Create CBM008 Salary records for the given term. Manual salary is intentionally excluded.
EXEC dbo.step3_v2_SalaryCreation_Manual;

-- Step 4: Create CBM008 Faculty Appointment records for the given term.
EXEC dbo.IntegrityCheck_2
    @TermCode=:cbm_term,
    @Term_Start_Date=:term_start,
    @Term_End_Date=:term_end;

-- Step 5: Create CBM008 Faculty Supplement records for the given term.
EXEC dbo.ImportingScripts_2 @term=:cbm_term;

