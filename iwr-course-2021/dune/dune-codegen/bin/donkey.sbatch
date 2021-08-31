#!/bin/bash

# IMPORTANT
# Remember to set the working directory of this script through
# sbatch -D <workdir>

# Set a name for the job
#SBATCH -J poisson_dg_tensor

# Number of processes
#SBATCH -n 32

# Choose the SLURM partition (sinfo for overview)
#SBATCH -p haswell16c

# Each process needs two PUs: circumvent hyperthreading
#SBATCH -c 2

# Load modules
ml gcc/7.3.0
ml openmpi
ml openblas
ml metis
ml superlu
ml suite-sparse

# Pin processes to cores
# (Possible values: socket, core)
SRUNOPT="--cpu_bind=verbose,core"

# Search for runnable executables
FILES=$(ls *.ini | grep -v '^verify')
for inifile in $FILES
do
  line=$(grep ^"opcounter = " $inifile)
  extract=${line##opcounter = }
  UPPER=10
  if [ $extract -eq 1 ]
  then
    UPPER=1
  fi
  COUNT=0
  while [ $COUNT -lt $UPPER ]; do
    exec=${inifile%.ini}
    srun $SRUNOPT ./$exec $inifile
    COUNT=$((COUNT + 1))
  done
done
