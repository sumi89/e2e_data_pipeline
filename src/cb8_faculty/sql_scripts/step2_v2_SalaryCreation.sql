SET ANSI_NULLS ON;
GO

SET QUOTED_IDENTIFIER ON;
GO

CREATE OR ALTER PROCEDURE dbo.step2_v2_SalaryCreation
    @TermCode VARCHAR(6),
    @Term_Start_Date DATE,
    @Term_End_Date DATE
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    -- 1. Validate arguments
    -- 2. Verify Step 1 generated BasicInfo records
    -- 3. Clear appointment staging data
    -- 4. Insert regular appointments
    -- 5. Aggregate regular salary and percent time
    -- 6. Calculate nine-month salary
    -- 7. Clear supplemental staging data
    -- 8. Insert supplemental salary
    -- 9. Add supplements to fund totals
    -- 10. Recalculate nine-month salary
    -- 11. Initialize faculty with no appointments
    -- 12. Return execution summary
END;
GO