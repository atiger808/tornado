# _*_ coding: utf-8 _*_
# @Time     : 2018/7/11 0:57
# @Author   : Ole211
# @Site     : 
# @File     : account_urls.py    
# @Software : PyCharm

from account_auth_handler import LoginHandler, CaptchaHandler, RegistHandler, MobileCodeHandler
from account_handler import (ProfileHandler,
                             ProfileEditHandler,
                             ProfileModifyEmailHandler,
                             ProfileAuthEmailHandler,
                             ProfileAddAvaterHandler,
                             )


account_urls = [
    (r'/auth/user_login', LoginHandler),
    (r'/auth/captcha', CaptchaHandler),
    (r'/auth/user_regist', RegistHandler),
    (r'/auth/mobile_code', MobileCodeHandler),
    (r'/account/user_profile', ProfileHandler),
    (r'/account/user_edit', ProfileEditHandler),
    (r'/account/send_user_email', ProfileModifyEmailHandler),
    (r'/account/auth_email_code', ProfileAuthEmailHandler),
    (r'/account/avatar', ProfileAddAvaterHandler),
]