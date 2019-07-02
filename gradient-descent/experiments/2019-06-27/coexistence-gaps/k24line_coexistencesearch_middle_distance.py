import numpy as np
import matplotlib.pyplot as plt
import sys
import time
sys.path.append('../../scripts/')
from singlerun import SingleRun
from readparams import ReadParams

Etol = 1e-8

def upper_Rguess(t):

    x0 = 0
    y0 = 0.269
    x1 = 1.135
    y1 = 0.644

    return (y1-y0)/(x1-x0)*t+y0

def lower_Rguess(t):

    x0 = 0
    y0 = 0.119
    x1 = 1.135
    y1 = 0.029

    return (y1-y0)/(x1-x0)*t+y0

def func_gamma(t):

    x0 = 0.0
    y0 = 0.0357
    x1 = 1.135
    y1 = 0.0459

    return (y1-y0)/(x1-x0)*t+y0


def single_E_calc(gamma,scan,loadsuf,savesuf,scan_dir):

    scan['\\gamma_s'] = str(gamma)

    k240 = 0.33

    k24 = float(scan['k_{24}'])

    t = (k24-k240)/k240

    if scan_dir == "scanforward":

        #Rguess0 = 0.045
        #Rupper0 = 0.6
        #Rlower0 = 0.4

        Rguess0 = lower_Rguess(t)
        Rupper0 = Rguess0*1.1
        Rlower0 = Rguess0*0.9

        etaguess0 = 6.295
        etalower0 = 6.29
        etaupper0 = 6.3

        deltaguess0 = 0.8
        deltalower0 = 0.799
        deltaupper0 = 0.805

    else:

        #Rguess0 = 0.7
        #Rupper0 = 0.9
        #Rlower0 = 0.6

        Rguess0 = upper_Rguess(t)
        Rupper0 = Rguess0*1.1
        Rlower0 = Rguess0*0.9

        etaguess0 = 6.34
        etalower0 = 6.32
        etaupper0 = 6.36

        deltaguess0 = 0.813
        deltalower0 = 0.808
        deltaupper0 = 0.816


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

    k240=0.33
    
    t = (k24-k240)/k240

    gamma0 = func_gamma(t)-0.0001#float(sys.argv[2])

    gamma2 = func_gamma(t)#float(sys.argv[3])

    dg = 0.0002


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
