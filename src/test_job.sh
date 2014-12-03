#!/bin/bash

#PBS -t 1-500%45
#PBS -l walltime=120:00:00 
#PBS -l nodes=1:ppn=1
#PBS -j oe

echo "SAMPLE_LEVEL:$SAMPLE_LEVEL"