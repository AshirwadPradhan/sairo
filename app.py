import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory
import subprocess
from obs.bucket import Bucket

OBS_TMP_DIR = '/home/dominouzu/sairo/tmp'
OBS_BUCKET_DIR = '/home/dominouzu/sairo'
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']

app = Flask(__name__)
app.config['OBS_TMP_DIR'] = OBS_TMP_DIR
app.config['OBS_BUCKET_DIR'] = OBS_BUCKET_DIR
app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'

def allowed_file(filename):

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/bucket', methods=['GET', 'POST'])
def bucket_create():

    if request.method == 'POST':

        bucket_name = str(request.form['bucketName'])
        try:
            returncode = subprocess.run('mkdir '+OBS_BUCKET_DIR+'/'+bucket_name, shell=True, check=True)
            print(f'{bucket_name} Bucket Created')
            flash(f'{bucket_name} Bucket Created')

            return redirect(request.url)

        except subprocess.CalledProcessError:

            print('Bucket Already Present')
            flash('Bucket Already Present')

            return redirect(request.url)

        except FileNotFoundError:

            print('File not found')
            flash('File not found error')

            return redirect(request.url)

    return ''' 
    <!doctype html>
    <title> Create Bucket </title>
    <h1> Create New Bucket </h1>
    <form method=post action='/bucket'>
        <input type=text name=bucketName placeholder='Enter bucket name'>
        <input type=submit value=Create Bucket>
    </form>
    '''



@app.route('/')
def index():

    return '<h1> Hello Sairo </h1>'



@app.route('/object', methods=['GET', 'POST'])
def upload_file():

    if request.method == 'POST':

        if 'file' not in request.files:

            print('No file added')
            flash('No file added')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':

            print('No file selected')
            flash('No file selected')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['OBS_TEMP_DIR'], filename))
            return redirect(url_for('uploaded_file', filename = filename))
    
    return ''' 
    <!doctype html>
    <title> Upload file </title>
    <h1> Upload New File </h1>
    <form method=post enctype=multipart/form-data>
        <input type=text name=bucketName placeholder="Enter Bucket Name">
        <br> <p> </p>
        <input type=file name=file>
        <input type= submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):

    return send_from_directory(app.config['OBS_TEMP_DIR'], filename)

if __name__ == "__main__":
    app.run(debug=True)


