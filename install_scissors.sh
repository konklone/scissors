# The contents of this file are licensed to you under the Reciprical Public License (RPL).  See the LICENSE file for details.
#this script installs scissors
set -e
apt-get install python3.3 python3-pip
pip install fabric
wget https://github.com/drewcrawford/scissors/archive/master.zip
unzip master.zip -d scissors
