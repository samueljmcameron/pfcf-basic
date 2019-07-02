import numpy as np
import matplotlib.pyplot as plt
import sys
import time
sys.path.append('../../../../scripts/')
from fig_settings import configure_fig_settings
sys.path.append('../../scripts/')
from observabledata import ObservableData
import seaborn as sns
from scipy.optimize import curve_fit

def func(x,a,b):

    return 0.5*np.log(x-a)+b

if __name__ == "__main__":

    Lambda = 600.0
    omega = 20.0
    K33 = 30

    width=3.37
    height=width/1.5

    configure_fig_settings()

    colors = sns.color_palette()

    colors = [colors[2],colors[3]] 

    scan = {}
    scan['\\Lambda'] = str(Lambda)
    scan['\\omega']= str(omega)
    scan['K_{33}'] = str(K33)

    loadsuf=["K_{33}","\\Lambda","\\omega"]
    savesuf=["K_{33}","\\Lambda","\\omega"]


    obsfwd = ObservableData(name="fw_coexist",loadfilepath="results",scan=scan,
                            loadsuf=loadsuf,savesuf=savesuf)
    obsbwd = ObservableData(name="bw_coexist",loadfilepath="results",scan=scan,
                            loadsuf=loadsuf,savesuf=savesuf)

    observables_list = ["E","R","eta","delta","psi(R)"]

    k24s = obsfwd.data[:,0]

    
    delR = (obsbwd.data[:,3]-obsfwd.data[:,3])

    ys = np.log(delR)

    popt,pcov = curve_fit(func,k24s,ys)



    fig = plt.figure()
    fig.set_size_inches(width,height)

    ax = fig.add_subplot(1,1,1)


    ax.set_ylabel(rf"$\Delta R$",fontsize=10)
    ax.set_xlabel(r"$k_{24}$",fontsize=10)

    ax.plot(k24s,delR,'.')
    ax.plot(k24s,np.exp(func(k24s,popt[0],popt[1])),'-')
    ax.plot(k24s,np.exp(func(k24s,0.3,-0.5)),'-')

    ax.legend(frameon=False,fontsize=10)
    fig.subplots_adjust(left=0.2,bottom=0.2)

    fig.savefig(obsfwd.observable_sname(f"delR-fit"))




    
