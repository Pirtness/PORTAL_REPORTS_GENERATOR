import dao
import logging

log = logging.getLogger(__name__)

def errors_report():
    log.info("generate error report")
    dao.begin_transaction()
    try:
        dao.get_failed_tests_logs()
        dao.commit()
    except Exception as e:
        dao.rollback()
        raise e