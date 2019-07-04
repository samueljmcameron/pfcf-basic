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
import matplotlib.patches as patches


def obs_finder(obs,observable,num_Lambdas):

    index = obs.ylabelstr_to_column(observable)
    datalength = len(obs.data[:,index])
    if datalength < num_Lambdas-1:
        dumarray = np.ones(num_Lambdas-datalength)*np.nan
        dataarray = np.concatenate((obs.data[:,index],dumarray))
    else:
        dataarray = obs.data[:num_Lambdas,index]

    return dataarray

def convert_to_NANS(eta_0s,dataarray):

    for i,eta in enumerate(eta_0s):

        if eta != eta:

            dataarray[i] = np.nan

    return dataarray

def mask_stuff(z,observable,gamma,k24):

    gamma = float(gamma)
    k24 = float(k24)

    mask = np.zeros_like(z,dtype = bool)

    

    mask[0:2,:] = True

    if observable != "delta" and observable != "E":

        mask[:,0:1] = True
        mask[:,600:] = True

    
    if observable == "delta":

        if np.isclose(k24,0.9):

            mask[0:5,100:] = True

    if observable == "R":
        
        if np.isclose(k24,0.9) and np.isclose(gamma,0.08):
            
            mask[:,100:300] = True


    elif observable == "eta":

        if np.isclose(k24,0.9) and np.isclose(gamma,0.08):
            
            mask[:,100:300] = True

        elif np.isclose(k24,0.5):


            if np.isclose(gamma,0.04):

                mask[:,800:] = True

            elif np.isclose(gamma,0.12):
            
                mask[:,6:8] = True


    elif observable == "surfacetwist":

        if np.isclose(k24,0.9):

            if np.isclose(gamma,0.08):
            
                mask[:,100:300] = True

            elif np.isclose(gamma,0.12):

                mask[:,20:35] = True
            
        elif np.isclose(k24,0.5):

            if np.isclose(gamma,0.08):

                mask[:,30:70] = True

            elif np.isclose(gamma,0.12):

                mask[:,5:10] = True
            
    return np.ma.array(z,mask=mask)

def cut_omega_index(gamma,k24):

    gamma = float(gamma)
    k24 = float(k24)

    if np.isclose(gamma,0.04):

        if np.isclose(k24,0.9):

            indx = 15

        elif np.isclose(k24,0.5):

            indx = 15

        elif np.isclose(k24,0.1):

            indx = 25

    elif np.isclose(gamma,0.08):

        if np.isclose(k24,0.9):

            indx = 15

        elif np.isclose(k24,0.5):

            indx = 20

        elif np.isclose(k24,0.1):

            indx = 15


    else:

        indx = 15

    return indx

def obs_lvls(observable,gamma,k24):

    gamma = float(gamma)
    k24 = float(k24)



    if observable == "E":

        lvls = energy_lvls(gamma,k24)

        fmt = '%.1lf'

    elif observable == "R":

        lvls = R_lvls(gamma,k24)

        fmt = '%.3lf'

    elif observable == "surfacetwist":


        lvls = surf_lvls(gamma,k24)

        fmt = '%.3lf'

    else:

        lvls = False

        fmt = '%.3lf'

    return lvls,fmt


def energy_lvls(gamma,k24):



    if np.isclose(k24,0.9):

        if np.isclose(gamma,0.04):

            levels = [(200,10),(200,20),(131,27)]

        elif np.isclose(gamma,0.12):

            levels = [(10,10),(10,20),(10,25)]

        else:

            levels = [(10,5),(10,20),(10,25)]


    elif  np.isclose(gamma,0.12):

        if not np.isclose(k24,0.9):

            levels = [(13,5),(13,20)]

    else:

        levels = [(10,5),(10,20),(10,25)]

    return levels

def R_lvls(gamma,k24):

    if np.isclose(gamma,0.04):

        if np.isclose(k24,0.9):

            levels = [(7,15),(50,15),(150,20)]

        else:

            levels = False

    else:

        levels = False

    return levels

def surf_lvls(gamma,k24):

    if np.isclose(gamma,0.04):

        if np.isclose(k24,0.9):

            levels = [(6,15),(50,15),(120,20),(400,15)]

        elif np.isclose(k24,0.5):

            levels = [(6,15),(22,15),(80,15),(400,15)]

        else:

            levels = False

    else:

        levels = False

    return levels

width  = 3.487
height = width

configure_fig_settings()

observable_list = ['E','R','eta','delta','surfacetwist']

observable_levels = {}

Lambda_yticks = {}

omega_yticks = {}

omega_ylims = {}

Lambda_xlims = {}

vmins = {}

vmaxs = {}

vmins['E'] = -5

vmins['R'] = 0.01

vmins['surfacetwist'] = 0.1

vmins['eta'] = 0.98

vmins['delta'] = 0.8

vmaxs['E'] = 0

vmaxs['R'] = 1.0

vmaxs['surfacetwist'] = 0.3

