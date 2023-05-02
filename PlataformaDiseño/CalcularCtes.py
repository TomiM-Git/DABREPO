def calcular(Vi,Vo,n,D,L,fs): 
    import math
    PI=3.14159265   #Constante PI.
    phi=D*PI        #Desfase entre puentes en radianes.
    Ts=1/(2*fs)     #Semiperiodo de conmutación.
    print("**********************************************************************")
    print("*************** PROCEDIMIENTO DE CÁLCULO DE CORRIENTES ***************")
    print("**********************************************************************")
#   ******************************************************************************
    print("********************** Parámetros de entrada: ************************")
    print("Tensión de entrada:                   Vi = ",round(Vi,1)," [V]")
    print("Tensión de salida:                    Vo = ",round(Vo,1)," [V]")
    print("Relación de transformación:           n = ",round(n,1))
    print("Desfase entre puentes en radianes:    phi = ",round(phi,1),"rad")
    print("Desfase proporcional entre puentes:   D = ",round(D,1))
    print("Inductancia equivalente total:        L = ",round(L*1e6,1),"[uHy]")
    print("Frecuencia de conmutación:            fs = ",round(fs*(1e-3),1),"[kHz]")
#**** Primeros cálculos auxiliares de variaciones de corriente. ****
    print("\n*** Intervalos de tiempo y variaciones de corriente en inductor: *****")
    print("     (dt1 = dt3 = D*Ts)  ;  (dt2 = dt4 = (1-D)*Ts)      ")
    print("Duración de intervalo        [0:phi]: dt1 = ",round(D*Ts*1e6,1)," [us]")
    print("Duración de intervalo       [phi:PI]: dt2 = ",round((1-D)*Ts*1e6,1)," [us]")
    print("Duración de intervalo    [PI:PI+phi]: dt3 = ",round(D*Ts*1e6,1)," [us]")
    print("Duración de intervalo  [PI+phi:2*PI]: dt4 = ",round((1-D)*Ts*1e6,1)," [us]")
    print("           (dI1 = -dI3)  ;  (dI2 = -dI4)      ")
    dI1=(Vi+Vo/n)*(D*Ts)/L          #Pendiente de corriente en intervalo [0:phi].
    dI2=(Vi-Vo/n)*((1-D)*Ts)/L      #Pendiente de corriente en intervalo [phi:PI].
    dI3=(-Vi-Vo/n)*(D*Ts)/L         #Pendiente de corriente en intervalo [PI:PI+phi].
    dI4=(-Vi+Vo/n)*((1-D)*Ts)/L     #Pendiente de corriente en intervalo [PI+phi:2*PI].
    print("Variación en intervalo       [0:phi]: dI1 = ",round(dI1,1)," [A]")
    print("Variación en intervalo      [phi:PI]: dI2 = ",round(dI2,1)," [A]")
    print("Variación en intervalo   [PI:PI+phi]: dI3 = ",round(dI3,1)," [A]")
    print("Variación en intervalo [PI+phi:2*PI]: dI4 = ",round(dI4,1)," [A]")
#****       ****
    print("\n*** Corrientes instantáneas en puntos de inflexión: ******************")
    IA=-(dI1+dI2)/2                 #Corriente instantánea en primario en 0 radianes.
    IB=IA+dI1                       #Corriente instantánea en primario en phi radianes.
    IC=IB+dI2                       #Corriente instantánea en primario en PI radianes.
    ID=IC+dI3                       #Corriente instantánea en primario en PI+phi radianes.
    print("Fase=0                                IA = ",round(IA,1)," [A]")
    print("Fase=phi                              IB = ",round(IB,1)," [A]")
    print("Fase=PI                               IC = ",round(IC,1)," [A]")
    print("Fase=PI+phi                           ID = ",round(ID,1)," [A]")
    IA_s=IA/n                       #Corriente instantánea en secundario en 0 radianes.
    IB_s=IB/n                       #Corriente instantánea en secundario en phi radianes.
    IC_s=IC/n                       #Corriente instantánea en secundario en PI radianes.
    ID_s=ID/n                       #Corriente instantánea en secundario en PI+phi radianes.
    print("Fase=0                                IA_s = ",round(IA_s,1)," [A]")
    print("Fase=phi                              IB_s = ",round(IB_s,1)," [A]")
    print("Fase=PI                               IC_s = ",round(IC_s,1)," [A]")
    print("Fase=PI+phi                           ID_s = ",round(ID_s,1)," [A]")
#****       ****
    alpha = math.atan(phi/dI1)          #Ángulo geométrico para calculo de theta_x.
    theta_x = abs(IA)*math.tan(alpha)   #Fase de cruce por cero.
    print("\n*** Ángulos para cálculos con figuras geométricas: *******************")
    print("Ángulo geométrico proyección eje x:   alpha = ",round(alpha,1)," rad")
    print("Fase de cruce por cero:               theta_x = ",round(theta_x,1),"rad")
#****       ****
    print("\n*** Cálculos de corrientes eficaces: *********************************")
#Corriente eficaz triangular entre [0:theta_x] y [PI:PI+theta_x].
    Ief1=(abs(IA)/theta_x)*math.sqrt((theta_x**3)/(3*PI))              
