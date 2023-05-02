def generarParametricas2(Vi,n,Leq1,Leq2,Rl1,Rl2):
    import numpy as np
    import CalcularVo
    import matplotlib.pyplot as plt
    #Vector con frecuencias programadas al medir los datos experimentales.
    fs_vec=[16e3,20e3,25e3,29e3,31e3,33e3,37e3,40e3,44e3]
    #Vectores con datos experimentales para trazado de curvas paramétricas.
    Vo_40 = [19.8,17.1,16.5,11.6,13.6,11.3,10.3,10,10.5]
    Vo_80 = [27,25.8,25.9,19.3,23.4,19.3,18.3,18.1,18.4]
    # Vectores para trazado de rectas de tendencia.
    Vo2_80 = [16.8,14.7,12.6,12.2,9.7,9.5,5.7,5.5,5.3]
    Vo2_40 = [9.7,8.3,6.8,6.5,5,4.9,3.8,3,2.7]
    minSQ_frecs = [16,44]           #Mínima y máxima frecuencia del barrido.
    # Vector para trazado de recta horizontal Vi para referencia visual elevador/reductor.
    Vi_ref=[Vi,Vi]
    D=0.2
    fig= plt.figure(figsize=[17,10])
    for x in range(2):  # Bucle para la realizacion de 2 gráficas.
        if(x==0):
            ax1=fig.add_subplot(2,2,(1,3))  #Dimensión de subploteo 1.
            ax=ax1      #Sobreescribo variable de subploteo.
            Rl=Rl1      #Sobreescribo variable de resistencia de carga.
            major_ticks_Vo=np.arange(0,74,2)    #Graficar de 0V a 74V cada 2V.
            #Agrego gráfico de recta horizontal con tensión de entrada para referencia.
            plt.plot(minSQ_frecs,Vi_ref,'ko-',linewidth=2.0,label="Entrada: Vi = "+str(Vi)+"[V]")
        else:
            ax2=fig.add_subplot(2,2,(2,4))  #Dimensión de subploteo 2.
            ax=ax2      #Sobreescribo variable de subploteo.
            Rl=Rl2      #Sobreescribo variable de resistencia de carga.
            major_ticks_Vo=np.arange(0,37,1)    #Graficar de 0V a 37V cada 2V.
            #Agrego gráfico de recta horizontal con tensión de entrada para referencia.
            plt.plot(minSQ_frecs,Vi_ref,'ko-',linewidth=2.0,label="Entrada: Vi = "+str(Vi)+"[V]")
        x = np.zeros((9,1),dtype=float) #Vector para frecuencias.
        y = np.zeros((9,1),dtype=float) #Vector para tensiones de salida.
        y2 = np.zeros((9,1),dtype=float) #Vector para tensiones de salida.
        for i in (range(len(fs_vec))):
            x[i] = fs_vec[i]/1000       #Ingreso frecuencia en kHz.
            y[i] = CalcularVo.calcSinPrint(Vi,n,D,Leq1,fs_vec[i],Rl) #Cálculo auxiliar de Vo.
            y2[i] = CalcularVo.calcSinPrint(Vi,n,D,Leq2,fs_vec[i],Rl) #Cálculo auxiliar de Vo.     
        plt.plot(x,y,'r^-',linewidth=2.0,label="Curva teórica: Leq1="+str(int(Leq1*1e6))+"[uHy]")
        plt.plot(x,y2,'b^-',linewidth=2.0,label="Curva teórica: Leq2="+str(int(Leq2*1e6))+"[uHy]")
        if(Rl==Rl1):
            plt.plot(x,Vo_80,'ro-',linewidth=2.0,label="Datos Reales: Leq1="+str(int(Leq1*1e6))+"[uHy]")
            plt.plot(x,Vo2_80,'bs-',linewidth=2.0,label="Datos Reales: Leq2="+str(int(Leq2*1e6))+"[uHy]")
        elif(Rl==Rl2):
            plt.plot(x,Vo_40,'ro-',linewidth=2.0,label="Datos Reales: Leq1="+str(int(Leq1*1e6))+"[uHy]")
            plt.plot(x,Vo2_40,'bs-',linewidth=2.0,label="Datos Reales: Leq2="+str(int(Leq2*1e6))+"[uHy]")
        plt.title("Ro="+str(Rl)+"[\u03A9]        \u03A6="+str(36)+"°")  #Grafico valores de paramétros.
        plt.legend()
        plt.grid(True)
        major_ticks_fs=np.arange(16,46,1)   #Graficar de 16kHz a 46kHz cada 1kHz.
        ax.set_xticks(major_ticks_fs)       #Configuro escala de gráfico en x.
        ax.set_yticks(major_ticks_Vo)       #Configuro escala de gráfico en y.
        plt.xlabel('Frecuencia [kHz]')
        plt.ylabel('Tensión de Salida Vo [V]')
    plt.show()