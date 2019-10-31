## executing command over ssh


#pip3 install paramiko to run this code
#PasswordAuthentication in sshd_config should be set to "yes" sudo gedit /etc/ssh/sshd_config
#sshd service should be running in target machine "sudo service ssh status"


import paramiko
user_name = "vm4"
password = "1234"
ip = "192.168.56.30"

print("creating ssh client ....")
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


print("connecting with remote server....")
ssh_client.connect(hostname=ip,username=user_name,password=password)
cmd = "ls /home/"

print("executing command on server ....")
stdin,stdout,stderr = ssh_client.exec_command(cmd)

#output of above is stored in stdout or stderr

stdout = stdout.readlines()
print(stdout)


ssh_client.close()
