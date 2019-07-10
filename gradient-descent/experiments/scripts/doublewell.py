import numpy as np
import subprocess
import sys
import os
from readparams import ReadParams
from observabledata import ObservableData

class DoubleWellRun(ReadParams):
    # perform a single run of calculation for psi(r), R, eta, ...

    # attributes:
    #  datfile - the data file that you read parameters from
    #  params  - an array that will have the string of parameters in it
    #  tmp_path - the path of where the output files are stored initially
    #  executable - the executable that creates and writes the output files
    
    def __init__(self,tmp_path="../../../tmp_data/",datfile="data/input.dat",scan={},
                 loadsuf=["K_{33}","k_{24}","\\Lambda",
                          "\\omega","\\gamma_s"],
                 savesuf=["K_{33}","k_{24}","\\Lambda",
                          "\\omega","\\gamma_s"],
                 name= "observables",loadfilepath="data",
                 params=None,executable="../../../bin/double_well_scan"):

        ReadParams.__init__(self,datfile=datfile,
                            scan=scan,loadsuf=loadsuf,savesuf=savesuf)

        self.tmp_path = tmp_path
        self.executable = executable

        return



    def run_exe(self,valgrind = False):
        # run c executable to determine psi(r), R, delta, etc.

        if valgrind:
            subprocess.run(['valgrind','--track-origins=yes',self.executable,self.tmp_path,
                            *self.params.values()],check=True)
        else:
            subprocess.run([self.executable,self.tmp_path,*self.params.values()],check=True)

        return


    def mv_file(self,mname,newname=None):
        # move a file from the temporary file folder to the data folder.
    
        suffix = self.write_suffix()


        fname = f"_{mname}_{suffix}.txt"

        mvfrom = f"{self.tmp_path}{fname}"

        if newname != None:
            newfname = f"_{newname}_{suffix}.txt"
        else:
            newfname = fname

        mvto = f"data/{newfname}"

        subprocess.run(["mv",mvfrom,mvto],check=True)

        return




class LoadDoubleWellData(ObservableData):

    def __init__(self,datfile="data/input.dat",scan = {},
                 loadsuf=["K_{33}","k_{24}","\\Lambda",
                          "\\omega","\\gamma_s"],
                 name="observables",loadfilepath="data"):

        ObservableData.__init__(self,datfile=datfile,scan=scan,loadsuf=loadsuf,
                                name='dummy',loadfilepath=loadfilepath)

        self.name = name

        self.double_well_set_scan()

    def load_data(self,s_dir):

        self.scan_dir = s_dir

        self.params = self.read_params()

        dum = np.loadtxt(self.observables_fname())

        if len(dum.shape)>1:

            data = dum[-1,:]

        else:
            data = dum

        return data

    def double_well_set_scan(self):

        d1 = self.load_data("scanforward")

        d2 = self.load_data("scanbackward")


        self.params['\\gamma_s'] = str(d1[0])
        self.params['R0'] = str(d1[2])
        self.params['R1'] = str(d2[2])
        self.params['eta0'] = str(d1[3])
        self.params['eta1'] = str(d2[3])
        self.params['delta0'] = str(d1[4])
        self.params['delta1'] = str(d2[4])

        return



# Everything below this line is deprecated!!!

################################################################################


class DoubleWell(object):
    # perform a single run of calculation for psi(r), R, eta, ...

    # attributes:
    #  datfile - the data file that you read parameters from
    #  params  - an array that will have the string of parameters in it
    #  tmp_path - the path of where the output files are stored initially
    #  executable - the executable that creates and writes the output files
    
    def __init__(self,readparams,tmp_path="../../../tmp_data/",
                 params=None,executable="../../../bin/double_well_scan"):

        self.readparams = readparams
        self.tmp_path = tmp_path
        self.executable = executable

        if (params == None):
            self.params = self.readparams.params
        else:
            self.params = params

        return



    def run_exe(self,valgrind = False):
        # run c executable to determine psi(r), R, delta, etc.

        if valgrind:
            subprocess.run(['valgrind','--track-origins=yes',self.executable,self.tmp_path,
                            *self.params.values()],check=True)
        else:
            subprocess.run([self.executable,self.tmp_path,*self.params.values()],check=True)

        return


    def write_suffix(self,p_list):
        
        suffix = '_'.join([f'{float(s):.4e}' for s in p_list])
        
        return suffix

    def mv_file(self,mname,newname=None):
        # move a file from the temporary file folder to the data folder.
    
        suffix = self.readparams.write_suffix()


        fname = f"_{mname}_{suffix}.txt"

        mvfrom = f"{self.tmp_path}{fname}"

        if newname != None:
            newfname = f"_{newname}_{suffix}.txt"
        else:
            newfname = fname

        mvto = f"data/{newfname}"

        subprocess.run(["mv",mvfrom,mvto],check=True)

        return

