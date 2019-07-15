# This file contains the class phase diagram for making a nice phase
# diagram of the linear and frustrated twist phases

import numpy as np
import seaborn as sns
from matplotlib import cm
from matplotlib.colors import ListedColormap


class PhaseDiagram(object):

    def __init__(self,gamma_coexists,k24_coexists,gamma_lower=0.001,gamma_upper=0.1,
                 gamma_num = 101,k24_lower=0,k24_upper=1,k24_num = 101,
                 lin_colors={'r':62,'g':137,'b':190,'a':256},
                 frust_colors={'r':256,'g':126,'b':13,'a':256}):

        self.gamma_coexists = gamma_coexists
        self.k24_coexists = k24_coexists
        self.gamma_lower = gamma_lower
        self.gamma_upper = gamma_upper
        self.gamma_num = gamma_num
        self.k24_lower = k24_lower
        self.k24_upper = k24_upper
        self.k24_num = k24_num
        self.gammas = np.linspace(self.gamma_lower,self.gamma_upper,
                                  num=self.gamma_num,endpoint=True)
        self.k24s = np.linspace(self.k24_lower,self.k24_upper,
                                num=self.k24_num,endpoint=True)

        self.k24_indx_nearest_critical = self.calc_k24_indx_nearest_critical()

        self.gamma_indx_nearest_critical = self.calc_gamma_indx_nearest_critical()

        self.lin_colors = lin_colors
        self.frust_colors = frust_colors

    def definitely_linear(self,gamma,k24):

        # if above the critical point and smaller than the smallest
        # gamma along the coexistence line, then it is definitely linear

        return (gamma < self.gamma_coexists[0] and
                k24 > self.k24_coexists[0])

    def definitely_frustrated(self,gamma,k24):

        # same argument as in definitely_linear above

        return (gamma > self.gamma_coexists[-1] and
                k24 > self.k24_coexists[0])

    def either_linear_or_frustrated(self,k24):

        # if above the critical point but the above two functions don't
        # work

        return k24 > self.k24_coexists[0]

    def close_to_linear(self,gamma):

        # if below the critical point, but on the linear side of it

        return gamma < self.gamma_coexists[0]

    """
    def find_gamma_coexists_index(self,k24):

        # if 

        index = -1

        distance = 1000

        for i,x in enumerate(self.k24_coexists):

            if np.abs(k24-x)<distance:

                distance = np.abs(k24-x)

                index = i

        return index
    """

    def gamma_coexist_at_this_k24(self,k24):

        g_i = np.abs(self.k24_coexists-k24).argmin()

        return self.gamma_coexists[g_i]


    def calc_k24_indx_nearest_critical(self):

        k24_i = np.abs(self.k24s-self.k24_coexists[0]).argmin()

        return k24_i

    def calc_gamma_indx_nearest_critical(self):

        gamma_i = np.abs(self.gammas-self.gamma_coexists[0]).argmin()

        return gamma_i

    def blur_width(self,k24_i):

        return self.k24_indx_nearest_critical-k24_i


    def apply_blur(self,gamma_j,k24_i):

        return (self.gamma_indx_nearest_critical-gamma_j
                <3*self.blur_width(k24_i)/4
                and
                gamma_j-self.gamma_indx_nearest_critical
                <self.blur_width(k24_i)/4)

    def blur(self,gamma_j,k24_i):

        bw = self.blur_width(k24_i)

        mid = self.gamma_indx_nearest_critical

        x0 = mid-3*bw/4

        xf = mid+bw/4

        m = 1/(xf-x0)

        x = gamma_j

        if x<x0:

            print(gamma_j,mid,bw/2,m)
            print(m*(x-x0))
        return m*(x-x0)

        


    def zz_array(self):

        zz = np.empty([len(self.k24s),len(self.gammas)],float)

        for i,k24 in enumerate(self.k24s):

            for j,gamma in enumerate(self.gammas):


                if self.definitely_linear(gamma,k24):

                    zz[i,j] = 0

                elif self.definitely_frustrated(gamma,k24):

                    zz[i,j] = 1


                elif self.either_linear_or_frustrated(k24):

                    if gamma >self.gamma_coexist_at_this_k24(k24):

                        zz[i,j] = 1

                    else:

                        zz[i,j] = 0

                else:

                    if self.apply_blur(j,i):

                        zz[i,j] = self.blur(j,i)

                    elif self.close_to_linear(gamma):

                        zz[i,j] = 0

                    else:

                        zz[i,j] = 1

        return zz



    def transition(self):

        a_len = 254

        rs = np.linspace(self.lin_colors['r']/256,self.frust_colors['r']/256,
                         num=a_len,endpoint=True)

        gs = np.linspace(self.lin_colors['g']/256,self.frust_colors['g']/256,
                         num=a_len,endpoint=True)

        bs = np.linspace(self.lin_colors['b']/256,self.frust_colors['b']/256,
                         num=a_len,endpoint=True)
        
        array = np.empty([4,a_len],float)

        array[0] = rs
        array[1] = gs
        array[2] = bs
        array[3] = np.ones(a_len)

        return array.T


    def TwoColorMap(self):


        viridis = cm.get_cmap('viridis',256)

        newcolors = viridis(np.linspace(0,1,256))

        color_lin = np.array(list(self.lin_colors.values()),float)/256

        color_frust = np.array(list(self.frust_colors.values()),float)/256

        newcolors[0,:] = color_lin

        newcolors[1:255,:] = self.transition()

        newcolors[255,:] = color_frust

        return ListedColormap(newcolors)
