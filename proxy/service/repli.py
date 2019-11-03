import os
import subprocess
import yaml
from pathlib import Path


HOME = str(Path.home())
OBS_SAIRO_HANDOFF = os.path.join(HOME, '.sairo_backhandoff')
OBS_BUCKET_DIR = os.path.join(HOME, '.sairo')

class ClusterNodes:

    @staticmethod
    def get_cluster_nodes() -> list:
        cluster_nodes: list = []

        with open('../clusterconfig.yaml', 'r') as file_handle:
            cluster_nodes = yaml.load(file_handle, Loader=yaml.FullLoader)
        
        return cluster_nodes

HOME = Path.home()
OBS_SAIRO_HANDOFF = os.path.join(HOME, '.sairo_backhandoff')
if not os.path.exists(OBS_SAIRO_HANDOFF):
    try:
        cp = subprocess.run('mkdir '+OBS_SAIRO_HANDOFF, shell=True, check=True)
        if cp.returncode == 0:
            print(f'{OBS_SAIRO_HANDOFF} Bucket Directory Created')
    except subprocess.CalledProcessError as e:
        print(e.stderr)

cluster_nodes = ClusterNodes.get_cluster_nodes()
for node in cluster_nodes:
    temp_handoff_node = os.path.join(OBS_SAIRO_HANDOFF, node)
    if not os.path.exists(temp_handoff_node):
        try:
            cp = subprocess.run('mkdir '+temp_handoff_node, shell=True, check=True)
            if cp.returncode == 0:
                print(f'{temp_handoff_node} Directory Created')
        except subprocess.CalledProcessError as e:
            print(e.stderr)

ipdict =	{
            "192.168.3.10": "shashank",
            "192.168.3.11": "vm2",
            "192.168.3.12": "shashank",
            "192.168.3.14": "jack",
            "192.168.3.15": "vm4"
        }

for dir_ip in os.listdir(OBS_SAIRO_HANDOFF):
    abs_dir_path = os.path.join(OBS_SAIRO_HANDOFF, dir_ip)
    basepath = ''
    for contents in os.listdir(abs_dir_path):
        # print(contents)
        basepath = os.path.join(OBS_SAIRO_HANDOFF, dir_ip, contents)
        print(basepath)
        # print(dir_ip[:-5])
        username = ipdict.get(dir_ip[:-5])
        # print(username)
        try:
            cp = subprocess.run('scp -r '+basepath+' '+username+'@'+dir_ip[:-5]+':'+'/home/'+username+'/.sairo' , shell=True, check=True)
            if cp.returncode == 0:
                print(f'{basepath} scp successful....')
            cp = subprocess.run('rm -rf '+basepath, shell=True, check=True)
            if cp.returncode == 0:
                print(f'{basepath} backup delete successful....')
        except subprocess.CalledProcessError as e:
            print(e.stderr)
