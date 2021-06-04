import numpy as np
from vv import *
from model import *
import sys
import copy
from numpy.random import normal as gran
import time



def run(param, output=False):
    ndof = param.ndof
    t0 = time.time()
    t = np.arange(0,param.t,param.dt) 
    xavg = np.zeros(len(t)) 
    fs = np.zeros(len(t)) 
    fs0 = 0.0
    np.random.seed(param.SEED)
    print (f"ID: {param.ID}, SEED: {param.SEED}")
    for itraj in range(param.traj):   
        x = np.zeros(ndof)  
        p = np.zeros(ndof)

        # Sample
        x, p = init(param)
        p0   = p[1] 
        fs0 += (p0  > 0) * p0  
        
        
        # MD
        f1 = force(x, param)
        for ti in range(len(t)):
            x, p, f1 = vvl( x , p, param, f1)
            xavg[ti] += x[1] 
            fs[ti] += (x[1]>0) * p0



    xavg = xavg/param.traj
    fs = fs/(fs0 )
    if output:
        np.savetxt(f"x-{param.ID}.txt",np.c_[t,xavg])
        np.savetxt(f"fs-{param.ID}.txt",np.c_[t,fs])
    print (f"Time: {time.time()-t0}")
    return fs



if __name__ == "__main__": 
    ndof = int(sys.argv[1])
    par = param(int(ndof))
    traj = int(sys.argv[2])
    par.traj = traj
    run(par, output=True)
