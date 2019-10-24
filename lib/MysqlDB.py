#coding=utf-8
import pymysql
from common.ReadAndWriteFiles import ReadAndWriteFiles



class MysqlDB(object):
    # ==========封装MySQL基本操作=====================
    def initMD(self, conf_mysql="test"):
        # ===========读取MysqlDB.ini文件===========
        rwf = ReadAndWriteFiles()
        self.host =  rwf.ini_read(rwf.pathmysql, "mysql_host")
        self.port = int( rwf.ini_read(rwf.pathmysql, "mysql_port"))
        self.db = rwf.ini_read(rwf.pathmysql, "mysql_db_name")
        self.user =  rwf.ini_read(rwf.pathmysql, "mysql_user")
        self.password =  rwf.ini_read(rwf.pathmysql, "mysql_password")
        self.conn = pymysql.connect(host=self.host,
                                    port=self.port,
                                    user=self.user,
                                    passwd=self.password,
                                    db=self.db)
        self.cursor = self.conn.cursor()

    # 查询,返回一条数据
    def select_return_A_data(self, select_sql):
        self.initMD()
        try:
            self.cursor.execute(select_sql)
            result = self.cursor.fetchone()
        except Exception as e:
            print(e)
        finally:
            self.close_db()
        return result

    # 查询,返回一组数据
    def select_return_datas(self, select_sql):
        self.initMD()
        try:
            self.cursor.execute(select_sql)
            result = self.cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            self.close_db()
        return result


    # 删除
    def delete(self, del_sql):
        self.initMD()
        try:
            self.cursor.execute(del_sql)
            self.conn.commit()
        except Exception as e:
            print(e.message)
        finally:
            self.close_db()

    # 更新
    def sql_update(self, update_sql):
        self.initMD()
        try:
            self.cursor.execute(update_sql)
            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            self.close_db()

    # 插入
    def insert(self, insert_sql):
        self.initMD()
        try:
            self.cursor.execute(insert_sql)
            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            self.close_db()

            # 关闭数据库连接
    def close_db(self):
        self.conn.close()

if __name__=="__main__":
    a = MysqlDB()
    # b = a.select_return_A_data("SELECT mes_body FROM qtw_invest_db.p2p_sms_record WHERE receive_address = '15600000040' ORDER BY send_time DESC LIMIT 1;")
    b = a.sql_update("UPDATE qtw_invest_db.p2p_user_reg SET lock_off_time='2019-01-01 01:01:01' WHERE cif_account='15600000002';")
    print(b)
