# _*_ coding: utf-8 _*_
# @Time     : 2018/9/4 22:25
# @Author   : Ole211
# @Site     : 
# @File     : celery_config.py    
# @Software : PyCharm
from __future__ import absolute_import
from datetime import timedelta
from celery.schedules import crontab  #设置计时器
"""
celery 主要实现异步任务和定时任务
"""


BROKER_URL = 'redis://127.0.0.1/2'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1/3'

CELERY_TIMEZONE = 'Asia/Shanghai'

# 定时任务
# celery 执行的命令
# celery -A celery_test_module worker -l info -c 5 -B
CELERYBEAT_SCHEDULE = {
    'redis_manage':{
        'task': 'celery_test_module.celery_tasks.manage_redis',
        'schedule': timedelta(seconds=5)  #每多少秒执行一次
    },
    'redis_manage2':{
        'task': 'celery_test_module.celery_tasks.manage_redis',
        'schedule': crontab(minute=50)  #这个定时器是在每个小时的第几分钟执行一次
    }
}
# crontab()参数
# minute 每小时的第几分钟
# hour    每天的几点
# day_of_week 每周的星期几
# day_of_month 每月的哪一天
# month_of_year 每年的那一个月