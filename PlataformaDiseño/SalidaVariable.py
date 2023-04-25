def graficarCorriente(Vi,Vo_inf,Vo_sup,n,L,fs,Id_max,Vo_max,MODO):
    import numpy as np
    import CalcularCtes
    import matplotlib.pyplot as plt
    pts = int(round(((Vo_sup-Vo_inf)*0.5),0)+1)  #Número de puntos a graficar

    Vo_var=Vo_inf                       #Tensión de salida inicial.
    Vo_step=(Vo_sup-Vo_inf)/(pts-1)     #Paso de tensión de salida.
    Id_max_vec=[Id_max,Id_max]          #Vector para trazar línea horizontal.
    Vo_vec=[Vo_inf,Vo_sup]              #Vector para trazar línea horizontal
    D_var=0.1           #Desfase proporcional inicial. D=0.1 equivale a phi=18°
    D_step=0.05         #Incremento del desfase proporcional para graficar paramétricas.

    fig = plt.figure(figsize=[14,10]) #Define tamaño de gráfica
    ax = fig.add_subplot(1,1,1)
    if(MODO==2):
        plt.plot(Vo_vec,Id_max_vec,'k^-',linewidth=2.0,label=r'$ Id,max = '+str(Id_max)+'$')
    for j in (range(9)):                    #Se ejecuta una vez por cada paramétrica.
        x = np.zeros((pts,1),dtype=float)   #Vector para tensiones de salida.
        y1 = np.zeros((pts,1),dtype=float)  #Vector para corriente eficaz en mosfets P1.
        y2 = np.zeros((pts,1),dtype=float)  #Vector para corriente media de salida.
        for i in (range(pts)):  #Se ejecuta la función para completar los vectores.
            x[i] = Vo_var       #Se guarda el valor vector x de tensiones.
            y1[i]=(CalcularCtes.calcSinPrint(Vi,Vo_var,n,D_var,L,fs))[0]
            y2[i]=(CalcularCtes.calcSinPrint(Vi,Vo_var,n,D_var,L,fs))[1]
            Vo_var = Vo_var+Vo_step         #Nuevo paso para próxima iteración.
        #El siguiente bloque incluye el gráfico segun el desfase proporcional y el valor MODO.
        #Algunas paramétricas no se grafican para mayor claridad.
        if(j==0 and MODO==1):#      (phi=18° => D=0.1) Limite Gef=1.2 en MODO=1.
            plt.plot(x,y1,'bs-',linewidth=2.0,label=r'$Id(\phi='+str(round(D_var*180,0))+')$')
            plt.plot(x,y2,'bo-',linewidth=2.0,label=r'$Io(\phi='+str(round(D_var*180,0))+')$')
        elif(j==1 and MODO==1):#    (phi=27° => D=0.15) Limite Gef=1.4 en MODO=1.
            plt.plot(x,y1,'gs-',linewidth=2.0,label=r'$Id(\phi='+str(round(D_var*180,0))+')$')
            plt.plot(x,y2,'go-',linewidth=2.0,label=r'$Io(\phi='+str(round(D_var*180,0))+')$')
        elif(j==2 and MODO==1):#    (phi=36° => D=0.2) Limite Gef=1.6 en MODO=1.
            plt.plot(x,y1,'rs-',linewidth=2.0,label=r'$Id(\phi='+str(round(D_var*180,0))+')$')
            plt.plot(x,y2,'ro-',linewidth=2.0,label=r'$Io(\phi='+str(round(D_var*180,0))+')$')
#        elif(j==3):#    (phi=45° => D=0.25) Valor intermedio de exigencia.
#            plt.plot(x,y1,'rs-',linewidth=2.0,label=r'$Id(\phi='+str(round(D_var*180,0))+')$')
#            plt.plot(x,y2,'ro-',linewidth=2.0,label=r'$Io(\phi='+str(round(D_var*180,0))+')$')
        elif(j==4 and MODO==2):#    (phi=54° => D=0.3) Valor con elevada exigencia, no maximo.
            plt.plot(x,y1,'bs-',linewidth=2.0,label=r'$Id(\phi='+str(round(D_var*180,0))+')$')
            plt.plot(x,y2,'bo-',linewidth=2.0,label=r'$Io(\phi='+str(round(D_var*180,0))+')$')
#        elif(j==5):#    (phi=63° => D=0.35) Valor con elevada exigencia, no maximo.
#            plt.plot(x,y1,'ks-',linewidth=2.0,label=r'$Id(\phi='+str(round(D_var*180,0))+')$')
#            plt.plot(x,y2,'ko-',linewidth=2.0,label=r'$Io(\phi='+str(round(D_var*180,0))+')$')
        elif(j==6 and MODO==2):#    (phi=72° => D=0.4) Maximo valor de exigencia "justificada".
            plt.plot(x,y1,'gs-',linewidth=2.0,label=r'$Id(\phi='+str(round(D_var*180,0))+')$')
            plt.plot(x,y2,'go-',linewidth=2.0,label=r'$Io(\phi='+str(round(D_var*180,0))+')$')
#        elif(j==7):#    (phi=81° => D=0.45) Valor con elevada exigencia "injustificada".
#            plt.plot(x,y1,'ys-',linewidth=2.0,label=r'$Id(\phi='+str(round(D_var*180,0))+')$')
#            plt.plot(x,y2,'yo-',linewidth=2.0,label=r'$Io(\phi='+str(round(D_var*180,0))+')$')
        elif(j==8 and MODO==2):# (phi=90° => D=0.5) Maximo valor de exigencia "injustificada".
            plt.plot(x,y1,'rs-',linewidth=2.0,label=r'$Id(\phi='+str(round(D_var*180,0))+')$')
            plt.plot(x,y2,'ro-',linewidth=2.0,label=r'$Io(\phi='+str(round(D_var*180,0))+')$')
        Vo_var=Vo_inf       #Se reinicializa el valor de la tensión mínima a graficar.
        D_var=D_var+D_step  #Se incrementa el desfase proporcional para próxima gráfica.
    plt.title("fs = "+str(fs*0.001)+" [kHz]    L = "+str(L*1e6)+" [uHy]    n = "+str(n))
    plt.legend()
    plt.grid(True)

    if(MODO==1):
        plt.axvline(x=110)#Recta vertical Gef=1
        plt.axvline(x=138)#Recta vertical Gef=1.2
        plt.axvline(x=158)#Recta vertical Gef=1.4
        plt.axvline(x=182)#Recta vertical Gef=1.6
        major_ticks_Id_Io = np.arange(2,10,1) #Graficar de 2A a 10A cada 1A.
        major_ticks_Vo = np.arange(100,204,4) #Graficar de 100V a 204V cada 4V.
        ax.set_xticks(major_ticks_Vo)
        ax.set_yticks(major_ticks_Id_Io)
    elif(MODO==2):
        plt.axvline(x=Vo_max)
        major_ticks_Id_Io = np.arange(6,17,1) #Graficar de 6A a 17A cada 1A.
        major_ticks_Vo = np.arange(84,224,4)  #Graficar de 84V a 224V cada 4V.
        ax.set_xticks(major_ticks_Vo)
        ax.set_yticks(major_ticks_Id_Io)
    plt.xlabel('Tensión de salida [V]')
    plt.ylabel('Corriente eficaz en MOSFET (P1) Id [A]\nCorriente media de salida Io [A]')
    plt.show()