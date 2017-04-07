import sqlite3
import configparser 
import sys

def get_connection():
	# instantiate
	# config = configparser.ConfigParser()
	# config.read('./config.cfg')
	# global DB_URL 
	# #DB_URL = os.path.abspath(config['DB'].get('url'))
	# DB_URL = config['DB'].get('url')
	# print('DB_URL:"{0}"'.format(DB_URL))
	global conn 

	##### Enter relative db location here #####
	conn = sqlite3.connect('./../../../work/MPB_17_18/mpb_17-18_grp.db')


	conn.row_factory = sqlite3.Row
	return conn



if __name__ == '__main__':
    # test1.py executed as script
    # do something
    execute()