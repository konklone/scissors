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

def init_setup():
	util.putstring("""#!/bin/sh
# https://launchpad.net/~dotcloud/+archive/lxc-docker/+packages

### BEGIN INIT INFO
# Provides:          docker
# Required-Start:    $local_fs $remote_fs
# Required-Stop:     $local_fs $remote_fs
# Should-Start:      autofs $network $named alsa-utils pulseaudio
# Should-Stop:       autofs $network $named alsa-utils pulseaudio
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Music Player Daemon
# Description:       Start the docker daemon
### END INIT INFO

. /lib/lsb/init-functions

PATH=/sbin:/bin:/usr/sbin:/usr/bin
NAME=docker
DESC="docker daemon"
DAEMON=/usr/local/bin/docker
PIDFILE=/var/run/docker.pid
DOCKER_OPTS="-d=true"

docker_start () {
    log_action_msg "Starting $DESC" "$NAME"

    start-stop-daemon --start --quiet --oknodo --pidfile "$PIDFILE" \
        --exec "$DAEMON" -- $DOCKER_OPTS &
    log_end_msg $?
}
docker_stop () {
    log_daemon_msg "Stopping $DESC" "$NAME"
    start-stop-daemon --stop --quiet --oknodo --retry 5 --pidfile "$PIDFILE" \
        --exec $DAEMON
    log_end_msg $?
}
case "$1" in
    start)
        docker_start
        ;;
    stop)
        docker_stop
        ;;
    status)
    	status_of_proc -p $PIDFILE $DAEMON $NAME
	;;
    restart|force-reload)
        docker_stop
        docker_start
        ;;
    force-start)
        docker_start
        ;;
    force-restart)
        docker_stop
        docker_start
        ;;
    force-reload)
	docker_stop
	docker_start
	;;
    *)
        echo "Usage: $0 {start|stop|status|restart}"
        exit 2
        ;;
esac""", "/etc/init.d/docker")
    	run("chmod +x /etc/init.d/docker")


def install_docker():

	kernel_upgrade()
	run("modprobe aufs")
	run("apt-get install curl")
	run("wget http://get.docker.io -O - | bash")
	init_setup()

	run("service docker start")
	