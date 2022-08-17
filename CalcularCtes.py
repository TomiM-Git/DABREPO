def Calcular(Vi,Vo,n,D,L,fs):
    import math

    PI=3.14159265
    phi=D*PI
    Ts=1/(2*fs)

    print("\n***************************************************")
    print("\n**** CORRIENTES DEL CIRCUITO EN PEOR CONDICION ****")
    print("\n***************************************************\n")
#*****************************************************************************

    print("\nVariaciones absolutas de corriente por intervalo en PRIMARIO [P] e INDUCTOR [L]:\n")

    dI1=(Vi+Vo/n)*(D*Ts)/L
    dI2=(Vi-Vo/n)*((1-D)*Ts)/L
    dI3=(-Vi-Vo/n)*(D*Ts)/L
    dI4=(-Vi+Vo/n)*((1-D)*Ts)/L
    
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

    Ief1=(abs(I0)/(phi/2))*math.sqrt(((phi/2)**3)/(3*PI))
    Ief2=math.sqrt(((I0)**2)*(PI-phi)/(PI))
    IefL=math.sqrt(2*(Ief1**2)+Ief2**2)

    #print("\nAuxiliar 1:      Ief1 = ",Ief1)
    #print("Auxiliar 2:      Ief1 = ",Ief2)
    print("\nEn PRIMARIO [P] e INDUCTOR [L]       IefL = ",IefL)


    Ief_ce_p=IefL/math.sqrt(2)
    print("\nEn IGBT del PRIMARIO [P]             Ief_ce_p = ",Ief_ce_p)

    Ief_s=IefL/n
    print("\nEn el SECUNDARIO[S]                  Ief_s = ",Ief_s)

    Ief_ce_s=Ief_s/math.sqrt(2)
    print("\nEn IGBT del SECUNDARIO[S]            Ief_ce_s = ",Ief_ce_s)

#******************************************************************************
def calcSinPrint(Vi,Vo,n,D,L,fs):

    import math
    PI=3.14159265
    phi=D*PI
    Ts=1/(2*fs)

    dI1=(Vi+Vo/n)*(D*Ts)/L
    dI2=(Vi-Vo/n)*((1-D)*Ts)/L
    dI3=(-Vi-Vo/n)*(D*Ts)/L
    dI4=(-Vi+Vo/n)*((1-D)*Ts)/L

    I0=-(dI1+dI2)/2
    I1=I0+dI1
    I2=I1+dI2
    I3=I2+dI3

    I0_s=I0/n
    I1_s=I1/n
    I2_s=I2/n
    I3_s=I3/n

    Ief1=(abs(I0)/(phi/2))*math.sqrt(((phi/2)**3)/(3*PI))
    Ief2=math.sqrt(((I0)**2)*(PI-phi)/(PI))
    IefL=math.sqrt(2*(Ief1**2)+Ief2**2)

    Ief_ce_p=IefL/math.sqrt(2)
    Ief_s=IefL/n
    Ief_ce_s=Ief_s/math.sqrt(2)

    return IefL

#*****************************************************************************


#*****************************************************************************


#*****************************************************************************



