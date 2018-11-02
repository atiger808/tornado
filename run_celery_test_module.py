# _*_ coding: utf-8 _*_
# @Time     : 2018/9/5 20:12
# @Author   : Ole211
# @Site     : 
# @File     : run_celery_test_module.py    
# @Software : PyCharm

from celery_test_module.celery_tasks import add, manage_redis

# celery 执行的命令
# celery -A celery_test_module worker -l info -c 5
# add.delay(5, 7)
# manage_redis.delay()

import time
for i in xrange(50):
    add.delay(i+1, 0)
    time.sleep(1)
