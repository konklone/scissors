from fabric.api import run, sudo, env, settings, local
from fabric.context_managers import cd
import fabric
import util

def install_virtualbox_additions():
	util.debian_install_from_source("virtualbox-guest-additions")