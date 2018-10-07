# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyDxchange(PythonPackage):
    """DXchange provides an interface with tomoPy and raw tomographic data
       collected at different synchrotron facilities."""

    homepage = "https://github.com/data-exchange/dxchange"
    url      = "https://github.com/data-exchange/dxchange/archive/v0.1.2.tar.gz"

    import_modules = ['dxchange']

    version('0.1.2', '36633bb67a1e7d1fb60c2300adbcbab3')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-h5py', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-netcdf4', type=('build', 'run'))
    depends_on('py-spefile', type=('build', 'run'))
    depends_on('py-edffile', type=('build', 'run'))
    depends_on('py-tifffile', type=('build', 'run'))
    depends_on('py-dxfile', type=('build', 'run'))
    depends_on('py-olefile', type=('build', 'run'))
    depends_on('py-astropy', type=('build', 'run'))
