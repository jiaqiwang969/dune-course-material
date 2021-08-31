#!/bin/bash

for f in "$@"
do
    perl -i -pe 's/FunctionSpace\(.*\)\), //g' $f
    dot -Tpdf -O $f
done
