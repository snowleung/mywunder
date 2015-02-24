#coding:utf-8
import os
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s:%(lineno)s - %(funcName)20s() - %(name)s - %(levelname)s - %(message)s')
logging.warning('load module:%s', __name__)

user_path = os.path.expanduser("~/")
dir_path = os.path.join(user_path, '.mywunder/')
try:
    os.mkdir(dir_path)
except OSError:
    pass
config_txt = os.path.join(dir_path, 'config.txt')
db_path = os.path.join(dir_path, "mywunder.db")

CLIENT_ID = 'ce310d4e732dc98c6a07'
