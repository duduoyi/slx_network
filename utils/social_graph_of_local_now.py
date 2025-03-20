import logging
from data.neo4j_connection import Neo4jConnection

# 配置日志
logging.basicConfig(level=logging.INFO)


# 获取数据（包括教师节点、关系、代理节点等）
def now_social(login_type, login_unit, login_section, login_name):
    neo4j_conn = Neo4jConnection()
    # 登录人节点信息
    login_node_query = f"""
        MATCH (a:`{login_type}` {{unit:'{login_unit}', section:'{login_section}', name:'{login_name}'}})
        RETURN 
            labels(a) as label,
            id(a) as id, 
            a.name AS name, 
            a.unit as unit, 
            a.section as section,
            a.post as post,
            a.weight as weight,
            a.communityId as communityId
    """
    logging.info(f"Executing query: {login_node_query}")
    login_node_data = neo4j_conn.run_query(login_node_query)

    # 地方一度关系
    now_first_rel = f"""
        MATCH (a:`{login_type}` {{unit:'{login_unit}', section:'{login_section}', name:'{login_name}'}})
        -[r1]-(b1)  // 一度关系
        WHERE labels(b1) in [`企业人员`, `政府人员`, `技术中介`]
        RETURN 
            id(a) as source, 
            type(r1) AS type,
            labels(b1) AS label, 
            id(b1) AS target,
            b1.name AS name,
            b1.unit AS unit,
            b1.section AS section,
            b1.post as post,
            b1.weight as weight,
            b1.communityId AS communityId
    """
    logging.info(f"Executing query: {now_first_rel}")
    first_rel_data = neo4j_conn.run_query(now_first_rel)
    
    # 二度关系
    now_second_rel = f"""
        MATCH (a:`{login_type}` {{unit:'{login_unit}', section:'{login_section}', name:'{login_name}'}})
            -[r1]-(b1)-[r2]-(b2)  // 二度关系
        WHERE labels(b1) in [`企业人员`, `政府人员`, `技术中介`] AND labels(b2) in [`企业人员`, `政府人员`, `技术中介`] 
        RETURN 
            id(b1) as source,  
            type(r2) AS type,       
            labels(b2) AS label, 
            id(b2) AS target,
            b2.name AS name,
            b2.unit AS unit,
            b2.section AS section,
            b2.post AS post,
            b2.weight AS weight,
            b2.communityId AS communityId
    """
    logging.info(f"Executing query: {now_second_rel}")
    second_rel_data = neo4j_conn.run_query(now_second_rel)

    neo4j_conn.close()

    # 节点列表，边列表
    nodes = []
    edges = []
    
    # 导入登陆人节点信息
    for login_node in login_node_data:
        # 确保 label 是字符串，如果是列表则转换为逗号分隔的字符串
        login_label_value = login_node['label']
        # 如果 label 是列表，遍历列表并将其中的元素转化为字符串后连接
        if isinstance(login_label_value, list):
            login_label_value = ', '.join(str(item) for item in login_label_value)

        login_node_json = {
            'data': {
                'id': str(login_node['id']),
                'name': login_node['name'],
                'label': login_label_value,
                'unit': login_node['unit'],
                'section': login_node['section'],
                'post': str(login_node['post']),
                'weight': str(login_node['weight']),
                'communityId': str(login_node['communityId']),
            },
            'style': {
                'width': 120,
                'height': 120,
                'background-color': '#FFF2E2'
            }
        }
        nodes.append(login_node_json)

    # 导入一度联系人节点信息
    for first_node in first_rel_data:
        # 确保 label 是字符串，如果是列表则转换为逗号分隔的字符串
        first_label_value = first_node['label']
        # 如果 label 是列表，遍历列表并将其中的元素转化为字符串后连接
        if isinstance(first_label_value, list):
            first_label_value = ', '.join(str(item) for item in first_label_value)
        # 根据节点的度分配节点大小
        first_weight = first_node['weight'] if first_node['weight'] is not None else 0
        first_width_height = first_weight * 10 + 100

        # 一度节点 节点格式
        first_contacts_node = {
            'data': {
                'id': str(first_node['target']),
                'name': first_node['name'],
                'label': first_label_value,
                'unit': first_node['unit'],
                'section': first_node['section'],
                'post': str(first_node['post']),
                'weight': str(first_node['weight']),
                'communityId': str(first_node['communityId']),
            },
            'style': {
                'width': first_width_height,
                'height': first_width_height,
                'background-color': '#FAF9DE'
            }
        }
        nodes.append(first_contacts_node)

        # 一度关系 边格式
        first_contacts_rel = {
            'data': {
                'source': str(first_node['source']),
                'target': str(first_node['target']),
                'label': str(first_node['type']),
            }
        }
        edges.append(first_contacts_rel)

    # 导入二度联系人节点信息
    for second_node in second_rel_data:
        # 确保 label 是字符串，如果是列表则转换为逗号分隔的字符串
        second_label_value = second_node['label']
        # 如果 label 是列表，遍历列表并将其中的元素转化为字符串后连接
        if isinstance(second_label_value, list):
            second_label_value = ', '.join(str(item) for item in second_label_value)

        # 根据节点的度分配节点大小
        second_weight = second_node['weight'] if second_node['weight'] is not None else 0
        second_width_height = second_weight + 100

        # 节点格式
        second_contacts_node = {
            'data': {
                'id': str(second_node['target']),
                'name': second_node['name'],
                'label': second_label_value,
                'unit': second_node['unit'],
                'section': second_node['section'],
                'post': str(second_node['post']),
                'weight': str(second_node['weight']),
                'communityId': str(second_node['communityId']),
            },
            'style': {
                'width': second_width_height,
                'height': second_width_height,
                'background-color': '#FAF9DE'
            }
        }
        nodes.append(second_contacts_node)
        # 边格式
        second_contacts_rel = {
            'data': {
                'source': str(second_node['source']),
                'target': str(second_node['target']),
                'label': str(second_node['type']),
            }
        }
        edges.append(second_contacts_rel)

    # 图：节点+边
    elements = nodes + edges
    return elements

# 测试
# graph = now_social('技术中介', '三螺旋', '运营部', '马晓雪')
# print(graph)




