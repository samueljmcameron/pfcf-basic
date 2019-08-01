import numpy as np
import matplotlib.pyplot as plt
import sys
import time
sys.path.append('../../scripts/')
from observabledata import ObservableData
from psidata import PsiData
from scipy.integrate import simps





if __name__ == "__main__":

    Lambda = 600.0
    omega = 20.0
    K33 = 30

    scan = {}
    scan['\\Lambda'] = str(Lambda)
    scan['\\omega']= str(omega)
    scan['K_{33}'] = str(K33)
    scan['k_{24}'] = '0.5'
    scan['\\gamma_s'] = '0.04'

    loadsuf=["K_{33}","k_{24}","\\Lambda","\\omega","\\gamma_s"]
    savesuf = loadsuf

    data_path = "../../2019-04-29/psivsr-K33is30-tendon"

    loadfilepath = data_path + "/data"

    datfile = data_path + "/data/input.dat"

    q = 4/1000 # nm^{-1}


    types = ['linear','frustrated']

    for i,type in enumerate(types):

        psistuff = PsiData(scan=scan,loadsuf=loadsuf,savesuf=savesuf,name=f"psivsr_{type}",
                           loadfilepath=loadfilepath,datfile=datfile,sfile_format="pdf")

        rs = psistuff.r()/q
        psis = psistuff.psi()

        if type == 'frustrated':
            label= 'constant'
        else:
            label=type

        cospsi2 = simps(np.cos(psis)**2*rs,rs)*2/rs[-1]**2

        cospsi4 = simps(np.cos(psis)**4*rs,rs)*2/rs[-1]**2

        print(f"For {type}, cos^2psi = {cospsi2}, cos^4psi = {cospsi4}.")
