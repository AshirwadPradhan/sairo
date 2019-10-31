import os
import subprocess
import hashlib
from flask import Flask, flash, request, redirect, url_for
from flask import jsonify
from flask import send_from_directory
from werkzeug.utils import secure_filename
from sairo_bucket import SairoBucket
from sairo_objects import SairoObject
from system_metadata import SystemMetadata
from persist_handler import PersistBucketHandler
from persist_handler import PersistObjectHandler
import base64
import simplejson as json


OBS_BUCKET_DIR = '/home/dominouzu/sairo'
if not os.path.exists(OBS_BUCKET_DIR):
    try:
        cp = subprocess.run('mkdir '+OBS_BUCKET_DIR, shell=True, check=True)
        if cp.returncode == 0:
            print(f'{OBS_BUCKET_DIR} Bucket Directory Created')
    except subprocess.CalledProcessError as e:
        print(e.stderr)


OBS_TMP_DIR = '/home/dominouzu/sairo/tmp'
if not os.path.exists(OBS_TMP_DIR):
    try:
        cp = subprocess.run('mkdir '+OBS_TMP_DIR, shell=True, check=True)
        if cp.returncode == 0:
            print(f'{OBS_TMP_DIR} Temp directory Created')
    except subprocess.CalledProcessError as e:
        print(e.stderr)

OBS_TMPOBJ_DIR = '/home/dominouzu/sairo/tmpobj'
if not os.path.exists(OBS_TMPOBJ_DIR):
    try:
        cp = subprocess.run('mkdir '+OBS_TMPOBJ_DIR, shell=True, check=True)
        if cp.returncode == 0:
            print(f'{OBS_TMP_DIR} TempOBJ directory Created')
    except subprocess.CalledProcessError as e:
        print(e.stderr)


ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']

app = Flask(__name__)
app.config['OBS_TMP_DIR'] = OBS_TMP_DIR
app.config['OBS_BUCKET_DIR'] = OBS_BUCKET_DIR
app.config['OBS_TMPOBJ_DIR'] = OBS_TMPOBJ_DIR
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

                pbh = PersistBucketHandler()
                if pbh.persist(sairo_bucket_obj):
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

    return "ok"
    # return '''
    # <!doctype html>
    # <title> Create Bucket </title>
    # <h1> Create New Bucket </h1>
    # <form method=post action='/createbucket'>
    #     <input type=text name=bucketName placeholder='Enter bucket name'>
    #     <input type=submit value=Create Bucket>
    # </form>
    # '''

@app.route('/getobjectlist', methods=['GET', 'POST'])
def get_object_list():

    if request.method == 'POST':

        bucket_name = str(request.form['bucketName'])
 
        #**************************************************************
        ##Make this part asynchronous
        bucket_path = os.path.join(OBS_BUCKET_DIR,bucket_name)
        bucket_ser_path = os.path.join(bucket_path, bucket_name+'.pk')

        pbh = PersistBucketHandler()
        buck_obj: SairoBucket = pbh.read(bucket_ser_path)

        print(buck_obj.object_list) #this is the var for all the object list
        #**************************************************************
        # return redirect(request.url)
        return jsonify(buck_obj.object_list), 200

    # return '''
    # <!doctype html>
    # <title> Get Object List </title>
    # <h1> Get Object List </h1>
    # <form method=post action='/getobjectlist'>
    #     <input type=text name=bucketName placeholder='Enter bucket name'>
    #     <input type=submit value=Get Bucket List>
    # </form>
    # '''

@app.route('/getbucketlist', methods=['GET'])
def get_bucket_list():
    
    bucket_list: list() = os.listdir(OBS_BUCKET_DIR)
    bucket_list.remove('tmp')
    bucket_list.remove('tmpobj')

    return jsonify(bucket_list), 200


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
                
                object_path = OBS_BUCKET_DIR+'/'+bucket_name+'/'+filename
                if not os.path.exists(object_path):
                    cp = subprocess.run('mkdir '+OBS_BUCKET_DIR+'/'+bucket_name+'/'+filename, shell=True, check=True)
                    if cp.returncode == 0:
                        print(f'{filename} Object Initialized...')
                        flash(f'{filename} Object Initialized')
                

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

                    poh = PersistObjectHandler()
                    if poh.persist(sairo_object_obj):
                        print(f'Object {sairo_object_obj.object_key} Serialized...')
                        flash('Bucket Saved')

                except FileNotFoundError:

                    print('Requested Bucket is not present')
                    flash('Bucket Not Created Yet') 
                
                #***********************************************************

                return redirect(request.url)
                # return redirect(url_for('uploaded_file', filename = filename))

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

# @app.route('/uploads/<filename>')
# def uploaded_file(filename):

#     return send_from_directory(app.config['OBS_TMPOBJ_DIR'], filename)


def get_uploaded_file(filename):
    payload = None
    with open(app.config['OBS_TMPOBJ_DIR']+"/"+filename, 'rb') as fh:
        payload = fh.read()
    return payload



@app.route('/getobject', methods=['GET', 'POST'])
def get_object():
    
    if request.method == 'POST':
        
        object_name = str(request.form['objectName'])
        bucket_name = str(request.form['bucketName'])
        
        #******************************************************************
        #**Make this async
        ph = PersistObjectHandler()
        sairo_object: SairoObject = ph.read(os.path.join(OBS_BUCKET_DIR, bucket_name, object_name), 
                        object_name)
        f = open(OBS_TMPOBJ_DIR+'/'+sairo_object.object_key, 'wb')
        f.write(sairo_object.file_bin)
        f.close()
        #*******************************************************************
        return get_uploaded_file(sairo_object.object_key)
        # return redirect(url_for('uploaded_file', filename = sairo_object.object_key))

    return ''' 
        <!doctype html>
        <title> Get Object </title>
        <h1> Get A Object </h1>
        <form method=post action='/getobject'>
            <input type=text name=bucketName placeholder='Enter Bucket Name'>
            <p> </p>
            <input type=text name=objectName placeholder='Enter Object Name'>
            <input type=submit value=Get Object>
        </form>
        '''


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
        
        return "ok"
        # return redirect(request.url)

    
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

                bucket_path = os.path.join(OBS_BUCKET_DIR, bucket_name)
                bucket_ser_path = os.path.join(bucket_path, bucket_name+'.pk')
                pbh = PersistBucketHandler()
                sairo_bucket_obj: SairoBucket = pbh.read(bucket_ser_path)
                sairo_bucket_obj.del_object_list(object_name)
                try:

                    if pbh.persist(sairo_bucket_obj):
                        print(f'Bucket Serialized after removing object {object_name}...')
                        flash(f'Bucket Saved')

                except FileNotFoundError:

                    print(f'Requested Bucket {bucket_name} is not present')
                    flash('Bucket Not Created Yet') 
                    
                print(f'{object_name} Object Deleted in bucket {bucket_name}')
                flash(f'{bucket_name} Object Deleted in bucket {bucket_name}')
        
        except subprocess.CalledProcessError as e:
            print(e.stderr)
            print(f'No such object {object_name} present to be deleted')
        
        return "ok"

    
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
