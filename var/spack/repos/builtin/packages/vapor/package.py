# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import re, sys
from spack.package import *


class Vapor(CMakePackage):
    """VAPOR is the Visualization and Analysis Platform for Ocean,
    Atmosphere, and Solar Researchers. VAPOR provides an interactive 3D
    visualization environment that can also produce animations and
    still frame images.
    """

    homepage = "https://www.vapor.ucar.edu"
    url = "https://github.com/NCAR/VAPOR/archive/refs/tags/v3.9.0.tar.gz"
    git = "https://github.com/NCAR/VAPOR.git"

    maintainers("vanderwb")

    version("main", branch="main")
    version(
        "3.9.0",
        sha256="343ababe40b5824ef826f16c935a6dc1fb18e1a4c88ef967c8d64386f28a99a3",
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
    depends_on("proj@:7")
    depends_on("libgeotiff")
    depends_on("python+ssl", type="build")
    depends_on("py-numpy@1.21", type="build")
    depends_on("py-scipy", type="build")
    depends_on("py-matplotlib", type="build")
    depends_on("ospray~mpi", when="+ospray")
    depends_on("glm")
    depends_on("qt+opengl+dbus@5")
    depends_on("doxygen", when="+doc")

    # These images are required but not provided by the source
    resource(
        name="map-images",
        url="https://stratus.ucar.edu/vapor-images/2023-Jun-images.tar.xz",
        sha256="3f0c6d40446abdb16d5aaaa314349a140e497b3be6f4971394b3e78f22d47c7d",
        placement="share/extras/images",
    )

    def cmake_args(self):
        spec = self.spec
        tp_root = self.build_directory + "/third_party"
        pyvers = spec["python"].version.up_to(2)
        pypath = "{}/lib/python{}".format(tp_root, pyvers)

        args = [
            self.define_from_variant("BUILD_OSP", "ospray"),
            self.define_from_variant("BUILD_DOC", "doc"),
            self.define("BUILD_PYTHON", False),
            self.define("THIRD_PARTY_DIR", tp_root),
            self.define("THIRD_PARTY_LIB_DIR", tp_root + "/lib"),
            self.define("THIRD_PARTY_INC_DIR", tp_root + "/include"),
            self.define("PYTHONVERSION", pyvers),
            self.define("PYTHONDIR", spec.prefix),
            self.define("PYTHONPATH", pypath),
            self.define("NUMPY_INCLUDE_DIR", pypath + "/site-packages/numpy/core/include"),
            self.define("MAP_IMAGES_PATH", "extras/images"),
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

    # Vapor wants all of the Python packages in its build path. This
    # somewhat objectionable code copies packages to the tree. It also
    # copies the Python library so that the site-library is found.
    @run_before("cmake")
    def copy_python_library(self):
        spec = self.spec
        tp_root = self.build_directory + "/third_party"
        mkdirp(tp_root)
        pp = re.compile("py-[a-z0-9-]*")

        for pydep in ["python"] + pp.findall(str(spec)):
            install_tree(spec[pydep].prefix, tp_root)

        # We also need to modify RPATH'ing so final binaries don't
        # use Python at its original prefix
    
    # The documentation will not be built without this target (though
    # it will try to install!)
    @property
    def build_targets(self):
        targets = []

        if "+doc" in self.spec:
            targets.append("doc")

        return targets + ["all"]

    # Finally, let's move the third_party library to the install prefix
    @run_after("install")
    def move_tp_library(self):
        install_tree(self.build_directory + "/third_party/lib", self.spec.prefix.lib)
