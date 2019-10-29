
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

@app.route('/buckets/<bucketName>')
def get_objectlist(bucketName):
    print(bucketName)
    r = requests.post('http://localhost:5000/getobjectlist', data={'bucketName' :bucketName})
    bucket_objects = json.loads(r.text)
    return render_template('objects.html', objects=bucket_objects, bucketName=bucketName)

@app.route('/buckets/<bucketName>/<fileName>')
def uploads(bucketName, fileName):
    r = requests.post('http://localhost:5000/getobject', data={'bucketName' :bucketName, 'objectName': fileName})
    if 'txt' in fileName:
        with open(os.path.join(app.config['OBS_TMP_OP_DIR'], fileName), 'w') as f:
            f.write(r.text)
    else:
        with open(os.path.join(app.config['OBS_TMP_OP_DIR'], fileName), 'wb') as f:
            f.write(r.content)
    return send_from_directory(app.config['OBS_TMP_OP_DIR'], fileName)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000, debug=True)