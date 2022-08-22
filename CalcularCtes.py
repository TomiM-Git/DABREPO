def Calcular(Vi,Vo,n,D,L,fs):
    import math

    PI=3.14159265
    phi=D*PI    #Desfase entre puentes en radianes
    Ts=1/(2*fs) #Semiperiodo de conmutacion

    print("\n***************************************************")
    print("\n**** CORRIENTES DEL CIRCUITO EN PEOR CONDICION ****")
    print("\n***************************************************\n")
#*****************************************************************************

    print("\nVariaciones absolutas de corriente por intervalo en PRIMARIO [P] e INDUCTOR [L]:\n")

    dI1=(Vi+Vo/n)*(D*Ts)/L          #Pendiente de corriente instantanea en intervalo [0:phi]
    dI2=(Vi-Vo/n)*((1-D)*Ts)/L      #Pendiente de corriente instantanea en intervalo [phi:PI]
    dI3=(-Vi-Vo/n)*(D*Ts)/L         #Pendiente de corriente instantanea en intervalo [PI:PI+phi]
    dI4=(-Vi+Vo/n)*((1-D)*Ts)/L     #Pendiente de corriente instantanea en intervalo [PI+phi:2*PI]
    
    print("Intervalo [0:phi]                    dI1 = ",dI1)
    print("Intervalo [phi:PI]                   dI2 = ",dI2)
    print("Intervalo [PI:PI+phi]                dI3 = ",dI3)
    print("Intervalo [PI+phi:2*PI]              dI4 = ",dI4)

#*****************************************************************************
    print("\nCorrientes instantaneas en PRIMARIO [P] e INDUCTOR [L] en puntos de inflexion:\n")

    I0=-(dI1+dI2)/2
    I1=I0+dI1
    I2=I1+dI2
    I3=I2+dI3
    
    print("Fase=0                               I0 = ",I0)
    print("Fase=phi     (CORRIENTE PICO)        I1 = ",I1)
    print("Fase=PI                              I2 = ",I2)
    print("Fase=PI+phi  (CORRIENTE PICO)        I3 = ",I3)

    print("\nCorrientes instantaneas en el SECUNDARIO [S] en puntos de inflexion:\n")

    I0_s=I0/n
    I1_s=I1/n
    I2_s=I2/n
    I3_s=I3/n

    print("Fase=0                               I0_s = ",I0_s)
    print("Fase=phi                             I1_s = ",I1_s)
    print("Fase=PI                              I2_s = ",I2_s)
    print("Fase=PI+phi                          I3_s = ",I3_s)

#*****************************************************************************
    print("\nCalculos de corrientes eficaces:\n")
    alpha = math.atan(phi/dI1)
    theta_x = abs(I0)*math.tan(alpha)
    print("\t\t\t\yt\t alpha = ",alpha)
    print("\t\t\t\yt\t theta_x = ",theta_x)
    print("\t\t\t\yt\t phi = ",phi)
 
    Ief1=(abs(I0)/theta_x)*math.sqrt((theta_x**3)/(3*PI))
    Ief2=(abs(I1)/(phi-theta_x))*math.sqrt(((phi-theta_x)**3)/(3*PI))

    Ief3=math.sqrt(((I1)**2)*(PI-phi)/(PI))
    Ief4=((abs(I2)-abs(I1))/(PI-phi))*math.sqrt(((PI-phi)**3)/(3*PI))

    IefL=math.sqrt(Ief1**2+Ief2**2+(Ief3+Ief4)**2)

    #print("\nAuxiliar 1:        Ief1 = ",Ief1)
    #print("Auxiliar 2:        Ief2 = ",Ief2)
    #print("Auxiliar 1:        Ief3 = ",Ief3)
    #print("Auxiliar 2:        Ief4 = ",Ief4)
    print("\nEn PRIMARIO [P] e INDUCTOR [L]       IefL = ",IefL)


    Ief_ce_p=IefL/math.sqrt(2)
    print("\nEn IGBT del PRIMARIO [P]             Ief_ce_p = ",Ief_ce_p)

    Ief_s=IefL/n
    print("\nEn el SECUNDARIO[S]                  Ief_s = ",Ief_s)

    Ief_ce_s=Ief_s/math.sqrt(2)
    print("\nEn IGBT del SECUNDARIO[S]            Ief_ce_s = ",Ief_ce_s)

#    return (IefL,Ief_s)

#******************************************************************************
def calcSinPrint(Vi,Vo,n,D,L,fs): #Funcion que retorna los valores, sin imprimir en consola

    import math
    PI=3.14159265
    phi=D*PI
    Ts=1/(2*fs)

    dI1=(Vi+Vo/n)*(D*Ts)/L          #Pendiente de corriente instantanea en intervalo [0:phi]
    dI2=(Vi-Vo/n)*((1-D)*Ts)/L      #Pendiente de corriente instantanea en intervalo [phi:PI]
    dI3=(-Vi-Vo/n)*(D*Ts)/L         #Pendiente de corriente instantanea en intervalo [PI:PI+phi]
    dI4=(-Vi+Vo/n)*((1-D)*Ts)/L     #Pendiente de corriente instantanea en intervalo [PI+phi:2*PI]

    I0=-(dI1+dI2)/2                 #Corriente instantanea en primario en 0 radianes
    I1=I0+dI1                       #Corriente instantanea en primario en phi radianes
    I2=I1+dI2                       #Corriente instantanea en primario en PI radianes
    I3=I2+dI3                       #Corriente instantanea en primario en PI+phi radianes

    I0_s=I0/n                       #Corriente instantanea en secundario en 0 radianes
    I1_s=I1/n                       #Corriente instantanea en secundario en phi radianes
    I2_s=I2/n                       #Corriente instantanea en secundario en PI radianes
    I3_s=I3/n                       #Corriente instantanea en secundario en PI+phi radianes

    alpha = math.atan(phi/dI1)          #Angulo geometrico para calculo de integrales triangulares entre 0 y phi
    theta_x = abs(I0)*math.tan(alpha)   #Fase en abscisas de cruce por cero de la corriente en el inductor

#    print("alpha = ",alpha)
#    print("theta_x = ",theta_x)
#    print("phi = ",phi)
#    print("I0 =",I0)
#    print("I1 =",I1)
#    print("I2 =",I2)
#    print("I3 =",I3)

    #Corriente eficaz triangular entre [0:theta_x] y [PI:PI+theta_x]
    Ief1=(abs(I0)/theta_x)*math.sqrt((theta_x**3)/(3*PI))  
    #Corriente eficaz triangular entre [theta_x:phi] y [PI+theta_x:PI+phi]
    Ief2=(abs(I1)/(phi-theta_x))*math.sqrt(((phi-theta_x)**3)/(3*PI)) 
    #Corriente eficaz rectangular entre [phi:PI]
    Ief3=math.sqrt(((I1)**2)*(PI-phi)/(PI))
    #Corriente eficaz triangular entre [phi:PI]
    Ief4=((abs(I2)-abs(I1))/(PI-phi))*math.sqrt(((PI-phi)**3)/(3*PI))
    #Suma vectorial para obtener corriente eficaz total en el inductor y devanado primario
    IefL=math.sqrt(Ief1**2+Ief2**2+(Ief3+Ief4)**2)

    Ief_ce_p=IefL/math.sqrt(2)      #Corriente eficaz en llaves del primario
    Ief_s=IefL/n                    #Corriente eficaz en devanado secundario
    Ief_ce_s=Ief_s/math.sqrt(2)     #Corriente eficaz en llaves del secundario

    return (IefL,Ief_s)     #Retorno corriente en inductor/primario y en secundario



