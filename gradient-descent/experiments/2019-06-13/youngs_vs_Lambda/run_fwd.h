#!/bin/bash
#SBATCH --time=04:00:00
#SBATCH --account=def-arutenbe
#SBATCH --array=0-500

module restore standard_modules

mkdir -p ../../../tmp_datapullfwd

python pullingfwd.py $SLURM_ARRAY_TASK_ID
