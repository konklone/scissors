wget https://raw.github.com/drewcrawford/scissors/master/install_scissors.sh -O - | sudo bash
sudo mkdir /root/.ssh
curl https://raw.github.com/mitchellh/vagrant/master/keys/vagrant -o /home/vagrant/.ssh/id_rsa
curl https://raw.github.com/mitchellh/vagrant/master/keys/vagrant.pub -o /home/vagrant/.ssh/id_rsa.pub
chown -R vagrant /home/vagrant/.ssh
chmod 600 /home/vagrant/.ssh/id_rsa

sudo /bin/bash -c "cat  /home/vagrant/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys"
echo "scissors has been installed.  To begin server configuration, you may run"
echo "scissors -H root@localhost config_scissors_server"