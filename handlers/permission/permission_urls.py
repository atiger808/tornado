# _*_ coding: utf-8 _*_
# @Time     : 2018/7/23 23:46
# @Author   : Ole211
# @Site     : 
# @File     : permission_urls.py    
# @Software : PyCharm

from permission_handler import (
    ManageHandler,
    AddRoleHandler,
    DelRoleHandler,
    AddPermissionHandler,
    DelPermissionHandler,
    AddMenuHandler,
    DelMenuHandler,
    AddHandlerHandler,
    DelHandlerHandler,
    AddUserRoleHandler,
    AddRolePermisssionHandler,
    DelUserRoleHandler,
    AddUserDevRoleHandler,
    DelUserDevRoleHandler,
)
permission_urls = [
    (r'/permission/manage_list', ManageHandler),
    (r'/permission/add_role', AddRoleHandler),
    (r'/permission/del_role', DelRoleHandler),
    (r'/permission/add_permission', AddPermissionHandler),
    (r'/permission/del_permission', DelPermissionHandler),
    (r'/permission/add_menu', AddMenuHandler),
    (r'/permission/del_menu', DelMenuHandler),
    (r'/permission/add_handler', AddHandlerHandler),
    (r'/permission/del_handler', DelHandlerHandler),
    (r'/permission/user_add_role', AddUserRoleHandler),
    (r'/permission/role_add_permission', AddRolePermisssionHandler),
    (r'/permission/del_user_role', DelUserRoleHandler),
    (r'/permission/add_user_dev', AddUserDevRoleHandler),
    (r'/permission/del_user_dev_role', DelUserDevRoleHandler),
]