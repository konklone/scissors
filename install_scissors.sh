#this script installs scissors
set -e
wget http://www.python.org/ftp/python/3.3.2/Python-3.3.2.tar.bz2
tar -xf Python-3.3.2.tar.bz2
cd Python-3.3.2/
./configure
make install
pip install fabric
wget https://github.com/drewcrawford/scissors/archive/master.zip
unzip master.zip -d scissors
