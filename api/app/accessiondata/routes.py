from distutils.util import change_root
from pickle import TRUE
from flask import request, make_response, send_file
from app import db
import sqlalchemy
from sqlalchemy import and_, func, distinct
from app.accessiondata import accessiondata_bp
from app.accessiondata.models import Accessiondata
from app.accessiondata.schema import AccessiondataSchema
from app.utils.responses import response_with
from app.utils import responses as resp
import pandas as pd
import psycopg2
import json
import re
import os
import io
import glob
import base64


DB_USERNAME = 'postgres'
DB_PASSWORD = '123654'
DB_NAME = 'accession_celldata_db'

def get_db_connection():
        conn = psycopg2.connect(host='localhost',
                                database=DB_NAME,
                                user=DB_USERNAME,
                                password=DB_PASSWORD)
        print("Succssfully create a connection to", conn)
        return conn

def create_engine_factory():
    engine = sqlalchemy.create_engine("postgresql:///?User=postgres&;Password=admin&Database=postgres&Server=127.0.0.1&Port=5432")
    factory = sqlalchemy.sessionmaker(bind=engine)
    session = factory()
    return session
'''
@accessiondata_bp.route('/',methods=['GET'])
def get_all_accessions():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM accessiondata;')
    all_accession = cur.fetchall()
    print(len(all_accession))
    cur.close()
    conn.close()
    return response_with(resp.SUCCESS_200,value={"Accessions":all_accession})
'''

@accessiondata_bp.route('/summary/',methods=['GET'])
def get_accession_summary():
    try:
        print("Trying to get metadata of the Accessiondata table")
        # print("Count of Unique Accession is: ", len(Accessiondata.query.distinct(Accessiondata.accession).all()))
        accession_counts = len(Accessiondata.query.distinct(Accessiondata.accession).all())
        collection_counts = len(Accessiondata.query.distinct(Accessiondata.gse_alias).all())
        tissue_counts = len(Accessiondata.query.distinct(Accessiondata.tissue).all())
        # print("Count of Unique Tissue is: ", tissue_list)
        disease_counts = len(Accessiondata.query.distinct(Accessiondata.disease).all())
        # print(disease_list)
        # print(query.select(func.min(Accessiondata.age).first()))
        # cell_num_total = db.session.query(func.sum(Accessiondata.cellnum)).group_by(Accessiondata.disease).all()
        # print(cell_num_total)

        return response_with(resp.SUCCESS_200,value={"accession_counts":accession_counts,
                                                    "collection_counts":collection_counts,
                                                    "tissue_counts":tissue_counts,
                                                    "disease_counts":disease_counts,
                                                    # "age_range":age_range,
                                                    # "cell_num_range":cell_num_range,
                                                    # "cell_num_total":cell_num_total
                                                    })
    except:
        return response_with(resp.INVALID_INPUT_422)

@accessiondata_bp.route('/summary/plot/',methods=['GET'])
def get_accession_plot():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    try:
        # print("Trying to plot the distribution of the Accessiondata table")
        img_dir = '/Users/justinzhang/Downloads/LungDB_DB/api/app/summary/summary/metaPlot'
        # print(base_dir, img_dir)
        all_plots = glob.glob(img_dir+"/*.png")
        img_list = []
        # print(all_plots)
        for p in all_plots:
            img_stream = ''
            with open(p, 'rb') as img_f:
                img_stream = img_f.read()
                img_stream = base64.b64encode(img_stream).decode()
                img_list.append(img_stream)
                # print(img_list)
                # return response_with(resp.SUCCESS_200,value={"img_list":img_list})
        print(len(img_list))
        return response_with(resp.SUCCESS_200,value={"img_list":img_list})

        '''
        img_stream = io.BytesIO(a)
        img = Image.open(img_stream)
        imgByteArr = io.BytesIO()
        img.save(imgByteArr,format="PNG")
        imgByteArr = imgByteArr.getvalue()
        print(imgByteArr)
        img.seek(0)
        '''        
        return response_with(resp.SUCCESS_200,value={"img_list":img_list
                                                    })
        # print("Count of Unique Accession is: ", len(Accessiondata.query.distinct(Accessiondata.accession).all()))
        accession_counts = len(Accessiondata.query.distinct(Accessiondata.accession).all())
        collection_counts = len(Accessiondata.query.distinct(Accessiondata.gse_alias).all())
        tissue_counts = len(Accessiondata.query.distinct(Accessiondata.tissue).all())
        # print("Count of Unique Tissue is: ", tissue_list)
        disease_counts = len(Accessiondata.query.distinct(Accessiondata.disease).all())
        # print(disease_list)
        # print(query.select(func.min(Accessiondata.age).first()))
        # cell_num_total = db.session.query(func.sum(Accessiondata.cellnum)).group_by(Accessiondata.disease).all()
        # print(cell_num_total)

        return response_with(resp.SUCCESS_200,value={"accession_counts":accession_counts,
                                                    "collection_counts":collection_counts,
                                                    "tissue_counts":tissue_counts,
                                                    "disease_counts":disease_counts,
                                                    # "age_range":age_range,
                                                    # "cell_num_range":cell_num_range,
                                                    # "cell_num_total":cell_num_total
                                                    })
    except:
        return response_with(resp.INVALID_INPUT_422)

    



