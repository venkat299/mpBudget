# script.py
import argparse
import pyexcel as pe
import configparser 
import os
import sys
import sqlite3

DB_URL = None
conn = None
sheet = None

desg_ls=None
unit_ls=None
sect_ls=None

def read_config():
	# instantiate
	config = configparser.ConfigParser()
	config.read('./config.cfg')
	global DB_URL 
	DB_URL = os.path.abspath(config['DB'].get('url'))
	global conn 
	conn = sqlite3.connect('./../../../work/MPB_17_18/mpb_17-18.db')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     'filename', metavar='int', type=int, choices=range(10),
    #      nargs='+', help='give a file name')
    parser.add_argument('table',  help='e for deleting employee; s for deleting sanction')
    parser.add_argument('column',  help='delete based on column; r for onroll_unit; w for working_unit;')
    parser.add_argument('value',  help='enter full/partial unit_code like "C07AOF","C07" or area_code "07"  for deletion; warning: use carefully')
    parser.add_argument("-d", "--delete", action="store_true", help="enter -d to confirm delete")

    args = parser.parse_args()
    print(args)
    read_config()

    if args.table == 'e':
        if args.column == 'r':
            c = conn.cursor()
            c.execute('select count(*) from employee where roll_ucde like ?',('%'+args.value+'%',))
            row_count = c.fetchone()
            print('{0} rows will be deleted'.format(row_count[0]))
            if args.delete:
                c.execute('delete from employee where roll_ucde like ?',('%'+args.value+'%',))
                conn.commit()
                print('----> {0} rows deleted'.format(row_count[0]))
        if args.column == 'w':
            c = conn.cursor()
            c.execute('select count(*) from employee where ucde like ?',('%'+args.value+'%',))
            row_count = c.fetchone()
            print('{0} rows will be deleted'.format(row_count[0]))
            if args.delete:
                c.execute('delete from employee where ucde like ?',('%'+args.value+'%',))
                conn.commit()
                print('----> {0} rows deleted'.format(row_count[0]))
  