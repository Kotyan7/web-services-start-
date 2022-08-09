from flask import Flask, request, jsonify, abort, redirect, url_for,render_template, send_file
from markupsafe import escape
import numpy as np
import joblib


app = Flask(__name__)


app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))


knn = joblib.load('model.pkl')

@app.route("/")
def hello_world():
    print(111)
    return "<p>Hello, my new World!</p>"



@app.route('/user/<username>')
def show_user_profile(username):
    temp = float(escape(username))
    temp = temp**2
    # show the user profile for that user
    return f'User {escape(temp)}'

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

@app.route('/avg/<nums>')
def avg(nums):
    temp = list(map(float, escape(nums).split(',')))
    # show the user profile for that user
    print(mean(temp))
    return f'Arr {temp}'


@app.route('/iris/<param>')
def iris(param):
    
    
    param = np.array(list(map(float, escape(param).split(','))))
    print(param.reshape(1,-1))
    param = param.reshape(1,-1)
    
    pred = knn.predict(param)
 
    return str(pred)


@app.route('/iris_post', methods=[ 'POST'])
def add_message():
    try:
        content = request.get_json()
        #print(content)
        param = np.array(list(map(float, escape(content['flower']).split(','))))
        #print(param.reshape(1,-1))
        param = param.reshape(1,-1)
        
        pred = knn.predict(param)
        #print(pred)
        predict = {"class":str(pred[0])}
    
    except:
        pass
    return redicretc(url_for('bad_request'))

    return jsonify(predict)



from flask import abort
@app.route('/badrequest400')
def bad_request():
    abort(400)



from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    file = FileField()

import os 
import pandas as pd
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = MyForm()
    if form.validate_on_submit():
        print(form.name.data)
        f = form.file.data
        df = pd.read_csv(f, header=None)
        print(df)
        filename = form.name.data+'.csv'
        f.save(os.path.join(
            filename
        ))

        predict = knn.predict(df)
        print(predict)

        pd.DataFrame(predict).to_csv(filename, index=False)
        send_file(
            filename,
            as_attachment=True,
            download_name=filename,
            mimetype='text/csv'
        )

        return  'form submitted'


        return 'form submitted'
    return render_template('submit.html', form=form)



import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    print(request.method)
    print(request.method == 'POST')
    if request.method == 'POST':
        # check if the post request has the file part
        print(request.files)
        if 'file' not in request.files:
            print(111)
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        print(22)
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename+'uploaded')
            print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'file uploaded'
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''