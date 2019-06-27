import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
import sys
import seaborn as sns
sys.path.append('../../../../scripts/')
from fig_settings import configure_fig_settings
sys.path.append('../../scripts/')
from observabledata import ObservableData
from gridmbyn import GridmByn
from readparams import ReadParams



configure_fig_settings()

observable_list = ['E','R','eta','delta','surfacetwist']

colors = sns.color_palette()

savesuf = ["K_{33}","k_{24}","\\Lambda","\\omega"]
loadsuf = ["K_{33}","k_{24}","\\Lambda","\\omega"]


k24s = np.linspace(0.2,1,num=41,endpoint=True)


Lambda = '600.0'
omega = '20.0'

scan = {}
scan['\\Lambda']=Lambda
scan['\\omega']=omega




# load in 2d grid of data in data2d for each observable at the
# specified gamma,k24 pair.
for i,k24 in enumerate(k24s):

    scan['k_{24}']=str(k24)

    obsbwd = ObservableData(["\\gamma_s"],scan_dir='scanbackward',scan=scan,
                            loadsuf=loadsuf,savesuf=savesuf,datfile='data/inputbwd.dat')

    obsbwd.data = obsbwd.data[np.argsort(obsbwd.data[:,0])]

    np.savetxt(obsbwd.observable_sname("observables_scanbackward",plot_format="txt"),obsbwd.data,
               fmt='\t'.join(["%15.8e"]*6))

