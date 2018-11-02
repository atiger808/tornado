# _*_ coding: utf-8 _*_
# @Time     : 2018/6/29 7:22
# @Author   : Ole211
# @Site     :
# @File     : 7server.py
# @Software : PyCharm
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
from handlers.test_handler.urls import handlers
from test_config import settings

define('port', default=8000, help='run port', type=int)



if __name__ == '__main__':
    tornado.options.parse_command_line()
    print(options.port)
    app = tornado.web.Application(handlers, **settings)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    print('07server...')
    tornado.ioloop.IOLoop.instance().start()
