def parametricasFrecuencia(Vi_max,Vo_n,n,D,L):

    import numpy as np
    import CalcularCtes
    import matplotlib.pyplot as plt

    PI=3.14159265

    fs_var=10e3
    fs_step=1e3

    x = np.zeros((101,1),dtype=float)
    y = np.zeros((101,1),dtype=float)

    for i in (range(101)):
        x[i] = fs_var
        y[i] = (CalcularCtes.calcSinPrint(Vi_max,Vo_n,n,D,L,fs_var))[0]
        fs_var=fs_var+fs_step

#    plt.figure(figsize=[14,7])
#    plt.plot(x/1000,y,'gs-',linewidth=2.0,label=r'$\ fs='+str(fs_var)+'$')
#    plt.legend()
#    plt.grid(True)
#    plt.xlabel('Frecuencia de conmutacion [kHz]')
#    plt.ylabel('Corriente Eficaz Inductor [A]')
#    plt.show()
    print("Vector x = \n",x)
    print("Vector y = \n",y)
    return (x,y)

 #   print("Vector x = \n",x)
 #   print("Vector y = \n",y)