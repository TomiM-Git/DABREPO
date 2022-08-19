def graficarCorriente(Vo_n,Vi_min,Vi_max,n,L,fs,pts):

    import numpy as np
    import CalcularCtes
    import matplotlib.pyplot as plt
    PI=3.14159265
    D_var=0.1
    D_step=0.1

    Vi_var=Vi_min
    Vi_step=(Vi_max-Vi_min)/(pts-1)

    ### Generacion de las graficas
    plt.figure(figsize=[14,7])
    for j in (range(5)):
        x = np.zeros((pts,1),dtype=float)
        y = np.zeros((pts,1),dtype=float)
        for i in (range(pts)):
            x[i] = Vi_var
            y[i] = (CalcularCtes.calcSinPrint(Vi_var,Vo_n,n,D_var,L,fs))[0]
            Vi_var = Vi_var+Vi_step
        if(j==0):
            plt.plot(x,y,'gs-',linewidth=2.0,label=r'$\phi='+str(D_var*180)+'$')
        elif(j==1):
            plt.plot(x,y,'ro-',linewidth=2.0,label=r'$\phi='+str(D_var*180)+'$')
        elif(j==2):
            plt.plot(x,y,'k^-',linewidth=2.0,label=r'$\phi='+str(D_var*180)+'$')
        elif(j==3):
            plt.plot(x,y,'g^-',linewidth=2.0,label=r'$\phi='+str(D_var*180)+'$')
        elif(j==4):
            plt.plot(x,y,'rs-',linewidth=2.0,label=r'$\phi='+str(D_var*180)+'$')
        elif(j==5):
            plt.plot(x,y,'ko-',linewidth=2.0,label=r'$\phi='+str(D_var*180)+'$')
        Vi_var=Vi_min
        D_var=D_var+D_step

    plt.legend()
    plt.grid(True)
    plt.xlabel('Voltaje Entrada [V]')
    plt.ylabel('Corriente Eficaz Inductor [A]')
    plt.show()
    print("Vector x = \n",x)
    print("Vector y = \n",y)
