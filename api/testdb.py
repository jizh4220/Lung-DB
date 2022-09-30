from flask import Blueprint
from database import init_db,db_session
from models import Operator

accession_bp = Blueprint('accession_bp',__name__)


@accession_bp.route('/initdb')
def initdb():
  init_db()
  return 'init_db'

@accession_bp.route('/addoper')
def addOper():
  oper = Operator(1,'admin', '111111')
  db_session.add(oper)
  db_session.commit()
  return 'addOper'

@accession_bp.route('/verifypws/<pws>')
def verifyPassword(pws):
   oper = Operator.query.filter_by(username='admin').first()
   return str(oper.verifyPassword(pws))
 
table1='''
create TABLE IF NOT EXISTS flask_info( 
 id  INTEGER   PRIMARY KEY AUTOINCREMENT,
    `pms_name` varchar(255) DEFAULT NULL,
    `content` varchar(1000) DEFAULT NULL,
    `status` varchar(255) DEFAULT NULL,
    `mark` varchar(255) DEFAULT NULL,
    `create_time` varchar(255) DEFAULT NULL
 );
'''

def accession_import_csv(dbname, tablename, importf):
    import psycopg2
    import csv
    from psycopg2 import Error
    import os
    import sys
    param_dic = {
        "host"      : "localhost",
        "database"  : dbname,
        "user"      : "postgres",
        "password"  : "123654"
    }
    try:
        conn = psycopg2.connect(**param_dic)
        print("Connected To accession_celldata_db Successfully")
    except (Exception, Error) as error:
        print(error)
        sys.exit(1)
    cur = conn.cursor()
    try:    
        create_table_query = '''CREATE TABLE accessiondata
                            (ID INT   PRIMARY KEY NOT NULL,
                            ACCESSION TEXT NOT NULL,
                            DISEASE TEXT NOT NULL,
                            TISSUE TEXT NOT NULL,
                            AGE TEXT NOT NULL,
                            GENDER TEXT NOT NULL,
                            GSE_ALIAS TEXT NOT NULL,
                            CELLNUM INT NOT NULL); '''
        cur.execute(create_table_query)
        conn.commit()
        print("accessiondata table created successfully")
    except (Exception, Error) as error:
        print("Table has already been created")

    df = pd.read_csv(importf)
    df = df.drop(df.columns[0], axis=1)
    tmp_df = "./tmp_dataframe.csv"
    df.to_csv(tmp_df, index_label='id', header=False, sep = ';')
    f = open(tmp_df, 'r')
    cur = conn.cursor()
    try:
        cur.copy_from(f, tablename, sep=";")
        select_query = "select * from" + tablename + "test where id > 5;"
        cur.execute(select_query)
        res = cur.fetchall()
        conn.commit()
        print("copy_from_file() done")
        cur.close()
        conn.close()
        os.remove(tmp_df)
        return(res)
    except (Exception, psycopg2.DatabaseError) as error:
        os.remove(tmp_df)
        print("Error: %s" % error)
        conn.rollback()
        cur.close()
    
#数据库操作：
def get_count(sql): #获取sql返回总条数
    db = sqlite3.connect('test_flask.db')
    cur = db.cursor()
    result=cur.execute(sql).fetchall()
    print(result[0][0])
    cur.close()
    db.close()
    return result[0][0]

def get_data(sql1):#获取sql返回记录数
  db = sqlite3.connect('test_flask.db')
  cur = db.cursor()
  print(sql1)
  cur.execute(sql1)
  results=cur.fetchall()
  cloumn=get_table_colum()
  res = {}
  reslist = []
  print(results)
  for r in range(len(list(results))):
    for m in range(len(list(cloumn))):
      res[str(list(cloumn)[m])] = str(list(results)[r][m])
    reslist.append(res)
    res = {}
    print(reslist)
  cur.close()
  db.close()
  return reslist