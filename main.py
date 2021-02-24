import numpy as np
from vv import *
from model import *
import sys
import copy
from numpy.random import normal as gran

global ndof
ndof = int(sys.argv[1])
par = param(int(ndof))
traj = int(sys.argv[2])

def run(param):
    t = np.arange(0,param.t,param.dt) 
    xf = np.zeros(len(t)) 
    xb = np.zeros(len(t)) 
    fs = np.zeros(len(t)) 
    fs0 = 0.0
    for itraj in range(traj):   
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

        # MD
        for ti in range(len(t)):
            x, p = vvl( x , p, param)
            xf[ti] += x[1] 
            xb[ti] += x[1] 
            fs[ti] += (x[1]>0) * p0


    xf = xf/traj
    xb = xb/traj
    fs = fs/(fs0 )
    np.savetxt("x.txt",np.c_[t,xf,xb])
    np.savetxt("fs.txt",np.c_[t,fs])




run(par)
