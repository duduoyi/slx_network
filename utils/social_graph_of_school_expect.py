import logging
from data.neo4j_connection import Neo4jConnection

# 配置日志
logging.basicConfig(level=logging.INFO)


def expect_social(login_type, login_unit, login_section, login_name, selected_unit, selected_section):
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

    expect_node_query = f"""
        MATCH (n: `高校人员`  {{unit:'{selected_unit}', section:'{selected_section}'}}) 
        with max(n.coreValue) as max_core         
        MATCH (n: `高校人员`  {{unit:'{selected_unit}', section:'{selected_section}'}}) 
        where n.coreValue = max_core
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

    neo4j_conn.close()

    # 节点列表，边列表
    nodes = []
    edges = []
    login_id = []

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
                'width': 100,
                'height': 100,
                'background-color': '#FFF2E2'
            }
        }
        nodes.append(login_node_json)
        login_id.append(str(login_node['id']))

    # 导入期望节点信息
    for expect_node in expect_node_data:
        # 根据节点的度分配节点大小
        expect_weight = expect_node['weight'] if expect_node['weight'] is not None else 0
        expect_width_height = expect_weight * 10 + 50

        # 节点格式
        expect_contacts_node = {
            'data': {
                'id': str(expect_node['target']),
                'name': expect_node['name'],
                'label': '高校人员',
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
                'background-color': '#FAF9DE'
            }
        }
        nodes.append(expect_contacts_node)

        if expect_node['r_type'] == '期望':
            # 边格式
            expect_contacts_rel = {
                'data': {
                    'source': login_id[0],
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
                    'source': login_id[0],
                    'target': str(expect_node['target']),
                    'label': '已有建联'
                }
            }
            edges.append(now_contacts_rel)

    # 图：节点+边
    elements = nodes + edges
    return elements


# 测试
if __name__ == '__main__':
    graph = expect_social('技术中介', '三螺旋', '运营部', '马晓雪', '华中科技大学', '环境科学与工程学院')
    print(graph)
