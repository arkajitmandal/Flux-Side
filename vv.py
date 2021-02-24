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

def vvl(x, p, param, fr = "Default"):
    if fr == "Default":
        fr = np.ones(len(x))

    ß  = param.β
    f1 = model.force(x, param) 
    v = p/param.m
    dt = param.dt
    λ = param.λ / param.m
    σ = (2.0 * λ/(ß * param.m )) ** 0.5
    r1 = np.array([0.5 * gran() for i in range(len(x))])
    r2 = np.array([gran() * 0.28867513459  for i in range(len(x))])
    A = (0.5 * dt**2) * (f1/param.m - λ * v) + (σ * dt**(3.0/2.0)) * (r1+r2) 
    #---- X update -----------
    x += (v * dt + A) * fr
    #-------------------------
    f2 = model.force(x, param)
    #---- V update ----------- 
    v += ( 0.5 * dt * (f1+f2)/param.m - dt * λ * v + σ * dt * gran() - A * λ ) * fr
    #-------------------------
    return x, v * param.m

