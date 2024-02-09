from flask import Flask,render_template,redirect,url_for,request,session,flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "sajiflash"
app.permanent_session_lifetime = timedelta(minutes=5)
@app.route('/')
def home():
    return render_template("login.html")

@app.route('/login', methods = ['POST','GET'])
def login():
    if request.method == "POST":
        name = request.form["name"]
        session["name"] = name
        session.permanent = True
        flash("Logged in succesfully")
        return redirect(url_for("user"))
    else:
        if "name" in session:
            flash("Already logged in ")
            return redirect(url_for("user"))
        return render_template("login.html")
    

@app.route('/user')
def user():
    if "name" in session:
        name = session["name"]
        return render_template("user.html",name=name)
    
    else:
        flash("You are not logged in")
        return redirect(url_for("login"))
    
    
@app.route('/logout')
def logout():
    flash("You have been logged out")
    session.pop("name",None)
    return redirect(url_for("login"))
  
    
if __name__ == "__main__":
    app.run(debug=True)
              
        
    