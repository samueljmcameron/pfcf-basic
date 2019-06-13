#!/bin/bash
#SBATCH --time=04:00:00
#SBATCH --account=def-arutenbe
#SBATCH --array=0-500

module restore standard_modules

mkdir -p ../../../tmp_datapullbwd

python pullingbwd.py $SLURM_ARRAY_TASK_ID
