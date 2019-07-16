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





if __name__ == "__main__":

    Lambda = 600.0
    omega = 20.0
    K33 = 30

    width=3.37
    height=width

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


    k24_coexists = obsfwd.data[:,0]

    gamma_coexists = obsbwd.data[:,1]


    pd = PhaseDiagram(gamma_coexists,k24_coexists)

    cmap = pd.TwoColorMap()

    fig = plt.figure()
    fig.set_size_inches(width,height)

    ax = fig.add_subplot(1,1,1)

    xs = pd.gammas

    ys = pd.k24s

    zz = pd.zz_array()

    print(zz.min())

    ax.pcolormesh(xs,ys,zz,cmap=cmap)

    ax.plot(gamma_coexists,k24_coexists,'-',color='k',
            lw=4)

    ax.plot(0.04,0.5,'*',color='w',markersize=8)
    ax.plot(gamma_coexists[0],k24_coexists[0],'o',color='k',
            markersize=8)


    ax.text(0.01,0.8,'linear\ntwist',color='k',fontsize=12)
    ax.text(0.065,0.8,'constant\ntwist',color='k',fontsize=12)

    ax.text(0.025,0.15,r'$(\gamma^c,k_{24}^c)$',fontsize=12)

    ax.set_xlabel(rf"$\gamma$",fontsize=10)
    ax.set_ylabel(r"$k_{24}$",fontsize=10)



    ax.legend(frameon=False,fontsize=10)
    fig.subplots_adjust(left=0.2,bottom=0.2)



    fig.savefig(obsfwd.observable_sname(f"phase-diagram"))




    
