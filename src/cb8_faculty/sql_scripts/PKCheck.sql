USE [PeopleSoftCBM008Creation];
GO

CREATE OR ALTER PROCEDURE dbo.PKCheck
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @message NVARCHAR(MAX) = N'';

    IF EXISTS
    (
        SELECT ID, [Empl Record]
        FROM dbo.ps_job
        GROUP BY ID, [Empl Record]
        HAVING COUNT(*) > 1
    )
    BEGIN
        SET @message = CONCAT(@message, N'ps_job PK violation; ');
    END;

    IF EXISTS
    (
        SELECT ID, [Empl Record]
        FROM dbo.ps_compensation
        GROUP BY ID, [Empl Record]
        HAVING COUNT(*) > 1
    )
    BEGIN
        SET @message = CONCAT(
            @message,
            N'ps_compensation PK violation; '
        );
    END;

    IF EXISTS
    (
        SELECT
            CONTRACT_EMPLID,
            [CONTRACT_Empl Record],
            [Contract Begin Date],
            [Contract End Date]
        FROM dbo.ps_contract
        GROUP BY
            CONTRACT_EMPLID,
            [CONTRACT_Empl Record],
            [Contract Begin Date],
            [Contract End Date]
        HAVING COUNT(*) > 1
    )
    BEGIN
        SET @message = CONCAT(
            @message,
            N'ps_contract PK violation; '
        );
    END;

    IF EXISTS
    (
        SELECT
            Position,
            [Dept ID],
            [Earn Code],
            [Combo Code]
        FROM dbo.ps_dept_bud_ern
        GROUP BY
            Position,
            [Dept ID],
            [Earn Code],
            [Combo Code]
        HAVING COUNT(*) > 1
    )
    BEGIN
        SET @message = CONCAT(
            @message,
            N'ps_dept_bud_ern PK violation; '
        );
    END;

    IF EXISTS
    (
        SELECT [GL Combo Code]
        FROM dbo.ps_pscombo_tbl
        GROUP BY [GL Combo Code]
        HAVING COUNT(*) > 1
    )
    BEGIN
        SET @message = CONCAT(
            @message,
            N'ps_pscombo_tbl PK violation; '
        );
    END;

    IF EXISTS
    (
        SELECT
            ID,
            [Empl Record],
            [Earn Code],
            [Eff Date],
            [Addl Seq #]
        FROM dbo.ps_additional
        GROUP BY
            ID,
            [Empl Record],
            [Earn Code],
            [Eff Date],
            [Addl Seq #]
        HAVING COUNT(*) > 1
    )
    BEGIN
        SET @message = CONCAT(
            @message,
            N'ps_additional PK violation; '
        );
    END;

    IF @message <> N''
    BEGIN
        THROW 50010, @message, 1;
    END;

    SELECT
        CAST(1 AS BIT) AS CheckPassed,
        N'No PK violations found.' AS CheckMessage;
END;
GO