# filter db accession per request and return as a list
@accessiondata_bp.route('/accession/list/',methods=['POST'])
def fetch_accession_list():
    # print("Backend Frontend Connection")
    try:
        listquery = request.get_json()
        print("length of current table is: ", len(Accessiondata.query.all()))

        # TODO Add Filter Clauses according to listquery
        # .name.like('Ra%')
        if (listquery['if_params'] == True):
            print("Here is the current query requested by the user: ", listquery)
            params = listquery['params']
            # User Selected Query
            query = Accessiondata.query
            for attr,value in params.items():
                if len(value) == 0:
                    continue
                attr = re.sub('[A-Z].*|\\_.*', '', attr)
                attr = re.sub('collection', 'gse_alias', attr)
                if attr in ['age', 'cellnum'] :
                    query = query.filter(getattr(Accessiondata,attr)>=value['min'], getattr(Accessiondata,attr)<=value['max'])
                else:
                    query = query.filter(getattr(Accessiondata,attr).in_(value))

            # filter_query = and_(query_list[params_idx])
            # print(query_list[params_idx])
            try:
                # cur_obj = Accessiondata.query.filter(filter_query).paginate(page=listquery['page'],per_page=listquery['limit'])
                cur_obj = query.paginate(page=listquery['page'],per_page=listquery['limit'])
                print('Filtered Accessions: ', cur_obj)
                pagi_obj = cur_obj
            except:
                print('Failed to filter')                
        else:
            pagi_obj = Accessiondata.query.paginate(page=listquery['page'],per_page=listquery['limit'])
    except:
        return response_with(resp.INVALID_INPUT_422)
    # pagi_obj = Accessiondata.query.paginate(page=data.page,per_page=data.limit)
    accession_schema = AccessiondataSchema(many=True)
    accession_list = accession_schema.dump(pagi_obj.items)
    total_pages = pagi_obj.pages
    # return response_with(resp.SUCCESS_200,value={"items":"tmp" ,"total":100 })
    return response_with(resp.SUCCESS_200,value={"items":accession_list, "total_pages":total_pages})
    conn = get_db_connection()
    cur = conn.cursor()
    tot = data.page * data.limit
    tis = data.tissuetype
    dis = data.diseasetype
    total_req = page*limit
    execute_query = 'SELECT * FROM accessiondata limit ' + 'ORDER BY' + sort +';'
    cur.execute(execute_query)
    all_accession = cur.fetchall()
    print(len(all_accession))
    cur.close()
    conn.close()
    return response_with(resp.SUCCESS_200,value={"Accessions":all_accession})

# filter db accession per request and return as a list
@accessiondata_bp.route('/sum',methods=['POST'])
def fetch_query_sum():
    # print("Backend Frontend Connection")
    try:
        listquery = request.get_json()
        print(Accessiondata.Table.key())
        for i in Accessiondata.Table.key():
            Accessiondata.filter(Accessiondata.i == listquery[i])
        print("Unique Entries of the current table are: ", len(Accessiondata.distinct().all()))
        # return response_with(resp.SUCCESS_200,value={"items":"tmp" ,"total":100 })
        # pagi_obj = Accessiondata.query.paginate(page=listquery['page'],per_page=listquery['limit'])
    except:
        return response_with(resp.INVALID_INPUT_422)
    # pagi_obj = Accessiondata.query.paginate(page=data.page,per_page=data.limit)
    accession_schema = AccessiondataSchema(many=True)
    accession_list = accession_schema.dump(pagi_obj.items)
    total_pages = pagi_obj.pages
    # return response_with(resp.SUCCESS_200,value={"items":"tmp" ,"total":100 })
    return response_with(resp.SUCCESS_200,value={"items":accession_list, "total_pages":total_pages})
    conn = get_db_connection()
    cur = conn.cursor()
    tot = data.page * data.limit
    tis = data.tissuetype
    dis = data.diseasetype
    total_req = page*limit
    execute_query = 'SELECT * FROM accessiondata limit ' + 'ORDER BY' + sort +';'
    cur.execute(execute_query)
    all_accession = cur.fetchall()
    print(len(all_accession))
    cur.close()
    conn.close()
    return response_with(resp.SUCCESS_200,value={"Accessions":all_accession})

