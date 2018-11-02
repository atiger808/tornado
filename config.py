# _*_ coding: utf-8 _*_
# @Time     : 2018/6/26 22:01
# @Author   : Ole211
# @Site     : 
# @File     : config.py    
# @Software : PyCharm
from libs.flash.flash_libs import get_flashed_messages
from libs.permission.permission_auth.permission_interface_libs import menu_permission

settings = dict(
    headers = {
'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
'upgrade-insecure-requests':'1',
},
    template_path = 'templates',
    static_path = 'static',
    debug = True,
    cookie_secret = 'aaaa',
    login_url = '/auth/user_login',
    xsrf_cookies = True,
    ui_methods = {
        "menu_permission":  menu_permission,
        "get_flashed_messages": get_flashed_messages
    },
    pycket = {
        'engine': 'redis', #  设置存储器类型
        'storage': {
            'host':'127.0.0.1',
            'port': 6379,
            'db_sessions': 5,
            'db_notifications': 11,
            'max_connections': 2 ** 31,
        },
        'cookies': {
            'expires_days': 30, # 设置过期时间
        },
    },
)
