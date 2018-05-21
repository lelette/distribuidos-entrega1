#!/bin/bash
#
#SBATCH --partition=all
#SBATCH --job-name=arguelles_jraiche
#SBATCH --time=1:00
#SBATCH --output=arguelles_jraiche.%j.out
#SBATCH --ntasks=12
#

echo "---------- Preparando el entorno -------------"
module purge
module load prun gnu7/7.3.0 openmpi3/3.0.0 py2-mpi4py/3.0.0

#Transferencia del libro a los discos locales de cada nodo
echo $(hostname)": Copiando archivo $WP/libro.txt a $LOCAL_HOME en los nodos $SLURM_NODELIST"


PDSH_SSH_ARGS_APPEN=D"-o StrictHostKeyChecking=no"
export LOCAL_HOME=/local_home/$USER
export WP=$(pwd)
pdsh -w $SLURM_NODELIST cp $WP/libro.txt $LOCAL_HOME

##################################################################
#    CORRIDA DEL CODIGO    #
echo "***** Inicio de Proceso MPI Arguelles y Jraiche *****"
prun thecode.py
echo "**      FIN DE LA MEJOR CORRIDA DEL MUNDO          **"


#Eliminar archivos locales de cada nodo >> libro!
echo $(hostname)": Eliminando archivo en los nodos $SLURM_NODELIST de la corrida"
PDSH_SSH_ARGS_APPEND="-o StrictHostKeyChecking=no"
pdsh -w $SLURM_NODELIST rm $LOCAL_HOME/libro.txt
