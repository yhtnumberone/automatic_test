from common.lib.pip_install import pymysql
from common.lib.module_tools.LogHandler import LogHandler
from common.lib.module_tools.set_config import Set_Section

confpath = Set_Section(section_name='environment',filename='test_env_conf')
db = confpath.read_section('database')


logger = LogHandler()

class OperateMDdb:
    def __init__(self):
        self.conn = pymysql.connect(
            host='',
            user='QiYeFuWuAll',
            password='aYtEnhdDlNvAwk2UvCp$',
            port=9090,
            db=db,
            charset='utf8mb4',
        )
        self.cur = self.conn.cursor()
        logger.info('连接数据库')

    def selectsql(self,sql):
        try:
            count = self.cur.execute(sql)
            res = self.cur.fetchall()
            # lenth = len(args)
            # res = cur.fetchall()
            # reslist = []
            # for i in range(count):
            #     for j in range(lenth):
            #         r = str(res[i][j])
            #         reslist.append(r)
            #         reslist.sort()
            # reslist.sort()
            logger.info(f'查询数据库：sql：{sql} \n 数据库查询结果:{res}')
            return res
        except Exception as e:
            logger.info((f'查询数据库出错：{e}'))
            print(e)
        finally:
            self.cur.close()
            self.conn.close()

    def updatesql(self,table,key,value,condition1,condition2):
        conn = self.conn
        cur = conn.cursor()
        try:
            sql = "update %s set %s = %s where %s = \'%s\'"
            # sql = 'select ent_full_name from tenant_ent where t_ent_id=10159'
            print('sql.',sql)
            cur.execute(sql,[table,key,value,condition1,condition2])
        except Exception as e:
            print(e)
        finally:
            cur.close()
            conn.close()

    def deletesql(self,sql):
        conn = self.conn
        cur = conn.cursor()
        try:
            # sql = "DELETE FROM %s WHERE %s = '%s' "%(table,condition1,condition2)
            # sql = 'select ent_full_name from tenant_ent where t_ent_id=10159'
            print('sql.',sql)
            cur.execute(sql)
        except Exception as e:
            print(e)
        finally:
            cur.close()
            conn.close()
    #完整sql操作数据库方法
    def realsql(self,sql):
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
            res = cur.fetchall()
            return res
        except Exception as e:
            print(e)
        finally:
            cur.close()
    #关闭数据库连接
    def close_db(self):
        self.cur.close()
        self.conn.close()
        logger.info('关闭数据库连接')


class OperateTMdb:
    def __init__(self):
        self.conn = pymysql.connect(
            host='',
            user='QiYeFuWuAll',
            password='aYtEnhdDlNvAwk2UvCp$',
            port=9090,
            db='jff-p-sit',
            charset='utf8mb4',
        )

    def selectsql(self,field,table,condition):
        conn = self.conn
        cur = conn.cursor()
        sql = 'select {field} from {table} where {condition}'.format(field=field, table=table, condition=condition)
        # sql = 'select * from name_list order by updated_tm desc limit 10;'
        cur.execute(sql)
        res = cur.fetchall()
        # print(res)
        cur.close()
        conn.close()
        return res


class djy_db():
    def __init__(self):
        self.conn = pymysql.connect(
            host='',
            user='QiYeFuWuAll',
            password='aYtEnhdDlNvAwk2UvCp$',
            port=9090,
            db='dajiaying-sit',
            charset='utf8mb4',
        )

    # 完整sql操作数据库方法
    def realsql(self, sql):
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
            res = cur.fetchall()
            return res
        except Exception as e:
            print(e)
        finally:
            cur.close()