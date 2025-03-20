import logging
from data.neo4j_connection import Neo4jConnection

# 配置日志
logging.basicConfig(level=logging.INFO)


# Neo4j 数据库连接
def expect_social(login_type, login_unit, login_section, login_name):
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
    login_node_data = neo4j_conn.run_query(login_node_query)
    logging.info(f"Executing query: {login_node_query}")

    # 已建联单位部门
    contact_unit_query = f"""
        MATCH (a:`{login_type}` {{unit:'{login_unit}', section:'{login_section}', name:'{login_name}'}})
        -[r1]-(b1: `企业人员`) 
        WITH collect(b1.unit) AS unit, collect(b1.section) AS section
        MATCH (n)
        WHERE n.unit in unit and n.section in section
        RETURN 
            labels(n) as label,
            n.unit as unit,
            max(n.coreValue) as max_core
    """
    contact_unit_data = neo4j_conn.run_query(contact_unit_query)
    logging.info(f"Executing query: {contact_unit_query}")

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

        # 导入期望节点信息
        for contact_unit in contact_unit_data:
            contact_unit_label = contact_unit['label']
            # 如果 label 是列表，遍历列表并将其中的元素转化为字符串后连接
            if isinstance(contact_unit_label, list):
                contact_unit_label = ', '.join(str(item) for item in contact_unit_label)
            unit = contact_unit['unit']
            max_core = contact_unit['max_core']
            expect_node_query = f"""
                MATCH (n: `高校人员`  {{unit:'{selected_unit}', section:'{selected_section}'}}) 
                with max(coreValue) as max_core         
                MATCH (n: `高校人员`  {{unit:'{selected_unit}', section:'{selected_section}'}}) 
                where coreValue = max_core
                optional match (n)-[r]-
                    (a:`{login_type}` {{unit:'{login_unit}', section:'{login_section}', name:'{login_name}'}})
                return 
                    id(n) AS target,
                    labels(n) AS label, 
                    n.name AS name,
                    n.unit AS unit,
                    n.section AS section,
                    n.post AS post,
                    n.weight AS weight,
                    n.communityId AS communityId,
                    case when a is null then '期望' else '已有' end as r_type
            """
            expect_node_data = neo4j_conn.run_query(expect_node_query)
            logging.info(f"Executing query: {expect_node_query}")

            neo4j_conn.close()  # Close connection

            for expect_node in expect_node_data:
                # 根据节点的度分配节点大小
                expect_weight = expect_node['weight'] if expect_node['weight'] is not None else 0
                expect_width_height = expect_weight + 100

                # 确保 label 是字符串，如果是列表则转换为逗号分隔的字符串
                expect_label_value = expect_node['label']
                # 如果 label 是列表，遍历列表并将其中的元素转化为字符串后连接
                if isinstance(expect_label_value, list):
                    expect_label_value = ', '.join(str(item) for item in expect_label_value)

                # 根据标签定义颜色
                if expect_label_value == '高校人员':
                    expect_background_color = '#FAF9DE'
                elif expect_label_value == '政府人员':
                    expect_background_color = '#C7EDCC'
                elif expect_label_value == '企业人员':
                    expect_background_color = '#DCE2F1'
                else:
                    expect_background_color = '#E9EBFE'

                # 节点格式
                expect_contacts_node = {
                    'data': {
                        'id': str(expect_node['target']),
                        'name': expect_node['name'],
                        'label': expect_label_value,
                        'unit': expect_node['unit'],
                        'section': expect_node['section'],
                        'post': str(expect_node['post']),
                        'weight': str(expect_node['weight']),
                        'communityId': str(expect_node['communityId']),
                        'r_type': expect_node['r_type'],
                    },
                    'style': {
                        'width': expect_width_height,
                        'height': expect_width_height,
                        'background-color': expect_background_color
                    }
                }
                nodes.append(expect_contacts_node)

                if expect_node['r_type'] == '期望':
                    # 边格式
                    expect_contacts_rel = {
                        'data': {
                            'source': str(login_node['id']),
                            'target': str(expect_node['target']),
                            'label': '期望建联'
                        },
                        'style': {
                            'line-style': 'dashed'  # 设置边为虚线
                        }
                    }
                    edges.append(expect_contacts_rel)
                else:
                    # 边格式
                    now_contacts_rel = {
                        'data': {
                            'source': str(login_node['id']),
                            'target': str(expect_node['target']),
                            'label': '已有建联'
                        }
                    }
                    edges.append(now_contacts_rel)

    # 图：节点+边
    elements = nodes + edges
    return elements


# # 测试
# if __name__ == '__main__':
#     graph = expect_social('技术中介', '三螺旋', '马晓雪')
#     print(graph)


