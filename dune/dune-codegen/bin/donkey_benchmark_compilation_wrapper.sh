#!/bin/bash

ml gcc/6.4.0
ml benchmark/1.4.0
ml python/3.6.3
ml openmpi
ml cmake
ml openblas
ml metis
ml suite-sparse
ml superlu
ml parmetis

("$@")
code=$?
exit $code