vmaxs['eta'] = 1.0

vmaxs['delta'] = 1.0


omega_ylims['E'] = Lambda_xlims['E'] = [-6,1]

omega_ylims['R'] = Lambda_xlims['R'] = [0.02,5]

omega_ylims['surfacetwist'] = Lambda_xlims['surfacetwist'] = [0,0.3]

omega_ylims['eta'] = Lambda_xlims['eta'] = [0.97,1.0]

omega_ylims['delta'] = Lambda_xlims['delta'] = [0.85,1.0]


observable_levels['E'] = np.array([-4,-3,-2,-1,0],float)

#observable_levels['R'] = np.array([0.01,0.05,0.1,1.0],float)

observable_levels['eta'] = np.array([0.97,0.98,0.99,1.0],float)

observable_levels['delta'] = np.array([0.87,0.9,0.93,0.95,0.99],float)

observable_levels['surfacetwist'] = np.array([0.1,0.15,0.2,0.25,0.3],float)

Lambda_yticks['surfacetwist'] = [0.05,0.15,0.25]

omega_yticks['surfacetwist'] = [0.05,0.15,0.25]

Lambda_yticks['delta'] = [0.9,0.95,1.0]

omega_yticks['delta'] = [0.9,0.95,1.0]

Lambda_yticks['eta'] = [0.98,0.99,1.0]

omega_yticks['eta'] = [0.98,0.99,1.0]

Lambda_yticks['R'] = [0.1,1.0]

omega_yticks['R'] = [0.1,1.0]

Lambda_yticks['E'] = [-5,-1,3]

omega_yticks['E'] = [-5,-1,3]


fig = {}
grid = {}

data2d = {}

colors = sns.color_palette()

savesuf = ["K_{33}"]
loadsuf = ["K_{33}","k_{24}","\\omega","\\gamma_s"]


num_Lambdas = max_Lambda = 1000
num_omegas = 30
Lambdas = np.linspace(1,max_Lambda,num=num_Lambdas,endpoint=True)
omegas = np.linspace(1,30,num=num_omegas,endpoint=True)

loadfilepath = "../../2019-02-05/omega-Lambda-space-K33is30/data"

datfile = loadfilepath + "/input.dat"

for observable in observable_list:
    
    fig[observable] = plt.figure()

    fig[observable].set_size_inches(3*width,3*height)

    grid[observable] = GridmByn(fig[observable])
    grid[observable].build_subplots_subgrid2x2(width_ratios=[3,1.2],
                                               hspace=0.1,wspace=0.1)

    data2d[observable]=np.empty([num_omegas,num_Lambdas],float)



