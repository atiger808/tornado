# _*_ coding: utf-8 _*_
# @Time     : 2018/6/26 22:01
# @Author   : Ole211
# @Site     : 
# @File     : server.py    
# @Software : PyCharm

import tornado.httpserver
import tornado.web
import tornado.ioloop
import tornado.escape
from tornado.options import define, options
from config import settings
from handlers.main.main_urls import handlers
from models.account.account_user_model import User
from models.article import article_model
from models.files.upload_file_model import  Files
from libs.db import create_tables
from libs.db.dbsession import dbSession



define('port', default=8888, help='run port', type=int)
define('runserver', default=False, help='start server', type=bool)
define('t', default=False, help='create table', type=bool)
define('u', default=False, help='create user', type=bool )




if __name__ == '__main__':
    options.parse_command_line()
    if options.t:
        create_tables.run()
    if options.u:
        user = User()
        user.name = '36965'
        user.password = '123'
        user.email = "119773452@qq.com"
        dbSession.add(user)
        dbSession.commit()

    if options.runserver:
        app = tornado.web.Application(handlers,**settings)
        http_server = tornado.httpserver.HTTPServer(app)
        http_server.listen(options.port)
        print('start server ...')
        tornado.ioloop.IOLoop.instance().start()
