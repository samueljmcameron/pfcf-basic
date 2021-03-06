import numpy as np
import subprocess
import sys
import time
sys.path.append('../../scripts/')
from singlerun import SingleRun
from readparams import ReadParams

if __name__=="__main__":

    start_time = time.time()

    k24s = np.linspace(0.2,1,num=41,endpoint=True)
    
    FAILED_E = 1e300

    if len(sys.argv)<4:

        user_input = input("input string of a gamma,k24,omega values, "
                           "using comma as delimiter: ")
        Lambda,omega,k24 = user_input.split(',')

    else:

        Lambda,omega,k24 = sys.argv[1],sys.argv[2],str(k24s[int(sys.argv[3])])


    tmp_path = "../../../tmp_databwd/"
    datfile = "data/inputbwd.dat"


    gamma_0s = np.linspace(0.01,0.4,num=101,endpoint=True)

    if float(Lambda) < 5.0:
        Rguess = str(10)
        gammamax = 0.2206+1e-8
    elif float(Lambda) <20.0:
        Rguess = str(6)
        gammamax = 0.1504+1e-8
    else:
        Rguess = str(2.0)
        gammamax = 0.1075+1e-8
    
    i_max_gamma = np.argmax(gamma_0s[gamma_0s<gammamax])

    gammas = gamma_0s[:i_max_gamma+1]


    scan = {}
    scan['\\Lambda'] = Lambda
    scan['\\omega']= omega
    scan['k_{24}'] = k24
    scan['Rguess'] = Rguess
    scan['Rupper'] = str(1.1*float(Rguess))
    scan['Rlower'] = str(0.75*float(Rguess))
    
    loadsuf=["K_{33}","k_{24}","\\Lambda","\\omega","\\gamma_s"]
    savesuf=["K_{33}","k_{24}","\\Lambda","\\omega"]
    scan_dir = "scanbackward"

    i = len(gammas)-1
    while (i >=0):

        gamma = gammas[i]
        scan['\\gamma_s'] = str(gamma)

        # read in file name info
        rp = ReadParams(scan=scan,loadsuf=loadsuf,savesuf=savesuf,datfile=datfile)
        
        # create a class to do calculations with current parameters in scan.
        run = SingleRun(rp,scan_dir=scan_dir,tmp_path=tmp_path)

        # run C executable.
        run.run_exe()

        # move file written by C executable from temporary data path to true data path
        run.mv_file('observables')

        # load the final values of E, R, eta, delta, and surface twist.
        Ei,Ri,etai,deltai,surftwisti = run.get_all_observables('observables',str2float=True)
        

        if (Ei > 0.1*FAILED_E and gamma > 0.15):

            # if the energy calculation fails, this will be true.
            print('hi')
            # remove current file with observables for the current gamma value that are higher than
            # the delta = 0 energy.
            print(Ei)
            run.remove_file("observables")

            for j,gamma in enumerate(gammas[i::-1]):

                # write the remaining values of observables as those corresponding to the delta = 0
                # case, as non-zero d-band produces a higher energy fibril.
                scan['\\gamma_s']=str(gamma)
                rp = ReadParams(scan=scan,loadsuf=loadsuf,savesuf=savesuf)
                run = SingleRun(rp,scan_dir=scan_dir)
                run.write_observables(E0,R0,eta0,delta0,surftwist0,"\\gamma_s")

            break

        

        if (np.isnan(Ri) or Ri <= 0) and gamma > 0.15:

            # if Ri is infinite, then the calculation failed.
            # Retry it with a different initial guess.

            print("Ri is NAN, trying again with Rguess = 1.0")

            # remove the current observables file, so that a new one can be written.
            run.remove_file("observables")
            if abs(float(scan['Rguess'])-1.0)>1e-10:
                Ri = 1.0
            else:
                break

        else:
            # calculation ran smoothly.
            run.concatenate_observables("\\gamma_s")
            i -= 1
        
        Rguess,etaguess,deltaguess = str(Ri),str(etai),str(deltai)

        if not np.isnan(float(Rguess)):
            scan['Rguess'] = Rguess
            scan['Rupper'] = str(1.0*float(Rguess))
            scan['Rlower'] = str(0.75*float(Rguess))

        if not np.isnan(float(etaguess)):
            scan['etaguess'] = etaguess
            scan['etaupper'] = str(float(etaguess)+0.01)
            scan['etalower'] = str(np.max([float(etaguess)-0.02,2*np.pi]))

        if not (np.isnan(float(deltaguess))
                or abs(float(deltaguess))<1e-5):
            scan['deltaguess'] = deltaguess
            scan['deltaupper'] = str(np.sqrt(2/3))
            scan['deltalower'] = str(0.95*float(deltaguess))

    print(f"Took {(time.time()-start_time)/3600} hours to complete.")
