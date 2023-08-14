# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Parallelio1(CMakePackage):
    """The Parallel IO libraries (PIO) are high-level parallel I/O C and
    Fortran libraries for applications that need to do netCDF I/O from
    large numbers of processors on a HPC system."""

    homepage = "https://ncar.github.io/ParallelIO/"
    url = "https://github.com/NCAR/ParallelIO/archive/refs/tags/pio1.10.1.tar.gz"
    git = "https://github.com/NCAR/ParallelIO.git"

    maintainers("vanderwb")

    version("1.10.1", sha256="bfe987e04c2ac74d27475ffbf7ceb4a83b0e2fbda8773690962f0b14e0cb39aa")

    variant("pnetcdf", default=False, description="enable pnetcdf")
    variant("timing", default=False, description="enable GPTL timing")
    variant("shared", default=True, description="build shared libraries")
    variant("mpi", default=True, description="Use mpi to build, otherwise use mpi-serial")

    depends_on("cmake@3.7:", type="build")
    depends_on("mpi", when="+mpi")
    depends_on("mpi-serial", when="~mpi")
    depends_on("netcdf-c +mpi", type="link", when="+mpi")
    depends_on("netcdf-c ~mpi", type="link", when="~mpi")
    depends_on("netcdf-fortran", type="link")
    depends_on("parallel-netcdf", type="link", when="+pnetcdf")

    # Tools required for CMake build
    resource(
        name="cmakeutils",
        git="https://github.com/CESM-Development/CMake_Fortran_utils",
        tag="CMake_Fortran_utils_150308"
    )

    resource(
        name="genf90",
        git="https://github.com/PARALLELIO/genf90.git",
        tag="genf90_140121"
    )

    def cmake_args(self):
        define = self.define
        define_from_variant = self.define_from_variant
        spec = self.spec
        src = self.stage.source_path

        args = [
            define("NETCDF_C_DIR", spec["netcdf-c"].prefix),
            define("NETCDF_Fortran_DIR", spec["netcdf-fortran"].prefix),
            define("USER_CMAKE_MODULE_PATH", join_path(src, "CMake_Fortran_utils")),
            define("GENF90_PATH", join_path(src, "genf90")),
            define_from_variant("BUILD_SHARED_LIBS", "shared"),
        ]

        if spec.satisfies("%gcc@10:"):
            env["FFLAGS"] = "-fallow-argument-mismatch"
        if spec.satisfies("+pnetcdf"):
            args.extend([define("PNETCDF_DIR", spec["parallel-netcdf"].prefix)])
        if spec.satisfies("+mpi"):
            env["CC"] = spec["mpi"].mpicc
            env["FC"] = spec["mpi"].mpifc
        else:
            env["FFLAGS"] = env["FFLAGS"] + " -DNO_MPIMOD"
            args.extend(
                [
                    define("PIO_USE_MPISERIAL", True),
                    define("MPISERIAL_PATH", spec["mpi-serial"].prefix),
                ]
            )
        args.extend(
            [
                define_from_variant("PIO_BUILD_TIMING", "timing"),
            ]
        )
        return args

    def install(self, spec, prefix):
        mkdir(prefix.lib)
        mkdir(prefix.include)

        with working_dir(join_path(self.build_directory, "pio")):
            install("*.mod", prefix.include)
            install("*.h", prefix.include)

            if spec.satisfies("+shared"):
                install("*.so", prefix.lib)
            else:
                install("*.a", prefix.lib)

    def setup_run_environment(self, env):
        env.set("PIO_VERSION_MAJOR", "1")
        valid_values = "netcdf"
        if self.spec.satisfies("+mpi"):
            valid_values += ",netcdf4p,netcdf4c"
            if self.spec.satisfies("+pnetcdf"):
                valid_values += ",pnetcdf"
        env.set("PIO_TYPENAME_VALID_VALUES", valid_values)
