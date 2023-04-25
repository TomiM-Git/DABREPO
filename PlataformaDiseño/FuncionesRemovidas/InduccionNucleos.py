def graficarInducciones(Aw_vector,Ae_vector,Ap_vector,Vi_max,Vo_n,n,D,Pmax,Gcc_min,k,J):

    import numpy as np
    import matplotlib.pyplot as plt
    import CorrienteMaxInductor
    import math

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
        Ae_var = Ae_vector[j]
        Aw_var = Aw_vector[j]
        Np=Aw_var*0.75/(8.35*(1+n))
        nuc_str=["E422120","E552821","E552825","E653227","E703332","E803820","E1306320"] # Nombres comerciales nucleos analizados
        print("\n NUMERO ESPIRAS PRIMARIO SIN REDONDEAR PARA NUCLEO ",nuc_str[j],"\tNp = ",Np)
        Np=math.floor(Np)
        i=0
        while(((Np/3)-math.floor(Np/3)) != 0):
            Np=Np-1
            i=i+1
            print("\nIteracion Nro:",i,"\t Np = ",Np)
        print("\nNUMERO ESPIRAS FINAL \t Np = ",Np)
        aux = CorrienteMaxInductor.parametricasFrecuencia(Vi_max,Vo_n,n,D,Pmax,Gcc_min) #Definicion vectores a graficar
        x = aux[0]  #Almaceno valor de frecuencia
        IefL_max = aux[1]   #Almaceno valor de corriente maxima en inductor
        y = np.zeros((26,1),dtype=float)   #Vector para almacenar valores de induccion

        print("Nucleo: \t",nuc_str[j],"\t\t\t\tAp = ", np.round_(Ap_var*1e12,0)," [mm4]")
        for i in (range(26)): # Se itera una vez por cada valor de frecuencia a graficar
            #y[i] = np.round_(Vi_max*IefL_max[i]/(2*x[i]*J*k*Ap_var),4)  #Ecuacion de diseño segun parametro Ap y frecuencia almacenada en x[i]
            y[i] = np.round_(Vi_max/(4*Ae_var*x[i]*Np),4)
            if(x[i]==25000):
                print(" f = 25 [kHz]\t\t\tL = ",np.round_((10**6)*aux[2][i],2)," [uHy]\t\t\t\tB = ",y[i]*1000," [mT]\t\t (B/Bsat)*100% = ",np.round_(y[i]*1000/3.2,1),"%")
            elif(x[i]==30000):
                print(" f = 30 [kHz]\t\t\tL = ",np.round_((10**6)*aux[2][i],2)," [uHy]\t\t\t\tB = ",y[i]*1000," [mT]\t\t (B/Bsat)*100% = ",np.round_(y[i]*1000/3.2,1),"%")
            elif(x[i]==35000):
                print(" f = 35 [kHz]\t\t\tL = ",np.round_((10**6)*aux[2][i],2)," [uHy]\t\t\t\tB = ",y[i]*1000," [mT]\t\t (B/Bsat)*100% = ",np.round_(y[i]*1000/3.2,1),"%")
            elif(x[i]==40000):
                print(" f = 40 [kHz]\t\t\tL = ",np.round_((10**6)*aux[2][i],2)," [uHy]\t\t\t\tB = ",y[i]*1000," [mT]\t\t (B/Bsat)*100% = ",np.round_(y[i]*1000/3.2,1),"%")

        if(j==0):
            plt.plot(x/1000,y*1000,'bx-',linewidth=2.0,label=r'$\ EE42/21/20 : Ap = '+str(np.round_(Ap_var*1e12,0))+' [mm4]'+'$')
        elif(j==1):
            plt.plot(x/1000,y*1000,'go-',linewidth=2.0,label=r'$\ EE55/28/21 : Ap = '+str(np.round_(Ap_var*1e12,0))+' [mm4]'+'$')
        elif(j==2):
            plt.plot(x/1000,y*1000,'gx-',linewidth=2.0,label=r'$\ EE55/28/25 : Ap = '+str(np.round_(Ap_var*1e12,0))+' [mm4]'+'$')
        elif(j==3):
            plt.plot(x/1000,y*1000,'g^-',linewidth=2.0,label=r'$\ EE65/32/27 : Ap = '+str(np.round_(Ap_var*1e12,0))+' [mm4]'+'$')
        elif(j==4):
            plt.plot(x/1000,y*1000,'g.-',linewidth=2.0,label=r'$\ EE70/33/32 : Ap = '+str(np.round_(Ap_var*1e12,0))+' [mm4]'+'$')
        elif(j==5):
            plt.plot(x/1000,y*1000,'b.-',linewidth=2.0,label=r'$\ EE80/38/20 : Ap = '+str(np.round_(Ap_var*1e12,0))+' [mm4]'+'$')
        elif(j==6):
            plt.plot(x/1000,y*1000,'rx-',linewidth=2.0,label=r'$\ EE130/63/20 : Ap = '+str(np.round_(Ap_var*1e12,0))+' [mm4]'+'$')

    Bsat1 = np.zeros((26,1),dtype=float) #Vector para graficar induccion maxima de material mf102.
    Bsat2 = np.zeros((26,1),dtype=float) #Vector para graficar induccion maxima de materiales CF138
    Bsat3 = np.zeros((26,1),dtype=float) #Vector para graficar induccion maxima de materiales CF139

    for k in range(26):
        Bsat1[k]=320 #Induccion de saturacion minima de 320mT
        Bsat2[k]=380 #Induccion de saturacion minima de 380mT
        Bsat3[k]=390 #Induccion de saturacion minima de 390mT

    plt.plot(x/1000,Bsat1,'gs-',linewidth=4.0,label=r'$\ MF102 : Bsat = '+str(320)+' [mT]'+'$') # Grafica de induccion de saturacion
    plt.plot(x/1000,Bsat2,'rs-',linewidth=4.0,label=r'$\ CF138 : Bsat = '+str(380)+' [mT]'+'$') # Grafica de induccion de saturacion
    plt.plot(x/1000,Bsat3,'bs-',linewidth=4.0,label=r'$\ CF139 : Bsat = '+str(390)+' [mT]'+'$') # Grafica de induccion de saturacion
    plt.legend()
    plt.grid(True)
  
    plt.xlabel('Frecuencia de Conmutacion [kHz]')
    plt.ylabel('Induccion magnetica [mT]')
    plt.show()

