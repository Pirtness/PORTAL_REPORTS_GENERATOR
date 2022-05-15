import dataset
from dataset import Database, Table
from utils import strip_list
import logging
from collections import OrderedDict

log = logging.getLogger(__name__)


def _build_values(batch: list):
    result = []
    for element in batch:
        element_values = map(lambda t: "'" + str(t).replace("'", "''") + "'" if t is not None else 'null',
                             element.values())
        result.append("(" + ",".join(element_values) + ")")
    return ','.join(result)


class SqlClient():
    def __init__(self, connection_string, user=None, password=None):
        conn_str = connection_string.format(user=user, password=password)
        self._db = dataset.connect(conn_str, schema='portal', ensure_schema=False)
        self._db.query("select 1")
        log.info("connection successful")

    def get_table(self, table_name) -> Table:
        return self._db.get_table(table_name)

    def get_client(self) -> Database:
        return self._db

    def exec_sql(self, sql_text):
        try:
            self._db.executable.execute(sql_text)
        except Exception as e:
            log.error(f'error while execution sql {sql_text}, {e}')
            raise e

    def insert_many(self, full_table_name, rows: list, chunk_size: int = 100):
        ordered_values_rows = [OrderedDict(row) for row in rows]

        batches = strip_list(ordered_values_rows, chunk_size)
        column_names = ','.join(batches[0][0].keys())
        insert_template = f'insert into {full_table_name} ({column_names}) values '
        for batch in batches:
            batch_values = _build_values(batch)
            statement = insert_template + batch_values
            statement = statement.replace('%', '%%')
            try:
                self._db.executable.execute(statement)
            except Exception as err:
                log.error(f'invalid sql "{statement}"')
                raise err

    def create_temp_table(self, table_name, parent_table):
        query = f'''
               create temp table if not exists {table_name} 
               as select * from portal.{parent_table} limit 0
            '''
        self.exec_sql(query)

    def clear_table(self, table_name):
        self.exec_sql(f"delete from {table_name}")