#coding:utf-8
import sqlite3
import os
from mywunder.myconfig import db_path

db_connect = sqlite3.connect(db_path)
db_cursor = db_connect.cursor()
def _dict_factory(cursor, row):
    '''
    see https://docs.python.org/2/library/sqlite3.html  (row_factory)
    '''
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
db_cursor.row_factory = _dict_factory

tb_lists = 'my_lists'
tb_tasks = 'my_tasks'

class DBHelper():
    def __init__(self):
        pass

    @classmethod
    def _execute(cls, sql):
        return db_cursor.execute(sql)

    @classmethod
    def fetchall(cls, sql):
        cls._execute(sql)
        return db_cursor.fetchall()

    @classmethod
    def update(cls, sql):
        cls._execute(sql)
        return db_connect.commit()

    @classmethod
    def insert(cls, sql):
        cls._execute(sql)
        return db_connect.commit()

    @classmethod
    def delete(cls, sql):
        cls._execute(sql)
        return db_connect.commit()


def init_db2():
    '''
    TODO: list_id need to set index for faster query at database??
    '''
    list_sql = '''
    create table my_lists (
    id Integer primary key autoincrement,
    list_id varchar(20),
    title varchar(50),
    updated_at datetime,
    created_at datetime,
    content text
    )
    '''
    DBHelper._execute(list_sql)
    tasks_sql ='''
    create table my_tasks(
    id Integer primary key autoincrement,
    task_id varchar(20),
    list_id varchar(20),
    title varchar(100),
    updated_at datetime,
    created_at datetime,
    content text
    )
    '''
    DBHelper._execute(tasks_sql)
    db_connect.commit()


if __name__ == '__main__':
    init_db2()
