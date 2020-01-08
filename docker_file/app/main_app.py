from flask import Flask,jsonify, abort,make_response,request
from flask_sqlalchemy import SQLAlchemy , Model 
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import Unicode,Integer,String
from flask_marshmallow import Marshmallow

app = Flask(__name__)
database_uri = 'postgresql+psycopg2://postgres:postgres@128.199.227.108:5432/videoserv'
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= True
db = SQLAlchemy(app)
ma = Marshmallow(app)

from app import Questions,Username, Login

class QuestionSchema(ma.ModelSchema):
    class Meta:
        model = Questions

class UserSchema(ma.ModelSchema):
    class Meta:
        model = Username

class LoginSchema(ma.ModelSchema):
    class Meta:
        model = Login

@app.route('/question/<question>', methods=['GET'])
def get_question(question):
    try:
        question = int(question)
        quest = db.session.query(Questions).filter_by(id=question).first()
        question_schema = QuestionSchema()
        output = question_schema.dump(quest)
        output_check= output['id']
        if output_check==question:
            return jsonify(output)
        else:
            return jsonify({"Error":"No Such Question"})

    except Exception:
        return jsonify({"Error":"No Such Question"})
    
@app.route('/video/new/<username>/<qnid>', methods=['POST'])
def post_video(username,qnid):
        if request.method=='POST':
            username = username
            videoname1 = (username+qnid+".mp4")
            db_insertvid = Username(username=username,videoname=videoname1)
            try:
                db.session.add(db_insertvid)
                db.session.commit()
                return 200
            except Exception :
                pass

@app.route('/video/videoname/<videoname>', methods=['GET'])
def get_video(videoname):
        try:
            videoname_query = db.session.query(Username).filter_by(videoname=videoname).first()
            videoname_schema = UserSchema()
            output = videoname_schema.dump(videoname_query)
            output = output['videoname']
            output = "rtmp://167.71.217.126:1935/vod2/" + output
            return jsonify ({"link ":output})
        except Exception:
            return jsonify({"Error":"no file specified exist"})
     
@app.route('/video/username/<username>', methods=['GET'])
def get_user(username):
        try:
            videoname = []
            for i in range(1,11):
                videoname = (username+str(i))+".mp4"
                videoname[i].append(videoname)
                return(videoname)

            result = []
            for a in range(11):
                username_query = db.session.query(Username).filter_by(videoname=videoname[a]).first()
                username_schema = UserSchema()
                output = username_schema.dump(username_query)
                result[a].append(output)
                return jsonify(result)

            # print(output)
            # for username in output['username']:
            #     output = output['videoname']
            #     return jsonify(output)
            
        except Exception as e:
            # return jsonify({"Error":"Error, no user specified exist"})
            print(e)

@app.route('/login/check/<email>/<password>', methods=['POST'])
def check_login(email,password):
    
    try:
        login_query = db.session.query(Login).filter_by(email=email,password=password).first()
        login_schema =LoginSchema()
        log = login_schema.dump(login_query)
        if log['is_company']==True:
            return jsonify({'Authentication':'Success','is_Company':True})
        else:
            return jsonify({'Authentication':'Success','is_Company':False})

    except:
        return jsonify({"Authentication":"Failed"})
        


if __name__ == '__main__':
    	app.run( 
            debug=True,
        host="",port=5000    # change to production server ipaddress
  )
