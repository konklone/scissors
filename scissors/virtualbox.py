from fabric.api import run, sudo, env, settings, local
from fabric.context_managers import cd
import fabric
import util

def install_virtualbox_additions():
	print "You must have the guest ISO connected for this to work."
	run("sudo mount /dev/cdrom /media/cdrom")
	run("apt-get install -t testing ")
	run("")