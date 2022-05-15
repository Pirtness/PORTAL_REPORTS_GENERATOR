from dao import SqlClient
from utils.errors_compare import generate_data_for_tables_with_errors_templates
import logging

log = logging.getLogger(__name__)

class TestErrorsDao:
    def __init__(self, sql_client: SqlClient):
        self._sql_client: SqlClient = sql_client


    def get_failed_tests_logs(self):
        #todo change to report_test_runs
        log.info('collect failed tests from db')
        sql_upsert = '''
            with failed_tests as (
                select * from portal.vi_report_test_runs rtr
                    where rtr.last_status= 'f'
            ),
            steps_with_logs as (
            select trp.id_alm_test as id_test, trp.id as id_pack from failed_tests ft
            join portal.test_run_package trp on trp.id_test_run = ft.id_last_run
                                                             and trp.id_alm_test = ft.id
            where trp.caption = 'server log collector after scenario error')
            select sl.id_test, trse.embed  from steps_with_logs sl
            join portal.test_run_step trs on trs.id_test_run_package = sl.id_pack
            join portal.test_run_step_embed trse on trse.id_test_run_step = trs.id;
        '''
        res = self._sql_client.get_client().query(sql_upsert)

        log.info("map errors to templates")

        templates = [""]
        test_to_errors = {}
        for row in res:
            logs = row['embed'].tobytes().decode("utf-8").split('\n')
            errors = []
            append_next = False
            for line in logs:
                if (len(line) == 0):
                    continue
                if 'ERROR' in line:
                    line = line.replace('\\', '\\\\')
                    errors.append(line)
                    append_next = True
                    continue
                if append_next and line[0] != '[':
                    errors[-1] += line
                else:
                    append_next = False
                    if len(errors) > 5:
                        break
            test_to_errors[row['id_test']] = errors

        select_templates = '''
        select id, error_template, hashed_error_template, description from portal.error_template;
        '''
        res = self._sql_client.get_client().query(select_templates)
        templates = {}
        for row in res:
            templates[row['id']] = set(bytes(row['hashed_error_template']).decode('utf-8').split(', '))

        test_to_templates_rows, error_templates_rows = generate_data_for_tables_with_errors_templates(test_to_errors, templates=templates)

        if len(error_templates_rows) > 0:
            log.info(f'found {len(error_templates_rows)} new templates')
            self._sql_client.insert_many('portal.error_template', error_templates_rows)
        else:
            log.info(f'no new templates found')

        self._sql_client.clear_table('portal.report_failed_test_to_error_template')
        if len(test_to_templates_rows) > 0:
            self._sql_client.insert_many('portal.report_failed_test_to_error_template', test_to_templates_rows)