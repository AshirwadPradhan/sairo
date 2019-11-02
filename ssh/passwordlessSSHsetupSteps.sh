

### this is not a script

## this file only Documents the steps to create passwordless SSH authentication in a cluster organization

ssh-keygen  #generates public and private keys
cd ~/.ssh
ls # gives id_rsa, id_rsa.pub which are private and public keys respectively
chmod 600 id_rsa
ssh-copy-id -i ~/.ssh/id_rsa.pub vm4@192.168.56.30  ##copies the public key to remote
scp  ~/.ssh/id_rsa ~/.ssh/id_rsa vm4@192.168.56.30:~/.ssh/  ##copies the private key to remote




ip pool:
shashank@192.168.3.10   #y540 local
vm2@192.168.3.11        #y540 vm2

shashank@192.168.3.12   #hp local
vm1@192.168.3.13        #hp vm1


jack@192.168.3.14       #yoga local
vm4@192.168.3.15        #yoga vm4
