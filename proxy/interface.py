
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, send_file
import requests
import json
import os


app = Flask(__name__)

OBS_TMP_OP_DIR = '//home/sairo/tmpmaster'
app.config['OBS_TMP_OP_DIR'] = OBS_TMP_OP_DIR



@app.route('/', methods=['GET', 'POST'])
def index():
    r =  requests.get('http://localhost:5000/getbucketlist')
    # print(json.loads(r.text))
    buckets = json.loads(r.text)
    return render_template('index.html', buckets=buckets)
    # return '<h1> Hello Sairo </h1>'



@app.route('/<bucketName>')
def get_objectlist(bucketName):
    # print(bucketName)
    r = requests.post('http://localhost:5000/getobjectlist', data={'bucketName' :bucketName})
    bucket_objects = json.loads(r.text)
    return render_template('objects.html', objects=bucket_objects, bucketName=bucketName)



@app.route('/<bucketName>/<fileName>')
def uploads(bucketName, fileName):
    r = requests.post('http://localhost:5000/getobject', data={'bucketName' :bucketName, 'objectName': fileName})
    if 'txt' in fileName:
        with open(os.path.join(app.config['OBS_TMP_OP_DIR'], fileName), 'w') as f:
            f.write(r.text)
    else:
        with open(os.path.join(app.config['OBS_TMP_OP_DIR'], fileName), 'wb') as f:
            f.write(r.content)
    return send_from_directory(app.config['OBS_TMP_OP_DIR'], fileName)



@app.route('/createbucket', methods=['GET', 'POST'])
def create_bucket():
    if request.method == 'POST':
        bucket_name = str(request.form['bucketName'])
        r = requests.post('http://localhost:5000/createbucket', data={'bucketName' : bucket_name })
        # print(r.text)
        return redirect(url_for('index'))

    return render_template('createbucket.html')



@app.route('/createobject/<bucketName>', methods=['GET', 'POST'] )
def create_object(bucketName):
    print(request.method)
    if request.method == 'POST':

        f = request.files['file']
        f.seek(0)
        sendFile = {"file": (f.filename, f.stream, f.mimetype)}

        r = requests.post("http://localhost:5000/createobject", files=sendFile, data={'bucketName': bucketName})

        return redirect(url_for('get_objectlist', bucketName=bucketName))
    return render_template('createobject.html')


@app.route('/deletebucket/<bucketName>', methods=['GET', 'POST'])
def delete_bucket(bucketName):
    # if request.method == 'POST':
    r = requests.post("http://localhost:5000/deletebucket", data={'bucketName': bucketName})
    return redirect(url_for('index'))


@app.route('/deleteobject/<bucketName>/<objectName>', methods=['GET', 'POST'])
def delete_object(bucketName, objectName):
    # if request.method == 'POST':
    print(bucketName)
    print(objectName)
    r = requests.post("http://localhost:5000/deleteobject", data={'bucketName': bucketName, 'objectName': objectName})
    return redirect(url_for('get_objectlist', bucketName=bucketName))


@app.route('/favicon.ico')
def favicon():
    return send_file('favicon.ico', mimetype='image/vnd.microsoft.icon')



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000, debug=True)