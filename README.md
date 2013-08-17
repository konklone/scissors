# What

Scissors is really two things:

* An administration tool for Debian
* A PaaS based on Docker.io

So basically, scissors will let you take any Debian system, and, *in one command*, configure the entire system so that you type "git push" and your Docker application deploys.  It's that easy.

scissors is powerful enough to wrangle complex administrative tasks like building Python from source and upgrading your kernel.  So you can also use scissors to configure the *inside* of your Docker container, if you're using Debian as a base.

# How

If you're on Debian, this installs all dependencies and places scissors in your home directory:

    wget https://raw.github.com/drewcrawford/scissors/master/install_scissors.sh -O - | sudo bash

Then spinning up a complete PaaS is as simple as:

    cd scissors && fab -H localhost config_scissors_host

 (Note: At present, Debian requires a reboot to upgrade the kernel.  So you must run the command at least twice.)

If your development environment has scissors installed, you can set up a remote application like this:

    cd ~/scissors && fab -H somebody@example.com add_remote /path/to/project.git production

And now just deploy with

    cd /path/to/project.git && git push production master

