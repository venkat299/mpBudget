import argparse
import sqlite3
import my_connection as connection


def get_connection(url):
	##### Enter relative db location here #####
	conn = sqlite3.connect(url)
	conn.row_factory = sqlite3.Row
	return conn



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     'filename', metavar='int', type=int, choices=range(10),
    #      nargs='+', help='give a file name')
    parser.add_argument('parent_db', help='(Parent - DB to be copied into)')
    parser.add_argument('child_db', help='(Child - DB to be copied from)')
    parser.add_argument('area_code', help='enter area code to be imported ')
    
    args = parser.parse_args()
    print(args)
    #read_config()

    ## area to be updated
    area_cd = args.area_code
    area_id = int(args.area_code)

    ## get connection
    parent_conn = get_connection(args.parent_db)
    child_conn = get_connection(args.child_db)

    p_c = parent_conn.cursor()
    c_c = child_conn.cursor()

    # delete all info from parent db
    p_c.execute('delete from employee where substr(ucde,2,2)=? or substr(roll_ucde,2,2)=?',(area_cd,area_cd))
    p_c.execute('delete from sanc where substr(unit,2,2)=?',(area_cd,))
    print('deleting all entries from parent db')

    # read from child db
    ##	read and mask employee data
    ##  read sanc data
    c_c.execute('select eis+? as mod_eis, name,dob,gend,desg,slu,roll_ucde,ucde,sect,o_dcd,working,emp_type,eis_status,comments  from employee where substr(ucde,2,2)=? or substr(roll_ucde,2,2)=?',((area_id*100000000),area_cd,area_cd))
    emp_ls = [ x for x in c_c.fetchall()]

    c_c.execute('select * from sanc where substr(unit,2,2)=?',(area_cd,))
    san_ls = [ x for x in c_c.fetchall()]

    print('reading all entries from child db')
    print('----- {0} employee record will be inserted'.format(len(emp_ls)))
    print('----- {0} sanc record will be inserted'.format(len(san_ls)))
    
    # insert into parent db
    p_c.executemany('insert into employee values (?,?,?,?,?, ?,?,?,?,?, ?,?,?,? )', emp_ls)
    p_c.executemany('insert into sanc values(?,?,?,?,?)',san_ls)


    print('inserting all entries into parent db')


    parent_conn.commit()
    print('task complete')







