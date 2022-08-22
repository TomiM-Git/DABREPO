def parametricasFrecuencia(Vi_max,Vo_n,n,D,L):

    import numpy as np
    import CalcularCtes
    import matplotlib.pyplot as plt

    PI=3.14159265

    fs_var=10e3     #Valor inicial de frecuencia a graficar
    fs_step=1e3     #Paso de iteracion para graficas

    x = np.zeros((101,1),dtype=float)   #Vector para almacenar frecuencias
    y = np.zeros((101,1),dtype=float)   #Vector para almacenar valor de corriente

    for i in (range(101)):  #Iteraciones para completar vectores
        x[i] = fs_var   #Guardo valor de frecuencia de la iteracion corriente
        y[i] = (CalcularCtes.calcSinPrint(Vi_max,Vo_n,n,D,L,fs_var))[0] #Calculo corriente y guardo en vector
        fs_var=fs_var+fs_step   #Actualizo valor de frecuencia para proxima iteracion

#    plt.figure(figsize=[14,7])
#    plt.plot(x/1000,y,'gs-',linewidth=2.0,label=r'$\ fs='+str(fs_var)+'$')
#    plt.legend()
#    plt.grid(True)
#    plt.xlabel('Frecuencia de conmutacion [kHz]')
#    plt.ylabel('Corriente Eficaz Inductor [A]')
#    plt.show()
    return (x,y)    #Devuelvo vectores (x,y) para utilizacion en funcion InduccionNucleos.graficarInducciones()

def graficarParametrica(Vi_max,Vo_n,n,D,L): #Funcion que realiza lo mismo, grafica pero no devuelve valores

    import numpy as np
    import CalcularCtes
    import matplotlib.pyplot as plt

    PI=3.14159265

    fs_var=10e3     #Valor inicial de frecuencia a graficar
    fs_step=1e3     #Paso de iteracion para graficas

    x = np.zeros((101,1),dtype=float)   #Vector para almacenar frecuencias
    y = np.zeros((101,1),dtype=float)   #Vector para almacenar valor de corriente

    for i in (range(101)):  #Iteraciones para completar vectores
        x[i] = fs_var   #Guardo valor de frecuencia de la iteracion corriente
        y[i] = (CalcularCtes.calcSinPrint(Vi_max,Vo_n,n,D,L,fs_var))[0] #Calculo corriente y guardo en vector
        fs_var=fs_var+fs_step   #Actualizo valor de frecuencia para proxima iteracion

    plt.figure(figsize=[14,7])
    plt.plot(x/1000,y,'gs-',linewidth=2.0,label=r'$\ fs='+str(fs_var)+'$')
    plt.legend()
    plt.grid(True)
    plt.xlabel('Frecuencia de conmutacion [kHz]')
    plt.ylabel('Corriente Eficaz Inductor [A]')
    plt.show()


