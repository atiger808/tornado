# _*_ coding: utf-8 _*_
# @Time     : 2018/9/1 15:44
# @Author   : Ole211
# @Site     : 
# @File     : message_urls.py    
# @Software : PyCharm
from message_handler import MessageHandler, MessageWebSocket, SendMessageHandler

message_urls = [
    (r'/message/message', MessageHandler),
    (r'/message/message_websocket', MessageWebSocket),
    (r'/message/send_message', SendMessageHandler),
]