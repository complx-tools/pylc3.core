==========
pylc3.core
==========

Python bindings for liblc3, the LC-3 simulator library behind complx.

* Free software: GNU General Public License v3
* Documentation: https://pylc3.core.readthedocs.io.

Installation
------------

* Install python, boost-python (should be compiled with your version of Python) and castxml.

``
  $ sudo add-apt-repository ppa:tricksterguy87/complx
  $ sudo apt update
  $ sudo apt-get install -y build-essential cmake libboost-python-dev castxml python-pip liblc3-dev
``

* Install scikit-build and dependencies

``$ sudo pip install scikit-build pygccxml pyplusplus``

* Install this package from PyPI:

``$ sudo pip install pylc3.core``

* Run ldconfig

``$ sudo ldconfig``

* Import it in Python:

``import pylc3.core``