#!/bin/bash

if [ "$1" = "full" ] ; then
    param=module
else
    param=only
fi

# store hash of current HEAD
oldhead=$(git rev-parse HEAD)

echo "Updating super module..."
git pull origin master

if [ $? -ne 0 ] ; then
    echo "ERROR while updating super module"
    exit 1
fi

# This checks whether the update script itself changed
newhead=$(git rev-parse HEAD)
git diff --exit-code $oldhead $newhead -- update.sh >/dev/null
if [ $? -ne 0 ] ; then
    echo "The update script changed, re-running for possible bug fixes..."
    ./update.sh
    exit $?
fi

pushd dune/dune-pdelab-tutorials
echo "Stashing local changes..."
if [ "$(git stash)" =  "No local changes to save" ] ; then
    skip_stash_pop=true
else
    skip_stash_pop=false
fi
popd

echo "Updating modules..."
git submodule update

if [ $? -ne 0 ] ; then

    echo "ERROR: There was a problem updating the submodules"
    exit 1
fi

if [ $skip_stash_pop = "false" ] ; then
    echo "Restoring local changes..."
    pushd dune/dune-pdelab-tutorials
    git stash pop
    if [ $? -ne 0 ] ; then

        echo "ERROR: Could not restore local changes, probably due to a merge conflict"
        exit 2
    fi
    popd
else
    echo "No local changes saved, skipping git stash pop..."
fi

./dune/dune-common/bin/dunecontrol --opts=release.opts --builddir=$(pwd)/release-build --$param=dune-pdelab-tutorials configure

if [ $? -ne 0 ] ; then

    echo "ERROR: Failed to configure modules"
    exit 2

fi

# ./dune/dune-common/bin/dunecontrol --opts=debug.opts --builddir=$(pwd)/debug-build --$param=dune-pdelab-tutorials configure

