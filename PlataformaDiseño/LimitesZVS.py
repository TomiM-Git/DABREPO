def graficarLimitesZVS():

    import numpy as np
    import matplotlib.pyplot as plt

    PI=3.14159265

    Gef_var=0.4     #Inicializa ganancia en continua reflejada al primario de primer parametrica.
    Gef_step=0.2    #Define paso entre curvas parametricas.
    phi_var=-90   #Inicializa angulo de control inicial a graficar
    phi_step=9    #Define paso del angulo de control

    fig=plt.figure(figsize=[14,7]) #Define tamaño de grafica
    ax = fig.add_subplot(1, 1, 1)
    for j in (range(10)):                    #Se ejecuta una vez por cada curva parametrica a graficar
        x = np.zeros((21,1),dtype=float)    #Vector para desfase phi entre puentes P1 y P2
        y = np.zeros((21,1),dtype=float)    #Vector para potencia de salida normalizada
#        y_aux = np.zeros((21,1),dtype=float)
        for i in (range(21)):   #Se ejecuta la funcion para completar los vectores
            x[i] = phi_var      #Se guarda el valor vector x
            if(j<8):            #Se ejecuta para todas las parametricas segun ganancias en continua reflejadas al primario.
                y[i] = Gef_var*phi_var*PI*(1-abs(phi_var)/180)/180  #Se guarda valor vector y
            elif(j==8):         #Se ejecuta para curva de limite ZVS del puente P1
                if(phi_var==-90):
                    y[i] = -10000
                elif(phi_var==90):
                    y[i] = 10000
                else:
                    y[i] = (-PI/(2*(PI/180)*abs(phi_var)-PI))*(phi_var*PI/180)*(1-(abs(phi_var))/180) #Se guarda valor vector y
            elif(j==9):         #Se ejecuta para curva de limite ZVS del puente P2
                y[i] = (1-2*abs(phi_var)/180)*phi_var*PI*(1-abs(phi_var)/180)/180  #Se guarda valor vector y
            phi_var=phi_var+phi_step    #Incremento de la variable independiente cada iteracion.
        if(j==0): #Selecciona el grafico segun la curva a graficar
            plt.plot(x,y,'r^-',linewidth=1.5,label=r'$Gef='+str(round(Gef_var,1))+'$')
        elif(j==1):
            plt.plot(x,y,'ro-',linewidth=1.5,label=r'$Gef='+str(round(Gef_var,1))+'$')
        elif(j==2):
            plt.plot(x,y,'gs-',linewidth=1.5,label=r'$Gef='+str(round(Gef_var,1))+'$')
        elif(j==3):
            plt.plot(x,y,'gx-',linewidth=1.5,label=r'$Gef='+str(round(Gef_var,1))+'$')
        elif(j==4):
            plt.plot(x,y,'go-',linewidth=1.5,label=r'$Gef='+str(round(Gef_var,1))+'$')
        elif(j==5):
            plt.plot(x,y,'g^-',linewidth=1.5,label=r'$Gef='+str(round(Gef_var,1))+'$')
        elif(j==6):
            plt.plot(x,y,'rs-',linewidth=1.5,label=r'$Gef='+str(round(Gef_var,1))+'$')
        elif(j==7):
            plt.plot(x,y,'rx-',linewidth=1.5,label=r'$Gef='+str(round(Gef_var,1))+'$')
        elif(j==8):
            plt.plot(x,y,'k^-',linewidth=1.5,label=r'$Limite ZVS P1$')
        elif(j==9):
            plt.plot(x,y,'k>-',linewidth=1.5,label=r'$Limite ZVS P2$')
        phi_var=-90     #Reinicializacion de la variable independiente.
        Gef_var=Gef_var+Gef_step    #Incremento para siguiente parametrica. Esta variable no se utiliza cuando j=7 y j=8.
    #Configuraciones del grafico
    plt.legend()
    plt.grid(True)
    plt.xlabel('Desfase '+r'$\phi$'+' entre P1 y P2 [°]')
    plt.ylabel('Potencia normalizada de salida Po,n')
    plt.xlim([-90,90])      #Limites horizontales entre -90° y 90°
    plt.ylim([-1.2,1.2])    #Limites verticales entre -1.2 y 1
    major_tick = [-1.2, -1, -0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1, 1.2]
    ax.set_yticks(major_tick)   #Lineas de grilla horizontales con valores fijos
    ax.set_xticks(x)            #Lineas de grilla verticales directamente los angulos ploteados.
    ax.grid(which='both')
    ax.grid(which='minor', alpha=1)
    ax.grid(which='major', alpha=2)
    plt.show()