# SABER BUNDLE
&copy; Copyright 2025 Meteorologisk Institutt

This software is licensed under the terms of the Apache Licence Version 2.0
which can be obtained at [http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0).

The goal of this repository is to keep an archive of the code and scripts required to reproduce the results and illustrations used in an article about the NICAS method. **Please do not use the SABER code of this repository for other purposes, since it will not be updated!**

This repository contains:
- an archive  of [SABER](https://github.com/jcsda/saber),
- the necessary CMakeLists.txt file to compile a bundle using [ecbuild](https://github.com/ecmwf/ecbuild),
- an archive of the data and Python script required to generate the illustrations of the article.

To compile and run SABER:
- Install [ecbuild](https://github.com/ecmwf/ecbuild) and add it in your PATH.
- Run the following bash script:
```bash
# Define the environment variable SABER_SRC pointing to the directory containing this README:
export SABER_SRC=${PWD}

# Create a build directory, whose path is stored in the environment variable SABER_BUILD:
export SABER_BUILD=$MY_BUILD_DIRECTORY/saber_bundle
mkdir -p ${SABER_BUILD}

# Go to the build directory:
cd ${SABER_BUILD}

# Run ecbuild (potentially with cmake-like options):
ecbuild ${SABER_SRC}

# Go to the saber directory
cd saber

# Run test (only the ones needed for the NICAS article)
ctest -R doc
```
