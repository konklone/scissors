# The contents of this file are licensed to you under the Reciprical Public License (RPL).  See the LICENSE file for details.
#this script installs scissors
set -e
apt-get install -y python-pip python-dev unzip
pip install pip git+https://github.com/drewcrawford/scissors.git
#wget https://github.com/drewcrawford/scissors/archive/master.zip
#unzip master.zip -d .
#cd scissors-master
#python setup.py install
