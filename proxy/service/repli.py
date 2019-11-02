from pathlib import Path
import os
import subprocess
import yaml

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

