def graficarCorriente(Vo_n,Vi_min,Vi_max,n,L,fs,pts):

    import numpy as np
    import CalcularCtes
    import matplotlib.pyplot as plt
    PI=3.14159265
    D_var=0.1       #Desfase porcentual inicial
    D_step=0.1      #Paso del desfase porcentual

    Vi_var=Vi_min   #Tension de entrada inicial
    Vi_step=(Vi_max-Vi_min)/(pts-1) #Paso de tension de entrada

    plt.figure(figsize=[14,7])  #Define tamaño de grafica
    for j in (range(5)):    #Se ejecuta una vez por cada desfase porcentual a graficar
        x = np.zeros((pts,1),dtype=float)   #Vector para voltajes de entrada
        y1 = np.zeros((pts,1),dtype=float)   #Vector para valores de corriente eficaz en mosfets P1.
        y2 = np.zeros((pts,1),dtype=float)   #Vector para valores de corriente eficaz en mosfets P1.
        for i in (range(pts)):  #Se ejecuta la funcion para completar los vectores
            x[i] = Vi_var       #Se guarda el valor vector x
#            print("D_var=",D_var)
            y1[i] = (CalcularCtes.calcSinPrint(Vi_var,Vo_n,n,D_var,L,fs))[0] #Se guarda valor de corriente eficaz en mosfets Ief_d_p.
            y2[i] = (CalcularCtes.calcSinPrint(Vi_var,Vo_n,n,D_var,L,fs))[1] #Se guarda valor de corriente media de salida Io.
            print("Vi_var=",x[i])
            print("I_d=",y1[i])
            print("I_o=",y2[i],"\n")
            Vi_var = Vi_var+Vi_step #Nuevo paso para proxima iteracion
        if(j==0):   #Selecciona el grafico segun el desfase porcentual a graficar
            plt.plot(x,y1,'gs-',linewidth=2.0,label=r'$I_d(\phi='+str(round(D_var*180,0))+')$')
            plt.plot(x,y2,'go-',linewidth=2.0,label=r'$I_o(\phi='+str(round(D_var*180,0))+')$')
        elif(j==1):
            plt.plot(x,y1,'rs-',linewidth=2.0,label=r'$I_d(\phi='+str(round(D_var*180,0))+')$')
            plt.plot(x,y2,'ro-',linewidth=2.0,label=r'$Io(\phi='+str(round(D_var*180,0))+')$')
        elif(j==2):
            plt.plot(x,y1,'ks-',linewidth=2.0,label=r'$I_d(\phi='+str(round(D_var*180,0))+')$')
            plt.plot(x,y2,'ko-',linewidth=2.0,label=r'$I_o(\phi='+str(round(D_var*180,0))+')$')
        elif(j==3):
            plt.plot(x,y1,'gs-',linewidth=2.0,label=r'$I_d(\phi='+str(round(D_var*180,0))+')$')
            plt.plot(x,y2,'go-',linewidth=2.0,label=r'$I_o(\phi='+str(round(D_var*180,0))+')$')
        elif(j==4):
            plt.plot(x,y1,'rs-',linewidth=2.0,label=r'$I_d(\phi='+str(round(D_var*180,0))+')$')
            plt.plot(x,y2,'ro-',linewidth=2.0,label=r'$I_o(\phi='+str(round(D_var*180,0))+')$')
        elif(j==5):
            plt.plot(x,y1,'ks-',linewidth=2.0,label=r'$I_d(\phi='+str(round(D_var*180,0))+')$')
            plt.plot(x,y2,'ko-',linewidth=2.0,label=r'$I_o(\phi='+str(round(D_var*180,0))+')$')
        Vi_var=Vi_min #Se reinicializa el valor del voltaje minimo a graficar
        D_var=D_var+D_step #Se incrementa el desfase porcentual para proxima grafica

    plt.legend()
    plt.grid(True)
    plt.xlabel('Voltaje Entrada [V]')
    plt.ylabel('Corriente Eficaz Inductor [A]')
    plt.show()
#    print("Vector x = \n",x)
#    print("Vector y = \n",y)
