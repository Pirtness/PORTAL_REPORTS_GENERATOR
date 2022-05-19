from dataset import Table

from .sql_client import SqlClient
from utils.properties import *
import json
import logging
from .test_errors_dao import TestErrorsDao
from .tests_dao import TestDao

log = logging.getLogger(__name__)

_sql_client: SqlClient = None


def _get_sql_client() -> SqlClient:
    global _sql_client
    if _sql_client is None:
        _sql_client = SqlClient(connection_string=DATABASE_URL, user=DATABASE_USER, password=DATABASE_PASS)
    return _sql_client


test_error_dao: TestErrorsDao = TestErrorsDao(_get_sql_client())
test_dao: TestDao = TestDao(_get_sql_client())


def generate_report():
    test_dao.generate_report()


def generate_report_test_runs():
    test_dao.generate_report_test_runs()


def generate_review():
    test_dao.generate_review()


def begin_transaction():
    _get_sql_client().get_client().begin()


def commit():
    _get_sql_client().get_client().commit()


def rollback():
    _get_sql_client().get_client().rollback()


def get_query_result(query):
    return _get_sql_client().get_client().query(query)


def get_failed_tests_logs():
    test_error_dao.get_failed_tests_logs()