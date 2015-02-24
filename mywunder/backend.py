#coding:utf-8

'''
    module: backend
    ~~~~~~~~~~~~~~~

    method to query db
'''


import json
from .db_helper import DBHelper, tb_lists, tb_tasks, init_db2
from sync import api_client
import myconfig


class DBMsg():
    not_exits = "db object not exists, init or update config again please"


def login(email, password):
    api_client.login(email, password)
    with open(myconfig.config_txt, 'wb') as f:
        f.write(json.dumps({'token': api_client.token}))

def init_db():
    init_db2()


def query_list(list_name=None):
    if list_name:
        #return list id
        a = DBHelper.fetchall("select list_id from %s"
                              " where title='%s'" % (tb_lists, list_name))
        assert a, DBMsg.not_exits
        return str(a[0]['list_id'])
    else:
        a = DBHelper.fetchall("select * from %s" % tb_lists)
        assert a, DBMsg.not_exits
        return list(a)


def query_task(task_name):
    a = DBHelper.fetchall("select * from %s"
                          " where title='%s'" % (tb_tasks, task_name))
    assert a, DBMsg.not_exits
    return list(a)


def _get_listID_by_title2(title):
    a = DBHelper.fetchall("select list_id from %s"
                          " where title='%s'" % (tb_lists, title))
    assert a, DBMsg.not_exits
    return a[0]['list_id']


def query_tasks(list_name):
    lid = _get_listID_by_title2(list_name)
    a = DBHelper.fetchall("select * from %s"
                          " where list_id='%s'" % (tb_tasks, lid))
    assert a, DBMsg.not_exits
    return list(a)
