# The contents of this file are licensed to you under the Reciprical Public License (RPL).  See the LICENSE file for details.
#this script installs scissors
set -e
apt-get install -y python-pip python-dev
pip install fabric
wget https://github.com/drewcrawford/scissors/archive/master.zip
apt-get install -y unzip
unzip master.zip -d .
mv scissors-master scissors
cd scissors && fab -l