#Corriente eficaz triangular entre [theta_x:phi] y [PI+theta_x:PI+phi]. 
    Ief2=(abs(IB)/(phi-theta_x))*math.sqrt(((phi-theta_x)**3)/(3*PI))   
#Corriente eficaz rectangular entre [phi:PI].
    Ief3=math.sqrt(((IB)**2)*(PI-phi)/(PI))                             
#Corriente eficaz triangular entre [phi:PI].
    Ief4=((abs(IC)-abs(IB))/(PI-phi))*math.sqrt(((PI-phi)**3)/(3*PI))   
#Suma vectorial para obtener corriente eficaz total en el inductor.
    IefL=math.sqrt(Ief1**2+Ief2**2+(Ief3+Ief4)**2)  

    print("En PRIMARIO [P] e INDUCTOR [L]        IefL = ",round(IefL,1)," [A]")
    Id_ef_p=IefL/math.sqrt(2) 
    print("En MOSFET del puente P1               Id_ef_p = ",round(Id_ef_p,1)," [A]")
    Ief_s=IefL/n 
    print("En el SECUNDARIO [S]                  Ief_s = ",round(Ief_s,1)," [A]")
    Id_ef_s=Ief_s/math.sqrt(2) 
    print("En MOSFET del puente P2               Id_ef_s = ",round(Id_ef_s,1)," [A]")
#****       ****
    Io1=((IB_s+IC_s)*(1-D)/2)
    Io2=IC_s*theta_x/(2*PI)
    Io3=ID_s*(phi-theta_x)/(2*PI)
    Io=Io1+Io2+Io3
    print("\n    Corriente media de salida:        Io = ",round(Io,1)," [A]")
    Rl=Vo/Io
    print("    Carga resistiva requerida:        Rl = Vo/Io = ",round(Rl,0)," [ohm]")
#****    Función mismo procedimiento, sin imprimir en pantalla.
# Retorna corriente eficaz en mosfets del primario y corriente media   ****
def calcSinPrint(Vi,Vo,n,D,L,fs):
    import math
    PI=3.14159265               #Constante PI.
    phi=D*PI                    #Desfase entre puentes.
    Ts=1/(2*fs)                 #Semiperiodo de conmutación.
    dI1=(Vi+Vo/n)*(D*Ts)/L      #Pendiente de corriente en intervalo [0:phi].
    dI2=(Vi-Vo/n)*((1-D)*Ts)/L  #Pendiente de corriente en intervalo [phi:PI].
    dI3=(-Vi-Vo/n)*(D*Ts)/L     #Pendiente de corriente en intervalo [PI:PI+phi].
    dI4=(-Vi+Vo/n)*((1-D)*Ts)/L #Pendiente de corriente en intervalo [PI+phi:2*PI].
    IA=-(dI1+dI2)/2             #Corriente instantánea en primario en 0 radianes.
    IB=IA+dI1                   #Corriente instantánea en primario en phi radianes.
    IC=IB+dI2                   #Corriente instantánea en primario en PI radianes.
    ID=IC+dI3                   #Corriente instantánea en primario en PI+phi radianes.
    IA_s=IA/n                   #Corriente instantánea en secundario en 0 radianes.
    IB_s=IB/n                   #Corriente instantánea en secundario en phi radianes.
    IC_s=IC/n                   #Corriente instantánea en secundario en PI radianes.
    ID_s=ID/n                   #Corriente instantánea en secundario en PI+phi radianes.
    alpha = math.atan(phi/dI1)          #Ángulo geométrico para calculo de theta_x.
    theta_x = abs(IA)*math.tan(alpha)   #Fase de cruce por cero.
#Corriente eficaz triangular entre [0:theta_x] y [PI:PI+theta_x].
    Ief1=(abs(IA)/theta_x)*math.sqrt((theta_x**3)/(3*PI))               
#Corriente eficaz triangular entre [theta_x:phi] y [PI+theta_x:PI+phi].
    Ief2=(abs(IB)/(phi-theta_x))*math.sqrt(((phi-theta_x)**3)/(3*PI))   
#Corriente eficaz rectangular entre [phi:PI].
    Ief3=math.sqrt(((IB)**2)*(PI-phi)/(PI))                             
#Corriente eficaz triangular entre [phi:PI].
    Ief4=((abs(IC)-abs(IB))/(PI-phi))*math.sqrt(((PI-phi)**3)/(3*PI))
#Suma vectorial para obtener corriente eficaz total en el inductor.  
    IefL=math.sqrt(Ief1**2+Ief2**2+(Ief3+Ief4)**2)      
    Id_ef_p=IefL/math.sqrt(2)     #Corriente eficaz en mosfet del primario.
    Ief_s=IefL/n                  #Corriente eficaz en devanado secundario.
    Id_ef_s=Ief_s/math.sqrt(2)    #Corriente eficaz en mosfet del secundario.
#****       ****
    Io1=((IB_s+IC_s)*(1-D)/2)
    Io2=IC_s*theta_x/(2*PI)
    Io3=ID_s*(phi-theta_x)/(2*PI)
    Io=Io1+Io2+Io3
#Retorno valor de corriente eficaz en primario y corriente media de salida.
    return (Id_ef_p,Io) 