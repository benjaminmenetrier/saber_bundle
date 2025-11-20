# (C) Copyright 2025 Meteorolgisk Institutt
#

# SABER bundle
cmake_minimum_required( VERSION 3.12 FATAL_ERROR )
find_package( ecbuild 3.6 REQUIRED HINTS ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_SOURCE_DIR}/../ecbuild)
project( saber_bundle VERSION 1.0.0 LANGUAGES C CXX Fortran )
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
include( ecbuild_bundle )

# Default release mode
set( ECBUILD_DEFAULT_BUILD_TYPE Release )

# Options
option( ENABLE_MPI "Compile with MPI" ON )
option( ENABLE_OMP "Compile with OpenMP" ON )
option( ENABLE_CUDA "Compile with CUDA" OFF )
option( ENABLE_MKL "Compile with MKL" OFF )
option( ENABLE_TRANSI "Compile TransI C-interface to trans" ON )
option( ENABLE_ETRANS "Include Limited-Area-Model Transforms" ON )
option( ENABLE_JEDI_MODEL_DATA "Obtain saber/vader test data from jedi-model-data repository (vs tarball)" OFF )

# Setup
link_directories( ${CMAKE_CURRENT_BINARY_DIR}/lib )
include( GNUInstallDirs )
set( INSTALL_LIB_DIR ${CMAKE_INSTALL_LIBDIR} CACHE STRING "Library installation directory" FORCE )
set( ECBUILD_DEFAULT_BUILD_TYPE Release CACHE STRING "ECBuild default build type" FORCE )
set( CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin )
set( CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib )
set( CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib )
set( CMAKE_INSTALL_RPATH_USE_LINK_PATH ON )
set( CMAKE_BUILD_WITH_INSTALL_RPATH ON )

# Initialize bundle
ecbuild_bundle_initialize()

# jedi-cmake
ecbuild_bundle( PROJECT jedicmake GIT "https://github.com/jcsda/jedi-cmake.git" TAG 40d521f9a2d796fcbc6234d77abceeffefb8eb7f RECURSIVE )
include( jedicmake/cmake/Functions/git_functions.cmake )
list( APPEND CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/jedicmake/CMakeModules/Modules )

# ECMWF tools
ecbuild_bundle( PROJECT eckit GIT "https://github.com/ecmwf/eckit.git" TAG 1.32.2 )
ecbuild_bundle( PROJECT fckit GIT "https://github.com/ecmwf/fckit.git" TAG 0.14.0 )
ecbuild_bundle( PROJECT fiat GIT "https://github.com/ecmwf-ifs/fiat.git" TAG 1.6.1 )
ecbuild_bundle( PROJECT ectrans GIT "https://github.com/ecmwf-ifs/ectrans.git" TAG 3094b24ec9c1862772e2b02f4e06c797247d57fc )
ecbuild_bundle( PROJECT atlas GIT "https://github.com/ecmwf/atlas.git" TAG 0.44.0 )

# oops
ecbuild_bundle( PROJECT oops GIT "https://github.com/jcsda/oops.git" TAG 47a42647228c3fa00165647227a2adba95b142fe )

# jedi-data
ecbuild_bundle( PROJECT jedi-model-data GIT "https://github.com/jcsda-internal/jedi-model-data.git" TAG e725b7f642e85fd33c4405e5244f2c2aefaaa21f )

# vader
ecbuild_bundle( PROJECT vader GIT "https://github.com/jcsda/vader.git" TAG 5c5970db95d7ad1191737e84c0b0f16e1f704110 )

# saber
ecbuild_bundle( PROJECT saber )

ecbuild_bundle_finalize()
