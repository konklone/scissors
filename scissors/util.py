# The contents of this file are licensed to you under the Reciprical Public License (RPL).  See the LICENSE file for details.

from fabric.api import run, sudo, env, settings, local
from fabric.context_managers import cd
DEBIAN = "debian"

def putstring(what, where):
    import StringIO
    from fabric.api import put
    put(StringIO.StringIO(what), where)

def append(what,where):
	import fabric.contrib.files
	fabric.contrib.files.append(where,what)


"""This ensures that the line you specify appears somewhere in the config file.  If not, it is added to the end."""
def config(what,where):
	import fabric.contrib.files
	if not fabric.contrib.files.contains(where,what):
		append(what,where)

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

GIT_VERSION = "1.8.3.4"
def install_git():
    debian_install('build-essential')
    debian_install('zlib1g-dev')
    debian_install('tcl')
    debian_install('gettext')
    with settings(warn_only=True):
        if run('git --version').find("git version {GIT_VERSION}".format(GIT_VERSION=GIT_VERSION)) != -1:
            return
    install_tarball("https://git-core.googlecode.com/files/git-{GIT_VERSION}.tar.gz".format(GIT_VERSION=GIT_VERSION))

def debian_install(what):
    if what_system() != DEBIAN:
        return
    with settings(warn_only=True):
        if run('dpkg -l | grep "%s\\s\\+"' % what).find(what) != -1:
            print "dep %s already installed" % what
            return
    sudo('apt-get install -y %s' % what)

def what_system():
    if run("ls /etc | grep debian_version").find("debian_version") != -1:
        return DEBIAN
    raise Exception()