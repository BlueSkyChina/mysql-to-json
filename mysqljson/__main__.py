#!/usr/bin/env python3

"""
mysql-to-json
Connects to a MySQL database and exports selected data to JSON.
copyright 2018 Seth Black
"""

import argparse
import getpass
import json
import MySQLdb
import sys,os

def cursor_to_dict(cursor):
    data = cursor.fetchone()

    if data is None:
        return None

    desc = cursor.description

    result = {}

    for (name, value) in zip(desc, data):
        result[name[0]] = value

    return result

def cursor_to_dicts(cursor,batch_size=1000):
    datas = cursor.fetchmany(batch_size)

    if data is None:
        return None

    desc = cursor.description
    results = []
    result = {}
    for data in datas:
        for (name, value) in zip(desc, data):
            result[name[0]] = value
        results.append(result)

    return results

def main():
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('-d', '--database', help='MySQL database name.', default='mysql')
    arg_parser.add_argument('-H', '--hostname', help='MySQL host name.', default='127.0.0.1')
    arg_parser.add_argument('-P', '--port', help='MySQL port number.', default=3306, type=int)
    arg_parser.add_argument('-u', '--user', help='MySQL username.', default='root')
    arg_parser.add_argument('-p', '--password', help='Shh! It\'s a secret.', action='store_true')
    arg_parser.add_argument('-b', '--batchsize', help='using fetchmany to get data',  default= 1 , type=int)
    arg_parser.add_argument('-G', '--jsonarray', help='json(one table as json array) or line(row of table as json object write to text line)',  default='json')
    arg_parser.add_argument('-e', '--query', help='Query to run.', required=True)

    args = arg_parser.parse_args()

    password = ''

    if args.password == True:
       password = getpass.getpass()

    conn = MySQLdb.connect(host=args.hostname, user=args.user, passwd=password, db=args.database, port=args.port)

    try:
        cursor = conn.cursor()
        # SET query encode
        cursor.execute("SET NAMES utf8")
        conn.commit();
        
        cursor.execute(args.query)
    except MySQLdb.Error as e:
        sys.stderr.write('MySQL Error [{}]: {}\n'.format((e.args[0], e.args[1])))
        sys.exit()
    if args.jsonarray == 'json':
        sys.stdout.write('[')
    if args.batchsize == 1:
        row = cursor_to_dict(cursor)
        first_line = True
        while row is not None:
            if first_line == True:
                first_line = False
            else:
                if args.jsonarray == 'json':
                    sys.stdout.write(',')
                    sys.stdout.write(os.linesep)
                else:
                    sys.stdout.write(os.linesep)

            json_str = json.dumps(row, default=str, ensure_ascii=False)

            sys.stdout.write(json_str)

            row = cursor_to_dict(cursor)
        if args.jsonarray == 'json':
            sys.stdout.write(']')
     else:
        rows = cursor_to_dicts(cursor,args.batchsize)
        first_line = True
        while rows is not None:
            for row in rows:
                if first_line == True:
                    first_line = False
                else:
                    if args.jsonarray == 'json':
                        sys.stdout.write(',')
                        sys.stdout.write(os.linesep)
                    else:
                        sys.stdout.write(os.linesep)

                json_str = json.dumps(row, default=str, ensure_ascii=False)

                sys.stdout.write(json_str)

            rows = cursor_to_dicts(cursor,args.batchsize)
        if args.jsonarray == 'json':
            sys.stdout.write(']')
        

if __name__ == "__main__":
    main()
