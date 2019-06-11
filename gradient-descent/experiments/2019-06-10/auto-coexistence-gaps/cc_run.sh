#!/bin/bash
#SBATCH --time=09:00:00
#SBATCH --account=def-arutenbe

module restore standard_modules

python k24line_coexistencesearch_auto.py
