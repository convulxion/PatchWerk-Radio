#!/bin/sh

#meant to be run from a directory containing the
#PatchWerk-Radio and Radio-Patches repositories

if [ -z "$1" ] ; then
    env=development
else
    env=$1
fi

#set the variables depending on whether a live or a test setup is wanted
if [ $env = "master" ] ; then
    INSTNAME=PatchWerk
    BRANCH=master
    CONFIG=config.cfg
else
    INSTNAME=TestPatchWerk
    BRANCH=development
    CONFIG=testconfig.cfg
fi

BINDIR=/usr/local/sbin/$INSTNAME
LOGDIR=/var/log/$INSTNAME
WORKDIR=/var/$INSTNAME
PATCHDIR=$WORKDIR/patches
TMPDIR=$WORKDIR/temp

#checkout the correct branches
cd PatchWerk-Radio
sudo -u guy git checkout $BRANCH

cd ../Radio-Patches
sudo -u guy git checkout master


cd ..

# Clear out the binary dir and then copy the correct files into it
rm -r $BINDIR
mkdir -p $BINDIR
cp -r PatchWerk-Radio/Radio.py   $BINDIR/
cp -r PatchWerk-Radio/master     $BINDIR/
cp -r PatchWerk-Radio/Pd         $BINDIR/
cp -r PatchWerk-Radio/config.cfg $BINDIR/

#if the config file exists in the same directory
#copy it to the bindir
if [ -f ./$CONFIG ]
then
    echo using the config file here
    rm  $BINDIR/config.cfg
    cp  ./$CONFIG $BINDIR/
fi

#give files the correct permissions
chmod 754 $BINDIR/Radio.py
chown -R patchwerk:radio $BINDIR


# Clear out the patch directory, then copy the new patches back into it
rm -r $WORKDIR
mkdir -p $PATCHDIR
cp -r ./Radio-Patches/* $PATCHDIR/
rm -r $PATCHDIR/README

mkdir -p $TMPDIR

#fix permissions
chown -R patchwerk:radio $WORKDIR
chmod -R 755 $WORKDIR


