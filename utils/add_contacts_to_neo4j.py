from data.neo4j_connection import Neo4jConnection


# 若不存在，创建节点并建立关系
def create_node_and_relationship(login_type, login_unit, login_section, login_name,
                                 rel_type, node_unit, node_section, node_post, node_name):
    neo4j_conn = Neo4jConnection()
    try:
        # 判断节点是否存在
        merge_node = f"""
            MERGE (
                n:`高校人员` {{
                unit: '{node_unit}', 
                section: '{node_section}', 
                post: '{node_post}', 
                name: '{node_name}'
                }}
            )
            RETURN n
        """
        neo4j_conn.run_query(merge_node)
        print(f"Node {node_name} created")

        # 建立技术经纪人与节点的关系
        create_rel = f"""
            MATCH (a: `{login_type}`), (b: `高校人员`)
            where a.unit = '{login_unit}' and a.section = '{login_section}' and a.name = '{login_name}'
            and b.unit = '{node_unit}' and b.section = '{node_section}' and b.post = '{node_post}' 
            and b.name = '{node_name}'
            CREATE (a)-[:`{rel_type}`]->(b)
        """
        neo4j_conn.run_query(create_rel)
        print(f"Relationship {rel_type} created")
    except Exception as e:
        print(f"Neo4j connection error: {e}")
        raise
    finally:
        neo4j_conn.close()