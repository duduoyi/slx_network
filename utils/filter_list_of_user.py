import logging
from data.neo4j_connection import Neo4jConnection
import pandas as pd


# 配置日志
logging.basicConfig(level=logging.INFO)


def school_contact_list(login_type, login_unit, login_section, login_name):
    neo4j_conn = Neo4jConnection()
    try:
        school_query = f"""
            MATCH (a:`{login_type}` {{unit:'{login_unit}', section:'{login_section}', name:'{login_name}'}})
                -[r]-(n: `高校人员`) 
            return distinct n.unit as unit, n.section as section
            """
        school_contact = neo4j_conn.run_query(school_query)
        print(f"Neo4j connection successful: {school_contact}")
        school_df = pd.DataFrame(school_contact)
        school_df_renamed = school_df.rename(columns={0: 'school', 1: 'college'})
        return school_df_renamed

    except Exception as e:
        print(f"Neo4j connection error: {e}")
        raise
    finally:
        neo4j_conn.close()


def company_contact_list(login_type, login_unit, login_section, login_name):
    neo4j_conn = Neo4jConnection()
    try:
        company_query = f"""
            MATCH (a:`{login_type}` {{unit:'{login_unit}', section:'{login_section}', name:'{login_name}'}})
                -[r]-(n: `企业人员`) 
            return distinct n.unit as unit
            """
        company_contact = neo4j_conn.run_query(company_query)
        print(f"Neo4j connection successful: {company_contact}")

        return [record["unit"] for record in company_contact]

    except Exception as e:
        print(f"Neo4j connection error: {e}")
        raise
    finally:
        neo4j_conn.close()


def government_contact_list(login_type, login_unit, login_section, login_name):
    neo4j_conn = Neo4jConnection()
    try:
        government_query = f"""
            MATCH (a:`{login_type}` {{unit:'{login_unit}', section:'{login_section}', name:'{login_name}'}})
                -[r]-(n: `政府人员`) 
            return distinct n.unit as unit
            """
        government_contact = neo4j_conn.run_query(government_query)
        print(f"Neo4j connection successful: {government_contact}")

        return [record["unit"] for record in government_contact]

    except Exception as e:
        print(f"Neo4j connection error: {e}")
        raise
    finally:
        neo4j_conn.close()


# 测试
if __name__ == '__main__':
    school_college = school_contact_list('技术中介', '三螺旋', '运营部', '马晓雪')
    print(school_college)
    company_list = company_contact_list('技术中介', '三螺旋', '运营部', '马晓雪')
    print(company_list)
    government_list = government_contact_list('技术中介', '三螺旋', '运营部', '马晓雪')
    print(government_list)