# _*_ coding: utf-8 _*_
# @Time     : 2018/6/26 22:52
# @Author   : Ole211
# @Site     : 
# @File     : base_handler.py    
# @Software : PyCharm
import tornado.escape
import tornado.websocket
from libs.pycket.session import SessionMixin
from libs.db.dbsession import dbSession
from libs.redis_conn.redis_conn import conn
from models.account.account_user_model import User

users = {
    'user': User
}

class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def initialize(self):
        self.db = dbSession
        self.conn = conn
        self.flashes = None

    def get_current_user(self):
        """获取当前用户"""
        username = self.session.get("user_name")
        user = None
        if username:
            user = User.by_name(username)
        return user if user else None

    def on_finish(self):
        self.db.close()

class BaseWebSocket(tornado.websocket.WebSocketHandler, SessionMixin):
    def initialize(self):
        self.db = dbSession
        self.conn = conn
        self.flashes = None

    def get_current_user(self):
        """获取当前用户"""
        username = self.session.get('user_name')
        user = None
        if username:
            user = User.by_name(username)
        return user if user else None

    def on_finish(self):
        self.db.close()
