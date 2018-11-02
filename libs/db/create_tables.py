# _*_ coding: utf-8 _*_
# @Time     : 2018/6/27 0:49
# @Author   : Ole211
# @Site     : 
# @File     : create_tables.py    
# @Software : PyCharm

from dbsession import engine
from dbsession import Base

# 创建好的User类， 映射到数据库的users表中

def run():
    print('---------------create_all--------------')
    Base.metadata.create_all(engine)
    print('---------------create_end--------------')

if __name__ == '__main__':
    run()