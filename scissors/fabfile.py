# The contents of this file are licensed to you under the Reciprical Public License (RPL).  See the LICENSE file for details.
from harden import harden
from docker import install_docker
from host import config_scissors_server, add_remote
import fabric.api
fabric.api.env.use_ssh_config = True