from fabric.api import run, sudo, env, settings, local
from fabric.context_managers import cd
from util import putstring
import fabric
env.use_ssh_config = True
DEBIAN = "debian"

def what_system():
    if run("ls /etc | grep debian_version").find("debian_version") != -1:
        return DEBIAN
    raise Exception()

def debian_install(what):
    if what_system() != DEBIAN:
        return
    with settings(warn_only=True):
        if run('dpkg -l | grep "%s\\s\\+"' % what).find(what) != -1:
            print "dep %s already installed" % what
            return
    sudo('apt-get install -y %s' % what)

def install_tarball(url, options="", config_options=""):
    tgz = url.split("/")[-1]
    basename = tgz.replace(".tar.gz", "")
    basename = basename.replace("tgz", "")
    #todo: add other filetypes
    with cd("~/"):
        run('rm -rf %s* tmp' % basename)
        run('mkdir tmp')
        run("wget '%s'" % url)
        run('tar xf %s -C tmp' % tgz)
        makefile_path = run("""find tmp -name configure | perl -lne 'print tr:/::, " $_"' | sort -n | cut -d' ' -f2""").split('\n')[0]  # http://stackoverflow.com/questions/539583/how-do-i-recursively-list-all-directories-at-a-location-breadth-first
        makefile_path = run('dirname ' + makefile_path)
        with cd(makefile_path):
            run('./configure %s' % config_options)
            run('make %s' % options)
            sudo('make install')

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

def install_git():
    debian_install('build-essential')
    debian_install('zlib1g-dev')
    debian_install('tcl')
    debian_install('gettext')
    with settings(warn_only=True):
        if run('git --version').find("git version 1.8.3") != -1:
            return
    install_tarball('https://git-core.googlecode.com/files/git-1.8.3.tar.gz')

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

