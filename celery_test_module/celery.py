# _*_ coding: utf-8 _*_
# @Time     : 2018/9/4 22:25
# @Author   : Ole211
# @Site     : 
# @File     : celery.py    
# @Software : PyCharm
from __future__ import absolute_import
from celery import Celery

celery_test = Celery('celery_tornado', include=['celery_test_module.celery_tasks'])

celery_test.config_from_object('celery_test_module.celery_config')

if __name__ == '__main__':
    celery_test.start()