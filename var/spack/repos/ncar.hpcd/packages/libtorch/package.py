# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

class Libtorch(BundlePackage):
    """We provide binary distributions of all headers, libraries and CMake configuration
    files required to depend on PyTorch. We call this distribution LibTorch. Note that LibTorch
    is only available for C++."""

    homepage = "https://pytorch.org/cppdocs/installing.html"

    maintainers = ['vanderwb']
    
    version('2.2.1')
    version('2.1.2')
