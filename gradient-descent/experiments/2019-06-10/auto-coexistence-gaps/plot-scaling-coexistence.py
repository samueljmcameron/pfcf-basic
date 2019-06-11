import numpy as np
import matplotlib.pyplot as plt
import sys
import time
sys.path.append('../../../../scripts/')
from fig_settings import configure_fig_settings
sys.path.append('../../scripts/')
from observabledata import ObservableData
import seaborn as sns

def y_scaling(xs,alpha,yint):

    return yint*xs**alpha

if __name__ == "__main__":

    Lambda = 27
    omega = 10
    K33 = 30

    width=3.37
    height=width/1.5

    configure_fig_settings()

    colors = sns.color_palette()

    colors = [colors[1],colors[2]] 

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

    ts = (k24s-k24s[0])/k24s[0]

    tcs = np.linspace(0.002,0.1,num=100,endpoint=True)

    yints = np.array([0,2,0.8,0.8,0.8],float)

    # these two lines are just to normalize delta, as in the code its still delta_0 = sqrt(2/3)
    obsfwd.data[:,5] = obsfwd.data[:,5]/np.sqrt(2/3)
    obsbwd.data[:,5] = obsbwd.data[:,5]/np.sqrt(2/3)

    for i,observable in enumerate(observables_list):

        fig = plt.figure()
        fig.set_size_inches(width,height)

        ax = fig.add_subplot(1,1,1)
        print(observable)


        if i > 1:

            ylabel = f"\\{observable}"

        else:

            ylabel = observable

        ax.plot(ts,np.abs(obsbwd.data[:,i+2]-obsfwd.data[:,i+2]),
                '^',color=colors[0],markersize=3)

        if observable != "E":
            
            ax.plot(tcs,y_scaling(tcs,0.5,yints[i]),'--',color='k',lw=1,
                    label=r'$x^{\frac{1}{2}}$')
        
        ax.set_yscale('log')
        ax.set_xscale('log')

        ax.set_ylabel(rf"$\Delta {ylabel}$",fontsize=10)
        ax.set_xlabel(r"$t$",fontsize=10)

        ax.legend(frameon=False,fontsize=10)
        fig.subplots_adjust(left=0.2,bottom=0.2)
        
        fig.savefig(obsfwd.observable_sname(f"{observable}_SCALING"))




    
