# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Vexcl(CMakePackage):
    """VexCL is a vector expression template library for OpenCL/CUDA. It has been
    created for ease of GPGPU development with C++. VexCL strives to reduce amount
    of boilerplate code needed to develop GPGPU applications. The library provides
    convenient and intuitive notation for vector arithmetic, reduction, sparse
    matrix-vector products, etc. Multi-device and even multi-platform computations
    are supported. The source code of the library is distributed under very
    permissive MIT license.
    """

    homepage = "https://vexcl.readthedocs.io/en/latest/"
    url = "https://github.com/ddemidov/vexcl/archive/refs/tags/1.4.3.tar.gz"
    git = "https://github.com/ddemidov/vexcl.git"

    maintainers("vanderwb")

    version("master", branch="master")
    version("1.4.3", sha256="c9f2a429dc4454e69332cc8b7fbaa5adcd831bce1267fcc1f19e1c110d82deb8")

    depends_on("cmake", type="build")
    depends_on("boost+chrono+date_time+filesystem~mpi+multithreaded+program_options+system~taggedlayout+test+thread~versionedlayout cxxstd=11")
    depends_on("opencl")

    def cmake_args(self):
        spec = self.spec

        args = [
            self.define("Boost_NO_BOOST_CMAKE", True),
            self.define("Boost_NO_SYSTEM_PATHS", True),
            self.define("BOOST_ROOT", spec["boost"].prefix),
            self.define("BOOST_INCLUDEDIR", spec["boost"].prefix.include),
            ]

        return args
