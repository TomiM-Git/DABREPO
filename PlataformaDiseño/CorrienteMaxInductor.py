def parametricasFrecuencia(Vi_max,Vo_n,n,D,Pmax,Gcc_min):

    import numpy as np
    import CalcularCtes
    import matplotlib.pyplot as plt

    PI=3.14159265

    fs_var=25e3     #Valor inicial de frecuencia a graficar
    fs_step=1e3     #Paso de iteracion para graficas

    x = np.zeros((26,1),dtype=float)   #Vector para almacenar frecuencias
    y = np.zeros((26,1),dtype=float)   #Vector para almacenar valor de corriente
    L_vec = np.zeros((26,1),dtype=float)

    for i in (range(26)):  #Iteraciones para completar vectores
        x[i] = fs_var   #Guardo valor de frecuencia de la iteracion corriente
        L_vec[i]= ((Vi_max)**2)*Gcc_min*D*(1-D)/(2*fs_var*Pmax)
#        print("\nVALOR L CON FRECUENCIA fs=",fs_var,"[Hz]    L = ",L)
        y[i] = 1.3*((CalcularCtes.calcSinPrint(Vi_max,Vo_n,n,D,L_vec[i],fs_var))[0]) #Calculo corriente y guardo en vector
        fs_var=fs_var+fs_step   #Actualizo valor de frecuencia para proxima iteracion

#    plt.figure(figsize=[14,7])
#    plt.plot(x/1000,y,'gs-',linewidth=2.0,label=r'$\ fs='+str(fs_var)+'$')
#    plt.legend()
#    plt.grid(True)
#    plt.xlabel('Frecuencia de conmutacion [kHz]')
#    plt.ylabel('Corriente Eficaz Inductor [A]')
#    plt.show()
    return (x,y,L_vec)    #Devuelvo vectores (x,y) para utilizacion en funcion InduccionNucleos.graficarInducciones()

def graficarParametrica(Vi_max,Vo_n,n,D,L): #Funcion que realiza lo mismo, grafica pero no devuelve valores

    import numpy as np
    import CalcularCtes
    import matplotlib.pyplot as plt

    PI=3.14159265

    fs_var=25e3     #Valor inicial de frecuencia a graficar
    fs_step=1e3     #Paso de iteracion para graficas

    x = np.zeros((26,1),dtype=float)   #Vector para almacenar frecuencias
    y = np.zeros((26,1),dtype=float)   #Vector para almacenar valor de corriente
    L_vec = np.zeros((26,1),dtype=float)

    for i in (range(26)):  #Iteraciones para completar vectores
        x[i] = fs_var   #Guardo valor de frecuencia de la iteracion corriente
        L_vec[i]= ((Vi_max)**2)*Gcc_min*D*(1-D)/(2*fs_var*Pmax)
#        print("\nVALOR L CON FRECUENCIA fs=",fs_var,"[Hz]    L = ",L)
        y[i] = (CalcularCtes.calcSinPrint(Vi_max,Vo_n,n,D,L_vec[i],fs_var))[0] #Calculo corriente y guardo en vector
        fs_var=fs_var+fs_step   #Actualizo valor de frecuencia para proxima iteracion

#    plt.figure(figsize=[14,7])
#    plt.plot(x/1000,y,'gs-',linewidth=2.0,label=r'$\ fs='+str(fs_var)+'$')
#    plt.legend()
#    plt.grid(True)
#    plt.xlabel('Frecuencia de conmutacion [kHz]')
#    plt.ylabel('Corriente Eficaz Inductor [A]')
#    plt.show()


