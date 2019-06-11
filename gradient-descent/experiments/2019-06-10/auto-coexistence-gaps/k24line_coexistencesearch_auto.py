import numpy as np
import matplotlib.pyplot as plt
import sys
import time
sys.path.append('../../scripts/')
from singlerun import SingleRun
from readparams import ReadParams

def single_E_calc(gamma,scan,scan_dir,fwd_ic,bwd_ic):

    loadsuf=["K_{33}","k_{24}","\\Lambda","\\omega","\\gamma_s"]
    savesuf=["K_{33}","k_{24}","\\Lambda","\\omega"]
    
    scan['\\gamma_s'] = str(gamma)

    ic_dict = {}

    if scan_dir=="scanforward":

        ic_dict = fwd_ic

    elif scan_dir=="scanbackward":

        ic_dict = bwd_ic

    scan['Rguess'] = str(ic_dict['Rguess0'])
    scan['Rupper'] = str(ic_dict['Rupper0'])
    scan['Rlower'] = str(ic_dict['Rlower0'])

    scan['etaguess'] = str(ic_dict['etaguess0'])
    scan['etaupper'] = str(ic_dict['etaupper0'])
    scan['etalower'] = str(ic_dict['etalower0'])

    scan['deltaguess'] = str(ic_dict['deltaguess0'])
    scan['deltaupper'] = str(ic_dict['deltaupper0'])
    scan['deltalower'] = str(ic_dict['deltalower0'])


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

    return Ei,Ri,etai,deltai

def set_fwd_ic(R0,eta0,delta0):

    fwd_ic = {}

    fwd_ic['Rguess0'] = R0*0.95
    fwd_ic['Rupper0'] = R0
    fwd_ic['Rlower0'] = R0*0.8

    fwd_ic['etaguess0'] = eta0
    fwd_ic['etaupper0'] = eta0*1.004
    fwd_ic['etalower0'] = np.min([6.29,eta0*0.9999])

    fwd_ic['deltaguess0'] = delta0*0.95
    fwd_ic['deltaupper0'] = delta0
    fwd_ic['deltalower0'] = np.min([0.79,delta0*0.94])
    
    return fwd_ic

def set_bwd_ic(R0,eta0,delta0):

    bwd_ic = {}
    
    bwd_ic['Rguess0'] = R0*1.005
    bwd_ic['Rupper0'] = R0*1.1
    bwd_ic['Rlower0'] = R0

    bwd_ic['etaguess0'] = eta0
    bwd_ic['etaupper0'] = eta0*1.004
    bwd_ic['etalower0'] = np.min([6.3,eta0*0.9999])

    bwd_ic['deltaguess0'] = delta0
    bwd_ic['deltaupper0'] = np.max([0.815,delta0*1.001])
    bwd_ic['deltalower0'] = np.min([0.807,delta0*0.9999])

    return bwd_ic

    

