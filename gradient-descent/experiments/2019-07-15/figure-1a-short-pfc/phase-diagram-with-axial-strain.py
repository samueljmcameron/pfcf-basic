import numpy as np
import matplotlib.pyplot as plt
import sys
import time
sys.path.append('../../../../scripts/')
from fig_settings import configure_fig_settings
sys.path.append('../../scripts/')
from observabledata import ObservableData
from psidata import PsiData
from fibrilstrain import FibrilStrain
from phasediagram import PhaseDiagram
import seaborn as sns
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from midpointnormalize import MidpointNormalize
from mpl_toolkits.axes_grid1.colorbar import colorbar
from matplotlib.ticker import Formatter





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


    ax.pcolormesh(xs,ys,zz,cmap=cmap)

    ax.plot(gamma_coexists,k24_coexists,'-',color='k',
            lw=4)

    ax.plot(0.04,0.5,'*',color='w',markersize=8)
    ax.plot(gamma_coexists[0],k24_coexists[0],'o',color='k',
            markersize=8)


    ax.text(0.01,0.75,'linear\ntwist (L)',color='k',fontsize=10)
    ax.text(0.063,0.75,'constant\ntwist (C)',color='k',fontsize=10)

    ax.text(0.02,0.1,r'$(\gamma^c,k_{24}^c)$',fontsize=12)

    ax.set_xlabel(rf"$\gamma$",fontsize=10)
    ax.set_ylabel(r"$k_{24}$",fontsize=10)
    ax.set_xticks([0.02,0.04,0.06,0.08,0.1])

    ax.annotate("(a)",xy=(-0.3,1.1),xycoords="axes fraction")




    ##### now do the inset ####



    loadsuf=["K_{33}","k_{24}","\\Lambda","\\omega","\\gamma_s"]
    savesuf = loadsuf

    scan['k_{24}'] = '0.5'
    scan['\\gamma_s'] = '0.04'

    markertypes=['--','-.']

    q = 4/1000 # nm^{-1}

    norm = MidpointNormalize(midpoint=0)

    data_path = "../../2019-04-29/psivsr-K33is30-tendon"

    loadfilepath = data_path + "/data"

    datfile = data_path + "/data/input.dat"

    types = ['linear','frustrated']

    axins = {}

    axins['linear'] = fig.add_axes([0.25,0.45,0.1,0.1],projection='polar')

    axins['frustrated'] = fig.add_axes([0.5,0.37,0.25,0.25],projection='polar')

    for i,type in enumerate(types):


        psistuff = PsiData(scan=scan,loadsuf=loadsuf,savesuf=savesuf,name=f"psivsr_{type}",
                           loadfilepath=loadfilepath,datfile=datfile,sfile_format="pdf")

        observablestuff = ObservableData(scan=scan,loadsuf=loadsuf,savesuf=loadsuf,
                                         name=f"observables_{type}",loadfilepath=loadfilepath,
                                         datfile=datfile)

        R = observablestuff.R()



        fibrilstrain = FibrilStrain(psistuff,observablestuff,sfile_format='pdf')

        rs,thetas = fibrilstrain.mesh_polar(grid_skip=4)

        strains = fibrilstrain.strain_polar(rs,grid_skip=4)

        strain_percents = strains*100 # turn into percentage

        vmin,vmax = -0.3,0.1

        im = axins[type].contourf(thetas,rs,strain_percents,100,norm=norm,
                                 cmap='seismic',vmin=vmin,vmax=vmax)



        axins[type].set_xticks([])
        axins[type].set_yticks([])
        axins[type].spines['polar'].set_linewidth(0.2)
        axins[type].spines['polar'].set_linestyle((0,(2,8)))


        #axins[type].annotate(rf'$R={R:1.3f}$',xy=(5*np.pi/4,R-0.01*R),
        #                    xytext=(5*np.pi/4,R+R-0.01*R),fontsize=20,
        #                    color=colors[i])


    cax_ticks=[-0.3,-0.2,-0.1,0,0.1]

    cax = inset_axes(ax,width = "5%",height="99%",
                     loc='lower left',bbox_to_anchor=(1,0,1,1),
                     bbox_transform=ax.transAxes,borderpad=0.12)

    cbar = colorbar(im,ax=ax,cax=cax,format='%.1f',ticks=cax_ticks)

    cax.set_title("strain (\%)",fontsize=8)


    
    fig.subplots_adjust(left=0.2,right=0.8,bottom=0.2,top=0.8)
    #plt.show()
    fig.savefig(obsfwd.observable_sname(f"phase-diagram-with-axial-strain"))




    
