# _*_ coding: utf-8 _*_
# @Time     : 2018/6/26 23:12
# @Author   : Ole211
# @Site     : 
# @File     : dbsession.py    
# @Software : PyCharm
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 连接数据库
HOSTNAME = '123.207.127.184'
PORT = '3306'
DATABASE = 'tornado_test_002'
USERNAME = 'develop'
PASSWORD = 'QWEqwe123'
# DB_URI 的格式; dialect（mysql/sqlite） + driver://username:password@host:port/database?charset=utf8
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format( USERNAME,
                                                               PASSWORD,
                                                               HOSTNAME,
                                                               PORT,
                                                               DATABASE
                                                            )

# 1创建一个engine引擎
engine = create_engine(DB_URI, echo=False)
# 2sessionmaker生成一个session类
Session = sessionmaker(bind=engine)
# 3创建一个session 实例
dbSession = Session()
# 4 创建一个模型基类
Base = declarative_base(engine)

if __name__== '__main__':
    print(dir(Base))
    print('--'*30)
    print(dir(Session))