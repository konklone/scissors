from fabric.api import run, sudo, env, settings, local
from fabric.context_managers import cd
import fabric
import util


def kernel_upgrade():
	version = run("uname -r")
	from distutils.version import LooseVersion
	actualVersion = LooseVersion(version)
	requiredVersion = LooseVersion("3.10")
	if actualVersion < requiredVersion:
		print "Kernel upgrade will be required."
	else:
		return
	#We need to enable testing
	util.append("deb http://ftp.us.debian.org/debian/ testing main non-free","/etc/apt/sources.list")
	util.append("deb-src http://ftp.us.debian.org/debian/ testing main non-free","/etc/apt/sources.list")
	util.append("deb http://security.debian.org/ testing/updates main non-free","/etc/apt/sources.list")
	util.append("deb-src http://security.debian.org/ testing/updates main non-free","/etc/apt/sources.list")
	util.append('APT::Default-Release "stable";',"/etc/apt/apt.conf.d/50usestable.conf")
	run("apt-get update")
	run("apt-get install -t testing linux-image-amd64 firmware-linux-nonfree")
	print "A reboot will be required."
	run("shutdown -r now")


def install_docker():

	kernel_upgrade()
	run("modprobe aufs")
	run("wget http://get.docker.io -O - | bash")
	