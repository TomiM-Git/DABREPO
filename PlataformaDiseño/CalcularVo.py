def calcular(Vi,n,D,L,fs,Rl):   #Función que calcula e imprime Io y Vo.
    Io=Vi*D*(1-D)/(2*n*L*fs)    #Ecuación hallada en Capitulo 3.
    Vo=Io*Rl                    #Tensión media de salida de acuerdo a Ley de Ohm.
    print("\nCorriente media de salida del convertidor:   Iav_out = ",round(Io,2)," [A]")
    print("\nTensión media de salida del convertidor:   Vav_out = ",round(Vo,2)," [V]")
#******************************************************************************
#Función que retorna la tensión media de salida, sin imprimir en consola.
def calcSinPrint(Vi,n,D,L,fs,Rl):   
    Io=Vi*D*(1-D)/(2*n*L*fs)        #Ecuación hallada en Capitulo 3.
    Vo=Io*Rl                        #Tensión media de salida de acuerdo a Ley de Ohm.
    return(Vo)                      #Retorna valor de tensión media de salida.