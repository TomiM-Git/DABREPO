def generarParametricas(Vi,n,L,Rl1,Rl2):
    import numpy as np
    import CalcularVo
    import matplotlib.pyplot as plt
    #Vector con frecuencias programadas al medir los datos experimentales.
    fs_vec=[16e3,20e3,25e3,29e3,31e3,33e3,37e3,40e3,44e3]
    #Vectores con datos experimentales para trazado de curvas paramétricas.
    Vo_40ohm_50 = [12.6,9.5,12.1,8,7.9,7.7,7.3,7.1,6.9]
    Vo_40ohm_100 = [19.8,17.1,16.5,11.6,13.6,11.3,10.3,10,10.5]
    Vo_40ohm_200 = [24.3,22.7,20,16.9,17.2,16.2,14.2,13.6,13.1]
    Vo_80ohm_50 = [19.4,14.1,19.7,14.6,14.5,14.3,13.9,13.6,13.5]
    Vo_80ohm_100 = [27,25.8,25.9,19.3,23.4,19.3,18.3,18.1,18.4]
    Vo_80ohm_200 =[33.1,31.3,29.7,27,27.5,26.6,22.6,22,23.7]
    # Vectores para trazado de rectas de tendencia.
    minSQ_frecs = [16,44]           #Mínima y máxima frecuencia del barrido.
    minSQ_40ohm_50 = [11.7,6.1]  
    minSQ_40ohm_100= [18.7,8.62]    #Dos puntos pertenecientes a la recta de tendencia.
    minSQ_40ohm_200= [23.8,11.9]
    minSQ_80ohm_50 = [17.9,12.8]
    minSQ_80ohm_100= [27,16.8]      #Dos puntos pertenecientes a la recta de tendencia.
    minSQ_80ohm_200= [32.9,21.7]
    # Vector para trazado de recta horizontal Vi para referencia visual elevador/reductor.
    Vi_ref=[Vi,Vi]

    fig= plt.figure(figsize=[17,10])
    for x in range(2):  # Bucle para la realizacion de 2 gráficas.
        D_var=0.1   #Inicializa desfase proporcional entre puentes.
        if(x==0):
            ax1=fig.add_subplot(2,2,(1,3))  #Dimensión de subploteo 1.
            ax=ax1      #Sobreescribo variable de subploteo.
            Rl=Rl1      #Sobreescribo variable de resistencia de carga.
            major_ticks_Vo=np.arange(0,112,4)    #Graficar de 0V a 80V cada 5V.
            #Agrego gráfico de recta horizontal con tensión de entrada para referencia.
            plt.plot(minSQ_frecs,Vi_ref,'ko-',linewidth=2.0,label="Entrada: Vi = "+str(Vi)+"[V]")
        else:
            ax2=fig.add_subplot(2,2,(2,4))  #Dimensión de subploteo 2.
            ax=ax2      #Sobreescribo variable de subploteo.
            Rl=Rl2      #Sobreescribo variable de resistencia de carga.
            major_ticks_Vo=np.arange(0,56,2)    #Graficar de 0V a 36V cada 2V.
            #Agrego gráfico de recta horizontal con tensión de entrada para referencia.
            plt.plot(minSQ_frecs,Vi_ref,'ko-',linewidth=2.0,label="Entrada: Vi = "+str(Vi)+"[V]")
        for j in (range(3)):
            x = np.zeros((9,1),dtype=float) #Vector para frecuencias.
            y = np.zeros((9,1),dtype=float) #Vector para tensiones de salida.
            for i in (range(len(fs_vec))):
                x[i] = fs_vec[i]/1000       #Ingreso frecuencia en kHz.
                y[i] = CalcularVo.calcSinPrint(Vi,n,D_var,L,fs_vec[i],Rl) #Cálculo auxiliar tensión de salida.
            if(j==0):   #Cada j corresponde a un incremento en la variable D_var.
                #En cada bloque se grafica primero el caso obtenido de las ecuaciones teóricas (Ideal).
                plt.plot(x,y,'b^-',linewidth=2.0,label="Curva teórica: \u03A6= "+str(D_var*180)+"°")
                if(Rl==Rl1):#Se ejecuta para el gráfico que corresponda segun que resistencia sobreescribio a Rl.
                    #Luego se grafican los datos experimentales (Reales), segun el vector que corresponda.
                    plt.plot(x,Vo_80ohm_50,'bo-',linewidth=2.0,label="Datos reales: \u03A6= "+str(D_var*180)+"°")
                    #Finalmente se grafica la recta de tendencia de los datos experimentales.
                    plt.plot(minSQ_frecs,minSQ_80ohm_50,'bs-',linewidth=2.0,label="Tendencia: \u03A6= "+str(D_var*180)+"°")
                elif(Rl==Rl2):
                    plt.plot(x,Vo_40ohm_50,'bo-',linewidth=2.0,label="Datos reales: \u03A6= "+str(D_var*180)+"°")
                    plt.plot(minSQ_frecs,minSQ_40ohm_50,'bs-',linewidth=2.0,label="Tendencia: \u03A6= "+str(D_var*180)+"°")
            elif(j==1):     
                plt.plot(x,y,'g^-',linewidth=2.0,label="Curva teórica: \u03A6= "+str(D_var*180)+"°")
                if(Rl==Rl1):
                    plt.plot(x,Vo_80ohm_100,'go-',linewidth=2.0,label="Datos reales: \u03A6= "+str(D_var*180)+"°")
                    plt.plot(minSQ_frecs,minSQ_80ohm_100,'gs-',linewidth=2.0,label="Tendencia: \u03A6= "+str(D_var*180)+"°")
                elif(Rl==Rl2):
                    plt.plot(x,Vo_40ohm_100,'go-',linewidth=2.0,label="Datos reales: \u03A6= "+str(D_var*180)+"°")
                    plt.plot(minSQ_frecs,minSQ_40ohm_100,'gs-',linewidth=2.0,label="Tendencia: \u03A6= "+str(D_var*180)+"°")
            elif(j==2):
                plt.plot(x,y,'r^-',linewidth=2.0,label="Curva teórica: \u03A6= "+str(D_var*180)+"°")
                if(Rl==Rl1):
                    plt.plot(x,Vo_80ohm_200,'ro-',linewidth=2.0,label="Datos reales: \u03A6= "+str(D_var*180)+"°")
                    plt.plot(minSQ_frecs,minSQ_80ohm_200,'rs-',linewidth=2.0,label="Tendencia: \u03A6= "+str(D_var*180)+"°")
                elif(Rl==Rl2):
                    plt.plot(x,Vo_40ohm_200,'ro-',linewidth=2.0,label="Datos reales: \u03A6= "+str(D_var*180)+"°")
                    plt.plot(minSQ_frecs,minSQ_40ohm_200,'rs-',linewidth=2.0,label="Tendencia: \u03A6= "+str(D_var*180)+"°")
            D_var = D_var*2     #Incrementeo el valor de D_var para siguiente paramétrica.
            plt.title("Ro = "+str(Rl)+"[\u03A9]           Leq = "+str(L*1e6)+" [uHy]")  #Grafico valores de paramétros.
            plt.legend()
            plt.grid(True)
            major_ticks_fs=np.arange(16,46,1)   #Graficar de 16kHz a 46kHz cada 1kHz.
            ax.set_xticks(major_ticks_fs)       #Configuro escala de gráfico en x.
            ax.set_yticks(major_ticks_Vo)       #Configuro escala de gráfico en y.
            plt.xlabel('Frecuencia [kHz]')
            plt.ylabel('Tensión de Salida Vo [V]')
    plt.show()
