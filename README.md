# What

Scissors is really two things:

* An administration tool for Debian
* A PaaS based on Docker.io

So basically, scissors will let you take any Debian system, and, *in one command*, configure the entire system so that you type "git push" and your Docker application deploys.  It's that easy.

You can also run a scissors host from inside Vagrant.  So if you are developing Docker applications on OSX, you can get them running in like 1 command.

scissors is powerful enough to wrangle complex administrative tasks like building Python from source and upgrading your kernel.  So you can also use scissors to configure the *inside* of your Docker container, if you're using Debian as a base.

# Installation

If you're on Debian, this installs scissors on any system whatsoever:

    wget https://raw.github.com/drewcrawford/scissors/master/install_scissors.sh -O - | sudo bash

On other platforms (e.g. OSX) you can install scissors from pip, [if you have pip installed](http://www.pip-installer.org/en/latest/installing.html):

    sudo pip install git+https://github.com/drewcrawford/scissors.git 

# Use

## In development

If you're developing any Docker applicaton and you want to run it on your Mac, we have pre-built Vagrant images that you can spin up that do exactly that.

Copy the prebuilt.Vagrantfile over to your project's respository.  Then just

    vagrant up
    vagrant ssh-config --host vagrant-deploy | sed -e 's/\(User\) vagrant/\1 deploy/g' >> ~/.ssh/config #configure normal SSH for use with vagrant
    scissors -H vagrant-deploy add_remote:.,development
    git push development master

Subsequent deploys only require the push.

## In production

Spinning up a complete PaaS is as simple as:

    scissors -H [SSHSpec] config_scissors_host

Where `SSHSpec` is something like `root@example.com`.  scissors will SSH into the server and configure everthing.  You can also use `localhost` as the spec.

 (Note: At present, Debian requires a reboot to upgrade the kernel.  So you must run the command at least twice.)

Now on your development machine, you can set up a git remote like this:

    scissors -H deploy@any-scissors-host.com add_remote /path/to/project.git production

And now just deploy with

    git push production master


