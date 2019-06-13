#!/bin/bash
#SBATCH --time=20:00:00
#SBATCH --account=def-arutenbe
#SBATCH --output=slurmoutput/run_%A_%a.out
#SBATCH --array=0-100

module restore standard_modules

mkdir -p ../../../tmp_datafwd

python scan2dforward.py 600.0 20.0 $SLURM_ARRAY_TASK_ID
