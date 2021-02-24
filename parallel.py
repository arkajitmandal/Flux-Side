#!/software/anaconda3/2020.02/bin/python
#SBATCH -p action 
#SBATCH -o my_output_%j
#SBATCH --mem-per-cpu=1GB
#SBATCH -t 1:00:00
#SBATCH -N 1
#SBATCH --ntasks-per-node=24

import sys
sys.path.append('/scratch/amandal4/QED-Ground/fs')
import main 
from multiprocessing import Pool
import time 
import numpy as np
from model import *

#-------- Parameters -----------
trajs = 10
ndof  = 12
#-------------------------------

par = param(int(ndof))
sbatch = [i for i in open('parallel.py',"r").readlines() if i[:10].find("#SBATCH") != -1 ]
nodes = int(sbatch[-1].split("=")[-1].replace("\n","")) 
cpu   = int(sbatch[-2].split()[-1].replace("\n",""))
print (f"nodes : {nodes} | cpu : {cpu}")
procs = cpu * nodes
print (f"Total trajectories {procs * trajs}")
ntraj = procs * trajs
par.traj = trajs
#---------- Run ----------------
with Pool(procs) as p:

    fs_  = p.map(main.run, [par for i in range(procs)])
    fs = np.zeros(fs_[0].shape, dtype = fs_[0].dtype)
    nSteps = fs.shape[0]
    for i in range(cpu):
        fs += fs_[i]
    fs /= ntraj
     
    np.savetxt("fs.txt",fs.T)
#-------------------------------
