import os
import subprocess
import yaml
import paramiko
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



class SSHCopy:

    @staticmethod
    def ssh_file_copy(ip, source, destination):

        ipdict =	{
            "192.168.3.10": "shashank",
            "192.168.3.11": "vm2",
            "192.168.3.12": "shashank",
            "192.168.3.13": "vm1",
            "192.168.3.14": "jack",
            "192.168.3.15": "vm4"
        }

        user_name = ipdict[ip]

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh_client.connect(hostname=ip,username=user_name,password='')


        sftp_client = ssh_client.open_sftp()
        sftp_client.put(source,destination)

        sftp_client.close()
        ssh_client.close()
    
    @staticmethod
    def ssh_mkdir(ip, path):

        ipdict =	{
            "192.168.3.10": "shashank",
            "192.168.3.11": "vm2",
            "192.168.3.12": "shashank",
            "192.168.3.13": "vm1",
            "192.168.3.14": "jack",
            "192.168.3.15": "vm4"
        }

        user_name = ipdict[ip]

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh_client.connect(hostname=ip,username=user_name,password='')


        sftp_client = ssh_client.open_sftp()
        sftp_client.mkdir(path)

        sftp_client.close()
        ssh_client.close()

for ip in os.listdir(OBS_SAIRO_HANDOFF):

    for bucket in os.listdir(os.path.join(OBS_SAIRO_HANDOFF, ip)):

        dest_bucket_path = os.path.join(OBS_BUCKET_DIR, bucket)
        # SSHCopy.ssh_mkdir(ip, dest_bucket_path)
        print(f'Created bucket {bucket} in {ip}')

        for obj in os.listdir(os.path.join(OBS_BUCKET_DIR, ip, bucket)):

            if os.path.isdir(obj):
                dest_obj_path = os.path.join(OBS_BUCKET_DIR, bucket, obj)
                # SSHCopy.ssh_mkdir(ip, dest_obj_path)
                print(f'Created folder {obj} in bucket {bucket} in {ip}')

                for ser_obs in os.listdir(obj):
                    # SSHCopy.ssh_file_copy(ip, os.path.abspath(ser_obs), dest_obj_path)
                    print(f'Created file {ser_obs} in folder {obj}')
            else:
                # SSHCopy.ssh_file_copy(ip, os.path.abspath(obj), dest_bucket_path)
                print(f'Created file {obj} in bucket {dest_bucket_path} in {ip}')