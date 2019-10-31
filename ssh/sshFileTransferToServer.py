## executing command over ssh


#pip3 install paramiko to run this code
#PasswordAuthentication in sshd_config should be set to "yes" sudo gedit /etc/ssh/sshd_config
#sshd service should be running in target machine "sudo service ssh status"


import paramiko

class sshFileTransfer:
    def sshFileTransferWizard(self,user_name,password,ip):

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print("connecting with remote server....")
        ssh_client.connect(hostname=ip,username=user_name,password=password)


        sftp_client = ssh_client.open_sftp()       #sftp_client object to open sftp connection with remote machine

        ## downloading file from remote         sftp_client.get('source','destination')
        ### if destination is not absolute path the downloaded file lies in the the directory of the script/cwd
        #### sftp_client.chdir("/home/shashank/")
        ##### sftp_client.get('sourcefile','destinationfile')

        ## transfer to remote
        ######sftp_client.put('source','destination')
        sftp_client.put('/home/jack/Desktop/virus.txt','/home/vm4/Desktop/copiedfile.txt')

        sftp_client.close()
        ssh_client.close()




# user_name = "vm4"
# password = "1234"
# ip = "192.168.3.15"
#
# obj = sshFileTransfer()
# obj.sshFileTransferWizard(user_name,password,ip)
