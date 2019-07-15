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


    ##### now do the inset ####


    loadsuf=["K_{33}","k_{24}","\\Lambda","\\omega","\\gamma_s"]
    savesuf = loadsuf

    scan['k_{24}'] = '0.5'
    scan['\\gamma_s'] = '0.04'

    markertypes=['--','-.']

    q = 4/1000 # nm^{-1}

    data_path = "../../2019-04-29/psivsr-K33is30-tendon"

    loadfilepath = data_path + "/data"

    datfile = data_path + "/data/input.dat"

    axins = inset_axes(ax,width=width/3,height=height/3,loc=4,
                       bbox_to_anchor=(0.1,0.1,1,1),bbox_transform=ax.transAxes)

    types = ['linear','frustrated']

    for i,type in enumerate(types):

        psistuff = PsiData(scan=scan,loadsuf=loadsuf,savesuf=savesuf,name=f"psivsr_{type}",
                           loadfilepath=loadfilepath,datfile=datfile,sfile_format="pdf")

        rs = psistuff.r()/q
        psis = psistuff.psi()

        axins.plot(rs,psis,markertypes[i],label=f'{type} twist',lw=2)

        print("Radius = ",rs[-1], " nm.")
        
        print("surface twist = ",psis[-1]," rad.")

        axins.set_xlabel(r'$\tilde{r}$' + ' (' + r'$\si{\nano\meter}$' + ')',fontsize=8,labelpad=0.0)
        axins.set_ylabel(r'$\psi(\tilde{r})$' + ' (' + r'$\si{\radian}$' + ')',fontsize=8)
        axins.set_xlim(0,120)
        axins.set_ylim(0,0.1)

        axins.set_xticks([0,50,100])
        axins.set_yticks([0,0.05,0.1])
        axins.legend(frameon=False,fontsize=8)

    plt.show()
    fig.savefig(obsfwd.observable_sname(f"phase-diagram"))




    
