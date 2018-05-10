#!/bin/bash
#
#SBATCH --partition=piv
#SBATCH --job-name=hello_world_py
#SBATCH --time=10:00
#SBATCH --output=hello_world_py.%j.out
#SBATCH --ntasks=4
#

echo "----------Preparando el entorno-------------"
module purge
module load prun gnu7/7.3.0 openmpi3/3.0.0 py2-mpi4py/3.0.0

echo "-------Inicio de Proceso en mpi Python------"
prun thecode.py
echo "-------Fin de Proceso en mpi Python------"
