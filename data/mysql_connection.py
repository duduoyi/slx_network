from sqlalchemy import create_engine
from config import Config
import pandas as pd


# sqlalchemy 自动关闭连接，无需手动 close()。
class MysqlPatent:
    def __init__(self):
        self.SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{Config.MYSQL_USER}:{Config.MYSQL_PASSWORD}@{Config.MYSQL_HOST}:{Config.MYSQL_PORT}/{Config.MYSQL_DB_PATENT}"
        self.engine = create_engine(self.SQLALCHEMY_DATABASE_URI)

    # 执行查询
    def get_mysql_data(self, query):
        try:
            with self.engine.connect() as connection:
                df = pd.read_sql(query, connection)
            return df  # 连接会在 `with` 结束时自动关闭
        except Exception as e:
            print(f"❌ MySQL 连接错误: {e}")
            return None