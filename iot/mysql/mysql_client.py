from sqlalchemy import create_engine, text, Result


class MysqlClient:
    def __init__(self, host, port, db_name, username, password):
        self.db_url = f"mysql+pymysql://" + \
                      f"{username}" + \
                      f":{password}" + \
                      f"@{host}" + \
                      f":{port}" + \
                      f"/{db_name}"

        print(f"## db_url : username:password@{host}:{port}/{db_name}")
        self.engine = create_engine(self.db_url, pool_size=5, max_overflow=30)

    # Let's implement DAO in this class

    def runSelectQuery(self, query_str) -> Result:
        to_return = None
        with self.engine.connect() as conn:
            try:
                to_return = conn.execute(text(query_str))
            except Exception as ex:
                print(f'Exception occurs {ex}')

        return to_return
