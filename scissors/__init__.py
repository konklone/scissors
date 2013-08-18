# The contents of this file are licensed to you under the Reciprical Public License (RPL).  See the LICENSE file for details.
#Exhibit B notice
print "Contains code from scissors, (C) 2013 Drew Crawford.  https://github.com/drewcrawford/scissors"
from fabric.api import run, sudo, env, settings, local
from fabric.context_managers import cd
from util import putstring
import fabric









def install_python():
    debian_install('build-essential')
    debian_install('libreadline-dev')  # this makes the arrow keys work
    debian_install('zlib1g-dev')
    debian_install('libsqlite3-dev')
    debian_install('libbz2-dev')
    debian_install('libssl-dev')
    with settings(warn_only=True):
        if run('python --version').find("Python 2.7.4") != -1:
            return
    install_tarball('http://python.org/ftp/python/2.7.4/Python-2.7.4.tgz')

def pip_install(what):
    install_pip()
    run('pip install "%s"' % what)

def install_pip():
    with settings(warn_only=True):
        if run('which pip').find("pip") != -1:
            return
    run('curl http://python-distribute.org/distribute_setup.py | python')
    run('curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python')

def install_python_worker_tools():
    pip_install("supervisor")
    pip_install("virtualenv")



def debian_upgrade():
    sudo('apt-get update')
    sudo('apt-get -y upgrade')



def code_drop(WORKING_TREE):
    GIT_REPO=WORKING_TREE+"/git"
    with settings(warn_only=True):
        run("mkdir " + WORKING_TREE)
        run("mkdir "+GIT_REPO)
        run("mkdir " + WORKING_TREE+"/log")
    drop = open("code.drop").read()
    with cd(GIT_REPO):
        run("git init --bare")
    drop = drop.format(GIT_REPO=GIT_REPO,WORKING_TREE=WORKING_TREE)
    putstring(drop,GIT_REPO+"/hooks/post-receive")
    run("chmod +x " + GIT_REPO + "/hooks/post-receive")

def emergency_start(WORKING_TREE):
    with cd(WORKING_TREE+"/git"):
        run("hooks/post-receive".format(TREE=WORKING_TREE))

def get_logs(WORKING_TREE):
    fabric.api.get("%s/log/*" % WORKING_TREE, ".")

def show_logs(WORKING_TREE):
    run("tail -f %s/log/*" % WORKING_TREE)

