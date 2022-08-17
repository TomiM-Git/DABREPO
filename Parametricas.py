def generarParametricas(Vi_n,Vo_n,n,D,L,fs,pts):

    import numpy as np
    import CalcularCtes
    import matplotlib.pyplot as plt

    PI=3.14159265

    D_var=0.001
    D_step=0.05

    fs_var=15e3
    fs_step=5e3

    plt.figure(figsize=[14,7])

    for j in (range(6)):
        x = np.zeros((11,1),dtype=float)
        y = np.zeros((11,1),dtype=float)
        for i in (range(11)):
            x[i] = D_var*180
            y[i] = CalcularCtes.calcSinPrint(Vi_n,Vo_n,n,D_var,L,fs_var)
            D_var = D_var+D_step
        if(j==0):
            plt.plot(x,y,'gs-',linewidth=2.0,label=r'$\ fs='+str(fs_var)+'$')
        elif(j==1):
            plt.plot(x,y,'ro-',linewidth=2.0,label=r'$\ fs='+str(fs_var)+'$')
        elif(j==2):
            plt.plot(x,y,'k^-',linewidth=2.0,label=r'$\ fs='+str(fs_var)+'$')
        elif(j==3):
            plt.plot(x,y,'g^-',linewidth=2.0,label=r'$\ fs='+str(fs_var)+'$')
        elif(j==4):
            plt.plot(x,y,'rs-',linewidth=2.0,label=r'$\ fs='+str(fs_var)+'$')
        elif(j==5):
            plt.plot(x,y,'ko-',linewidth=2.0,label=r'$\ fs='+str(fs_var)+'$')

        D_var=0.001
        fs_var=fs_var+fs_step
    plt.legend()
    plt.grid(True)
    #plt.xlim(0,len(rc0)-1)
    plt.xlabel('Desfase entre puentes')
    plt.ylabel('Corriente Eficaz Inductor')
    plt.show()

    print("Vector x = \n",x)
    print("Vector y = \n",y)