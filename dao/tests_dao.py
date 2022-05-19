from dao import SqlClient
import logging

log = logging.getLogger(__name__)

class TestDao:
    def __init__(self, sql_client: SqlClient):
        self._sql_client: SqlClient = sql_client

    def generate_report(self):
        sql_upsert = '''
        insert into portal.report_folder
        select t.*
        from portal.vi_report_folder t
        on conflict(id) do update set name=excluded.name,
                                      parent_id=excluded.parent_id,
                                      last_modified = excluded.last_modified,
                                      visible_order = excluded.visible_order,
                                      level = excluded.level,
                                      cnt_all = excluded.cnt_all,
                                      cnt_pass = excluded.cnt_pass,
                                      cnt_fail = excluded.cnt_fail,
                                      cnt_warn = excluded.cnt_warn,
                                      cnt_impl = excluded.cnt_impl,
                                      cnt_pr = excluded.cnt_pr,
                                      cnt_defect = excluded.cnt_defect;
                '''
        self._sql_client.exec_sql(sql_text=sql_upsert)

        sql_delete_old = '''
        delete from portal.report_folder rf
        where not exists(select 1 from portal.vi_report_folder vrf where vrf.id = rf.id);        
                '''
        self._sql_client.exec_sql(sql_text=sql_delete_old)

    def generate_report_test_runs(self):
        sql_upsert = '''
                insert into portal.report_test_runs
                select t.*
                from portal.vi_report_test_runs t
                on conflict(id) do update set name=excluded.name,
                                              parent_id=excluded.parent_id,
                                              id_last_run = excluded.id_last_run,
                                              last_build_name = excluded.last_build_name,
                                              last_status = excluded.last_status,
                                              prev_status = excluded.prev_status,
                                              id_last_pass_run = excluded.id_last_pass_run,
                                              last_pass_build_name = excluded.last_pass_build_name,
                                              cnt_run = excluded.cnt_run,
                                              cnt_pass = excluded.cnt_pass,
                                              cnt_fail = excluded.cnt_fail;
                        '''
        self._sql_client.exec_sql(sql_text=sql_upsert)

        sql_delete_old = '''
        delete from portal.report_test_runs rf
                        where not exists(select 1 from portal.vi_report_test_runs vrf 
                                         where vrf.id = rf.id);        
                                '''
        self._sql_client.exec_sql(sql_text=sql_delete_old)

    def generate_review(self):
        query = '''
                insert into portal.test_runs_and_automation_review
                select t.*
                    from portal.vi_test_runs_and_automation_review t
                on conflict(id_test_group) do update set total_alm_tests_amount=excluded.total_alm_tests_amount,
                                                        automated_tests_amount=excluded.automated_tests_amount,
                                                        new_tests_in_pr_amount=excluded.new_tests_in_pr_amount,
                                                        failed_tests_amount=excluded.failed_tests_amount,
                                                        passed_tests_amount=excluded.passed_tests_amount,
                                                        build_name=excluded.build_name,
                                                        test_run_start_date=excluded.test_run_start_date,
                                                        report_creation_date=excluded.report_creation_date,
                                                        description=excluded.description;
                    '''
        self._sql_client.exec_sql(sql_text=query)