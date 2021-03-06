import numpy as np
import matplotlib.pyplot as plt
import sys
import time
sys.path.append('../../../../scripts/')
from fig_settings import configure_fig_settings
sys.path.append('../../scripts/')
from observabledata import ObservableData
import seaborn as sns

def func_f(x):
    
    x0 = 0
    y0 = 0.269
    x1 = 1.135
    y1 = 0.644

    return (y1-y0)/(x1-x0)*x+y0

def func_l(x):

    x0 = 0
    y0 = 0.119
    x1 = 1.135
    y1 = 0.029

    return (y1-y0)/(x1-x0)*x+y0

def func_g(x):

    x0 = 0.0
    y0 = 0.0357
    x1 = 1.135
    y1 = 0.0459

    return (y1-y0)/(x1-x0)*x+y0

if __name__ == "__main__":

    Lambda = 600.0
    omega = 20.0
    K33 = 30

    width=3.37
    height=width/1.5

    configure_fig_settings()

    colors = sns.color_palette()

    colors = [colors[0],colors[1]] 

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

    observables_list = ["gamma","E","R","eta","delta","psi(R)"]

    k24s = obsfwd.data[:,0]
    gammas = obsfwd.data[:,1]

    ts = (k24s-k24s[0])/k24s[0]

    xs = np.linspace(0,1.2,num=100,endpoint=True)


    # these two lines are just to normalize delta, as in the code its still delta_0 = sqrt(2/3)
    obsfwd.data[:,5] = obsfwd.data[:,5]/np.sqrt(2/3)
    obsbwd.data[:,5] = obsbwd.data[:,5]/np.sqrt(2/3)

    for i,observable in enumerate(observables_list):

        fig = plt.figure()
        fig.set_size_inches(width,height)

        ax = fig.add_subplot(1,1,1)
        print(observable)


        if i > 2:

            ylabel = f"\\{observable}"

        else:

            ylabel = observable

        if i == 0:

            ax.plot(ts,gammas,'.',color='k')
            #ax.plot(xs,func_g(xs),'-')
            ylabel="\\gamma"

        else:
            
            if observable == "psi(R)":

                linearlab = r"$\psi_{L}^*(R)$"
                frustlab = r"$\psi_{F}^*(R)$"

            else:

                linearlab = rf"${ylabel}_L^*$"
                frustlab = rf"${ylabel}_F^*$"

            ax.plot(ts,obsfwd.data[:,i+1],'^',color=colors[0],
                    label=linearlab,markersize=3)
            ax.plot(ts,obsbwd.data[:,i+1],'s',color=colors[1],
                    label=frustlab,markersize=3)

        if observable == "R":

            ax.set_yscale('log')
            #ax.plot(xs,func_l(xs),'-')
            #ax.plot(xs,func_f(xs),'-')

        ax.set_ylabel(rf"${ylabel}$",fontsize=10)
        ax.set_xlabel(r"$t$",fontsize=10)
        ax.legend(frameon=False,fontsize=10)
        fig.subplots_adjust(left=0.2,bottom=0.2)
        
        fig.savefig(obsfwd.observable_sname(f"{observable}_GAP"))