@accessiondata_bp.route('/',methods=['POST'])
def create_accession():
    try:
        #ensure json data
        data = request.get_json()
        print("Successfully get the data from front end")
        accession_schema = AccessiondataSchema(load_instance=True)
        accession = accession_schema.load(data)
        result = accession_schema.dump(accession)
        return response_with(resp.SUCCESS_200,value={"Accessions":result})
    except:
        return response_with(resp.INVALID_INPUT_422)

@accessiondata_bp.route('/analyze',methods=['POST'])
def analyze_accession_query():
    try:
        print("Successfully get the data from front end")
        data = request.get_json()
        print(data)
        # ['GSM5100069', 'GSM4904124', 'GSM4904123', 'GSM4904122']
        # accession_schema = AccessiondataSchema(load_instance=True)
        # accession = accession_schema.load(data)
        # result = accession_schema.dump(accession)
        # print("Trying to plot the distribution of the Accessiondata table")
        tmp_dir = '/Users/justinzhang/Downloads/LungDB_DB/api/app/analyze/temp/temp'
        # print(base_dir, img_dir)
        all_plots = glob.glob(tmp_dir+"/*.png")
        img_list = []
        # load Plots into the list
        for p in all_plots:
            img_stream = ''
            p_name = re.sub(".*/|temp_|.png", "", p)
            print(p_name)
            with open(p, 'rb') as img_f:
                img_stream = img_f.read()
                img_stream = base64.b64encode(img_stream).decode()
                #img_list[p_name] = img_stream
                img_list.append(img_stream)
                # print(img_list)
                # return response_with(resp.SUCCESS_200,value={"img_list":img_list})
        celltypeTable = pd.read_csv(tmp_dir+"/temp_celltype_table.csv").set_index('Var1').to_dict()['Freq']
        return response_with(resp.SUCCESS_200,value={
                                                    "img_list":img_list,
                                                    "celltypeTable": celltypeTable})
        return response_with(resp.SUCCESS_200,value={"Accessions":result})
    except:
        return response_with(resp.INVALID_INPUT_422)
'''
@accession_bp.route('/',methods=['GET'])
def get_author_list():
    fetched = Author.query.all()
    author_schema = AuthorSchema(many=True,only=['first_name','last_name','id'])
    authors = author_schema.dump(fetched)
    return response_with(resp.SUCCESS_200,value={"authors":authors})

@classmethod
def get(cls, session: Session, geneset_id: str, dataset_id: str):
    link = (
        session.query(cls.table)
        .filter(cls.table.geneset_id == geneset_id, cls.table.dataset_id == dataset_id)
        .one_or_none()
    )
    if link:
        return cls(link)
    else:
        return None

@accession_bp.route('/<int:author_id>',methods=['GET'])
def get_author_detail(author_id):
    fetched = Author.query.get_or_404(author_id)
    author_schema = AuthorSchema()
    author = author_schema.dump(fetched)
    return response_with(resp.SUCCESS_200,value={"author":author})

@accession_bp.route('/<int:author_id>',methods=['PUT'])
def update_author_detail(author_id):
    print("Updating Author Info")
    data = request.get_json()
    print(data)
    get_author = Author.query.get_or_404(author_id)
    get_author.first_name = data['first_name']
    get_author.last_name = data['last_name']
    db.session.add(get_author)
    db.session.commit()
    author_schema = AuthorSchema()
    author = author_schema.dump(get_author)
    return response_with(resp.SUCCESS_200,value={"author":author})

@accession_bp.route('/<int:author_id>',methods=['PATCH'])
def modify_author_detail(author_id):
    data = request.get_json()
    get_author = Author.query.get(author_id)
    if data.get('first_name'):
        get_author.first_name = data['first_name']
    if data.get('last_name'):
        get_author.last_name = data['last_name']

    db.session.add(get_author)
    db.session.commit()
    author_schema = AuthorSchema()
    author = author_schema.dump(get_author)
    return response_with(resp.SUCCESS_200,value={"author":author})

@accession_bp.route('/<int:author_id>',methods=['DELETE'])
def delete_author(author_id):
    get_author = Author.query.get_or_404(author_id)
    db.session.delete(get_author)
    db.session.commit()
    print("Successfully deleted selected author")
    return response_with(resp.SUCCESS_202)
'''