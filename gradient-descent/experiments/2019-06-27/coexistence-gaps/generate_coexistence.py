import numpy as np
import matplotlib.pyplot as plt
import sys
import time
sys.path.append('../../scripts/')
from observabledata import ObservableData
from readparams import ReadParams
import seaborn as sns

if __name__ == "__main__":

    Lambda = 600
    omega = 20
    K33 = 30


    scan = {}
    scan['\\Lambda'] = str(Lambda)
    scan['\\omega']= str(omega)
    scan['K_{33}'] = str(K33)

    loadsuf=["K_{33}","k_{24}","\\Lambda","\\omega"]
    savesuf=["K_{33}","\\Lambda","\\omega"]

    k24s = np.array([0.2553,0.2554,0.2555,0.256,0.26,0.265,0.27,
                     0.28,0.29,0.3,0.31,0.33,0.34,0.35,0.36,0.37,0.375,0.38,0.385,0.4,0.45,
                     0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.0],float)

    
    
    for i,k24 in enumerate(k24s):

        scan['k_{24}'] = str(k24)

        obsfwd = ObservableData(scan_dir="scanforward",scan=scan,loadsuf=loadsuf,
                                savesuf=savesuf)
        obsbwd = ObservableData(scan_dir="scanbackward",scan=scan,loadsuf=loadsuf,
                                savesuf=savesuf)

        if i == 0:

            fw_coexist = np.empty([len(k24s),obsfwd.data.shape[-1]+1],float)
            bw_coexist = np.empty([len(k24s),obsbwd.data.shape[-1]+1],float)
            

        if len(obsfwd.data.shape)>1:
        
            dum1 = obsfwd.data[-1,:]

        else:

            dum1 = obsfwd.data

        if len(obsbwd.data.shape)>1:
        
            dum2 = obsbwd.data[-1,:]

        else:

            dum2 = obsbwd.data

        fw_coexist[i] = np.concatenate(([k24],dum1))

        bw_coexist[i] = np.concatenate(([k24],dum2))

        

    np.savetxt(obsfwd.observable_sname("fw_coexist",plot_format="txt"),fw_coexist,
               fmt='%15.8e')
    np.savetxt(obsbwd.observable_sname("bw_coexist",plot_format="txt"),bw_coexist,
               fmt='%15.8e')
