import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "scissors",
    version = "0.1",
    author = "Drew Crawford",
    author_email = "drew@sealedabstract.com",
    description = ("An administration tool for Debian, and a PaaS based on Docker.io"),
    license = "RPL",
    keywords = "PaaS, Docker, administration, debian",
    url = "http://github.com/drewcrawford/scissors",
    packages=['scissors'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: System :: Software Distribution",
		"Topic :: System :: Systems Administration",
		"Topic :: System :: Installation/Setup",
        "Operating System :: POSIX :: Linux"
    ],
    package_data = {
        '': ['*.drop'],
    },
    scripts=["scripts/scissors"],
    install_requires=['fabric >= 1.7']
)