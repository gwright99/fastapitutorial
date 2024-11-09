import os
import subprocess
from typing import Optional

import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app


# # ---------------------------------------------------------------------------------------------
# def pytest_configure(config):
#     """
#     Allows plugins and conftest files to perform initial configuration.
#     This hook is called for every plugin and initial conftest
#     file after command line options have been parsed.
#     """
#     pass
def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    print("\n\n[PYTEST SESSION - STANDUP] Creating test db.\n")
    # https://stackoverflow.com/questions/27844088/python-get-directory-two-levels-up
    # Assumes following path: .. > installer > tests > conftest.py
    # import sys
    # from pathlib import Path
    # grandparent_dir = Path(__file__).resolve().parents[2]
    # sys.path.append(str(grandparent_dir))
    print(os.getcwd())
    # Assumes activation from ~/fastapitutorial

    # Create test DB
    db_file_dir = os.path.dirname(settings.TEST_DB_FILE)
    if not os.path.exists(db_file_dir):
        os.makedirs(db_file_dir)
    open(settings.TEST_DB_FILE, "a").close()

    # Invoke DB setup scripts.
    _ = subprocess.call("src/scripts/boot_prestart.sh", shell=True)

    # TODO: Replace with logger.debug
    # print(f"+++++++++++++++++++++++++++++++++ {result}")


def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """

    print("\n\n[PYTEST SESSION - TEARDOWN] Deleting test db.")
    os.remove(settings.TEST_DB_FILE)


#     pass
# def pytest_unconfigure(config):
#     """
#     Called before test process is exited.
#     """
#     pass
# # ---------------------------------------------------------------------------------------------
