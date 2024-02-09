from flask import Flask,render_template,redirect,url_for,request,session,flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "sajiflash"
app.permanent_session_lifetime = timedelta(minutes=5)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=2)


db = SQLAlchemy(app)
app.app_context().push()
class users(db.Model):
    _id = db.Column("id",db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    
    def __init__(self,name,email):
        self.name = name
        self.email = email    
    
    


@app.route('/')
def home():
    return render_template("login.html")

@app.route("/view")
def view():
    return render_template("view.html",values = users.query.all())

@app.route('/login', methods = ['POST','GET'])
def login():
    if request.method == "POST":
        name = request.form["name"]
        session["name"] = name
        session.permanent = True
        found_user = users.query.filter_by(name=name).first()
        if found_user:
            session["email"] = found_user.email
            
        else:
            usr = users(name,"")
            db.session.add(usr)
            db.session.commit()
            
        flash("Logged in succesfully")
        return redirect(url_for("user"))
    else:
        if "name" in session:
            flash("Already logged in ")
            return redirect(url_for("user"))
        return render_template("login.html")
    

@app.route('/user', methods=["POST","GET"])
def user():
    email = None
    if "name" in session:
        name = session["name"]
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=name).first()
            found_user.email = email
            db.session.commit()
            flash("Your email was saved")
        else:
            if "email" in session:
                email = session["email"]
            
        return render_template("user.html",email=email)
    
    else:
        flash("You are not logged in")
        return redirect(url_for("login"))
    
    
@app.route('/logout')
def logout():
    flash("You have been logged out")
    session.pop("name",None)
    session.pop("email",None)
    return redirect(url_for("login"))
  
    
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
              