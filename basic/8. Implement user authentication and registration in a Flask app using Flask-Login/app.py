from flask import Flask,render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user,current_user
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import InputRequired,length,ValidationError
from flask_bcrypt import Bcrypt



app = Flask(__name__)
db = SQLAlchemy()
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.__init__(app)
app.config['SECRET_KEY'] = '1234'
app.app_context().push()


#creating a login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 



class User(db.Model,UserMixin):
    _id = db.Column("id",db.Integer,primary_key =True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(80))
    
    
class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(),length(min=4, max=20)], render_kw={"placeholder":"username"})
    password = PasswordField(validators=[InputRequired(),length(min=4, max=20)], render_kw={"placeholder":"username"})

    submit = SubmitField("Register")
    
    
    def validate_username(self,username):
        existing_user_username = User.query.filter_by(username = username.data).first()
        
        if existing_user_username:
            raise ValidationError("username already exists try a different one")
        
class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(),length(min=4, max=20)], render_kw={"placeholder":"username"})
    password = PasswordField(validators=[InputRequired(),length(min=4, max=20)], render_kw={"placeholder":"username"})

    submit = SubmitField("Login")

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password,form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template("login.html",form=form)


@app.route('/logout',methods = ['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/dashboard",methods = ['GET','POST'])
@login_required
def dashboard():
    return render_template("dashboard.html")
    

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm() 
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data,password = hashed_password )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("register.html",form=form)

if __name__ =='__main__':
    db.create_all()
    app.run(debug=True)