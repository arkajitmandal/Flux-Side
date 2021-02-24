#!/software/python3/3.8.3/bin/python3
#SBATCH -p action 
#SBATCH -o my_output_%j
#SBATCH --mem-per-cpu=1GB
#SBATCH -t 1:00:00
#SBATCH -N 2
#SBATCH --ntasks-per-node = 24

import sys
sys.path.append('/scratch/amandal4/QED-Ground/fs')
import main 
from multiprocessing import Pool
import time 
import numpy as np
from model import *


sbatch = [i for i in open('parallel.py',"r").readlines() if i[:10].find("#SBATCH") != -1 ]
nodes = int(sbatch[-1].split()[-1].replace("\n","")) 
cpu   = int(sbatch[-2].split()[-1].replace("\n",""))
print ("nodes, cpu :", nodes, cpu)