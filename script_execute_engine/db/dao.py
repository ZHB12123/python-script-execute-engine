from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base, Modules

DB_PATH = "data.db"


class ModulesDao:
    engine = create_engine(f'sqlite://{""}/{DB_PATH}')

    def __new__(cls, *args, **kwargs):
        cls.DbSession = sessionmaker(bind=cls.engine)
        cls.session = cls.DbSession()

    @staticmethod
    def create_table():
        Base.metadata.create_all(ModulesDao.engine, checkfirst=True)

    @staticmethod
    def insert(module_info: dict):
        """
        增加一条记录
        :param module_info:
        :return:
        """
        module_info_model = Modules()
        module_info_model.__dict__.update(module_info)
        ModulesDao.session.add(module_info_model)
        ModulesDao.session.commit()

    @staticmethod
    def delete_by_id(_id: int):
        """
        根据主键删除一条数据
        :param _id:
        :return:
        """
        ModulesDao.session.query(Modules).filter(Modules.id == _id).delete()
        ModulesDao.session.commit()

    @staticmethod
    def query_by_id(_id: int):
        """
        根据主键查询
        :param _id:
        :return:
        """
        line = ModulesDao.session.query(Modules).filter(Modules.name == "cc").first()
        result = line.__dict__
        result.pop("_sa_instance_state")
        return result

    @staticmethod
    def query_all():
        lines = ModulesDao.session.query(Modules).all()
        result = []
        for line in lines:
            result_line = line.__dict__
            result_line.pop("_sa_instance_state")
            result.append(result_line)
        return result

    @staticmethod
    def update_by_id(_id: int, module_info: dict):
        """
        更新数据
        :param _id:
        :param module_info:
        :return:
        """
        module_info_model = Modules()
        module_info_model.__dict__.update(module_info)
        ModulesDao.session.add(module_info_model)
        ModulesDao.session.commit()

# 执行一次__new__方法
ModulesDao()
