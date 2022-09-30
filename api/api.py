from flask_sqlalchemy import SQLAlchemy
from flask import (
    Flask,
    current_app,
    jsonify,
    make_response,
    render_template,
    Blueprint,
    request,
    send_from_directory,
)
from flask_cors import CORS
from wordcloud import WordCloud
import time
import io
import base64
from flask_migrate import Migrate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

app = Flask(__name__,
                static_folder='../../dist',
                template_folder="../../dist",
                static_url_path='/')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app,db)
CORS(app)


@app.route('/time')
def get_current_time():
    return {'time': time.time()}

class Author(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))
    specialization = db.Column(db.String(50))

    def __init__(self,name,specialization):
        self.name = name
        self.specialization = specialization
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return '<Product %d>' % self.id

class AuthorSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Author
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    specialization = fields.String(required=True)
    
@app.route('/authors',methods=['GET'])
def get_authors():
    get_authors = Author.query.all()
    author_schema = AuthorSchema(many=True)
    authors = author_schema.dump(get_authors)
    return make_response(jsonify({"authors":authors}))

@app.route('/authors/<id>',methods=['GET','POST'])
def get_author_by_id():
    get_authors = Author.query.all()
    author_schema = AuthorSchema(many=True)
    authors = author_schema.dump(get_authors)
    return make_response(jsonify({"authors":authors}))
    
@app.route('/authors',methods=['POST'])
def create_author():
    data = request.get_json()
    author_schema = AuthorSchema()
    authors = author_schema.load(data)
    result = author_schema.dump(authors.create()).data
    return make_response(jsonify({"author":result}),201)

@app.route('/authors/<id>',methods=['PUT'])
def update_author_by_id(id):
    data = request.get_json()
    get_author = Author.query.get(id)
    if data.get('specialization'):
        get_author.specialization = data['specialization']

    if data.get('name'):
        get_author.name = data['name']

    db.session.add(get_author)
    db.session.commit()
    author_schema = AuthorSchema(only=['id','name','specialization'])
    author = author_schema.dump(get_author)
    return make_response(jsonify({"author":author}))

@app.route('/authors/<id>',methods=['DELETE'])
def delete_author_by_id(id):
    get_author = Author.query.get(id)
    db.session.delete(get_author)
    db.session.commit()
    return make_response({"msg":"Sucessfully Deleted"},204)


BOOKS = [
    {
        'Title': 'On the Road',
        'Author': 'Jack Kerouac',
        'read': True
    },
    {
        'Title': 'Harry Potter',
        'Author': 'J. K. Rowling',
        'read': True
    },
    {
        'Title': 'Green Eggs and Ham',
        'Author': 'Dr.Seuss',
        'read': False
    }
]

def get_word_cloud(text):
    pil_img = WordCloud(width=800, height=300, background_color="white").generate(text=text).to_image()
    img = io.BytesIO()
    pil_img.save(img, "PNG")
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()
    return img_base64


# Index page
@app.route('/')
@app.route('/index')
def index():
    return jsonify(
        {
            'status': 'Success',
            'books': BOOKS
        }
    )
    
@app.route('/greeting')
def greeting():
    return {"greeting": "Lung DB Database Construction"}


@app.route('/page/<page>',methods=['GET'])
def pageapi(page):
    '''
    All_page
    All_Record: All_Record/PageCount=All_page
    Current_page:
    PageCount: records per page
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

@app.route('/Books')
def getBooks():
    return jsonify(
        {
            'status': 'Success',
            'books': BOOKS
        }
    )

# return base4 img
@app.route('/word/cloud/generate', methods=["POST"])
def cloud():
    text = request.json.get("word")
    res = get_word_cloud(text)
    return res


if __name__ == '__main__':
    app.run()