from flask import Flask, request, jsonify,render_template,redirect,flash
from flask_sqlalchemy import SQLAlchemy
import flask_excel as excel
import json
# from email_validator import validate_email,EmailNotValidError
import re



app=Flask(__name__)
db=SQLAlchemy(app)
excel.init_excel(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:keerthi292@localhost/students"
app.config['SECRET_KEY']='keerthi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

@app.route('/', methods=['GET','POST'])
def index():
    return redirect('/import')




class Orders(db.Model):
    
    id=db.Column(db.Integer,primary_key=True)
    sno=db.Column(db.Integer)
    firstname=db.Column(db.Text)
    lastname=db.Column(db.Text)
    gender=db.Column(db.String(10))
    rollname=db.Column(db.String(10))
    email=db.Column(db.Text)
    phone=db.Column(db.String(12))
    address=db.Column(db.Text)
    city=db.Column(db.Text)
    state=db.Column(db.Text)
    country=db.Column(db.Text)
    branch=db.Column(db.Text)
    section=db.Column(db.String(10))



db.create_all()
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'    

@app.route("/import", methods=['GET', 'POST'])
def doimport():
    if request.method == 'POST':
        with open ('datares.json','w') as f:
            json.dump({"result":request.get_array(field_name='file')},f)
       
    
        
        with open('datares.json') as f:
            data=json.load(f)

        def check(email):
            if(re.search(regex,email)):
                email=email
            else:
                email='NULL'
            return email



        for i in range(1,len(data['result'])):
            data['result'][i][5]=check(data['result'][i][5])
            if len(str(data['result'][i][6]))<10 or data['result'][i][6]=='' :
                data['result'][i][6]='Null'
            data['result'][i][3].islower()
            if not (data['result'][i][3]=="f" or data['result'][i][3]=="female" or data['result'][i][3]=="male" or data['result'][i][3]=="m" or data['result'][i][3]=="other" ):
                data['result'][i][3]='Null'
        
        for i in range(1,len(data['result'])):
            details=Orders(email=data['result'][i][5],gender=data['result'][i][3],rollname=data['result'][i][4],sno=data['result'][i][0],firstname=data['result'][i][1],lastname=data['result'][i][2],phone=data['result'][i][6],address=data['result'][i][7],city=data['result'][i][8],state=data['result'][i][9],country=data['result'][i][10],branch=data['result'][i][11],section=data['result'][i][12])
            db.session.add(details)
        db.session.commit()
        flash('saved successfully')
        return redirect('/import')
    return render_template('index.html')




if __name__ == "__main__":
   
    excel.init_excel(app)
   
    app.run(debug=True)