# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import re
from spack.package import *


class Vapor(CMakePackage):
    """VAPOR is the Visualization and Analysis Platform for Ocean,
    Atmosphere, and Solar Researchers. VAPOR provides an interactive 3D
    visualization environment that can also produce animations and
    still frame images.
    """

    homepage = "https://www.vapor.ucar.edu"
    url = "https://github.com/NCAR/VAPOR/archive/refs/tags/3.8.1.tar.gz"
    git = "https://github.com/NCAR/VAPOR.git"

    maintainers("vanderwb")

    version("main", branch="main")
    version(
        "3.8.1",
        sha256="b7503665cfad6f66e38058209e46fd367f123c65aa53ba93862977826a0400aa",
        preferred=True,
    )

    variant("doc", default=True, description="Build docs using Doxygen")
    variant("ospray", default=False, description="Enable OSPRay raytracing")

    depends_on("cmake@3.17:", type="build")
    depends_on("xz")
    depends_on("zlib")
    depends_on("openssl")
    depends_on("expat")
    depends_on("curl")
    depends_on("which")
    depends_on("mesa-glu")
    depends_on("gl")
    depends_on("libxtst")
    depends_on("libxcb")
    depends_on("xcb-util")
    depends_on("libxkbcommon")
    depends_on("libpng")
    depends_on("assimp")
    depends_on("netcdf-c~dap~byterange")
    depends_on("udunits")
    depends_on("freetype")
    depends_on("proj@:8")
    depends_on("libgeotiff")
    depends_on("python+ssl")
    depends_on("py-numpy@1.21")
    depends_on("py-scipy")
    depends_on("py-matplotlib")
    depends_on("ospray~mpi", when="+ospray")
    depends_on("glm")
    depends_on("qt+opengl+dbus@5")
    depends_on("doxygen", when="+doc")

    # The build is designed to make a contained installer with
    # dependencies. This patch disables this behavior since dependencies
    # will persist in Spack install tree
    patch("no_dep_install.patch")

    def cmake_args(self):
        spec = self.spec
        args = [
            self.define_from_variant("BUILD_OSP", "ospray"),
            self.define_from_variant("BUILD_DOC", "doc"),
            self.define("BUILD_PYTHON", True),
            ]

        return args

    # VAPOR depends on custom version of GeometryEngine that is
    # packaged with the source code - need to extract and move
    @run_before("cmake")
    def extract_gte(self):
        unzip = which("unzip")
        
        with working_dir("buildutils"):
            unzip("GTE.zip")
            move("GTE", "../include")
    
    # Build will use these optional site defaults which aren't
    # generally applicable to other sites
    @run_before("cmake")
    def clean_local_refs(self):
        force_remove("site_files/site.NCAR")
    
    # The documentation will not be built without this target (though
    # it will try to install!)
    @property
    def build_targets(self):
        targets = []

        if "+doc" in self.spec:
            targets.append("doc")

        return targets + ["all"]

    # Vapor wants all of the Python packages in its build path. This
    # somewhat objectionable code copies packages to the tree.
    @run_after("install")
    def copy_python_packages(self):
        spec = self.spec
        pp = re.compile("py-[a-z0-9-]*")

        for pydep in pp.findall(str(spec)):
            install_tree(spec[pydep].prefix.lib, prefix.lib)
