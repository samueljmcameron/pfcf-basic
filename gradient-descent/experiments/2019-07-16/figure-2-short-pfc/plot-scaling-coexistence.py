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

    Lambda = 600.0
    omega = 20.0
    K33 = 30

    width=2.8
    height=2.5

    configure_fig_settings()

    colors = sns.color_palette()



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

    observable = "R"#"E","R","eta","delta","psi(R)"]

    k24s = obsfwd.data[:,0]

    k24c = 0.2544
    print(f"gamma values closest to gamma_c are {obsfwd.data[0:2,1]}")

    ts = (k24s-k24c)/k24c

    # I am omitting the first data point as the double well scans at it show that it isn't
    # really a minimum.

    ts = ts[1:]

    print(ts)

    tcs = np.linspace(0.003,0.2,num=100,endpoint=True)

    fig = plt.figure()
    fig.set_size_inches(width,height)

    ax = fig.add_subplot(1,1,1)


    ylabel=observable

    Rlin = obsfwd.R(observables_num=7)[1:]

    Rfrust = obsbwd.R(observables_num=7)[1:]

    ax.plot(ts,Rfrust-Rlin,
            '^',color=colors[2],markersize=3)

    if observable != "E":

        ax.plot(tcs,y_scaling(tcs,0.5,0.25),'--',color='k',lw=1,
                label=r'$t^{\frac{1}{2}}$')

    #ax.set_xlim(0.002,8)
    ax.set_yscale('log')
    ax.set_xscale('log')

    linearlab = rf"{ylabel}_L^*"
    frustlab = rf"{ylabel}_C^*"

    ax.set_ylabel(rf"${frustlab}-{linearlab}$",fontsize=10,labelpad=2)
    ax.set_xlabel(r"$t$",fontsize=10)
    ax.set_ylim(top=5)

    fig.subplots_adjust(left=0.2,bottom=0.2)


    # now set inset

    axins = fig.add_axes([0.36,0.61,0.32,0.25])

    axins.plot(ts,Rfrust,'>',color=colors[1],label=rf"${frustlab}$",markersize=2)
    axins.plot(ts,Rlin,'s',color=colors[0],label=rf"${linearlab}$",markersize=2)


    axins.set_xticks([0,1,2,3])
    axins.set_ylim(0.02,8)


    #axins.set_xscale('log')
    axins.set_yscale('log')

    axins.tick_params(axis='x',labelsize=6,pad=0.3)
    axins.tick_params(axis='y',labelsize=6,pad=0)

    axins.set_xlabel(r"$t$",labelpad=-0.4)
    axins.set_ylabel(r"$R$",labelpad=0.0)
    axins.legend(frameon=False,loc='upper left',
                 fontsize=6,ncol=1,bbox_to_anchor=(-0.05,1.05),
                 borderpad=0.3,columnspacing=0.7,handletextpad=-0.1)


    ax.legend(frameon=False,loc='lower right',fontsize=10)


    fig.savefig(obsfwd.observable_sname(f"{observable}_SCALING"))





