def generarParametricas(Vi,n,L,Rl1,Rl2):

    import numpy as np
    import CalcularVo
    import matplotlib.pyplot as plt

    # Vectores para trazado de curvas parametricas.
    fs_vec=[16e3,20e3,25e3,29e3,31e3,33e3,37e3,40e3,44e3]
    Vo_40ohm_50 = [12.6,9.5,12.1,8,7.9,7.7,7.3,7.1,6.9]
    Vo_40ohm_100 = [19.8,17.1,16.5,11.6,13.6,11.3,10.3,10,10.5]
    Vo_40ohm_200 = [24.3,22.7,20,16.9,17.2,16.2,14.2,13.6,13.1]
    Vo_80ohm_50 = [19.4,14.1,19.7,14.6,14.5,14.3,13.9,13.6,13.5]
    Vo_80ohm_100 = [27,25.8,25.9,19.3,23.4,19.3,18.3,18.1,18.4]
    Vo_80ohm_200 =[33.1,31.3,29.7,27,27.5,26.6,22.6,22,23.7]
    # Vectores para trazado de rectas de tendencia.
    minSQ_frecs = [16,44]
    minSQ_40ohm_50 = [11.7,6.1]
    minSQ_40ohm_100= [18.7,8.62]
    minSQ_40ohm_200= [23.8,11.9]
    minSQ_80ohm_50 = [17.9,12.8]
    minSQ_80ohm_100= [27,16.8]
    minSQ_80ohm_200= [32.9,21.7]
    # Vector para trazado de linea horizontal Vi para referencia visual elevador/reductor.
    Vi_ref=[Vi,Vi]

    fig= plt.figure(figsize=[14,10])

    for x in range(2):
        D_var=0.1
        if(x==0):
            ax1=fig.add_subplot(2,2,(1,3))
            ax=ax1
            Rl=Rl1
            major_ticks_Vo=np.arange(0,80,5)
            plt.plot(minSQ_frecs,Vi_ref,'ko-',linewidth=2.0,label=r'$ Entrada: Vi = '+str(Vi)+' [V]$')
        else:
            ax2=fig.add_subplot(2,2,(2,4))
            ax=ax2
            Rl=Rl2
            major_ticks_Vo=np.arange(0,36,2)
            plt.plot(minSQ_frecs,Vi_ref,'ko-',linewidth=2.0,label=r'$ Entrada: Vi = '+str(Vi)+' [V]$')
        for j in (range(3)):
            x = np.zeros((9,1),dtype=float)
            y = np.zeros((9,1),dtype=float)
            for i in (range(len(fs_vec))):
                x[i] = fs_vec[i]/1000
                y[i] = CalcularVo.calcSinPrint(Vi,n,D_var,L,fs_vec[i],Rl)
            if(j==0):
                plt.plot(x,y,'b^-',linewidth=2.0,label=r'$Ideal: D = '+str(D_var)+'$')
                if(Rl==80):
                    plt.plot(x,Vo_80ohm_50,'bo-',linewidth=2.0,label=r'$Real: D = '+str(D_var)+'$')
                    plt.plot(minSQ_frecs,minSQ_80ohm_50,'bs-',linewidth=2.0,label=r'$Tendencia: D = '+str(D_var)+'$')
                elif(Rl==40):
                    plt.plot(x,Vo_40ohm_50,'bo-',linewidth=2.0,label=r'$Ideal: D = '+str(D_var)+'$')
                    plt.plot(minSQ_frecs,minSQ_40ohm_50,'bs-',linewidth=2.0,label=r'$Tendencia: D = '+str(D_var)+'$')
            elif(j==1):
                plt.plot(x,y,'g^-',linewidth=2.0,label=r'$Ideal: D = '+str(D_var)+'$')
                if(Rl==80):
                    plt.plot(x,Vo_80ohm_100,'go-',linewidth=2.0,label=r'$Real: D = '+str(D_var)+'$')
                    plt.plot(minSQ_frecs,minSQ_80ohm_100,'gs-',linewidth=2.0,label=r'$Tendencia: D = '+str(D_var)+'$')
                elif(Rl==40):
                    plt.plot(x,Vo_40ohm_100,'go-',linewidth=2.0,label=r'$Real: D = '+str(D_var)+'$')
                    plt.plot(minSQ_frecs,minSQ_40ohm_100,'gs-',linewidth=2.0,label=r'$Tendencia: D = '+str(D_var)+'$')
            elif(j==2):
                plt.plot(x,y,'r^-',linewidth=2.0,label=r'$Ideal: D = '+str(D_var)+'$')
                if(Rl==80):
                    plt.plot(x,Vo_80ohm_200,'ro-',linewidth=2.0,label=r'$Real: D = '+str(D_var)+'$')
                    plt.plot(minSQ_frecs,minSQ_80ohm_200,'rs-',linewidth=2.0,label=r'$\ Tendencia: D = '+str(D_var)+'$')
                elif(Rl==40):
                    plt.plot(x,Vo_40ohm_200,'ro-',linewidth=2.0,label=r'$Real: D = '+str(D_var)+'$')
                    plt.plot(minSQ_frecs,minSQ_40ohm_200,'rs-',linewidth=2.0,label=r'$\ Tendencia: D = '+str(D_var)+'$')
            D_var = D_var*2
            plt.title("Ro = "+str(Rl)+"[ohm]    L = "+str(L*1e6)+" [uHy]")
            plt.legend()
            plt.grid(True)
            major_ticks_fs=np.arange(16,46,2)
            ax.set_xticks(major_ticks_fs)
            ax.set_yticks(major_ticks_Vo)
            #plt.xlim(0,len(rc0)-1)
            plt.xlabel('Frecuencia [kHz]')
            plt.ylabel('Tensión de Salida Vo [V]')
    plt.show()
