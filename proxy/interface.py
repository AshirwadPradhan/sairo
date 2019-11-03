
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, send_file
import requests
import json
import os
from nodering import NodeRing, ClusterNodes
import subprocess
import hashlib
from pathlib import Path
import sys

app = Flask(__name__)

HOME = str(Path.home())
OBS_TMP_SAIRO_SERVE = os.path.join(HOME,'.sairo_if_serve')
OBS_SAIRO_HANDOFF = os.path.join(HOME, '.sairo_backhandoff')
if not os.path.exists(OBS_TMP_SAIRO_SERVE):
    try:
        cp = subprocess.run('mkdir '+OBS_TMP_SAIRO_SERVE, shell=True, check=True)
        if cp.returncode == 0:
            print(f'{OBS_TMP_SAIRO_SERVE} Bucket Directory Created')
    except subprocess.CalledProcessError as e:
        print(e.stderr)


OBS_TMP_OP_DIR = os.path.join(OBS_TMP_SAIRO_SERVE,'tmpmaster')
if not os.path.exists(OBS_TMP_OP_DIR):
    try:
        cp = subprocess.run('mkdir '+OBS_TMP_OP_DIR, shell=True, check=True)
        if cp.returncode == 0:
            print(f'{OBS_TMP_OP_DIR} Bucket Directory Created')
    except subprocess.CalledProcessError as e:
        print(e.stderr)
app.config['OBS_TMP_OP_DIR'] = OBS_TMP_OP_DIR


def get_nodes(bucketName):
    nr = NodeRing()
    nodes = nr.get_nodes(bucketName)
    print(nodes)
    return nodes


def get_all_buckets():
    cluster_nodes = ClusterNodes.get_cluster_nodes()
    buckets = []
    for node in cluster_nodes:
        r =  requests.get('http://'+ node +'/getbucketlist')
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
                r = requests.delete('http://'+ node +'/deleteallbuckets')
        
            return "OK", 200
    
    return "METHOD NOT ALLOWED", 405


@app.route('/<bucketName>')
def get_objectlist(bucketName):
    # print(bucketName)
    # nr = NodeRing()
    nodes = get_nodes(bucketName)
    # print(nodes)
    bucket_objects = {}
    for node in nodes['member_nodes']:
        r = requests.post('http://'+ node +'/getobjectlist', data={'bucketName' :bucketName})
        bucket_objects.update(json.loads(r.text))
    return render_template('objects.html', objects=bucket_objects, bucketName=bucketName)



@app.route('/<bucketName>/<fileName>')
def uploads(bucketName, fileName):

    tmpmasterpath = os.path.join(app.config['OBS_TMP_OP_DIR'])
    for root, dirs, files in os.walk(tmpmasterpath):
        for file in files:
            print(file)
            os.remove(os.path.join(root, file))

    # nr = NodeRing()
    nodes = get_nodes(bucketName)
    # print(nodes)

    hasher = hashlib.md5()
    contents =  {}
    conflicted_objects =  {}
    
    for i, node in enumerate(nodes['member_nodes']):
        r = requests.post('http://'+ node +'/getobject', data={'bucketName' :bucketName, 'objectName': fileName})
        if 'txt' in fileName:
            with open(os.path.join(app.config['OBS_TMP_OP_DIR'], str(i) + fileName), 'w') as f:
                f.write(r.text)
            with open(os.path.join(app.config['OBS_TMP_OP_DIR'], str(i) + fileName) , 'r') as fh:
                buf = fh.read()
                hasher.update(buf.encode())
                if not hasher.hexdigest() in contents:
                    contents[hasher.hexdigest()] = str(i) + fileName

                print('================added from node ' + node)
        else:
            with open(os.path.join(app.config['OBS_TMP_OP_DIR'], str(i) + fileName), 'wb') as f:
                f.write(r.content)
            with open(os.path.join(app.config['OBS_TMP_OP_DIR'], str(i) + fileName), 'rb') as fh:
                buf = fh.read()
                hasher.update(buf)
                # contents.add(str(hasher.hexdigest()))
                if not hasher.hexdigest() in contents:
                    contents[hasher.hexdigest()] = str(i) + fileName
                print("=================added from node " + node)

    # import pdb; pdb.set_trace()
    # return render_template('user_reconcile.html', files=contents)
    
     
    print(contents)
    
    if len(contents) > 1:
        print('Conflict !!!!')
        # TODO: add code for read reconcilation
        return render_template('user_reconcile.html', files=contents)

    else:
        print(app.config['OBS_TMP_OP_DIR'])
        out_file = None
        for k, v in contents.items():
            out_file = v
        return send_from_directory(app.config['OBS_TMP_OP_DIR'], out_file)



