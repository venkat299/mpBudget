import argparse
import pyexcel as pe
import configparser 
import os
import sys
import sqlite3
import my_connection as connection
import functools 
# DB_URL = None
conn = connection.get_connection()
# conn = None
# sheet = None

desg_ls=None
unit_ls=None
sect_ls=None
discp_ls=None


def load_tables():
	# conn.row_factory = sqlite3.Row
	c = conn.cursor()
	c.execute("select dscd from desg")
	global desg_ls
	desg_ls = [ x[0] for x in c.fetchall()]

	c.execute("select discp from desg")
	global discp_ls
	discp_ls = [ x[0] for x in c.fetchall()]

	c.execute("select code from unit")
	global unit_ls
	unit_ls = [ x[0] for x in c.fetchall()]

	c.execute("select code from section")
	global sect_ls
	sect_ls = [ x[0] for x in c.fetchall()]

	c.execute("select eis from employee")
	global eis_ls
	eis_ls = [ x[0] for x in c.fetchall()]

desg_dup_ls = []

def validate_row(row):
	err = []
	if row['DSCD'] not in desg_ls:
		err.append(" dscd("+row['DSCD']+")")
	# if row['SECTION_CD'] not in sect_ls:
	# 	err.append(" sect("+row['SECTION_CD']+")")
	# if row['WORKING UNIT'] not in unit_ls:
	# 	err.append(" unit("+row['WORKING UNIT']+")")
	# if row['ONROLL_UNIT'] not in unit_ls:
	# 	err.append(" roll_unit("+row['ONROLL_UNIT']+")")

	global desg_dup_ls

	if str(row['DSCD']) in desg_dup_ls:
		err.append(" DSCD_repeat("+str(row['DSCD'])+")")
	else:
		desg_dup_ls.append(str(row['DSCD']))

	# try:
	# 	if int(row['EIS']) in eis_ls:
	# 		err.append(" eis_dup_db("+str(row['EIS'])+")")
	# except ValueError as e:
	# 	err.append(" eis_err("+str(row['EIS'])+")")
		
	if not err:
		return None
	else:
		return err

def filter_records(row, unit_code):
	if row['DSCD'] in desg_ls or ((len(row['DSCD'])==7 and row['DSCD'] not in discp_ls)and row['DSCD'] not in sect_ls) or row['IDX']==unit_code+'_g':
		return True
	else:
		return False

def sum_acc_tot(result, row):
	try:
		return result+int(row['TOT'])
	except ValueError:
		return result+0

def sum_acc_req(result, row):
	try:
		return result+int(row['AREA REQT 18-19'])
	except ValueError:
		return result+0
	

def sum_acc_sanc(result, row):
	try:
		return result+int(row['SANC 18-19'])
	except ValueError:
		return result+0
	


def read_file(xls_path, sheet_name, upload):
	# book = pe.get_book(file_name=os.path.normpath(xls_path))
	# sheets = book.to_dict()
	# for name in sheets.keys():
	# 	print(name)
	unit_code = (os.path.basename(xls_path)).split('.')[0]

	if unit_code not in unit_ls:
		raise ValueError('Unit code mentioned in file_name is wrong')


	print("uploading for unit:{0}".format(unit_code))
	try:
		sheet = pe.get_sheet(file_name=os.path.normpath(xls_path), sheet_name=sheet_name, name_columns_by_row=0)

	except ValueError as e:
		print("Sheet name not in excel file: {0}".format(e))
		sys.exit()
	except AttributeError as e:
		print("Sheet name not in excel file: {0}".format(e))
		sys.exit()
		#raise e
	except NotImplementedError as e:
		print("File not found or File not in proper format: {0}".format(e))
		sys.exit()
		#raise e

	records = sheet.get_records()
	error_ls = []
	filtered_rec = []

	for idx, record in enumerate(records):
		if filter_records(record, unit_code):
			filtered_rec.append(record)
			err_row = validate_row(record)
			#print(record)

			if err_row:
				error_ls.append(err_row)
				print('ERR @ ROW {} => {}'.format(idx+2,validate_row(record)))


	if error_ls:
		print('correct the above error and upload')
	else:
		sum_req = functools.reduce(sum_acc_req,filtered_rec,0)
		print("REQT total: {0}".format(sum_req))
		sum_sanc = functools.reduce(sum_acc_sanc,filtered_rec,0)
		print("SANC total: {0}".format(sum_sanc))

		print('{0} rows will be inserted. add "-u" to upload'.format(len(records)))
		if upload:
			ls=[]
			for idx, r in enumerate(filtered_rec):
				# unit, dscd, req, sanc remark
				#sno	AREA	UNIT	MINE_TYPE	ONROLL_UNIT	WORKING UNIT	SECTION_TYPE	CADRE	SECTION	SECTION_CD	DESIG	DSCD	EIS	NAME	GENDER	DOB	Comments
				ls.append((unit_code, r['DSCD'],r['AREA REQT 18-19'],r['SANC 18-19'],r['COMMENTS, IF ANY']))
			c = conn.cursor()
			#print(ls)
			c.execute('delete from sanc where unit = ?',(unit_code,))
			print('deleting rows for unit : {0}'.format(unit_code))
			c.executemany('''insert into sanc (unit, dscd, req, san, remark) values(?,?,?,?,?)''',ls)
			conn.commit()
			print('--->{0} records inserted sucessfully'.format(len(ls)))



