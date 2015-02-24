#coding:utf-8
import argparse
import backend as my_wunder
from sync import start_sync
import dateutil.parser
import re
from datetime import datetime
import logging


_not_in_list = ('content', 'list_id', 'task_id', 'id')
def format_printer(l, fields = []):
    def print_iter2(l):
        for t in l:
            if isinstance(t, list) or isinstance(t, tuple):
                print_iter2(t)
            else:
                print " "*4 + t,
        print ""
    display_list = []
    if not fields:
        fields = [k for k in l[0].keys() if k not in _not_in_list]
    display_list.insert(0, fields)
    display_list.insert(1, ('',)) # whitespace
    for r in l:
        tmp = [r.get(k, 'None') for k in fields]
        display_list.append(tmp)

    print_iter2(display_list)


def main():
    '''entry point '''
    # my_wunder = MyWunder()

    parser = argparse.ArgumentParser()
    parser.add_argument('--init', help='init local support, user -eEMail -pPassword to finish it', action = 'store_true')
    parser.add_argument('-e', '--email', help='your email address')
    parser.add_argument('-p', '--password', help='your password')
    parser.add_argument('-l', '--lists', help='show lists', action = 'store_true')
    parser.add_argument('-t', '--tasks', help='show tasks', action = 'store_true')
    parser.add_argument('-u', '--update', help='update database', action = 'store_true')
    parser.add_argument('-n', '--name', help="list name")
    parser.add_argument('-m', '--month', help="query by month", type=int)
    parser.add_argument('-s', '--sum', help="sum the number at title", action = "store_true")

    args = parser.parse_args()

    if args.init:
        assert args.email, 'need user, use -h to see more.'
        assert args.password, 'need password, use -h to see more.'
        my_wunder.login(args.email, args.password)
        my_wunder.init_db()

    elif args.lists:
        if args.name:
            list_id = my_wunder.query_list(args.name)
            print list_id
        else:
            l = my_wunder.query_list()
            format_printer(l)
    elif args.tasks:
        assert args.name, "you must use -n LISTNAME to assign the list name for tasks"
        l = my_wunder.query_tasks(args.name)
        if args.month:
            month = args.month
            def month_filter(tk):
                d = dateutil.parser.parse(tk['created_at'])
                y,da,day = str(d).split('-')
                return int(da) == month and datetime.now().year == int(y)
            l = filter(month_filter, l)
        format_printer(l)
        if args.sum:
            number_filter_func = lambda d : list(set(re.findall('\d*',d)) - set(['']))
            item_number_result_list = [number_filter_func(d['title']) for d in l if len(number_filter_func(d['title'])) > 0]
            totals = sum([sum([float(ii) for ii in i]) for i in item_number_result_list])
            logging.info("totals %f", totals)
            print "totals %f" % totals
    elif args.update:
        start_sync()
    else:
        l = my_wunder.query_list()
        format_printer(l)
