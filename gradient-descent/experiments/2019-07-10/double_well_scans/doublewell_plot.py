import numpy as np
import matplotlib.pyplot as plt
import sys
import seaborn as sns
sys.path.append('../../../../scripts/')
from fig_settings import configure_fig_settings
sys.path.append('../../scripts/')
from doublewell import LoadDoubleWellData
from plotdoublewell import PlotDoubleWell


if __name__=="__main__":




    Lambda = 600.0
    omega = 20.0
    K33 = 30.0

    k24 = float(sys.argv[1])

    scan = {}

    scan['\\Lambda'] = str(Lambda)
    scan['\\omega'] = str(omega)
    scan['K_{33}'] = str(K33)

    scan['k_{24}'] = str(k24)


    loadsuf=["K_{33}","k_{24}","\\Lambda","\\omega"]

    data_path = "../../2019-06-27/coexistence-gaps"

    loadfilepath = data_path + "/data"

    datfile = data_path + "/data/input.dat"


    ldwd = LoadDoubleWellData(datfile=datfile,loadfilepath=loadfilepath,scan=scan,
                              loadsuf=loadsuf)


    scan=ldwd.params


    """
    # uncomment block for k24 = 0.2553 data


    scan['R0'] = str(1.99544378e-01)
    scan['R1'] = str(2.09709706e-01)
    scan['eta0'] = str(6.29330019e+00)
    scan['eta1'] = str(6.29375888e+00)
    scan['delta0'] = str(8.11429868e-01)
    scan['delta1'] = str(8.11705459e-01)

    """


    """
    scan['R0'] = str(1.97853576e-01)
    scan['R1'] = str(2.14754794e-01)
    scan['eta0'] = str(6.29322529e+00)
    scan['eta1'] = str(6.29398881e+00)
    scan['delta0'] = str(8.11380060e-01)
    scan['delta1'] = str(8.11834705e-01)
    scan['k_{24}'] = str(0.2555)
    scan['\\gamma_s'] = str(3.48827000e-02)
    """

    pdw = PlotDoubleWell(scan=scan);

    ts = pdw.data[:,0]

    Es = pdw.data[:,1]

    configure_fig_settings()
    
    fig,ax = plt.subplots()


    width = 3.37
    height = 3.37

    fig.set_size_inches(width,height)


    ax.plot(ts,Es,'.')


    ax.legend(frameon=False)
    ax.set_xlabel(r'$t$')
    ax.set_ylabel(r'$E$')

    ax.get_xaxis().set_ticks([0,1])
    fig.subplots_adjust(left=0.3,bottom=0.2)

    fig.savefig(pdw.sname("Evst"))

