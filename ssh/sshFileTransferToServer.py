#pip3 install paramiko to run this code
#PasswordAuthentication in sshd_config should be set to "yes" sudo gedit /etc/ssh/sshd_config


import paramiko

class sshFileTransfer:
    def sshCopy(self,ip,source,destination):

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
        #print("connecting with remote server....")
        ssh_client.connect(hostname=ip,username=user_name,password='')


        sftp_client = ssh_client.open_sftp()       #sftp_client object to open sftp connection with remote machine

        ## downloading file from remote         sftp_client.get('source','destination')
        ### if destination is not absolute path the downloaded file lies in the the directory of the script/cwd
        #### sftp_client.chdir("/home/shashank/")
        ##### sftp_client.get('sourcefile','destinationfile')

        ## transfer to remote
        ######sftp_client.put('source','destination')
        sftp_client.put(source,destination)

        sftp_client.close()
        ssh_client.close()





#ip,source,destination, are parameters

ip = "192.168.3.12"
source = '/home/jack/Desktop/virus.txt'
destination = '/home/shashank/Desktop/copiedfile.txt'
obj = sshFileTransfer()
obj.sshCopy(ip,source,destination)
