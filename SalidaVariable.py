def graficarCorriente(Vi,Vo_min,Vo_max,n,D,L,fs,pts):

    import numpy as np
    import CalcularCtes
    import matplotlib.pyplot as plt

#    switch(MODO){
#        case 1:
#       
#            break
#        case 2:
#
#            break
#
#    }

    x = np.zeros((pts,1),dtype=float)
    y = np.zeros((pts,1),dtype=float)

    Vo_var=Vo_min
    step=(Vo_max-Vo_min)/(pts-1)

    for i in (range(pts)):
        x[i] = Vo_var
        y[i] = CalcularCtes.calcSinPrint(Vi,Vo_var,n,D,L,fs)
        Vo_var = Vo_var+step


    print("Vector x = \n",x)
    print("Vector y = \n",y)

    ### Generacion de las graficas
    plt.figure(figsize=[14,7])
    #plt.plot(t,rc0,'ro-',linewidth=2.0,label=r'$\phi=15$')
    plt.plot(x,y,'gs-',linewidth=2.0,label=r'$\phi=45$')
    #plt.plot(t,rc2,'k^-',linewidth=2.0,label=r'$\phi=75$')
    plt.legend()
    plt.grid(True)
    #plt.xlim(0,len(rc0)-1)
    plt.xlabel('Voltaje Salida')
    plt.ylabel('Corriente Inductor')

    plt.show()

    


#def graficarVectores():