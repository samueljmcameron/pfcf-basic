#!/bin/bash
#SBATCH --time=20:00:00
#SBATCH --account=def-arutenbe
#SBATCH --output=slurmoutput/run_%A_%a.out
#SBATCH --array=0-40

module restore standard_modules

mkdir -p ../../../tmp_databwd

python scan2dbackward.py 600.0 20.0 $SLURM_ARRAY_TASK_ID
