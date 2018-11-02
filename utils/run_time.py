# _*_ coding: utf-8 _*_
# @Time     : 2018/7/16 2:11
# @Author   : Ole211
# @Site     : 
# @File     : run_time.py    
# @Software : PyCharm

import time

def run_time(func):
    def wrapper(*args, **kwargs):
        t0 = time.time()
        print('start time: %s' %time.strftime('%x', time.localtime()))
        back = func(*args, **kwargs)
        print('end time: %s' %time.strftime('%x', time.localtime()))
        print('run time: %s' %(time.time() - t0))
        return back
    return wrapper