import numpy as np 
import os
#N = [1,10,20,30,40,50]#,60,70,80,90,100]
N = [1]
traj  = 5000
nfold = 20 
#os.system("rm -rf N-*")
for n in N:
    os.system("rm -rf N-%s"%(n))
    os.mkdir("N-%s"%(n)) 
    os.chdir("N-%s"%(n)) 
    for ifold in range(nfold):
        
        os.mkdir("f%s"%(ifold)) 
        os.chdir("f%s"%(ifold)) 
        os.system("cp ../../*.py ./")
        sb = open("submit.sbatch","w+")
        sb.writelines(open("../../submit.sbatch").readlines())
        sb.write("python3  main.py %s %s"%(n, traj/nfold))
        sb.close()
        os.system("sbatch submit.sbatch")
        os.chdir("../") 
    os.chdir("../") 