#from crypt import methods
from app import create_app
app = create_app()

if __name__ == '__main__':
	app.run(host='0.0.0.0')

#main connector to front end api
@app.route("/")
def index():
  return app.send_static_file('index.html')

from flask_swagger import swagger
from flask import jsonify


@app.route("/api/spec")
def spec():
    swag = swagger(app,prefix='/api')
    swag['info']['base'] = "http://locahost:5000"
    swag['info']['version'] = "1.0"
    swag['info']['title'] = 'Flask API Docs'
    return jsonify(swag)


@app.route('/page/<page>',methods=['GET'])
def pageapi(page):
    '''
    All_page:
    All_Record: All_Record/PageCount=All_page
    Current_page: current page id
    PageCount: num of record per page
    '''
    sql = "select count(*) from flask_info"
    PageCount=10
    All_Record = get_count(sql)
    if (int(All_Record) % int(PageCount) == 0):
        All_page = All_Record / PageCount
    else:
        All_page = All_Record / PageCount + 1
    tiao=(int(page)-1)*int(PageCount)
    # print "tiao:",tiao
    sql1="select id,pms_name,content,status,mark,create_time from flask_info order by create_time desc limit %s,%s"%(tiao,PageCount)
    content=get_data(sql1)
    pagedict={}
    pagedict['content']=content
    pagedict['pageNum']=page
    pagedict['pages']=All_page
    pagedict['amount']=All_Record
    return jsonify(pagedict)