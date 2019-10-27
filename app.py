import os
import subprocess
import hashlib
from flask import Flask, flash, request, redirect, url_for
from flask import send_from_directory
from werkzeug.utils import secure_filename
from obs.sairo_bucket import SairoBucket
from obs.sairo_objects import SairoObject
from obs.system_metadata import SystemMetadata
from obs.persist_handler import PersistBucketHandler
from obs.persist_handler import PersistObjectHandler


OBS_BUCKET_DIR = '/home/dominouzu/sairo'
if not os.path.exists(OBS_BUCKET_DIR):
    try:
        cp = subprocess.run('mkdir '+OBS_BUCKET_DIR, shell=True, check=True)
        if cp.returncode == 0:
            print(f'{OBS_BUCKET_DIR} Bucket Created')
    except subprocess.CalledProcessError as e:
        print(e.stderr)


OBS_TMP_DIR = '/home/dominouzu/sairo/tmp'
if not os.path.exists(OBS_TMP_DIR):
    try:
        cp = subprocess.run('mkdir '+OBS_TMP_DIR, shell=True, check=True)
        if cp.returncode == 0:
            print(f'{OBS_TMP_DIR} Bucket Created')
    except subprocess.CalledProcessError as e:
        print(e.stderr)


ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']

app = Flask(__name__)
app.config['OBS_TMP_DIR'] = OBS_TMP_DIR
app.config['OBS_BUCKET_DIR'] = OBS_BUCKET_DIR
app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'

def allowed_file(filename):

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/createbucket', methods=['GET', 'POST'])
def create_bucket():

    if request.method == 'POST':

        bucket_name = str(request.form['bucketName'])
        try:
            cp = subprocess.run('mkdir '+OBS_BUCKET_DIR+'/'+bucket_name, shell=True, check=True)
            if cp.returncode == 0:
                print(f'{bucket_name} Bucket Created')
                flash(f'{bucket_name} Bucket Created')

            #**************************************************
            ##Make this part asynchronous
            sairo_bucket_obj = SairoBucket(bucket_name)
            try:

                pbh = PersistBucketHandler(sairo_bucket_obj)
                if pbh.persist():
                    print('Bucket Serialized...')
                    flash('Bucket Saved')

            except FileNotFoundError:

                print('Requested Bucket is not present')
                flash('Bucket Not Created Yet') 
            #***************************************************

            return redirect(request.url)

        except subprocess.CalledProcessError as e:
            print(e.output)
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
    <form method=post action='/createbucket'>
        <input type=text name=bucketName placeholder='Enter bucket name'>
        <input type=submit value=Create Bucket>
    </form>
    '''



@app.route('/')
def index():

    return '<h1> Hello Sairo </h1>'



@app.route('/createobject', methods=['GET', 'POST'])
def create_object():

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
            bucket_name = str(request.form['bucketName'])
            try:

                save_path = os.path.join(app.config['OBS_TMP_DIR'], filename) 
                file.save(save_path)
                print(f'File {filename} saved...')

                cp = subprocess.run('mkdir '+OBS_BUCKET_DIR+'/'+bucket_name+'/'+filename, shell=True, check=True)
                if cp.returncode == 0:
                    print(f'{filename} Object Initialized...')
                    flash(f'{filename} Object Initialized')
                
                object_path = OBS_BUCKET_DIR+'/'+bucket_name+'/'+filename

                #**********************************************************
                #**Make this part aysnchronous
                try:
                    content_length = os.path.getsize(save_path)
                except NotImplementedError:
                    print('Unable to get content length.. Setting it to 0')
                    content_length = 0
                
                hasher = hashlib.md5()
                buf = None
                with open(save_path, 'rb') as fh:
                    buf = fh.read()
                    hasher.update(buf)
                
                metadata = SystemMetadata(content_length, file.mimetype, hasher.hexdigest())

                sairo_object_obj = SairoObject(filename, bucket_name, 
                                buf, metadata, hasher.hexdigest())
                
                try:

                    poh = PersistObjectHandler(sairo_object_obj)
                    if poh.persist():
                        print(f'Object {sairo_object_obj.object_key} Serialized...')
                        flash('Bucket Saved')

                except FileNotFoundError:

                    print('Requested Bucket is not present')
                    flash('Bucket Not Created Yet') 
                
                #***********************************************************

                return redirect(url_for('uploaded_file', filename = filename))

            except FileNotFoundError:
                print(f'File Dest not found {filename}')

                return redirect(request.url)
            
            except subprocess.CalledProcessError as e:
                print(e.stdout)
                print('Object Already Present')
                flash('Object Already Present')

                return redirect(request.url)

    
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

    return send_from_directory(app.config['OBS_TMP_DIR'], filename)


@app.route('/deletebucket', methods=['GET', 'POST'])
def delete_bucket():

    if request.method == 'POST':
        
        bucket_name = str(request.form['bucketName'])
        try:
            cp = subprocess.run('rm -rf '+OBS_BUCKET_DIR+'/'+bucket_name, shell=True, check=True)
            if cp.returncode == 0:
                print(f'{bucket_name} Bucket Deleted')
                flash(f'{bucket_name} Bucket Deleted')
        
        except subprocess.CalledProcessError as e:
            print(e.stderr)
            print(f'No such bucket {bucket_name} present to be deleted')
        
        return redirect(request.url)

    
    return ''' 
    <!doctype html>
    <title> Delete Bucket </title>
    <h1> Delete A Bucket </h1>
    <form method=post action='/deletebucket'>
        <input type=text name=bucketName placeholder='Enter bucket name'>
        <input type=submit value=Delete Bucket>
    </form>
    '''

@app.route('/deleteobject', methods=['GET', 'POST'])
def delete_object():

    if request.method == 'POST':
        
        object_name = str(request.form['objectName'])
        bucket_name = str(request.form['bucketName'])
        try:
            cp = subprocess.run('rm -rf '+OBS_BUCKET_DIR+'/'+bucket_name+'/'+object_name, 
                shell=True, check=True)
            if cp.returncode == 0:
                print(f'{object_name} Object Deleted in bucket {bucket_name}')
                flash(f'{bucket_name} Object Deleted in bucket {bucket_name}')
        
        except subprocess.CalledProcessError as e:
            print(e.stderr)
            print(f'No such object {object_name} present to be deleted')
        
        return redirect(request.url)

    
    return ''' 
    <!doctype html>
    <title> Delete Object </title>
    <h1> Delete A Object </h1>
    <form method=post action='/deleteobject'>
        <input type=text name=bucketName placeholder='Enter bucket name'>
        <p> </p>
        <input type=text name=objectName placeholder='Enter object name'>
        <input type=submit value=Delete Object>
    </form>
    '''



if __name__ == "__main__":
    app.run(debug=True)
