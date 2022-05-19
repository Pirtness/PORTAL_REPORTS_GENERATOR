import logging
import dao

log = logging.getLogger(__name__)


def generate_report():
    log.info("generate report")
    dao.begin_transaction()
    try:
        dao.generate_report_test_runs()
        dao.generate_report()
        dao.generate_review()
        dao.commit()
    except Exception as e:
        dao.rollback()
        raise e