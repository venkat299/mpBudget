# script.py
import argparse
import pyexcel as pe
import configparser 
import os
import sys

import my_connection as connection

DB_URL = None
global conn
conn = None
sheet = None

desg_ls=None
unit_ls=None
sect_ls=None

def decor(s,length):
    return (s+(' '*length))[0:length]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     'filename', metavar='int', type=int, choices=range(10),
    #      nargs='+', help='give a file name')
    parser.add_argument("-f",'--filter',  help='enter unit_code full/partial to filter')

    args = parser.parse_args()
    print(args)
    #read_config()
    conn = connection.get_connection()


    
    c = conn.cursor()
    if args.filter:
        c.execute('select * from unit_count_working where unit like ?',('%'+args.filter+'%',))
    else:
        c.execute('select * from unit_count_working')
    rows = c.fetchall()
    count = len(rows)
    ext, req, san, MNOVM, MNSPA, SVR_NO_C_GR = 0,0,0,0,0,0
    print('{}	{}	{}	{}	{}	{}	{}	{}		{}'.format('area','unit',decor('name',20),'ext','req','san','MNOVM','MNSPA','SVR_NO_C_GR'))
    print('{}	{}	{}	{}	{}	{}	{}	{}		{}'.format('====','====',decor('====',20),'===','===','===','=====','=====','==========='))
    for x in rows:
        #print (x.keys())
        #['ac', 'unit', 'name', 'working_unit', 'ext', 'req', 'san', 'MNOVM', 'MNSPA', 'SVR_NO_C_GR']
        print('{}	{}	{}	{}	{}	{}	{}	{}		{}'.format(x['ac'],x['unit'],decor(x['name'],20),x['ext'],x['req'],x['san'],x['MNOVM'],x['MNSPA'],x['SVR_NO_C_GR']))
        ext = ext + (x['ext'] or 0)
        req = req + (x['req'] or 0)
        san = san + (x['san'] or 0)
        MNOVM = MNOVM + (x['MNOVM'] or 0)
        MNSPA = MNSPA + (x['MNSPA'] or 0)
        SVR_NO_C_GR = SVR_NO_C_GR + (x['SVR_NO_C_GR'] or 0)
    print('{}	{}	{}	{}	{}	{}	{}	{}		{}'.format('----','----',decor('total',20),ext,req,san,MNOVM,MNSPA,SVR_NO_C_GR))
    print('{0} records found'.format(count))
 