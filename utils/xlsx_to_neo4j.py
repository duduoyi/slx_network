import openpyxl
from data.neo4j_connection import Neo4jConnection


# 打开Excel文件
wb = openpyxl.load_workbook('E:\技术经纪人沟通记录_MaXX.xlsx')

# # 选择工作表（假设为节点数据和关系数据）
# nodes_sheet = wb['Nodes']  # 假设有一个'Nodes'表
# relationships_sheet = wb['Relationships']  # 假设有一个'Relationships'表
sheet = wb.active


# 从Excel中读取节点数据
def read_nodes(sheet):
    nodes = []
    for row in sheet.iter_rows(min_row=2, min_col=4, values_only=True):  # 从第二行第4列开始读取
        type, name, unit, section, post = row
        nodes.append((type, name, unit, section, post))
    return nodes


# 从Excel中读取关系数据
def read_relationships(sheet):
    relationships = []
    for row in sheet.iter_rows(min_row=2, values_only=True):  # 从第二行开始读取
        start_name, start_unit, rel_type, end_type, end_name, end_unit, end_section, end_post = row
        relationships.append((start_name, start_unit, rel_type, end_type, end_name, end_unit, end_section, end_post))
    return relationships


# 导入节点到Neo4j
def import_nodes(nodes):
    # 连接到Neo4j
    neo4j_conn = Neo4jConnection()
    for type, name, unit, section, post in nodes:
        section = section if section is not None else "Unknown"
        post = post if post is not None else "Unknown"
        neo4j_conn.run_query(
            f"merge (n:`{type}` {{name: {name}, unit: {unit}, section: {section}, post: {post}}})"
        )
    neo4j_conn.close()


# 导入关系到Neo4j
def import_relationships(relationships):
    neo4j_conn = Neo4jConnection()
    for start_name, start_unit, rel_type, end_type, end_name, end_unit, end_section, end_post in relationships:
        end_section = end_section if end_section is not None else "Unknown"
        end_post = end_post if end_post is not None else "Unknown"
        neo4j_conn.run_query(
            f"""
            MATCH (a:`技术中介`), (b:`{end_type}`)
            where a.name = {start_name} and a.unit = {start_unit} 
            and b.name = {end_name} and b.unit = {end_unit} and b.section = {end_section} and b.post = {end_post}
            CREATE (a)-[r:`{rel_type}`]->(b)
            """
        )
    neo4j_conn.close()


# 主函数
def main():
    # 读取节点和关系数据
    nodes = read_nodes(sheet)
    relationships = read_relationships(sheet)
    # 导入neo4j
    import_nodes(nodes)
    import_relationships(relationships)

    print("数据导入完成！")


if __name__ == "__main__":
    main()
