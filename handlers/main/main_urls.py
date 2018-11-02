# _*_ coding: utf-8 _*_
# @Time     : 2018/6/26 22:49
# @Author   : Ole211
# @Site     : 
# @File     : main_urls.py    
# @Software : PyCharm

from tornado.web import StaticFileHandler
from main_handler import MainHandler
from handlers.account.account_urls import account_urls
from handlers.permission.permission_urls import permission_urls
from handlers.article.article_urls import  article_urls
from handlers.files.files_urls import  files_urls
from handlers.message.message_urls import message_urls
from tornado.web import StaticFileHandler # tornado自带的返回静态文件路径


handlers = [
    (r'/', MainHandler),
    (r'/images/(.*\.(png|jpg|jpeg|mp3|mp4|ogg))', StaticFileHandler, {'path':  'files/'}),
]

handlers += account_urls
handlers += permission_urls
handlers += article_urls
handlers += files_urls
handlers += message_urls
