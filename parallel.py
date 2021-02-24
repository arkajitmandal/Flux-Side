#!/software/anaconda3/2020.02/bin/python
#SBATCH -p action 
#SBATCH -o my_output_%j
#SBATCH --mem-per-cpu=1GB
#SBATCH -t 1:00:00
#SBATCH -N 4
#SBATCH --ntasks-per-node=24

import sys
sys.path.append('/scratch/amandal4/QED-Ground/fs')
import main 
from multiprocessing import Pool
import time 
import numpy as np
from model import *

#-------- Parameters -----------
trajs = 40
ndof  = 12
#-------------------------------
t0 = time.time()

sbatch = [i for i in open('parallel.py',"r").readlines() if i[:10].find("#SBATCH") != -1 ]
cpu = int(sbatch[-1].split("=")[-1].replace("\n","")) 
nodes = int(sbatch[-2].split()[-1].replace("\n",""))
print (f"nodes : {nodes} | cpu : {cpu}")
procs = cpu * nodes
print (f"Total trajectories {procs * trajs}")
ntraj = procs * trajs

#---------- Run ----------------------------
with Pool(procs) as p:
    #------ Arguments for each CPU--------
    args = []
    for j in range(procs):
        par = param(int(ndof)) 
        par.traj = trajs
        par.ID   = j
        par.SEED   = np.random.randint(0,100000000)
        args.append(par)
    #-------------------------------------
    fs_  = p.map(main.run, args)

fs = np.zeros(fs_[0].shape, dtype = fs_[0].dtype)
nSteps = fs.shape[0]
for i in range(procs):
    fs += fs_[i]
fs /= procs
t =  np.arange(0,par.t,par.dt) 
np.savetxt("fs.txt",np.c_[t,fs])

print (f"Total Time: {time.time()-t0}")
#-------------------------------
