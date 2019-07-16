import numpy as np
import matplotlib.pyplot as plt
import sys
import time
sys.path.append('../../../../scripts/')
from fig_settings import configure_fig_settings
sys.path.append('../../scripts/')
from observabledata import ObservableData
from psidata import PsiData
from phasediagram import PhaseDiagram
import seaborn as sns
from matplotlib import cm
from matplotlib.colors import ListedColormap
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.ticker import AutoMinorLocator





if __name__ == "__main__":

    Lambda = 600.0
    omega = 20.0
    K33 = 30

    width=2.5
    height=width

    configure_fig_settings()

    colors = sns.color_palette()

    colors = [colors[2],colors[3]] 

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

    markertypes=['--','-.']

    q = 4/1000 # nm^{-1}


    fig = plt.figure()
    fig.set_size_inches(width,height)
    ax = fig.add_subplot(1,1,1)

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

        ax.plot(rs,psis,markertypes[i],label=f'{label} twist',lw=2)

        print("Radius = ",rs[-1], " nm.")
        
        print("surface twist = ",psis[-1]," rad.")

        ax.set_xlabel(r'$\tilde{r}$' + ' (' + r'$\si{\nano\meter}$' + ')',fontsize=10)
        ax.set_ylabel(r'$\psi(\tilde{r})$' + ' (' + r'$\si{\radian}$' + ')',fontsize=10)
        ax.set_xlim(0,120)
        ax.set_ylim(0,0.1)


    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.legend(frameon=False,loc='lower right',fontsize=10)
    ax.tick_params(which='minor',length=2)
    fig.subplots_adjust(left=0.23,right=0.83,bottom=0.2,top=0.8)
    plt.show()


    fig.savefig(psistuff.psivsr_sname(f"psi-vs-r"))




    
