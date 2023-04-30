from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy #USED AS ORM WRAPPER 
from datetime import datetime
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:@localhost/todo"
db=SQLAlchemy(app)
class Todolist1(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(50),nullable=False)
    description=db.Column(db.String(200),nullable=False)
    date=db.Column(db.DateTime,default=datetime.utcnow())
    
    def __repr__(self):
        return f"{self.sno} -- {self.title}"
    

@app.route("/",methods=['GET','POST'])
def name():
    if(request.method=='POST'):
        title=request.form.get('title')
        desc=request.form.get('desc')
        todo=Todolist1(title=title,description=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo=Todolist1.query.all()
    return render_template('index.html',alltodo=alltodo)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/update/<int:sno>",methods=['GET','POST'])
def update(sno):
    if(request.method=='POST'):
        title=request.form.get('title')
        desc=request.form.get('desc')
        todo=Todolist1.query.filter_by(sno=sno).first()
        todo.title=title
        todo.description=desc
        db.session.add(todo)
        db.session.commit()
    
    todo=Todolist1.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)
    

@app.route("/delete/<int:sno>")
def delete(sno):
    todo=Todolist1.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

app.run(debug=True)

    