if __name__ == "__main__":

    Lambda = 27
    omega = 10
    K33 = 30

    scan = {}
    scan['\\Lambda'] = str(Lambda)
    scan['\\omega']= str(omega)
    scan['K_{33}'] = str(K33)


    E_tol = 1e-8
    R_tol = 1e-3

    
    Rf1 = 0.47
    etaf1 = 6.3206
    deltaf1 = 0.8069

    Rb1 = 0.515
    etab1 = 6.3234
    deltab1 = 0.80816

    gamma0 = 0.08356881

    gamma2 = 0.08356883

    k24s = np.array([0.4205],float)
    
    for k24 in k24s:

        print(f"k24 = {k24}.\n\n\n")

        scan['k_{24}'] = str(k24)
        
        fwd_ic = set_fwd_ic(Rf1,etaf1,deltaf1)
        bwd_ic = set_bwd_ic(Rb1,etab1,deltab1)

        start_time = time.time()

        dg = (gamma2-gamma0)/20.0

        Ef0,Rf0,etaf0,deltaf0 = single_E_calc(gamma0,scan,"scanforward",
                                              fwd_ic,bwd_ic)
        Eb0,Rb0,etab0,deltab0 = single_E_calc(gamma0,scan,"scanbackward",
                                              fwd_ic,bwd_ic)

        if (Rf0 > Rb1):

            Ef0 = Eb0 + 10

        while (Ef0>Eb0):

            Rf0 = Rb1 + 10
            
            while (Rf0 > Rb1):

                gamma0 -= dg*1.5
            
                Ef0,Rf0,etaf0,deltaf0 = single_E_calc(gamma0,scan,"scanforward",
                                                      fwd_ic,bwd_ic)

            Eb0,Rb0,etab0,deltab0 = single_E_calc(gamma0,scan,"scanbackward",
                                                  fwd_ic,bwd_ic)

            gamma2 = gamma0 + 1.5*dg

        while (np.abs(Rf0-Rb0)<R_tol):

            gamma0 += dg

            print(f"loop 1, gamma0 = {gamma0}")

            Ef0,Rf0,etaf0,deltaf0 = single_E_calc(gamma0,scan,"scanforward",
                                                  fwd_ic,bwd_ic)
            Eb0,Rb0,etab0,deltab0 = single_E_calc(gamma0,scan,"scanbackward",
                                                  fwd_ic,bwd_ic)


        print("finished loop 1")

        if np.abs(Ef0-Eb0)<E_tol:

            print("successfully found coexistence!")
            continue

        elif Ef0>Eb0:

            print("lower bounding gamma is not small enough.")
            print("Coexistence point not bracketed from below.")
            print("exiting but FAILED!")

            exit()

        Ef2,Rf2,etaf2,deltaf2 = single_E_calc(gamma2,scan,"scanforward",
                                              fwd_ic,bwd_ic)
        Eb2,Rb2,etab2,deltab2 = single_E_calc(gamma2,scan,"scanbackward",
                                              fwd_ic,bwd_ic)

        if Rb2 < Rf1:

            Eb2 = Ef2 + 10
        
        while (Eb2>Ef2):

            Rb2 = Rf1 - 10
        

            while (Rb2 < Rf1):

                gamma2 += dg*1.5

                Eb2,Rb2,etab2,deltab2 = single_E_calc(gamma2,scan,"scanbackward",
                                                      fwd_ic,bwd_ic)

            Ef2,Rf2,etaf2,deltaf2 = single_E_calc(gamma2,scan,"scanforward",
                                                  fwd_ic,bwd_ic)
            

        while (np.abs(Rf2-Rb2)<R_tol):

            gamma2 -= dg

            print(f"loop 2, gamma2 = {gamma2}")

            Ef2,Rf2,etaf2,deltaf2 = single_E_calc(gamma2,scan,"scanforward",
                                                  fwd_ic,bwd_ic)
            Eb2,Rb2,etab2,deltab2 = single_E_calc(gamma2,scan,"scanbackward",
                                                  fwd_ic,bwd_ic)

        print("finished loop 2")

        if np.abs(Ef2-Eb2)<E_tol:

            print("successfully found coexistence!")
            continue

        elif Eb2>Ef2:

            print("upper bounding gamma is not big enough.")
            print("Coexistence point not bracketed from above.")
            print("exiting but FAILED!")

            exit()

        Ef1 = 1
        Eb1 = 1000



        while(np.abs(Ef1-Eb1)>E_tol):

            gamma1 = 0.5*(gamma0+gamma2)

            Ef1,Rf1,etaf1,deltaf1 = single_E_calc(gamma1,scan,"scanforward",
                                                  fwd_ic,bwd_ic)
            Eb1,Rb1,etab1,deltab1 = single_E_calc(gamma1,scan,"scanbackward",
                                                  fwd_ic,bwd_ic)

            if Ef1<Eb1:

                Ef0 = Ef1
                Eb0 = Eb1

                gamma0 = gamma1
                
                zero_eq_1 = True

            else:

                Ef2 = Ef1
                Eb2 = Eb1

                gamma2 = gamma1

                zero_eq_1 = False


        print("successfully found coexistence!")

        if zero_eq_1:

            gamma2 = gamma1

            gamma0 = gamma1*(0.9998)

        else:

            gamma0 = gamma0*(0.9998)
            
            gamma2 = gamma1*(0.9998)
