# The contents of this file are licensed to you under the Reciprical Public License (RPL).  See the LICENSE file for details.
from fabric.api import run, sudo, env, settings, local
from fabric.context_managers import cd
import fabric
import util

def upgrade():
	run("apt-get update")
	run("apt-get upgrade")

def autoupgrade():
	util.debian_install("unattended-upgrades")
	util.putstring("""APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Download-Upgradeable-Packages "1";
APT::Periodic::AutocleanInterval "7";
APT::Periodic::Unattended-Upgrade "1";""","/etc/apt/apt.conf.d/10periodic")


def firewall():
	util.debian_install("ufw")
	run("ufw allow 22")
	run("""sed -i /etc/default/ufw -e 's/DEFAULT_FORWARD_POLICY="DROP"/DEFAULT_FORWARD_POLICY="ACCEPT"/g'""") #https://github.com/dotcloud/docker/issues/1251
	run("ufw enable")

def logwatch():
	util.debian_install("logwatch")
	util.append("/usr/sbin/logwatch --output mail --mailto test@gmail.com --detail high","/etc/cron.daily/00logwatch")


def setupDeployUser():
	if not fabric.contrib.files.contains("/etc/passwd",r"deploy"):
		print "Creating deploy user"
		run("useradd deploy")
		run("mkdir /home/deploy")
		run("mkdir /home/deploy/.ssh")
		run("cp ~/.ssh/authorized_keys /home/deploy/.ssh/authorized_keys")

		run("chmod 700 /home/deploy/.ssh")
		run("chmod 400 /home/deploy/.ssh/authorized_keys")
		run("chown deploy:deploy /home/deploy -R")

	#add to sudoers file
	util.append("deploy  ALL=(ALL) ALL","/etc/sudoers")

	#configure AllowUsers
	util.append("AllowUsers root deploy vagrant","/etc/ssh/sshd_config")

	run('service ssh restart')
	
def harden():
	upgrade()
	autoupgrade()
	util.debian_install("fail2ban")


	print "attempting to configure key-based auth for root..."
	import os.path
	localKey = open(os.path.expanduser("~/.ssh/id_rsa.pub")).read()
	util.append(localKey,"~/.ssh/authorized_keys")

	print "WARNING: YOU *MUST* have root configured to continue.  Type YES to confirm."
	confirm = None
	while confirm != "YES":
		confirm = raw_input()
		pass


	print "disabling password auth for root"
	util.config("PasswordAuthentication no","/etc/ssh/sshd_config")

	run("service ssh restart")

	setupDeployUser()
	logwatch()


	firewall() #this should be run last, since it can abort the SSH connection



