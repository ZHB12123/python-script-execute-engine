from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, TEXT

Base = declarative_base()


class Modules(Base):
    __tablename__ = "modules"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(64), unique=False, nullable=False)
    upload_time = Column(DateTime)
    package_name = Column(String(1024))
    enter_func = Column(String(64))
    params = Column(TEXT)
    module_path = Column(String(256), nullable=False)

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.upload_time = kwargs.get("upload_time")
        self.package_name = kwargs.get("module_name")
        self.enter_func = kwargs.get("enter_func_name")
        self.params = kwargs.get("run_params")

    def __repr__(self):
        return f"{self.id}--{self.name}--{self.upload_time}--{self.module_name}--{self.enter_func_name}--{self.run_params}"
