from datetime import date
import logging

import pyodbc

from db_connection import get_db_connection, run_diagnostics


logger = logging.getLogger(__name__)


def execute_procedure(cursor, procedure_name, params=None):
    """
    Execute one SQL Server stored procedure.

    Parameters
    ----------
    cursor : pyodbc.Cursor
        Active SQL Server cursor.

    procedure_name : str
        Stored procedure name, for example:
        dbo.step1_v2_BasicInfoCreation

    params : list, optional
        Parameters required by the stored procedure.
    """

    params = params or []

    placeholders = ", ".join("?" for _ in params)

    if placeholders:
        sql = f"EXEC {procedure_name} {placeholders}"
    else:
        sql = f"EXEC {procedure_name}"

    logger.info("Starting %s", procedure_name)

    cursor.execute(sql, params)

    # Consume any result sets/messages returned by SQL Server.
    while cursor.nextset():
        pass

    logger.info("Completed %s", procedure_name)


def validate_parameters(
    term_code: str,
    start_date: date,
    end_date: date,
):
    """
    Validate CBM008 pipeline parameters before SQL is executed.
    """

    if not term_code:
        raise ValueError("Term code is required.")

    if len(term_code) != 6 or not term_code.isdigit():
        raise ValueError(
            "Term code must contain exactly 6 digits."
        )

    if not isinstance(start_date, date):
        raise TypeError("start_date must be a date.")

    if not isinstance(end_date, date):
        raise TypeError("end_date must be a date.")

    if start_date >= end_date:
        raise ValueError(
            "Term start date must be before term end date."
        )


def run_cb8_faculty_pipeline(
    term_code: str,
    start_date: date,
    end_date: date,
    publish: bool = False,
):
    """
    Run the CBM008 faculty pipeline.

    Pipeline order:
        1. PKCheck
        2. step1_v2_BasicInfoCreation
        3. step2_v2_SalaryCreation
        4. step3_v2_SalaryCreation_Manual
        5. IntegrityCheck_2
        6. ImportingScripts_2 (optional)
    """

    validate_parameters(
        term_code,
        start_date,
        end_date,
    )

    logger.info("=" * 60)
    logger.info(
        "Starting CBM008 faculty pipeline | Term: %s",
        term_code,
    )
    logger.info(
        "Term dates: %s to %s",
        start_date,
        end_date,
    )
    logger.info(
        "Publishing enabled: %s",
        publish,
    )
    logger.info("=" * 60)

    connection = None

    try:
        connection = get_db_connection("TestDatabase_Sumi")
        run_diagnostics(connection)
        cursor = connection.cursor()

        # --------------------------------------------------
        # STEP 1: Validate source data
        # --------------------------------------------------

        logger.info("STEP 1: Checking source-table PK violations")

        execute_procedure(
            cursor,
            "dbo.PKCheck",
        )

        # --------------------------------------------------
        # STEP 2: Build CBM008 basic faculty population
        # --------------------------------------------------

        logger.info("STEP 2: Creating CBM008 basic information")

        execute_procedure(
            cursor,
            "dbo.step1_v2_BasicInfoCreation",
            [
                term_code,
                start_date,
                end_date,
            ],
        )

        # --------------------------------------------------
        # STEP 3: Calculate salary and percent-time
        # --------------------------------------------------

        logger.info("STEP 3: Creating CBM008 salary information")

        execute_procedure(
            cursor,
            "dbo.step2_v2_SalaryCreation",
            [
                term_code,
                start_date,
                end_date,
            ],
        )

        """
        # --------------------------------------------------
        # STEP 4: Apply manual salary adjustments
        # --------------------------------------------------

        logger.info("STEP 4: Applying manual salary adjustments")

        execute_procedure(
            cursor,
            "dbo.step3_v2_SalaryCreation_Manual",
        )
        """

        # --------------------------------------------------
        # STEP 5: Integrity validation
        # --------------------------------------------------

        logger.info("STEP 5: Running CBM008 integrity checks")

        execute_procedure(
            cursor,
            "dbo.IntegrityCheck_2",
            [
                term_code,
                start_date,
                end_date,
            ],
        )

        # --------------------------------------------------
        # STEP 6: Publish final CBM008 data
        # --------------------------------------------------

        if publish:

            logger.info(
                "STEP 6: Publishing CBM008 data for %s",
                term_code,
            )

            execute_procedure(
                cursor,
                "dbo.ImportingScripts_2",
                [term_code],
            )

        else:

            logger.info(
                "STEP 6: Publication skipped "
                "(publish=False)"
            )

        connection.commit()

        logger.info("=" * 60)
        logger.info(
            "CBM008 pipeline completed successfully | Term: %s",
            term_code,
        )
        logger.info("=" * 60)

    except pyodbc.Error:
        if connection is not None:
            connection.rollback()

        logger.exception(
            "SQL Server error while running CBM008 "
            "pipeline for term %s",
            term_code,
        )

        raise

    except Exception:
        if connection is not None:
            connection.rollback()

        logger.exception(
            "CBM008 pipeline failed for term %s",
            term_code,
        )

        raise

    finally:
        if connection is not None:
            connection.close()
            logger.info("Database connection closed.")