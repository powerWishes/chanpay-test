from configparser import ConfigParser
import psycopg2 as psycopg2

from facade.dto.db.DBConnectionInfo import DBConnectionInfo
from facade.enum.db import DBName, DBENV
from util import WorkspaceUtil

DB_CONFIG_PATH = WorkspaceUtil.get_root_path()+"/resource/config/db/"


def get_db_config(file_path_name, env):
    cp = ConfigParser()
    cp.read(file_path_name)
    global section
    if env is None or not cp.has_section(env):
        section = cp.sections()[0]
    else:
        section = env
    if section is None:
        return
    username = cp.get(section, 'username')
    password = cp.get(section, 'password')
    host = cp.get(section, 'host')
    port = cp.get(section, 'port')
    database = cp.get(section, 'database')
    dbtype = cp.get(section, 'dbtype')
    db_config = DBConnectionInfo(database, username, password, host, port, dbtype)
    return db_config


def get_connection_by_config(db_config_info):
    if db_config_info is None:
        return None
    conn = psycopg2.connect(database=db_config_info.database, user=db_config_info.username,
                            password=db_config_info.password, host=db_config_info.host, port=db_config_info.port)
    return conn


def get_connection(db_name, env):
    db_config = get_db_config(DB_CONFIG_PATH + db_name + ".cfg", env)
    return get_connection_by_config(db_config)


# if __name__ == '__main__':
#     a = get_db_config(DB_CONFIG_PATH + DBName.CHANJET_PAY_CHANNEL + ".cfg", "stable")
#     with get_connection_by_config(a) as aaa:
#         cur = aaa.cursor()
#         bbb = cur.execute("select * from cp_chn_pay_trans limit 10")
#         ccc = cur.fetchall()
#         print(ccc)
#         cur.close()
#     with get_connection(DBName.CHANJET_PAY_CHANNEL, DBENV.STABLE) as aaa:
#         cur = aaa.cursor()
#         bbb = cur.execute("select * from cp_chn_pay_trans limit 10")
#         ccc = cur.fetchall()
#         print(ccc)
#         cur.close()
