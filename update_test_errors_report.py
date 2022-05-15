from service import test_error_service
import logging

log = logging.getLogger(__name__)

if __name__ == '__main__':
    status = 0

    try:
        test_error_service.errors_report()
    except Exception as e:
        log.error("fail errors report", exc_info=e)
        status = 1

    exit(status)