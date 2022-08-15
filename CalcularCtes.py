def Calcular(Vi,Vo,n,D,L,fs):
    import math

    PI=3.14159265
    phi=D*PI
    Ts=1/(2*fs)

#*****************************************************************************

    dI1=(Vi+Vo/n)*(D*Ts)/L
    dI2=(Vi-Vo/n)*((1-D)*Ts)/L
    dI3=(-Vi-Vo/n)*(D*Ts)/L
    dI4=(-Vi+Vo/n)*((1-D)*Ts)/L
    
    print("Variacion corriente [0:phi]       dI1 = ",dI1)
    print("Variacion corriente [phi:PI]      dI2 = ",dI2)
    print("Variacion corriente [PI:PI+phi]   dI3 = ",dI3)
    print("Variacion corriente [PI+phi:2*PI] dI4 = ",dI4)


#*****************************************************************************
    print("Corrientes instantaneas en PRIMARIO [P] e INDUCTOR [L] en puntos de inflexion\n")

    I0=-(dI1+dI2)/2
    I1=I0+dI1
    I2=I1+dI2
    I3=I2+dI3


    print("Corriente en [P] y [L] en fase=0      I0 = ",I0)
    print("Corriente en [P] y [L] en fase=phi    I1 = ",I1)
    print("Corriente en [P] y [L] en fase=PI     I2 = ",I2)
    print("Corriente en [P] y [L] en fase=PI+phi I3 = ",I3)

    print("\nCorrientes instantaneas en el SECUNDARIO [S] en puntos de inflexion\n")

    I0_s=I0/n
    I1_s=I1/n
    I2_s=I2/n
    I3_s=I3/n

    print("Corriente en [S] en fase=0            I0_s = ",I0_s)
    print("Corriente en [S] en fase=phi          I1_s = ",I1_s)
    print("Corriente en [S] en fase=PI           I2_s = ",I2_s)
    print("Corriente en [S] en fase=PI+phi       I3_s = ",I3_s)

#*****************************************************************************
    print("Calculos de corrientes eficaces\n")

    Ief1=(abs(I0)/(phi/2))*math.sqrt(((phi/2)**3)/(3*PI))
    Ief2=math.sqrt(((I0)**2)*(PI-phi)/(PI))
    IefL=math.sqrt(2*(Ief1**2)+Ief2**2)

    print("Corriente eficaz auxiliar 1:      Ief1 = ",Ief1)
    print("Corriente eficaz auxiliar 2:      Ief1 = ",Ief2)
    print("\nCorriente eficaz total en PRIMARIO [P] e INDUCTOR [L]   IefL = ",IefL)


    Ief_ce_p=IefL/math.sqrt(2)
    print("\nCorriente eficaz en IGBT del PRIMARIO [P]               Ief_ce_p = ",Ief_ce_p)

    Ief_s=IefL/n
    print("\nCorriente eficaz en el SECUNDARIO [S]                   Ief_s = ",Ief_s)

    Ief_ce_s=Ief_s/math.sqrt(2)
    print("\nCorrientes eficaces en IGBT del SECUNDARIO [S]          Ief_ce_s = ",Ief_ce_s)

#*****************************************************************************
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