@app.route('/createbucket', methods=['GET', 'POST'])
def create_bucket():
    if request.method == 'POST':
        bucket_name = str(request.form['bucketName'])
        # nr = NodeRing()
        nodes = get_nodes(bucket_name)
        print(nodes)
        for node in nodes['member_nodes']:
            r = requests.post('http://'+ node + '/createbucket', data={'bucketName' : bucket_name })
            if r.status_code != 200:
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

        # nr = NodeRing()
        nodes = get_nodes(bucketName)
        for node in nodes['member_nodes']:
            r = requests.post("http://"+ node +"/createobject", files=sendFile, data={'bucketName': bucketName})
        return redirect(url_for('get_objectlist', bucketName=bucketName))
    return render_template('createobject.html')


@app.route('/deletebucket/<bucketName>', methods=['GET', 'POST'])
def delete_bucket(bucketName):
    # if request.method == 'POST':
    # nr = NodeRing()
    nodes = get_nodes(bucketName)
    # print(nodes)
    for node in nodes['member_nodes']:
        r = requests.post('http://'+ node +'/deletebucket', data={'bucketName': bucketName})
        if r.status_code == 200:
            print("============================== deleted from" + node + "===================================")
    return redirect(url_for('index'))


@app.route('/deleteobject/<bucketName>/<objectName>', methods=['GET', 'POST'])
def delete_object(bucketName, objectName):
    # if request.method == 'POST':
    print(bucketName)
    print(objectName)
    # nr = NodeRing()
    nodes = get_nodes(bucketName)
    print(nodes)
    for node in nodes['member_nodes']:
        r = requests.post("http://"+ node +"/deleteobject", data={'bucketName': bucketName, 'objectName': objectName})
    return redirect(url_for('get_objectlist', bucketName=bucketName))


@app.route('/reconcile/<bucketName>/<fileName>')
def read_reconcile(bucketName, fileName):
    if os.path.exists(os.path.join(app.config['OBS_TMP_OP_DIR'], fileName)):
        os.rename(os.path.join(app.config['OBS_TMP_OP_DIR'], fileName), os.path.join(app.config['OBS_TMP_OP_DIR'], fileName[1:]))
        
        tmpmasterpath = os.path.join(app.config['OBS_TMP_OP_DIR'])
        for root, dirs, files in os.walk(tmpmasterpath):
            for file in files:
                print(file)
                print('-----------------------')

        fileName = fileName[1:]
        print(fileName)
        sendFile = {"file": open(os.path.join(app.config['OBS_TMP_OP_DIR'], fileName), 'r')}
        nodes = get_nodes(bucketName)
        for node in nodes['member_nodes']:
            r = requests.post("http://"+ node +"/createobject", files=sendFile, data={'bucketName': bucketName})
        return redirect(url_for('get_objectlist', bucketName=bucketName))
    else:
        print("doesnt exitsn")
    return redirect(url_for('get_objectlist', bucketName=bucketName)) 



@app.route('/favicon.ico')
def favicon():
    return send_file('favicon.ico', mimetype='image/vnd.microsoft.icon')



if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=sys.argv[1], debug=True)
        
    except IndexError:
        app.run(host='0.0.0.0', port=10000, debug=True)
