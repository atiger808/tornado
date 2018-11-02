# _*_ coding: utf-8 _*_
# @Time     : 2018/9/1 15:44
# @Author   : Ole211
# @Site     : 
# @File     : message_handler.py    
# @Software : PyCharm
from datetime import datetime
import tornado.escape
from handlers.base.base_handler import BaseWebSocket,BaseHandler
from models.permission.permission_model import Role




# class SendMessageHandler(BaseHandler):
#     def get(self):
#         kw = {
#             'user_msg': [],
#             'role_msg': [],
#             'system_msg': [],
#             'roles': Role.all(),
#         }
#         self.render('message/message_send_message.html', **kw)
#     def post(self):
#         content = self.get_argument('content', '')
#         send_type = self.get_argument('send_type', '')
#         roleid = self.get_argument('roleid', '')
#         user = self.get_argument('user', '')
#         if send_type == "system":
#             MessageWebSocket.send_system_message(content)
#         if send_type == "role":
#             MessageWebSocket.send_role_message(content, roleid)
#         if send_type == "user":
#             MessageWebSocket.send_user_message(content, user)



# class MessageHandler(BaseHandler):
#     def get(self):
#         cache = self.conn.lrange('message:list', -5 , -1)  #['','']
#         cache.reverse()
#         cache_list = []
#         for c in cache:
#             msg = tornado.escape.json_decode(c)
#             cache_list.append(msg)
#
#         user_list = self.conn.lrange('message:user_list',0, -1)
#         kw = {'cache': cache_list,'user_list':user_list}
#         self.render('message/message_chat.html', **kw)

#
# class MessageWebSocket(BaseWebSocket): #zhangsan  lishi
#
#     users = {}# {'zhangsan': MessageWebSocket(), 'lishi': MessageWebSocket()}
#
#     @classmethod
#     def send_system_message(cls, message):
#         for f, v in MessageWebSocket.users.iteritems():
#             v.write_message(message)
#
#     @classmethod
#     def send_role_message(cls, message, role_id):
#         role = Role.by_id(role_id)
#         role_users = role.users #[zhangsan, lishi , wangwu]  [zhangsan, lishi]
#         for user in role_users:
#             if MessageWebSocket.users.get(user.name, None) is not None:
#                 MessageWebSocket.users[user.name].write_message(message)
#             else:
#                 #self.conn.lpush("ws:role_off_line",message)
#                 pass
#
#     @classmethod
#     def send_user_message(cls, message, user):
#         if cls.users.get(user, None) is not None:
#             cls.users[user].write_message(message)
#         else:
#             #self.conn.lpush("ws:user_off_line",message)
#             pass
#
#     def open(self):
#         print '----------------open------------------'
#         MessageWebSocket.users[self.current_user.name] = self
#         # users['zhangsan'] = self
#         # users['lishi'] =self
#         print MessageWebSocket.users
#         pass
#
#     def on_close(self):
#         print '---------------close------------------'
#         pass
#
#     def on_message(self, message):
#         for f, v in MessageWebSocket.users.iteritems():
#             v.write_message(message)



#---------------------------------------------------------------------------


class SendMessageHandler(BaseHandler):
    def get(self):
        kw = {
            'user_msg': self.get_redis_json_to_dict('user'),# 发送给个人
            'role_msg': self.get_redis_json_to_dict('role'),# 发送给部门
            'system_msg': self.get_redis_json_to_dict('system'), #发送给所有人
            'roles': Role.all(),
        }
        self.render('message/message_send_message.html', **kw)

    def get_redis_json_to_dict(self, target):
        msgs = self.conn.lrange('message:%s'%target, -3, -1)
        msgs.reverse()
        dict_list = []
        for c in msgs:
            msg = tornado.escape.json_decode(c)
            dict_list.append(msg)
        return dict_list

    def post(self):
        content = self.get_argument('content', '')
        send_type = self.get_argument('send_type', '')
        roleid = self.get_argument('roleid', '')
        user = self.get_argument('user', '')

        if send_type == 'system':
            MessageWebSocket.send_system_message(self, content, send_type)
        if send_type == 'role':
            MessageWebSocket.send_role_message(self, content, send_type, roleid)
        if send_type == 'user':
            MessageWebSocket.send_user_message(self, content, send_type, user)

