# What

Scissors is my deployment / remote administration framework.  I deploy a lot of things that use Python on Debian.  So if that's what you are doing, good.

Scissors automates, among other things, building Python from source, server security hardening, configuring Docker, and updating Debian kernels.

# How

Like this:

    wget https://raw.github.com/drewcrawford/scissors/master/install_scissors.sh -O - | bash