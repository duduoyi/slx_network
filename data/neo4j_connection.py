from neo4j import GraphDatabase
from config import Config


class Neo4jConnection:
    def __init__(self):
        self.uri = Config.NEO4J_URI
        self.username = Config.NEO4J_USER
        self.password = Config.NEO4J_PASSWORD
        self.driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))

    def close(self):
        self.driver.close()

    # 执行查询
    def run_query(self, query):
        with self.driver.session() as session:
            result = session.run(query)
            return [record for record in result]


# # 测试 Neo4j 连接
# def test_neo4j_connection():
#     try:
#         neo4j_conn = Neo4jConnection()
#         result = neo4j_conn.run_query("MATCH (n) RETURN n LIMIT 1")
#         print(f"Neo4j connection successful: {result}")
#     except Exception as e:
#         print(f"Neo4j connection error: {e}")
