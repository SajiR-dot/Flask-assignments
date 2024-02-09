from flask import Flask,render_template,request
from flask_wtf import FlaskForm
from wtforms import FileField,SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired


class UploadFileForm(FlaskForm):
    file = FileField("File",validators=[InputRequired()])
    submit = SubmitField("upload file")


app = Flask(__name__)
app.config['SECRET_KEY'] = 'key1234'
app.config['UPLOAD_FOLDER'] = 'static/files'

@app.route('/',methods=['GET','POST'])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        return 'File has been uploaded succesfully'
    return render_template('index.html',form=form)

if __name__ =='__main__':
    app.run(debug=True)
    

