def graficarInducciones(Ap_vector,Vi_max,Vo_n,n,D,L,k,J):

    import numpy as np
    import matplotlib.pyplot as plt
    import CorrienteMaxInductor

    PI=3.14159265

    aux = np.zeros((2,1),dtype=float)   #Vector auxiliar para almacenar salidas temporalmente

    plt.figure(figsize=[14,7])  #Define tamaño de grafica

    for j in (range(5)):    #Iteraciones por numero de graficas segun Ap variable

        Ap_var = Ap_vector[j]   #Inicializacion valor area producto segun vector

        aux = CorrienteMaxInductor.parametricasFrecuencia(Vi_max,Vo_n,n,D,L) #Definicion vectores a graficar
        x = aux[0]  #Almaceno valor de frecuencia
        IefL_max = aux[1]   #Almaceno valor de corriente maxima en inductor
        y = np.zeros((101,1),dtype=float)   #

        for i in (range(101)):
            y[i] = Vi_max*IefL_max[i]/(2*x[i]*J*k*Ap_var)

        if(j==0):
            plt.plot(x/1000,y,'gs-',linewidth=2.0,label=r'$\ Ap='+str(Ap_var)+'$')
        elif(j==1):
            plt.plot(x/1000,y,'ro-',linewidth=2.0,label=r'$\ Ap='+str(Ap_var)+'$')
        elif(j==2):
            plt.plot(x/1000,y,'k^-',linewidth=2.0,label=r'$\ Ap='+str(Ap_var)+'$')
        elif(j==3):
            plt.plot(x/1000,y,'g^-',linewidth=2.0,label=r'$\ Ap='+str(Ap_var)+'$')
        elif(j==4):
            plt.plot(x/1000,y,'rs-',linewidth=2.0,label=r'$\ Ap='+str(Ap_var)+'$')
        elif(j==5):
            plt.plot(x/1000,y,'ko-',linewidth=2.0,label=r'$\ Ap='+str(Ap_var)+'$')


    plt.legend()
    plt.grid(True)
  
    plt.xlabel('Frecuencia de Conmutacion [kHz]')
    plt.ylabel('Induccion magnetica [T]')
    plt.show()

#    print("Vector x = \n",x)
#    print("Vector y = \n",y)