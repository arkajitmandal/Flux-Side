import numpy as np
from numpy import sum  
from numpy.random import normal as gran
def µ(x):
    a = 0.496646
    b = 2.25715 
    return (a * x - b * np.tanh(x))

def dµ(x):
    a = 0.496646
    b = 2.25715 
    return (a - (b/np.cosh(x)**2))
 

def dV(x, param):
    ωc = param.ωc
    χ = param.χ
    dv = np.zeros(len(x))
    c = χ * (2.0 /ωc**3.0)**0.5
    #-----------------------------------------------------------------!
    # Nuclear DOFs ---------------------------------------------------!
    #-----------------------------------------------------------------!
    dv[1:]  =  dE(x[1:]) # Molecular part
    dv[1:] +=  (ωc**2.0) * ( x[0] + c * sum(µ(x[1:])) ) * c * dµ(x[1:]) 
    #-----------------------------------------------------------------!
    # Cavity DOFs ----------------------------------------------------!
    #-----------------------------------------------------------------!
    dv[0]   =  (ωc**2.0) * ( x[0] + c * sum(µ(x[1:])) ) 
    #-----------------------------------------------------------------!
    #print(c)
    return dv

def force(x, param):
    return -1.0 * dV(x, param)

def E(R):
    a = 0.00328951 #/10.0
    b = -0.0210145 #/10.0
    return a*(R**4) + b*(R**2) #+ c * R

def dE(R):
    a = 0.00328951 #/10.0
    b = -0.0210145 #/10.0
    return 4.0 * a * (R**3) + 2.0 * b * R #+ c * R

def ddE(R):
    a = 0.00328951 #/10.0
    b = -0.0210145 #/10.0
    return 12.0 * a * (R**2) + 2.0 * b  #+ c * R

def init(param):
    m = param.m
    β = param.β
    ndof = param.ndof
    ωc = param.ωc
    χ = param.χ
    ω = np.zeros((ndof))
    ω[0] = param.ωc
    # find minima --------------------
    xGrid = np.linspace(-2,-1.5,1000)
    x0 = xGrid[np.argmin(E(xGrid))]
    #--------------------------
    ω[1:] = (ddE(np.ones(ndof-1) * x0)/m[1:])**0.5 
    σx = (1/ (β * m * ω**2.0) ) ** 0.5
    σp = (m/β)**0.5 
    #-------- Nuclear DOF ----------
    x = gran(x0, σx, ndof)
    x[1]  = 0.0
    #-------- cavity DOF -----------
    c = χ * (2.0 /ωc**3.0)**0.5
    x[0] = gran(-sum(µ(x[1:])) * c, σx[0])
    #-------------------------------
    p =  gran(0,σp,ndof)
    return x, p

class param:
    def __init__(self,ndof=3):
        self.ndof = ndof
        self.T = 298.0
        self.β = 315774/self.T  
        self.m = np.ones(ndof) 
        self.m[1:] *= 1836.0 # protons
        self.t = 8400
        self.dt = 1.0
        self.ωc = 0.06/27.2114
        self.χ  = self.ωc * 0.0
        self.λ = np.zeros(ndof)   
        self.λ[1] = 0.1/27.2114
        self.traj = 1
