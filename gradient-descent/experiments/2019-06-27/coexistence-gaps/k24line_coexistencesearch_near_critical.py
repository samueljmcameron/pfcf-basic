import numpy as np
import matplotlib.pyplot as plt
import sys
import time
sys.path.append('../../scripts/')
from singlerun import SingleRun
from readparams import ReadParams

Etol = 1e-8

def gamma_guess(k24):

    a = 0.01951639
    b = -1.53152877

    g0 = a*(k24-b)

    return g0-1e-5,g0-5e-6

def single_E_calc(gamma,scan,loadsuf,savesuf,scan_dir):

    scan['\\gamma_s'] = str(gamma)

    if scan_dir == "scanforward":

        Rguess0 = 0.175
        Rupper0 = 0.18
        Rlower0 = 0.16

        etaguess0 = 6.292
        etalower0 = 6.291
        etaupper0 = 6.3

        deltaguess0 = 0.811
        deltalower0 = 0.808
        deltaupper0 = 0.812

    else:

        Rguess0 = 0.25
        Rupper0 = 0.26
        Rlower0 = 0.24

        etaguess0 = 6.294
        etalower0 = 6.293
        etaupper0 = 6.31

        deltaguess0 = 0.812
        deltalower0 = 0.810
        deltaupper0 = 0.814


    scan['Rguess'] = str(Rguess0)
    scan['Rupper'] = str(Rupper0)
    scan['Rlower'] = str(Rlower0)

    scan['etaguess'] = str(etaguess0)
    scan['etaupper'] = str(etaupper0)
    scan['etalower'] = str(etalower0)

    scan['deltaguess'] = str(deltaguess0)
    scan['deltaupper'] = str(deltaupper0)
    scan['deltalower'] = str(deltalower0)


    # read in file name info
    rp = ReadParams(scan=scan,loadsuf=loadsuf,savesuf=savesuf)

    # create a class to do calculations with current parameters in scan.
    run = SingleRun(rp,scan_dir=scan_dir)

    # run C executable.
    run.run_exe()

    # move file written by C executable from temporary data path to true data path
    run.mv_file('observables')

    # load the final values of E, R, eta, delta, and surface twist.
    Ei,Ri,etai,deltai,surftwisti = run.get_all_observables('observables',str2float=True)

    run.concatenate_observables(["\\gamma_s"])

    return Ei,Ri


if __name__ == "__main__":

    Lambda = 600.0
    omega = 20.0
    K33 = 30
    k24 = float(sys.argv[1])



    loadsuf=["K_{33}","k_{24}","\\Lambda","\\omega","\\gamma_s"]
    savesuf=["K_{33}","k_{24}","\\Lambda","\\omega"]



    scan = {}
    scan['\\Lambda'] = str(Lambda)
    scan['\\omega']= str(omega)
    scan['K_{33}'] = str(K33)
    scan['k_{24}'] = str(k24)


    start_time = time.time()

    gamma0 = float(sys.argv[2])

    gamma2 = float(sys.argv[3])

    #gamma0,gamma2 = gamma_guess(k24)

    dg = 0.00005


    Ef0,Rf0 = single_E_calc(gamma0,scan,loadsuf,savesuf,"scanforward")
    Eb0,Rb0 = single_E_calc(gamma0,scan,loadsuf,savesuf,"scanbackward")

    while (np.abs(Rf0-Rb0)<1e-5):

        gamma0 += dg

        print(f"loop 1, gamma0 = {gamma0}")

        Ef0,Rf0 = single_E_calc(gamma0,scan,loadsuf,savesuf,"scanforward")
        Eb0,Rb0 = single_E_calc(gamma0,scan,loadsuf,savesuf,"scanbackward")

        
    print("finished loop 1")

    if np.abs(Ef0-Eb0)<Etol:

        print("successfully found coexistence!")
        exit()

    elif Ef0>Eb0:
        
        print("lower bounding gamma is not small enough.")
        print("Coexistence point not bracketed from below.")
        print("exiting but FAILED!")

        exit()

    Ef2,Rf2 = single_E_calc(gamma2,scan,loadsuf,savesuf,"scanforward")
    Eb2,Rb2 = single_E_calc(gamma2,scan,loadsuf,savesuf,"scanbackward")



    while (np.abs(Rf2-Rb2)<1e-5):

        gamma2 -= dg

        print(f"loop 2, gamma2 = {gamma2}")

        Ef2,Rf2 = single_E_calc(gamma2,scan,loadsuf,savesuf,"scanforward")
        Eb2,Rb2 = single_E_calc(gamma2,scan,loadsuf,savesuf,"scanbackward")

    print("finished loop 2")

    if np.abs(Ef2-Eb2)<Etol:

        print("successfully found coexistence!")
        exit()

    elif Eb2>Ef2:

        print("upper bounding gamma is not big enough.")
        print("Coexistence point not bracketed from above.")
        print("exiting but FAILED!")

        exit()
        
    Ef1 = 1
    Eb1 = 1000

    while(np.abs(Ef1-Eb1)>Etol):

        gamma1 = 0.5*(gamma0+gamma2)

        Ef1,Rf1 = single_E_calc(gamma1,scan,loadsuf,savesuf,"scanforward")
        Eb1,Rb1 = single_E_calc(gamma1,scan,loadsuf,savesuf,"scanbackward")

        if Ef1<Eb1:

            Ef0 = Ef1
            Eb0 = Eb1

            gamma0 = gamma1

        else:

            Ef2 = Ef1
            Eb2 = Eb1

            gamma2 = gamma1


    print("successfully found coexistence!")
