import sqlite3
import time
import traceback

CREATE_TABLE_SQL1 = '''
CREATE TABLE "app_flow_control_table" (
    "key" text NOT NULL,
    "next_run_time" text,
    PRIMARY KEY ("key")
)
'''

CREATE_TABLE_SQL2 = '''
CREATE TABLE "action_run_lock_table" (
    "key" text NOT NULL,
    "run_status" text,
    "update_time" integer,
    PRIMARY KEY ("key")
)
'''


class LocalFlowControlDB:
    db_file_path = "local_flow_control.db"

    def __init__(self) -> None:
        self.conn = sqlite3.connect(self.db_file_path)
        self.cursor = self.conn.cursor()

    @staticmethod
    def create_flow_control_local_db():
        """
        服务启动的时候建表
        :return:
        """
        conn = sqlite3.connect(LocalFlowControlDB.db_file_path)
        cur = conn.cursor()

        cur.execute('DROP TABLE IF EXISTS "app_flow_control_table";')
        cur.execute(CREATE_TABLE_SQL1)

        cur.execute('DROP TABLE IF EXISTS "action_run_lock_table";')
        cur.execute(CREATE_TABLE_SQL2)

        conn.commit()
        cur.close()
        conn.close()

    def get_next_run_time(self, key):
        """
        抢锁和获取下次执行时间
        :param key: 主键id
        :return:
        """
        # 清缓存
        self.clean_lock()

        # 获取锁
        now_time = int(time.time())
        insert_sql = f"INSERT INTO action_run_lock_table (key,run_status,update_time) VALUES ('{key}','RUNNING',{now_time});"
        try:
            self.cursor.execute(insert_sql)
            self.conn.commit()
        except Exception as e:
            traceback.print_exc()
            return ["RUNNING"]

        # 获取下次执行时间
        query_sql = f"SELECT next_run_time FROM app_flow_control_table WHERE key='{key}';"
        query_result = self.cursor.execute(query_sql).fetchone()
        if not query_result:
            next_run_time = -1
        else:
            next_run_time = int(query_result[0])

        self.close_connection()

        return ["WAITING", next_run_time, time.time() * 1000]

    def renew_next_run_time(self, key, next_run_time):
        """
        更新下次执行时间
        :param key:
        :param next_run_time:
        :return:
        """
        # 释放锁
        delete_sql = f"DELETE FROM action_run_lock_table WHERE key='{key}';"
        self.cursor.execute(delete_sql)
        self.conn.commit()

        # 更新下次执行时间
        update_sql = f"REPLACE INTO app_flow_control_table (key,next_run_time) VALUES ('{key}','{next_run_time}');"
        self.cursor.execute(update_sql)
        self.conn.commit()

        self.close_connection()

    def close_connection(self):
        self.cursor.close()
        self.conn.close()

    def clean_lock(self):
        delete_sql = f"DELETE FROM action_run_lock_table WHERE update_time<{int(time.time()) - 60}"
        self.cursor.execute(delete_sql)
        self.conn.commit()
