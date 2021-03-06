#!/usr/bin/env python
"""A fast sparse matrix library for Python (Commonsense Computing version)

Pysparse is a fast sparse matrix library for Python. It provides several sparse
matrix storage formats and conversion methods. It also implements a number of
iterative solvers, preconditioners, and interfaces to efficient factorization
packages. Both low-level and high-level interfaces are available, each with
different strengths.

This is not the official source to PySparse. This is csc-pysparse, a downstream
package maintained by the Commonsense Computing Group
(http://csc.media.mit.edu) with the goal of making it install automatically
through Pip or easy_install.

Original authors of PySparse:

- R. Geus    <hamsel@sf.net>
- D. Orban   <d-orban@sf.net>
- D. Wheeler <wd15@sf.net>

Packaged by: Rob Speer <rspeer@mit.edu>
"""

DOCLINES = __doc__.split("\n")

import os
import sys

try:
    import setuptools  # If you want to enable 'python setup.py develop'
    #pass
except:
    print 'setuptools module not found.'
    print "Install setuptools if you want to enable 'python setup.py develop'."

CLASSIFIERS = """\
Development Status :: 4 - Beta
Intended Audience :: Science/Research
Intended Audience :: Developers
License :: OSI Approved :: BSD License
Programming Language :: Python
Programming Language :: C
Topic :: Software Development
Topic :: Scientific/Engineering
Operating System :: Microsoft :: Windows
Operating System :: POSIX
Operating System :: Unix
Operating System :: MacOS
"""

# BEFORE importing distutils, remove MANIFEST. distutils doesn't properly
# update it when the contents of directories change.
if os.path.exists('MANIFEST'): os.remove('MANIFEST')

def configuration(parent_package='',top_path=None):
    import numpy
    from numpy.distutils.misc_util import Configuration
    config = Configuration(None, parent_package, top_path)
    config.set_options(ignore_setup_xxx_py=True,
                       assume_default_configuration=True,
                       delegate_options_to_subpackages=True,
                       quiet=True)

    config.add_include_dirs(numpy.get_include())
    config.add_include_dirs(os.path.join(config.top_path,'pysparse','include'))
    config.add_subpackage('pysparse')

    # Set config.version
    config.get_version(os.path.join('pysparse','version.py'))

    return config

def setup_package():

    from numpy.distutils.core import setup, Extension
    from numpy.distutils.misc_util import Configuration

    old_path = os.getcwd()
    local_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(local_path)
    sys.path.insert(0,local_path)
    sys.path.insert(0,os.path.join(local_path,'pysparse')) # to retrieve version

    try:
        setup(
            name = 'csc-pysparse',
            author = "Roman Geus, Dominique Orban, Daniel Wheeler",
            author_email = "{hamsel,d-orban,wd15}@sf.net,",
            maintainer = "Rob Speer",
            maintainer_email = "rspeer@mit.edu",
            description = DOCLINES[0],
            long_description = "\n".join(DOCLINES[2:]),
            url = "http://github.com/rspeer/csc-pysparse",
            #download_url = "sf.net/projects/pysparse",
            license = 'BSD-style',
            classifiers=filter(None, CLASSIFIERS.split('\n')),
            platforms = ["Windows", "Linux", "Solaris", "Mac OS-X", "Unix"],
            configuration=configuration,
            )
    finally:
        del sys.path[0]
        os.chdir(old_path)

    return

if __name__ == '__main__':
    setup_package()
