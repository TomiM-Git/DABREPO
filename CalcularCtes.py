def Calcular(Vi,Vo,n,D,L,fs):
    import math
    import numpy as np
    PI=3.14159265
    phi=D*PI    #Desfase entre puentes en radianes
    Ts=1/(2*fs) #Semiperiodo de conmutacion

    print("********************************************************")
    print("********* CORRIENTES EN CONDICION MAS EXIGENTE *********")
    print("********************************************************")

#*****************************************************************************
    print("Parametros:\n")
    print("Tension de entrada                   Vi = ",round(Vi,2)," [V]")
    print("Tension de salida                    Vo = ",round(Vo,2)," [V]")
    print("Relacion de transformacion           n = ",round(n,2))
    print("Desfase entre puentes en radianes    phi = ",round(phi,2),"rad")
    print("Desfase porcentual entre puentes     D = ",round(D,2))
    print("Inductancia equivalente total        L = ",round(L*1e6,2),"[uHy]")
    print("Frecuencia de conmutacion            fs = ",round(fs*(1e-3),2),"[kHz]")


    print("\nVariaciones absolutas de corriente por intervalo en PRIMARIO [P] e INDUCTOR [L]:\n")

    dI1=(Vi+Vo/n)*(D*Ts)/L          #Pendiente de corriente instantanea en intervalo [0:phi]
    dI2=(Vi-Vo/n)*((1-D)*Ts)/L      #Pendiente de corriente instantanea en intervalo [phi:PI]
    dI3=(-Vi-Vo/n)*(D*Ts)/L         #Pendiente de corriente instantanea en intervalo [PI:PI+phi]
    dI4=(-Vi+Vo/n)*((1-D)*Ts)/L     #Pendiente de corriente instantanea en intervalo [PI+phi:2*PI]
    
    print("Intervalo [0:phi]                    dI1 = ",round(dI1,1)," [A]")
    print("Intervalo [phi:PI]                   dI2 = ",round(dI2,1)," [A]")
    print("Intervalo [PI:PI+phi]                dI3 = ",round(dI3,1)," [A]")
    print("Intervalo [PI+phi:2*PI]              dI4 = ",round(dI4,1)," [A]")

#*****************************************************************************
    print("\nCorrientes instantaneas en PRIMARIO [P] e INDUCTOR [L] en puntos de inflexion:\n")

    I0=-(dI1+dI2)/2
    I1=I0+dI1
    I2=I1+dI2
    I3=I2+dI3
    
    print("Fase=0                               I0 = ",round(I0,1)," [A]")
    print("Fase=phi                             I1 = ",round(I1,1)," [A]")
    print("Fase=PI                              I2 = ",round(I2,1)," [A]")
    print("Fase=PI+phi                          I3 = ",round(I3,1)," [A]")

    print("\nCorrientes instantaneas en el SECUNDARIO [S] en puntos de inflexion:\n")

    I0_s=I0/n
    I1_s=I1/n
    I2_s=I2/n
    I3_s=I3/n

    print("Fase=0                               I0_s = ",round(I0_s,1)," [A]")
    print("Fase=phi                             I1_s = ",round(I1_s,1)," [A]")
    print("Fase=PI                              I2_s = ",round(I2_s,1)," [A]")
    print("Fase=PI+phi                          I3_s = ",round(I3_s,1)," [A]")
#*****************************************************************************

    alpha = math.atan(phi/dI1)
    theta_x = abs(I0)*math.tan(alpha)
    print("\nAngulos para calculo de corrientes eficaces y corriente media:\n")
    print("Angulo geometrico proyeccion ejex alpha = ",round(alpha,3)," rad")
    print("Fase de cruce por cero theta_x = ",round(theta_x,3),"rad")

    Iav_out1=((I1+I2)*(1-D)/2)
    Iav_out2=I2*theta_x/(2*PI)
    Iav_out3=I3*(phi-theta_x)/(2*PI)
    Iav_out=Iav_out1+Iav_out2+Iav_out3
    print("\nCorriente media de salida del convertidor:   Iav_out = ",round(Iav_out,2)," [A]")

#*****************************************************************************
    print("\nCalculos de corrientes eficaces:\n")
 
    Ief1=(abs(I0)/theta_x)*math.sqrt((theta_x**3)/(3*PI))
    Ief2=(abs(I1)/(phi-theta_x))*math.sqrt(((phi-theta_x)**3)/(3*PI))

    Ief3=math.sqrt(((I1)**2)*(PI-phi)/(PI))
    Ief4=((abs(I2)-abs(I1))/(PI-phi))*math.sqrt(((PI-phi)**3)/(3*PI))

    IefL=math.sqrt(Ief1**2+Ief2**2+(Ief3+Ief4)**2)

    #print("\nAuxiliar 1:        Ief1 = ",Ief1)
    #print("Auxiliar 2:        Ief2 = ",Ief2)
    #print("Auxiliar 1:        Ief3 = ",Ief3)
    #print("Auxiliar 2:        Ief4 = ",Ief4)
    print("En PRIMARIO [P] e INDUCTOR [L]       IefL = ",round(IefL,2)," [A]")

    Ief_ce_p=IefL/math.sqrt(2)
    print("En IGBT del PRIMARIO [P]             Ief_ce_p = ",round(Ief_ce_p,2)," [A]")

    Ief_s=IefL/n
    print("En el SECUNDARIO[S]                  Ief_s = ",round(Ief_s,2)," [A]")

    Ief_ce_s=Ief_s/math.sqrt(2)
    print("En IGBT del SECUNDARIO[S]            Ief_ce_s = ",round(Ief_ce_s,2)," [A]")

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



