#!/bin/bash
#SBATCH --time=04:00:00
#SBATCH --account=def-arutenbe
#SBATCH --array=1,10-1000:10

module restore standard_modules


python pulling.py 0.04 0.1 $1 $SLURM_ARRAY_TASK_ID
