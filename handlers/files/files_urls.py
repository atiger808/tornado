# _*_ coding: utf-8 _*_
# @Time     : 2018/8/18 16:24
# @Author   : Ole211
# @Site     : 
# @File     : files_urls.py    
# @Software : PyCharm
from handlers.files.files_handlers import  (
    FilesListHandler,
    FilesUploadHandler,
    FilesListDelFileHandler,

    FilesMessageHandler,
    FilesPageListHandler,
    FileCreateSharingLinks,
    FileAuthSharingLinks,
    FileSharingListHandler,
    FileSaveSharingHandler,

    DelFileHandler,
    FinalDelFilesHandler,
    RecoverFileHandler,
    FilesDownLoadHandler, #非阻塞
    FilesDownLoadHandler2, #阻塞
)

files_urls = [
    (r'/files/files_list/([1-9]{1,3})', FilesListHandler),  #文件列表
    (r'/files/files_up_load', FilesUploadHandler),  #文件上传
    (r'/files/files_del', FilesListDelFileHandler),  #删除文件
    (r'/files/files_message', FilesMessageHandler), #文件详情
    (r'/files/files_page_list/([1-9]{1,3})', FilesPageListHandler), #文件分页
    (r'/files/files_down', FilesDownLoadHandler), #文件下载


    # 分享链接接口
    (r'/files/files_create_sharing_links', FileCreateSharingLinks), #创建分享链接
    (r'/files/files_auth_sharing_links', FileAuthSharingLinks), #验证分享链接
    (r'/files/files_sharing_list', FileSharingListHandler), #分享链接的文件列表
    (r'/files/files_save_sharing_links', FileSaveSharingHandler), #保存分享链接的文件

    # 回收站接口
    (r'/files/files_delete', DelFileHandler), #删除文件
    (r'/files/files_delete_final', FinalDelFilesHandler), #彻底删除文件
    (r'/files/files_recovery', RecoverFileHandler), #恢复文件
]