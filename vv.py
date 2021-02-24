import numpy as np 
import model
from numpy.random import normal as gran
def vv(x, p, param):
    f1 = model.force(x, param) 
    m = param.m 
    dt = param.dt
    v  = p/m 
    x += v * dt + 0.5 * (f1/m) * (dt ** 2)   
    f2 = model.force(x, param) 
    p += 0.5 * (f1 + f2) * dt 
    return x,p

def vvl(x, p, param, f1 = "DO" ):
    if f1=="DO":
        f1 = model.force(x, param)
    ndof = param.ndof
    ß  = param.β
    v = p/param.m
    dt = param.dt
    λ = param.λ #/ param.m
    σ = (2.0 * λ/(ß * param.m )) ** 0.5
    r1 = gran(0, 0.5, ndof)  #np.array([0.5 * gran() for i in range(len(x))])
    r2 = gran(0, 0.28867513459, ndof) #np.array([gran() * 0.28867513459  for i in range(len(x))])
    A = (0.5 * dt**2) * (f1/param.m - λ * v) + (σ * dt**(3.0/2.0)) * (r1+r2) 
    #---- X update -----------
    x += (v * dt + A) 
    #-------------------------
    f2 = model.force(x, param)
    #---- V update ----------- 
    v += ( 0.5 * dt * (f1+f2)/param.m - dt * λ * v +  gran(0, σ * dt, ndof) - A * λ ) 
    #-------------------------
    return x, v * param.m, f2

