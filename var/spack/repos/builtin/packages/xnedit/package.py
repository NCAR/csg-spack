# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

class Xnedit(MakefilePackage):
    """XNEdit is a multi-purpose text editor for the X Window System, which 
    combines a standard, easy to use, graphical user interface with the thorough 
    functionality and stability required by users who edit text eight hours a day. 
    It provides intensive support for development in a wide variety of languages, 
    text processors, and other tools, but at the same time can be used productively 
    by just about anyone who needs to edit text.

    XNEdit is a fork of the Nirvana Editor (NEdit) and provides new functionality 
    like antialiased text rendering and support for unicode."""

    homepage = "https://github.com/unixwork/xnedit"
    url = "https://github.com/unixwork/xnedit/archive/refs/tags/v1.5.1.tar.gz"
    git = "https://github.com/unixwork/xnedit"

    maintainers("neumanbrett")
    #version("master", branch="master", submodules=True)
    version("1.5.1", sha256="c871589e912ed9f9a02cc57932f5bb9694ec91cc5487be0cd55e7d3aade372d6")

    depends_on("motif")
    depends_on("libxt")
    depends_on("libxrender")
    depends_on("libxft")
    depends_on("fontconfig")
    depends_on("pcre")
    depends_on("iconv")

    def setup_build_environment(self, env):
        env.set("LIBS", "-lpcre -lXm -lXt -lX11 -lXrender -lm -liconv")

    def edit(self, spec, prefix):
        # Make edits to the linux version makefile spec
        makefile = FileFilter("makefiles/Makefile.linux")

        # Use the Spack compiler wrappers and add iconv dependency
        makefile.filter("CC=.*", "CC={0}".format(spack_cc))
        makefile.filter("-L/usr/X11R6/lib", "-liconv")
        makefile.filter("-I/usr/X11R6/include", "")
        makefile.filter("-I/usr/include/X11", "") 

    def build(self, spec, prefix):
        make("linux")

    def install(self, spec, prefix):
        make("install","PREFIX={0}".format(prefix))

