from flask import Flask,render_template,redirect,request

app = Flask(__name__)

@app.route('/')
def show_form():
    return render_template('index.html')


@app.route('/submit',methods=['POST'])
def get_details():
    username = request.form.get('username')
    password = request.form.get('password')
    return f' The user name is {username} The password is {password}'
    
    

if __name__ =='__main__':
    app.run(debug=True) 