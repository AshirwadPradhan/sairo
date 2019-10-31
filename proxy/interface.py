
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, send_file
import requests
import json
import os
from nodering import NodeRing, ClusterNodes
import subprocess

app = Flask(__name__)

OBS_TMP_OP_DIR = '/home/sairo/tmpmaster'
app.config['OBS_TMP_OP_DIR'] = OBS_TMP_OP_DIR
if not os.path.exists(OBS_TMP_OP_DIR):
    try:
        cp = subprocess.run('mkdir '+OBS_TMP_OP_DIR, shell=True, check=True)
        if cp.returncode == 0:
            print(f'{OBS_TMP_OP_DIR} Bucket Directory Created')
    except subprocess.CalledProcessError as e:
        print(e.stderr)


def get_all_buckets():
    cluster_nodes = ClusterNodes.get_cluster_nodes()
    buckets = []
    for node in cluster_nodes:
        r =  requests.get('http://'+ node +':5000/getbucketlist')
        buckets.extend(json.loads(r.text))
    print(buckets)
    all_buckets = list(set(buckets))
    return all_buckets



@app.route('/', methods=['GET', 'POST'])
def index():
    # r =  requests.get('http://localhost:5000/getbucketlist')
    # print(json.loads(r.text))
    # buckets = json.loads(r.text)
    buckets = get_all_buckets()
    buckets.sort()
    return render_template('index.html', buckets=buckets)
    # return '<h1> Hello Sairo </h1>'

@app.route('/deleteallbuckets', methods=['POST'])
def delete_all_buckets():

    if request.method == 'POST':
        data = str(request.form['delAll'])
        if data == 'true':
            cluster_nodes = ClusterNodes.get_cluster_nodes()
            for node in cluster_nodes:
                r = requests.delete('http://'+ node +'5000:/deleteallbuckets')
        
            return "OK", 200
    
    return "METHOD NOT ALLOWED", 405

@app.route('/<bucketName>')
def get_objectlist(bucketName):
    # print(bucketName)
    nr = NodeRing()
    nodes = nr.get_nodes(bucketName)
    print(nodes)
    bucket_objects = {}
    for node in nodes:
        r = requests.post('http://'+ node +':5000/getobjectlist', data={'bucketName' :bucketName})
        bucket_objects.update(json.loads(r.text))
    return render_template('objects.html', objects=bucket_objects, bucketName=bucketName)



@app.route('/<bucketName>/<fileName>')
def uploads(bucketName, fileName):
    nr = NodeRing()
    nodes = nr.get_nodes(bucketName)
    print(nodes)
    for node in nodes:
        r = requests.post('http://'+ node +':5000/getobject', data={'bucketName' :bucketName, 'objectName': fileName})
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
        nr = NodeRing()
        nodes = nr.get_nodes(bucket_name)
        print(nodes)
        for node in nodes:
            r = requests.post('http://'+ node + ':5000/createbucket', data={'bucketName' : bucket_name })
            if r.status_code  != 200:
                print('start hinted handoff')
            else:
                print("created bucket in " + node)
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

        nr = NodeRing()
        nodes = nr.get_nodes(bucketName)
        for node in nodes:
            r = requests.post("http://"+ node +":5000/createobject", files=sendFile, data={'bucketName': bucketName})
        return redirect(url_for('get_objectlist', bucketName=bucketName))
    return render_template('createobject.html')


@app.route('/deletebucket/<bucketName>', methods=['GET', 'POST'])
def delete_bucket(bucketName):
    # if request.method == 'POST':
    nr = NodeRing()
    nodes = nr.get_nodes(bucketName)
    print(nodes)
    for node in nodes:
        r = requests.post('http://'+ node +':5000/deletebucket', data={'bucketName': bucketName})
        if r.status_code == 200:
            print("============================== deleted from" + node + "===================================")
    return redirect(url_for('index'))


@app.route('/deleteobject/<bucketName>/<objectName>', methods=['GET', 'POST'])
def delete_object(bucketName, objectName):
    # if request.method == 'POST':
    print(bucketName)
    print(objectName)
    nr = NodeRing()
    nodes = nr.get_nodes(bucketName)
    print(nodes)
    for node in nodes:
        r = requests.post("http://"+ node +":5000/deleteobject", data={'bucketName': bucketName, 'objectName': objectName})
    return redirect(url_for('get_objectlist', bucketName=bucketName))


@app.route('/favicon.ico')
def favicon():
    return send_file('favicon.ico', mimetype='image/vnd.microsoft.icon')



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000, debug=True)