from sqlite3_backend import LocalFlowControlDB


class CacheUtil:
    @staticmethod
    def try_get_execute_lock(key):
        """
        尝试获取分布式锁，获取不到返回第一个元素为RUNNING，获取到了锁就把下次执行时间也一起返回
        :param key:
        :return:
        """
        local_flow_control_db = LocalFlowControlDB()
        return local_flow_control_db.get_next_run_time(key)

    @staticmethod
    def try_release_execute_lock(key, next_run_time):
        """
        释放分布式锁的同时更新计划下次执行时间
        :param key:
        :param next_run_time:
        :return:
        """
        local_flow_control_db = LocalFlowControlDB()
        return local_flow_control_db.renew_next_run_time(key, next_run_time)
