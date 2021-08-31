#!/bin/bash

pushd python/loopy
git apply ../../patches/loopy/Current.patch
git apply ../../patches/loopy/0001-Disable-a-logging-statement-that-breaks.patch
git apply ../../patches/loopy/0001-fix-parameter.patch
popd

pushd python/ufl
git apply ../../patches/ufl/0001-Remove-special-case-for-variable-in-ufl2dot.patch
popd
