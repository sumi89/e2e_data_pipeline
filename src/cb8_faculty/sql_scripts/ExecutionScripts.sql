USE [PeopleSoftCBM008Creation];
GO

CREATE OR ALTER PROCEDURE dbo.ExecutionScripts
    @TermCode VARCHAR(6),
    @Term_Start_Date DATE,
    @Term_End_Date DATE,
    @RunImport BIT = 0
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    IF @TermCode IS NULL OR LEN(@TermCode) <> 6
    BEGIN
        THROW 50001, 'TermCode must contain exactly six characters.', 1;
    END;

    IF @Term_Start_Date IS NULL OR @Term_End_Date IS NULL
    BEGIN
        THROW 50002, 'Term start and end dates are required.', 1;
    END;

    IF @Term_Start_Date >= @Term_End_Date
    BEGIN
        THROW 50003, 'Term start date must be before term end date.', 1;
    END;

    EXEC dbo.PKCheck;

    DELETE FROM dbo.CBM008_BasicInfo_2;
    DELETE FROM dbo.FacultyAppointments_2;
    DELETE FROM dbo.FacultySupplements_2;
    DELETE FROM dbo.CBM008_Sal_Manual;

    EXEC dbo.step1_v2_BasicInfoCreation
        @TermCode,
        @Term_Start_Date,
        @Term_End_Date;

    EXEC dbo.step2_v2_SalaryCreation
        @TermCode,
        @Term_Start_Date,
        @Term_End_Date;

    EXEC dbo.step3_v2_SalaryCreation_Manual;

    EXEC dbo.IntegrityCheck_2
        @TermCode,
        @Term_Start_Date,
        @Term_End_Date;

    IF @RunImport = 1
    BEGIN
        EXEC dbo.ImportingScripts_2 @TermCode;
    END;
END;
GO