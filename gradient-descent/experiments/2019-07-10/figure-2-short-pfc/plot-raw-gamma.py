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

def func_gamma(k24,a,b):

    return a*(k24-b)

if __name__ == "__main__":

    p0 = (0.25,0.6)

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

    data_path = "../../2019-06-27/coexistence-gaps"

    loadfilepath = data_path + "/results"

    datfile = data_path + "/data/input.dat"


    obsfwd = ObservableData(name="fw_coexist",loadfilepath=loadfilepath,scan=scan,
                            loadsuf=loadsuf,savesuf=savesuf,datfile=datfile)
    obsbwd = ObservableData(name="bw_coexist",loadfilepath=loadfilepath,scan=scan,
                            loadsuf=loadsuf,savesuf=savesuf,datfile=datfile)

    observables_list = ["R"]

    k24s = obsfwd.data[:,0]

    gammas = obsbwd.data[:,1]

    gammas = gammas[k24s<0.35]

    k24s = k24s[k24s<0.35]

    x = np.linspace(k24s[0],k24s[-1],num=100,endpoint=True)

    popt,pcov = curve_fit(func_gamma,k24s,gammas)#,p0=p0)

    print(popt,pcov)

    fig = plt.figure()
    fig.set_size_inches(width,height)

    ax = fig.add_subplot(1,1,1)

    ax.plot(k24s,gammas,'.')

    ax.plot(x,func_gamma(x,*popt),'-',label=rf'$a=\num{{{popt[0]:.3e}}},\:b=\num{{{popt[1]:.3e}}}$')


    ax.set_ylabel(rf"$\gamma$",fontsize=10)
    ax.set_xlabel(r"$k_{24}$",fontsize=10)

    ax.legend(frameon=False,fontsize=10)
    fig.subplots_adjust(left=0.2,bottom=0.2)
    plt.show()   
    #fig.savefig(obsfwd.observable_sname(f"raw-delR"))




    
