#!/usr/bin/env bash
# Install the ML enviroment for strangeness analysis
#
# Author: Gianni Liveraro
# Date: 2024-03-31
#

flag=$1

#First things first: We will touch on users .bashrc, so we backupo it
cp $HOME/.bashrc $HOME/.bashrc_backup

BASEDIR=$PWD

# Check if I will use python3 or python2. Exit if python is not found;
PYTHON3=`which python3`
PYTHON=`which python`
PYTHON_VERSION=`$PYTHON3 --version`

if [ $PYTHON_VERSION='' ]; then
  PYTHON_VERSION=`$PYTHON --version`
  if [ $PYTHON_VERSION='' ]; then
    echo "Python not found"
    exit -1
  fi
  PYTHON3_FOUND=false
else
  PYTHON3_FOUND=true
fi

# If python3 is found, gets the latest Miniconda3. Else, gets Miniconda 2
if [ $PYTHON3_FOUND ]; then
  wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
  mv Miniconda3-latest-Linux-x86_64.sh Miniconda-latest-Linux-x86_64.sh
else
  wget https://repo.anaconda.com/miniconda/Miniconda2-latest-Linux-x86_64.sh
  mv Miniconda2-latest-Linux-x86_64.sh Miniconda-latest-Linux-x86_64.sh
fi

#Install miniconda
chmod u+x Miniconda-latest-Linux-x86_64.sh
./Miniconda-latest-Linux-x86_64.sh -p $HOME/.conda -b
rm Miniconda-latest-Linux-x86_64.sh #Clean up install file

#Install environment and setup automatic activation
export PATH=$HOME/.conda/bin:$PATH
conda init
source $HOME/.bashrc
#conda config --add channels conda-forge #Add conda-forge channel
conda update -n base -c defaults conda  #Update conda


conda env create -f $BASEDIR/src/ML_Env.yaml
echo "conda activate ML_Env" >> $HOME/.bashrc
