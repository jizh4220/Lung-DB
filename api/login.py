import time
import json
from flask import Blueprint,request
from flask_login import LoginManager,login_user,logout_user,login_required,current_user
from user import UserLogin


login_page = Blueprint('login_page',__name__)

login_manager = LoginManager()
login_manager.login_view = None

@login_page.record_once
def on_load(state):
  login_manager.init_app(state.app)


@login_manager.request_loader
def load_user_from_request(request):
  token = request.headers.get('Authorization')
  if token == None:
    return None

  payload = UserLogin.verfiyUserToken(token)
  if payload != None:
    alternativeID = payload['data']['alternativeID']
    sessionID = payload['data']['sessionID']
    user = UserLogin.queryUser(alternativeID=alternativeID,sessionID=sessionID)
  else:
    user = None
  return user


@login_page.route('/first')
@login_required
def firstPage():
  returnData = {'code': 0, 'msg': 'success', 'data': {'token':current_user.token,'tips':'First Registered User: (' + current_user.userName +')'}}
  return returnData,200

@login_page.route('/login', methods=['GET','POST'])
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    user = UserLogin.queryUser(userName = username)
    if (user != None) and (user.verifyPassword(password)) :
      login_user(user)
      returnData = {'code': 0, 'msg': 'success', 'data': {'token':user.token}}
      return json.dumps(returnData),200
    else :
      returnData = {'code': 1, 'msg': 'failed', 'data': {'tips':'username or password is not correct'} }
      return json.dumps(returnData),200  

@login_page.route('/logout') 
@login_required
def logout():
  userName = current_user.userName
  # alternativeID = current_user.alternativeID
  sessionID = current_user.sessionID
  UserLogin.dropSessionID(sessionID)
  logout_user()
  returnData = {'code': 0, 'msg': 'success', 'data': {'tips':'Bye ' + userName} }
  return json.dumps(returnData),200  

@login_page.route('/changepws') 
@login_required
def changePws():
  user = UserLogin.queryUser(userID = current_user.id)  
  user.changePws()
  returnData = {'code': 0, 'msg': 'success', 'data': {'tips':'password was changed'} }
  return json.dumps(returnData),200  