class MessageHandler(BaseHandler):
    def get(self):
        # 从redis取出数据，是个列表
        cache = self.conn.lrange('message:list', -8, -1)
        cache.reverse() #反转一下
        cache_list = []
        for c in cache:
            msg = tornado.escape.json_decode(c)
            cache_list.append(msg)

        kw = {'cache': cache_list}
        self.render('message/message_chat.html', **kw)



class MessageWebSocket(BaseWebSocket):

    users = {} # {'zhangsan':MessageWebSocket(), '27452': MessageWebSocket()}

    @classmethod
    def send_system_message(cls, self, content, send_type):
        target = 'system'
        redis_msg = cls.dict_to_json(self, content, send_type, target)
        self.conn.rpush('message:%s'%send_type, redis_msg)
        for f, v in MessageWebSocket.users.iteritems():
            v.write_message(redis_msg)

    @classmethod
    def dict_to_json(cls, self, content, send_type, target):
        msg = {
            'content': content,
            'send_type': send_type,
            'sender': self.current_user.name,
            'target': target,
            'datetime': datetime.now().strftime('%y-%m-%d %H:%M:%S'),
        }
        return tornado.escape.json_encode(msg)


    @classmethod
    def send_role_message(cls, self, content, send_type, roleid):
        role = Role.by_id(roleid)
        redis_msg = cls.dict_to_json(self, content, send_type, role.name)
        self.conn.rpush('message:%s' % send_type, redis_msg)
        role_users = role.users
        for user in role_users:
            if MessageWebSocket.users.get(user.name, None) is not None:
                MessageWebSocket.users[user.name].write_message(redis_msg)
            else:
                # self.conn.lpush('ws: role off line', message)
                pass
    @classmethod
    def send_user_message(cls, self, content, send_type, user):
        redis_msg = cls.dict_to_json(self, content, send_type, user)
        self.conn.rpush('message:%s' % send_type, redis_msg)
        if cls.users.get(user, None) is not None:
            cls.users[user].write_message(redis_msg)
        else:
            # self.conn.lpush('ws: user off line', message)
            pass

    def open(self):
        print('----------------------open-----------------------')
        MessageWebSocket.users[self.current_user.name] = self
        self.conn.rpush('message:user_list', self.current_user.name)
        print(MessageWebSocket.users)
        # users['zhangsan'] = self
        # users['27452'] = self
        print(MessageWebSocket.users)
        MessageWebSocket.send_system_message(
            self, '%s: 上线了' % self.current_user.name.encode('utf-8'), 'system'
        )


    def on_close(self):
        print('----------------------close-----------------------')
        del MessageWebSocket.users[self.current_user.name]
        print(MessageWebSocket.users)
        MessageWebSocket.send_system_message(
            self, '%s: 下线了' % self.current_user.name.encode('utf-8'), 'system'
        )

    def on_message(self, message):
        print '---------------on_message------------------'
        print(message) # 服务器向后台发消息
        # json字符串转python字典，调用tornado.escape.json_decode()方法
        msg = tornado.escape.json_decode(message)
        msg.update({
            'name': self.current_user.name,
            'useravatar': self.current_user.avatar,
            'datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        })
        # python字典转json字符串，调用tornado.escape.json_encode()方法
        message = tornado.escape.json_encode(msg)
        self.conn.rpush('message:list', message) #保存到redis

        for f, v in MessageWebSocket.users.iteritems():
            v.write_message(msg)


        # 给其他人发信息
        # f:是用户名，
        # v:MessageWebSocket() 类似<handlers.message.message_handler.MessageWebSocket object at 0xb62bcdcc>
        # if name:
        #     for f, v in MessageWebSocket.users.iteritems():
        #         # 做了个判断，把自己排除，也就是给除了自己的其他人发消息
        #         print('f--', f)
        #         print('v--', v)
        #         # if f != self.current_user.name: #排除自己
        #         #     v.write_message(message)
        #         # if f == 'aaa': #给指定一个人发送消息
        #         if f == message['name']:
        #             v.write_message(message)
        #
        # # 群发， 给指定角色的用户群发消息
        # elif role_id:
        #     role = Role.by_id(role_id)
        #     role_users = role.users
        #     for user in role_users:
        #         # 判断是否在线， 如果在线就发送消息
        #         if MessageWebSocket.users.get(user.name, None) is not None:
        #             MessageWebSocket.uses[user.name].write_message(message)
        #
        # # 给所有人发送消息
        # else:
        #     for f, v in MessageWebSocket.users.iteritems():
        #         v.write_message(message)

        # self.write_message(message) # 服务器向浏览器发消息（主动发送）