for i,k24 in enumerate(['0.9','0.5','0.1']):

    for j,gamma in enumerate(['0.04','0.08','0.12']):

        print(f"gamma,k24 = {gamma},{k24}")
        scan = {}
        scan['\\gamma_s']=gamma
        scan['k_{24}']=k24



        # load in 2d grid of data in data2d for each observable at the
        # specified gamma,k24 pair.
        for om,omega in enumerate(omegas):

            scan['\\omega']=str(omega)

            obs = ObservableData(["\\Lambda"],scan=scan,scan_dir='scanforward',
                                 loadsuf=loadsuf,savesuf=savesuf,datfile=datfile,
                                 loadfilepath=loadfilepath)
            print(omega)

            eta_0s = obs_finder(obs,"eta",num_Lambdas)
            
            for observable in observable_list:
        
                dataarray = obs_finder(obs,observable,num_Lambdas)

                dataarray = convert_to_NANS(eta_0s,dataarray)
                    
                if observable == 'eta':
                    data2d[observable][om,:] = 2*np.pi/dataarray
                    if Lambdas[0] == 0.0:
                        data2d[observable][om,0] = np.nan
                elif observable == 'delta':
                    data2d[observable][om,:] = dataarray/np.sqrt(2/3)
                else:
                    data2d[observable][om,:] = dataarray



        xlabel = r'$\Lambda$'
        ylabel = r'$\omega$'



        for observable in observable_list:

            num_lvls = 3

            if observable == 'surfacetwist':
                plabel = r'$\psi(R)$'
            elif observable == 'eta':
                plabel = r'$2\pi/\eta$'
            elif observable == 'delta':
                plabel = r'$\delta$'
                num_lvls = 4
            elif len(observable) > 1:
                plabel = fr'$\{observable}$'
            else:
                plabel = fr'${observable}$'



            z = data2d[observable]
            energies = data2d['E']

            zmask = mask_stuff(z,observable,gamma,k24)


            cs = grid[observable].axarr[i][j]['main'].contourf(Lambdas,omegas,z,
                                                               vmin = vmins[observable],
                                                               vmax = vmaxs[observable])

            css = grid[observable].axarr[i][j]['main'].contour(Lambdas,omegas,zmask,
                                                               colors='r',levels=num_lvls)

            cssE = grid[observable].axarr[i][j]['main'].contour(Lambdas,omegas,energies,
                                                               [0],
                                                               colors='w')
            grid[observable].axarr[i][j]['main'].clabel(cssE,cssE.levels,inline=True,
                                                        manual = [(100,3)],
                                                        fmt={cssE.levels[0]:'E=0'})

            lvls,fmt = obs_lvls(observable,gamma,k24)

            grid[observable].axarr[i][j]['main'].clabel(css,fontsize=9,inline=1,
                                                        manual=lvls,fmt = fmt)


            indx =  cut_omega_index(gamma,k24)

            cutout_omega_at_x = data2d[observable][indx,:]

            cutout_Lambda_at_10 = data2d[observable][:,10]


            grid[observable].axarr[i][j]['slice_const_y'].plot(Lambdas,cutout_omega_at_x,'.',
                                                               color='orange')
            
            grid[observable].axarr[i][j]['slice_const_y'].set_yticks(Lambda_yticks[observable])

            grid[observable].axarr[i][j]['slice_const_y'].set_xlim(Lambdas[0],Lambdas[-1])
            grid[observable].axarr[i][j]['slice_const_y'].set_ylim(*omega_ylims[observable])
            if observable == 'R':
                grid[observable].axarr[i][j]['slice_const_y'].set_yscale('log')
                #labels = [tick.get_text() for tick in
                #          grid[observable].axarr[i][j]['slice_const_y'].get_yticklabels()]


            grid[observable].axarr[i][j]['main'].set_xscale('log')
            grid[observable].axarr[i][j]['main'].set_xticks([1,10,100,1000])
            grid[observable].axarr[i][j]['main'].get_xticklabels()[1].set_color("magenta")

            grid[observable].axarr[i][j]['slice_const_x'].plot(cutout_Lambda_at_10,omegas,'.',
                                      color='magenta')
            grid[observable].axarr[i][j]['slice_const_x'].set_xticks(omega_yticks[observable])
            grid[observable].axarr[i][j]['slice_const_x'].xaxis.tick_top()
            plt.setp(grid[observable].axarr[i][j]['slice_const_x'].get_yticklabels(),visible=False)
            grid[observable].axarr[i][j]['slice_const_x'].xaxis.set_label_position('top')

            grid[observable].axarr[i][j]['slice_const_x'].set_xlim(*Lambda_xlims[observable])
            grid[observable].axarr[i][j]['slice_const_x'].set_ylim(omegas[0],omegas[-1])
            if observable == 'R':
                grid[observable].axarr[i][j]['slice_const_x'].set_xscale('log')

            grid[observable].axarr[i][j]['slice_const_x'].set_xticklabels([])


            grid[observable].axarr[i][j]['main'].get_yticklabels()[indx//5].set_color("orange")

            xtick_sim = np.linspace(1,2,num=2,endpoint=True)
            ytick_sim = indx*np.ones([2],float)

            rect_omega = patches.Rectangle((0.8,indx-0.1),0.5,0.3,color="orange",
                                           clip_on=False,zorder=5)

            grid[observable].axarr[i][j]['main'].add_patch(rect_omega)

            rect_Lambda = patches.Rectangle((10-0.5,0),0.8,2,color="magenta",
                                           clip_on=False,zorder=5)

            grid[observable].axarr[i][j]['main'].add_patch(rect_Lambda)


            if i == 0:
                grid[observable].axarr[i][j]['slice_const_x'].set_xlabel(plabel)
            elif i == 2:
                grid[observable].axarr[i][j]['main'].set_xlabel(xlabel)
                grid[observable].axarr[i][j]['main'].annotate(rf'$\gamma={gamma}$',
                                                              xy=(0.7,-0.39),
                                                              xytext=(0.7,-0.4),
                                                              xycoords='axes fraction', 
                                                              ha='center',
                                                              va='center',
                                                              bbox=dict(boxstyle='square',
                                                                        fc='white'),
                                                              arrowprops=dict(arrowstyle='-[, widthB=9.5, lengthB=1.0', lw=2.0))
                                                              
            if j == 0:
                grid[observable].axarr[i][j]['main'].set_ylabel(ylabel)
                grid[observable].axarr[i][j]['slice_const_y'].set_ylabel(plabel)
                grid[observable].axarr[i][j]['main'].annotate(rf'$k_{{24}}={k24}$',
                                                              xy=(-0.49,0.7),
                                                              xytext=(-0.5,0.7),
                                                              xycoords='axes fraction', 
                                                              ha='center',
                                                              va='center',
                                                              bbox=dict(boxstyle='square',
                                                                        fc='white'),
                                                              arrowprops=dict(arrowstyle='-[, widthB=9.5, lengthB=1.0', lw=2.0))

            else:

                plt.setp(grid[observable].axarr[i][j]['slice_const_y'].get_yticklabels(),
                         visible=False)

for observable in observable_list:
    
    fig[observable].subplots_adjust(left=0.2,right=0.95)
    fig[observable].savefig(obs.observable_sname("LO_" + observable))

plt.show()



