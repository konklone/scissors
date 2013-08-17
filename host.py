# The contents of this file are licensed to you under the Reciprical Public License (RPL).  See the LICENSE file for details.
from fabric.api import run, sudo, env, settings, local
from fabric.context_managers import cd
import fabric
import util

def config_scissors_server():
    import harden
    #harden.harden()
    import docker
    #docker.install_docker()
    util.install_git()

def add_remote(gitrepo,name):
    with settings(warn_only=True):
        user = run("whoami")
        if user != "deploy":
            print "Error, try running as deploy user"
            return
        bname = run("basename {GITREPO}".format(GITREPO=gitrepo))+"-"+name
        print "bname is",bname
        namepath = "~/deploy/{NAME}".format(NAME=bname)
        run("rm -rf {NAMEPATH}".format(NAMEPATH=namepath))
        run("mkdir ~/deploy")
        run("mkdir {NAMEPATH}".format(NAMEPATH=namepath))
        run("mkdir {NAMEPATH}/bare".format(NAMEPATH=namepath))
        run("mkdir {NAMEPATH}/work".format(NAMEPATH=namepath))
        with cd("{NAMEPATH}/bare".format(NAMEPATH=namepath)):
            run("git init --bare")
    drop = open("scissors.drop").read()
    util.putstring(drop,"{NAMEPATH}/bare/hooks/post-receive".format(NAMEPATH=namepath))
    run("chmod +x {NAMEPATH}/bare/hooks/post-receive".format(NAMEPATH=namepath))
    local("cd {GITREPO} && git remote add {NAME} deploy@{SERVER}:{NAMEPATH}/bare".format(GITREPO=gitrepo,NAME=name,NAMEPATH=namepath,SERVER=env.host))




