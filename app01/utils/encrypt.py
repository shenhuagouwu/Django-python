"""
定义md5加密方法
"""
from django.conf import settings
import hashlib

def md5(data_string):
    obj=hashlib.md5()
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()