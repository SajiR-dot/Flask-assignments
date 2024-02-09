from flask import Flask,render_template,request,redirect,url_for

app = Flask(__name__)

@app.route('/saji')
def person1():
    return render_template('saji.html')

@app.route('/mani')
def person2():
    return render_template('mani.html')

@app.route('/details/<name>')
def details(name):
    if name =='saji':
        return redirect('/saji')
    else:
        return redirect('/mani')
    

if __name__ =='__main__':
    app.run(debug=True)