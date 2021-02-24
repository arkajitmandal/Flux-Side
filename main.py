import numpy as np
from vv import *
from model import *
import sys
import copy
from numpy.random import normal as gran
import time



def run(param, output=False):
    ndof = param.ndof
    t = np.arange(0,param.t,param.dt) 
    xavg = np.zeros(len(t)) 
    fs = np.zeros(len(t)) 
    fs0 = 0.0
    for itraj in range(param.traj):   
        x = np.zeros(ndof)  
        p = np.zeros(ndof)

        
        
        # Eql
        """
        #--- Freeze 1 ------
        # 0 is cavity, 1 barrier, 2 to N is rest
        fr = np.ones((3))
        fr[1] = 0.0  
        #-------------------
        for ti in range(len(t)*10):
            x, p = vvl( x , p, param, fr)
        """
        # Sample
        x, p = init(param)
        p0   = p[1] 
        fs0 += (p0  > 0) * p0  

        print (f"Traj : {itraj} | p : {p[1]} | Time: {time.time()}")
        # MD
        for ti in range(len(t)):
            x, p = vvl( x , p, param)
            xavg[ti] += x[1] 
            fs[ti] += (x[1]>0) * p0



    xavg = xavg/param.traj
    fs = fs/(fs0 )
    if output:
        np.savetxt("x.txt",np.c_[t,xavg])
        np.savetxt("fs.txt",np.c_[t,fs])
    return fs



if __name__ == "__main__": 
    ndof = int(sys.argv[1])
    par = param(int(ndof))
    traj = int(sys.argv[2])
    par.traj = traj
    run(par, output=True)
