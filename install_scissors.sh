# The contents of this file are licensed to you under the Reciprical Public License (RPL).  See the LICENSE file for details.
#this script installs scissors
set -e
apt-get install -y python-pip python-dev unzip
pip install https://github.com/drewcrawford/scissors/zipball/master
