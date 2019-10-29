
from flask import Flask, flash, request, redirect, url_for, render_template
import requests
import json


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    r =  requests.get('http://localhost:5000/getbucketlist')
    # print(json.loads(r.text))
    buckets = json.loads(r.text, encoding='utf-8')
    return render_template('index.html', buckets=buckets)
    # return '<h1> Hello Sairo </h1>'

@app.route('/buckets/<bucketName>')
def get_objectlist(bucketName):
    print(bucketName)
    r = requests.post('http://localhost:5000/getobjectlist', data={'bucketName' :bucketName})
    bucket_objects = json.loads(r.text, encoding='utf-8')
    return render_template('objects.html', objects=bucket_objects, bucketName=bucketName)

@app.route('/<bucketName>/<fileName>')
def uploads(bucketName, fileName):
    r = requests.post('http://localhost:5000/getobject', data={'bucketName' :bucketName, 'objectName': fileName})
    # print(r.text)
    return "ok"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000, debug=True)