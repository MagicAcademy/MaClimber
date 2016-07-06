#!/usr/bin/env python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Conn(object):
    """
    数据库连接对象
    更换db_config以更换数据库
    连接session作为属性
    """
    db_config = 'mysql+pymysql://root:@localhost:3306/maclimber?charset=utf8'

    session = None

    def __init__(self):
        if self.session is None:
            config = self.db_config
            engine = create_engine(config)
            DBSession = sessionmaker(bind=engine)
            self.session = DBSession()
        else:
            pass

    def __del__(self):
        if self.session is not None:
            self.session.close()
        else:
            pass


