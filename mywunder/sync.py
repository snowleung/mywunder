#coding:utf-8

'''
    module:sync
    ~~~~~~~~~~~

    fetch data from wunderlist, and store to database
'''


import json
import time
import dateutil.parser
from datetime import datetime
from wunderpy import api
from db_helper import DBHelper, tb_lists, tb_tasks
from . import myconfig


api_client = api.APIClient(myconfig.CLIENT_ID)


def login(email, password):
    pass

def auth():
    try:
        with open(myconfig.config_txt, 'r') as f:
            content = f.read()
            token = json.loads(content)['token']
            api_client.set_token(token)
    except TypeError, e:
        print 'error :{}'.format(e)

def get_tasks(list_id):
    '''
    :returns: JsonResponse
    '''
    return api_client.send_request(api.calls.get_tasks(list_id, True))


def get_lists():
    return api_client.send_request(api.calls.get_lists())


def sync_tasks(data):
    '''
    insert or update database
    '''
    try:
        list_id = data[0]['list_id']
        d = DBHelper.fetchall("select task_id from {0} where list_id = {1}".format(tb_tasks, list_id))
        d2 = [o['id'] for o in data]
        _delete_task = [ddd['task_id'] for ddd in d if ddd['task_id'] not in d2]
        for dx in _delete_task:
            print 'now delete..'
            sql = "delete from %s where task_id = '%s'" % (tb_tasks, dx)
            print sql
            DBHelper.delete(sql)
    except IndexError, e:
        print 'index error ,msg:{}'.format(e)
        print 'data:{}'.format(data)
    for o in data:
        q = DBHelper.fetchall("select * from %s"
                              " where task_id = '%s'" % (tb_tasks, o['id']))
        updated_at = datetime.now().date()
        created_at = dateutil.parser.parse(o['created_at']).date()
        if q:
            q = q[0]
            if str(q['updated_at']) == str(updated_at):
                print 'no update!'
            else:
                print '%s update now...' % o['title']
                update_sql = "update %s set title='%s', created_at='%s', updated_at='%s', content='%s', list_id='%s' where task_id='%s'" % (tb_tasks, o['title'], created_at, updated_at, json.dumps(o), o['list_id'], o['id'])
                DBHelper.update(update_sql)
        else:
            print 'insert now...'
            sql = ''
            sql = "insert into %s (title,created_at,updated_at,content,task_id,list_id) values('%s', '%s', '%s','%s','%s','%s')" % (tb_tasks, o['title'], created_at, updated_at, json.dumps(o), o['id'], o['list_id'])
            print sql
            DBHelper.update(sql)
    print 'success sync lists'


def sync_lists():
    '''
    insert or update database
    :return data: list data, json, ref https://developer.wunderlist.com/documentation/endpoints/list
    '''
    data = get_lists()
    print data
    d = DBHelper.fetchall("select list_id from %s" % tb_lists)
    d2 = [o['id'] for o in data]
    _delete_list = [ddd['list_id'] for ddd in d if ddd['list_id'] not in d2]
    for dx in _delete_list:
        print 'now delete..'
        sql = "delete from %s where list_id = '%s'" % (tb_lists, dx)
        print sql
        DBHelper.delete(sql)
    for o in data:
        q = DBHelper.fetchall("select * from %s"
                              " where list_id = '%s'" % (tb_lists, o['id']))
        #updated_at = dateutil.parser.parse(o['updated_at']).date() # deprecated
        updated_at = datetime.now().date()
        created_at = dateutil.parser.parse(o['created_at']).date()
        if q:
            q = q[0]
            if str(q['updated_at']) == str(updated_at):
                print 'no update!'
            else:
                print '%s update now...' % o['title']
                update_sql = "update %s set title='%s', created_at = '%s', updated_at='%s', content='%s' where list_id='%s'" % (tb_lists, o['title'],
                                                                                                                                created_at, updated_at,
                                                                                                                                json.dumps(o), o['id'])
                DBHelper.update(update_sql)
        else:
            print 'insert now...'
            sql = '''insert into %s (title,created_at,updated_at,content,list_id) values('%s','%s','%s', '%s','%s')''' % (tb_lists, o['title'], created_at, updated_at,json.dumps(o), o['id'])
            print sql
            DBHelper.update(sql)
    print 'success sync lists'
    return data


def start_sync():
    auth()
    lists = sync_lists()
    for l in lists:
        sync_tasks(get_tasks(l['id']))
        time.sleep(1)
