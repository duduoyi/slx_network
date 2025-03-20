import logging
from data.mysql_connection import MysqlPatent
import pandas as pd


# 配置日志
logging.basicConfig(level=logging.INFO)


def school_list():
    mysql_conn = MysqlPatent()
    school_query = """
        select
            school,
            case when department = 'NaN' then college else department end as college
        from ods_school_teacher
        group by 1,2
    """
    school_df = mysql_conn.get_mysql_data(school_query)

    return school_df


def company_list():
    mysql_conn = MysqlPatent()
    company_query = """
        select
            `企业名称` as company
        from ods_company_info
        group by 1
    """
    company_df = mysql_conn.get_mysql_data(company_query)

    return company_df


def government_list():
    mysql_conn = MysqlPatent()
    government_query = """
        select
            unit as government
        from ods_government_info
        group by 1
    """
    government_df = mysql_conn.get_mysql_data(government_query)

    return government_df


def intermediary_list():
    mysql_conn = MysqlPatent()
    intermediary_query = """
        select
            unit as intermediary
        from ods_intermediary_info
        group by 1
    """
    intermediary_df = mysql_conn.get_mysql_data(intermediary_query)

    return intermediary_df


# 测试
if __name__ == '__main__':
    try:
        school_data = school_list()
        print(school_data)
        # company_data = company_list()
        # print(company_data)
        # government_data = government_list()
        # print(government_data)
        # intermediary_data = intermediary_list()
        # print(intermediary_data)
    except Exception as e:
        logging.error(f"Error processing data from Mysql: {e}")
        raise
