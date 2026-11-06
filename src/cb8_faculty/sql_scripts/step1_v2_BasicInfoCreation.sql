SET ANSI_NULLS ON;
GO

SET QUOTED_IDENTIFIER ON;
GO

CREATE OR ALTER PROCEDURE dbo.step1_v2_BasicInfoCreation
    @TermCode VARCHAR(6),
    @Term_Start_Date DATE,
    @Term_End_Date DATE
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    -- Parameter validation
    IF @TermCode IS NULL
       OR LEN(@TermCode) <> 6
       OR @TermCode LIKE '%[^0-9]%'
    BEGIN
        THROW 50011,
              'TermCode must contain exactly six numeric characters.',
              1;
    END;

    IF @Term_Start_Date IS NULL
       OR @Term_End_Date IS NULL
    BEGIN
        THROW 50012,
              'Term dates are required.',
              1;
    END;

    IF @Term_Start_Date >= @Term_End_Date
    BEGIN
        THROW 50013,
              'Term start date must be before term end date.',
              1;
    END;

    -- Single-term staging-table initialization
    DELETE FROM dbo.CBM008_BasicInfo_2;

    /*
        existing population, biographical,
        tenure, rank, department, emeritus, and
        ethnicity logic here.
    */

    -- Return execution summary to Python
    SELECT
        @TermCode AS TermCode,
        COUNT(*) AS BasicInfoRowCount
    FROM dbo.CBM008_BasicInfo_2;
END;
GO