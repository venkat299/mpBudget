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
	conn.row_factory = sqlite3.Row

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     'filename', metavar='int', type=int, choices=range(10),
    #      nargs='+', help='give a file name')
    parser.add_argument("-f",'--filter',  help='enter unit_code full/partial to filter')

    args = parser.parse_args()
    print(args)
    read_config()


    
    c = conn.cursor()
    if args.filter:
        c.execute('select * from unit_count_working where unit like ?',('%'+args.filter+'%',))
    else:
        c.execute('select * from unit_count_working')
    rows = c.fetchall()
    count = len(rows)
    ext, req, san, MNOVM, MNSPA, SVR_NO_C_GR = 0,0,0,0,0,0
    for x in rows:
        print('{}	{}	{}			{}	{}	{}	{}	{}		{}'.format('area','unit','name','ext','req','san','MNOVM','MNSPA','SVR_NO_C_GR'))
        print('{}	{}	{}			{}	{}	{}	{}	{}		{}'.format('====','====','====','===','===','===','=====','=====','==========='))
        print('{}	{}	{}		{}	{}	{}	{}	{}		{}'.format(x['ac'],x['unit'],x['name'],x['ext'],x['req'],x['san'],x['MNOVM'],x['MNSPA'],x['SVR_NO_C_GR']))
        ext = ext + (x['ext'] or 0)
        req = req + (x['req'] or 0)
        san = san + (x['san'] or 0)
        MNOVM = MNOVM + (x['MNOVM'] or 0)
        MNSPA = MNSPA + (x['MNSPA'] or 0)
        SVR_NO_C_GR = SVR_NO_C_GR + (x['SVR_NO_C_GR'] or 0)
    print('{}	{}	{}			{}	{}	{}	{}	{}		{}'.format('----','----','total',ext,req,san,MNOVM,MNSPA,SVR_NO_C_GR))
    print('{0} records found'.format(count))
 