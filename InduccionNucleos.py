def graficarInducciones(Ap_vector,Vi_max,Vo_n,n,D,Pmax,Gcc_min,k,J):

    import numpy as np
    import matplotlib.pyplot as plt
    import CorrienteMaxInductor

    PI=3.14159265


    aux = np.zeros((2,1),dtype=float)   #Vector auxiliar para almacenar salidas temporalmente

    plt.figure(figsize=[25,12])  #Define tamaño de grafica

    print("********************************************************")
    print("********* INDUCCIONES EN CONDICION MAS EXIGENTE ********")
    print("********************************************************\n")

    print("Inducciones en nucleos segun la frecuencia y parametro Area-Producto Ap.")
    print("La inductancia se ajusta al variar la frecuencia, manteniendo la potencia de diseño.\n")


    for j in (range(7)):    #Iteraciones por numero de graficas segun Ap variable

        Ap_var = Ap_vector[j]   #Inicializacion valor area producto segun vector

        aux = CorrienteMaxInductor.parametricasFrecuencia(Vi_max,Vo_n,n,D,Pmax,Gcc_min) #Definicion vectores a graficar
        x = aux[0]  #Almaceno valor de frecuencia
        IefL_max = aux[1]   #Almaceno valor de corriente maxima en inductor
        y = np.zeros((26,1),dtype=float)   #Vector para almacenar valores de induccion

        nuc_str=["E422120","E552821","E552825","E653227","E703332","E803820","E1306320"] # Nombres comerciales nucleos analizados
        print("Nucleo: \t",nuc_str[j],"\t\t\t\tAp = ", np.round_(Ap_var*1e12,0)," [mm4]")
        for i in (range(26)): # Se itera una vez por cada valor de frecuencia a graficar
            y[i] = np.round_(Vi_max*IefL_max[i]/(2*x[i]*J*k*Ap_var),4)  #Ecuacion de diseño segun parametro Ap y frecuencia almacenada en x[i]
            if(x[i]==25000):
                print(" f = 25 [kHz]\t\t\tL = ",np.round_((10**6)*aux[2][i],2)," [uHy]\t\t\t\tB = ",y[i]*1000," [mT]\t\t (B/Bsat)*100% = ",np.round_(y[i]*1000/3.2,1),"%")
            elif(x[i]==30000):
                print(" f = 30 [kHz]\t\t\tL = ",np.round_((10**6)*aux[2][i],2)," [uHy]\t\t\t\tB = ",y[i]*1000," [mT]\t\t (B/Bsat)*100% = ",np.round_(y[i]*1000/3.2,1),"%")
            elif(x[i]==35000):
                print(" f = 35 [kHz]\t\t\tL = ",np.round_((10**6)*aux[2][i],2)," [uHy]\t\t\t\tB = ",y[i]*1000," [mT]\t\t (B/Bsat)*100% = ",np.round_(y[i]*1000/3.2,1),"%")
            elif(x[i]==40000):
                print(" f = 40 [kHz]\t\t\tL = ",np.round_((10**6)*aux[2][i],2)," [uHy]\t\t\t\tB = ",y[i]*1000," [mT]\t\t (B/Bsat)*100% = ",np.round_(y[i]*1000/3.2,1),"%")

        if(j==0):
            plt.plot(x/1000,y*1000,'r^-',linewidth=2.0,label=r'$\ EE42/21/20'+'$')
        elif(j==1):
            plt.plot(x/1000,y*1000,'gs-',linewidth=2.0,label=r'$\ EE55/28/21'+'$')
        elif(j==2):
            plt.plot(x/1000,y*1000,'ro-',linewidth=2.0,label=r'$\ EE55/28/25'+'$')
        elif(j==3):
            plt.plot(x/1000,y*1000,'k^-',linewidth=2.0,label=r'$\ EE65/32/27'+'$')
        elif(j==4):
            plt.plot(x/1000,y*1000,'g^-',linewidth=2.0,label=r'$\ EE70/33/32'+'$')
        elif(j==5):
            plt.plot(x/1000,y*1000,'rs-',linewidth=2.0,label=r'$\ EE80/38/20'+'$')
        elif(j==6):
            plt.plot(x/1000,y*1000,'ko-',linewidth=2.0,label=r'$\ EE130/63/20'+'$')

    Bsat = np.zeros((26,1),dtype=float) #Vector para graficar induccion maxima de materiales mf102, CF139 y CF138
    for k in range(26):
        Bsat[k]=320 #Induccion de saturacion minima de 320mT en los 3 tipos de materiales

    plt.plot(x/1000,Bsat,'ks-',linewidth=4.0,label=r'$\ Bsat = '+str(320)+' [mT]'+'$') # Grafica de induccion de saturacion
    plt.legend()
    plt.grid(True)
  
    plt.xlabel('Frecuencia de Conmutacion [kHz]')
    plt.ylabel('Induccion magnetica [mT]')
    plt.show()

