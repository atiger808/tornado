# _*_ coding: utf-8 _*_
# @Time     : 2018/9/29 4:31
# @Author   : Ole211
# @Site     : 
# @File     : urls.py
# @Software : PyCharm

from handler import *

handlers = [
    (r'/', IndexHandler),
    (r'/login', LoginHandler),
    (r'/key_login', KeyLoginHandler),
    (r'/home', HomeHandler),
    (r'/extend', ExtendHandler),
    (r'/taobao', TaobaoHandler),
    (r"/tieba", TiebaHandler),
    (r"/uploadfile", UploadAvatarHandler),
    (r"/baike_crawl", BaikeCrawlHandler),
    (r"/doc", DocHandler),
    (r"/dahua", DahuaHandler),
    (r"/dahuanews", DahuaNewsHandler),
    (r"/huawei", HwHandler),
    (r"/hikvision", HkHandler),
    (r"/wage", WageHandler),
]