# _*_ coding: utf-8 _*_
# @Time     : 2018/6/26 22:49
# @Author   : Ole211
# @Site     : 
# @File     : main_handler.py    
# @Software : PyCharm

import tornado.web
from handlers.base.base_handler import BaseHandler

class MainHandler(BaseHandler):
    def get(self):
        # self.render('account/account_edit.html')
        self.redirect('/permission/manage_list')

