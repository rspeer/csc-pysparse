#!/usr/bin/env python

def getoption(config, section, option):
    try:
        val = config.get(section,option)
    except:
        val = None
    return val


def configuration(parent_package='',top_path=None):
    import numpy
    import fnmatch
    import os
    import sys
    import ConfigParser
    from numpy.distutils.misc_util import Configuration
    from numpy.distutils.system_info import get_info, NotFoundError

    # Read relevant PySparse-specific configuration options.
    pysparse_config = ConfigParser.SafeConfigParser()
    pysparse_config.read(os.path.join(top_path, 'site.cfg'))

    umfpack_libdir = getoption(pysparse_config, 'UMFPACK', 'umfpack_libdir')
    umfpack_include = getoption(pysparse_config, 'UMFPACK', 'umfpack_include')
    superlu_libdir = getoption(pysparse_config, 'SuperLU', 'superlu_libdir')
    superlu_include = getoption(pysparse_config, 'SuperLU', 'superlu_include')
    amd_libdir = getoption(pysparse_config, 'AMD', 'amd_libdir')
    amd_include = getoption(pysparse_config, 'AMD', 'amd_include')

    config = Configuration('direct', parent_package, top_path)
    cwd = config.local_path

    # Get BLAS info from site.cfg
    blas_info = get_info('blas_opt',0)
    if not blas_info:
        print 'No blas info found'

    # If UMFPACK or AMD library was not specified, use default.
    umfpack_lib = ['umfpack']
    umfpack_src = []
    amd_lib = ['amd']
    amd_src = []
    if umfpack_libdir is None or amd_libdir is None:
        print 'Using default UMFPACK and AMD'
        print ' If you do not like this, edit the [UMFPACK] and [AMD]'
        print ' sections of site.cfg'
        umfpack_lib = []
        umfpack_libdir = []
        umfpack_srcs = fnmatch.filter(os.listdir(os.path.join(cwd,
                                                              'umfpack','src')),
                                      '*.c')
        umfpack_src = [os.path.join('umfpack','src',f) for f in umfpack_srcs]
        umfpack_include = [os.path.join('umfpack','include')]
        amd_lib = []
        amd_libdir = []
        amd_srcs = fnmatch.filter(os.listdir(os.path.join(cwd,'amd','src')),
                                             '*.c')
        amd_src = [os.path.join('amd','src',f) for f in amd_srcs]
        amd_include = [os.path.join('amd','include')]
    else:
        amd_libdir = [amd_libdir]
        amd_include = [amd_include]
        umfpack_libdir = [umfpack_libdir]
        umfpack_include = [umfpack_include]

    # Build UMFPACK extension.
    umfpack_src.append(os.path.join('src','umfpackmodule.c'))
    config.add_extension(
        name='umfpack',
        sources=umfpack_src + amd_src,
        libraries=amd_lib + umfpack_lib,
        library_dirs=amd_libdir + umfpack_libdir,
        include_dirs=['src'] + umfpack_include + amd_include,
        extra_info=blas_info,
        )

    # If SuperLU library was not specified, use default.
    superlu_lib = ['superlu']
    superlu_src = []
    if superlu_libdir is None:
        print 'Using default SuperLU.'
        print ' If you do not like this, edit the [SuperLU] section of site.cfg'
        superlu_lib = []
        superlu_libdir = []
        superlu_srcs = fnmatch.filter(os.listdir(os.path.join(cwd,
                                                              'superlu','src')),
                                      '*.c')
        superlu_src = [os.path.join('superlu','src',f) for f in superlu_srcs]
        superlu_src += [os.path.join('src','superlumodule.c')]
        superlu_include = [os.path.join('superlu','include')]
    else:
        superlu_libdir = [superlu_libdir]
        superlu_include = [superlu_include]
        superlu_src= [os.path.join('src','superlu3module.c')]

    # Build SuperLU extension.
    superlu_defs = [('USE_VENDOR_BLAS',1)]
    if sys.platform == 'win32':
            superlu_defs += [('NO_TIMER', 1)]

    config.add_extension(
        name='superlu',
        sources=superlu_src,
        define_macros=superlu_defs,
        libraries=superlu_lib,
        library_dirs=superlu_libdir,
        include_dirs=['src'] + superlu_include,
        extra_info=blas_info,
        )

    config.make_config_py()
    return config

if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())
