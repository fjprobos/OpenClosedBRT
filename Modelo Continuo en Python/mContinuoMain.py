##Primer modelo continuo optimizacion de red##

#from gurobipy import*
from mContinuoClases import*
from mContinuoGraficos import*
from mContinuoResultados import*

#Primero comenzamos a setear los datos del modelo

sMin = 3
lambdap = 400.0#Segun DICTUC 2102, en Valdivia ese anio hubieron 21485822 viajes en tp mayor.
lambdac = 750.0#Segun DICTUC 2102, en hora punta manana 7:00-8:00 hay 8868 viajes en el sistema.
lambdaCBD = 1900.0
R = 0.6 #El area donde se nota mayor densidad al rededor de picarte mide unos 600 mts.
R1 = 1.5 #Desde Pedro Montt hasta la plaza hay 1,5 km.
beta = 5.5 #Desde la carcel hasta la municipalidad hay unos 5,5 km.
alpha = 3.9# Desde Luis Daman con Pedro Montt, hasta el final de la Corvi, hay unos 3,9 km
alpha1 = 1.1#La Corvi, tiene en promedio unos 1,4 km de ancho.
alpha2 = alpha-alpha1-R
beta1 = 4.0
beta2 = beta-beta1-R1
delta = 0.09766 #Penalidad por transferencia. Cercano a 5.86 minutos segun Raveau para una transferencia descendiente en metro de Santiago.
Va = 4.5###Buscar una fuente relevante
Vp = 25.0######Corresponde a los running speed, los cuales solo consideran la velocidad en movimiento. 25 es el promedio entre urbano poco denso, urbano medio y urbano densp en el modelo discreto.
Vc = 40.0######Velcoidad en Corredor. Lo mismo que fijamos para el modelo discreto.
#TODO Acá estan los tres parámetros a modificar sobre los tiempos de parada
tmuertop = 0.00166###Sale de Tirachini al parecer.Incluir en el escrito!!!
tpp = tmuertop + (Vp)*(1/15552.0+1/15552.0)*(1-1/2)#tiempo de detencion como tmuerto de parada mas demora por aceleracion/desacel menos el tiempo que hubiese ganado si no hubiese parado, es decir, la distancia de frenado y aceleracion a velocidad libre
tpc = tmuertop + (Vc)*(1/15552.0+1/15552.0)*(1-1/2)#Se utilizan unidades de Mkm y hr. De Tiachini 2014.a=1.2m/s^2 es el que utiliza Tirachini.
gammaV = 1498.0#Valor obtenido de "Precios Sociales Vigentes 2015" del Ministerio de Desarrollo Social.
gammaA = gammaV*2.185 #Costo del tiempo de acceso. De promedio de comparacion TE vsTV para hombres y mujeres Raveau 2014.
gammaE = gammaV*1.570 #Costo del tiempo de espera. De comparacion TE vs TV de Raveau 2014.
k = 0.8 #Constante para tiempo de espera en paraderos. Se hace sensibilidad respecto a este parámetro.
k_troncal = 0.6
theta = 0.1 #Coeficiente que se utiliza en la funcion de costos para el modelo de distribucion. Varia
rhop = 0.4 #Porcentaje de viajes atraidos por la periferia
rhoc = 0.3 #Porcentaje de viajes atraidos por el corredor
rhoCBD = 0.3 #Porcentaje de viajes atraidos por el CBD
ad = 182.4 #Costo de operacion fijo por km recorrido de bus
bd = 2.28 #Costo de operacion variable(por tamano) por km recorrido de bus
at = 4189.115 #Costo de operacion fijo por hora de operacion de un bus->No genera concavidad, cambia decimalmente.
bt = 13 #Costo de operacion variable(por tamano) por hora de operacion de un bus
tsp = 0.001123  #Tiempo de subida por persona en periferia. Se ocupan los valores promedio de Fernandez 2009.
tsc = 0.0004861 #Tiempo de subida o bajada por persona en corredor. Promedio de Tsubida de HCM 2000, en tirachini 2014.
tbp = 0.0006555#2,36 segundos tiempo de bajada por persona en periferia. Se ocupan los valores promedio de Fernandez 2009
tpVariable = True#->No genera concavidad al estar solo con ad
nivelRiqueza = (0.5, 2)#Parametro de nivel de riqueza de la ciudad. Multiplicara todos los valores asociados a las personas al hacer sensibilidad.
nivelDemandaTotal = (0.5, 2, 4)#Multiplicador de la demanda total de la ciudad. Multiplica los parametros de densidad de generacion en la sensibilidad.
nivelTheta = (0, 0.5, 1.5, 2, 3)#Multiplicador de la sensibilidad de la demanda ante el largo de los viajes. En parte, indica largo de viajes.
nivelDelta = (0, 0.5, 1.5, 2, 3)
nivelKEspera = (1, 1.2, 1.4, 1.6, 1.8, 2.0) #Ponderadores para sensibilidad erespecto a la constante de espera

ciudades = []

for g in range(0, 1):
    gammaV = 1498.0#Valor obtenido de "Precios Sociales Vigentes 2015" del Ministerio de Desarrollo Social.
    gammaA = gammaV*2.185 #Costo del tiempo de acceso. De promedio de comparacion TE vsTV para hombres y mujeres Raveau 2014.
    gammaE = gammaV*1.570 #Costo del tiempo de espera. De comparacion TE vs TV de Raveau 2014.
    #gammaV = gammaV*nivelRiqueza[g]
    #gammaA = gammaA*nivelRiqueza[g]
    #gammaE = gammaE*nivelRiqueza[g]
    #theta = 0.1
    #theta = theta*nivelTheta[g]
    #delta = 0.09766
    #delta = delta*nivelDelta[g]
    #lambdap = 400.0
    #lambdac = 750.0
    #lambdaCBD = 1900.0
    #lambdap = lambdap*nivelDemandaTotal[g]
    #lambdac = lambdac*nivelDemandaTotal[g]
    #lambdaCBD = lambdaCBD*nivelDemandaTotal[g]
    #k = k*nivelKEspera[g]

    city = ciudad(lambdap, lambdac, lambdaCBD, R, R1, beta, beta1, alpha, alpha1, Va, Vp, Vc, tpp, tpc, delta,
                  gammaV, gammaA, gammaE, k, sMin, rhop, rhoc, rhoCBD, theta, ad, bd, at, bt, tsp, tsc, tbp, tpVariable,
                  k_troncal)

    #resultadosNLineas(city)
    n = 5
    contador = 0
    for i in range(n, 26):
        print('Corriendo n='+str(i))
        city.agregarRedAbierta(i)
        city.agregarRedCerrada(i)
        opA = optimiScipy(city.red['Abierta'][contador])
        opC = optimiScipy(city.red['Cerrada'][contador])
        city.red['Abierta'][contador].actualizarFrecuencias(opA[0], opA[1])
        city.red['Cerrada'][contador].actualizarFrecuencias(opC[0], opC[1])
        #resultadosRed(city.red['Abierta'][contador],'ResFinalesPrueba1n'+str(n))
        contador += 1


    ##LISTAS PARA GUARDAR VARIABLES PARA GRAFICOS
    Varn = []
    VarCT = [[], []]
    VarCO = [[], []]
    VarTV = [[], []]
    VarTA = [[], []]
    VarTE = [[], []]
    VarTT = [[], []]
    VarDT = [[], []]
    VarQT = [[], []]
    VarTcD = [[], []]
    VarTsD = [[], []]
    VarFD = [[], []]
    VarTP = [[], []]
    VarTM = [[], []]
    nombreRedes = ('Abierta', 'Cerrada')

    for j in range(0, len(nombreRedes)):
        for r in city.red[nombreRedes[j]]:
            print('#######################################################################################################################')
            print(r.tipo+"-n= "+str(len(r.lineas)))
            ###INFO LINEAS###
            for l in r.lineas:
                print("ID"+str(l.ID))
                print("Capacidad Bus: "+str(l.cargaMaxima))
                print("Flota: "+str(l.flota))
                print("ASK: "+str(l.ASK))
                print("RPK: "+str(l.RPK))
                print("FO: "+str(l.FOPromedio))
                print("Ida")
                for mz in l.microZonas:
                    print(mz.ID+": "+str(l.infoCarga['Ida'][0][mz.ID])+"-"+str(l.infoCarga['Ida'][1][mz.ID])+"-"+str(l.infoCarga['Ida'][2][mz.ID])+"-"+str(l.infoCarga['Ida'][3][mz.ID])+"-tParada: "+str(l.tiemposParada['Ida'][mz.ID])+";",)
                print("Vuelta")
                for mz in l.microZonas:
                    print(mz.ID+": "+str(l.infoCarga['Vuelta'][0][mz.ID])+"-"+str(l.infoCarga['Vuelta'][1][mz.ID])+"-"+str(l.infoCarga['Vuelta'][2][mz.ID])+"-"+str(l.infoCarga['Vuelta'][3][mz.ID])+"-tParada: "+str(l.tiemposParada['Vuelta'][mz.ID])+";",)

                print(" f: "+str(l.f))#", dp: "+str(l.distanciaPeriferia)+", pp: "+str(l.paradasPeriferia)+", dc: "+str(l.distanciaCorredor)+", pc: "+str(l.paradasCorredor)+", CostoLinea: "+str(r.CostosLineas[l.ID])

            ##INFOR MACROZONAS
            #print("n= "+str(n)+", CP= "+str(r.macroZonas['CP'].nMicroZonas)+", demanda= "+str(r.macroZonas['CP'].anchoEfectivo*r.macroZonas['CP'].largo*r.macroZonas['CP'].densidadDemanda),
            #print(", CBD= "+str(r.macroZonas['CBD'].nMicroZonas)+", demanda= "+str(r.macroZonas['CBD'].anchoEfectivo*r.macroZonas['CBD'].largo*r.macroZonas['CBD'].densidadDemanda),
            #print(", CO= " + str(r.macroZonas['CO'].nMicroZonas)+", demanda= "+str(r.macroZonas['CO'].anchoEfectivo*r.macroZonas['CO'].largo*r.macroZonas['CO'].densidadDemanda)
            #directa = 0
            #dem0 = 0
            #for od in r.ODs:
            #    if(od.destino.MZ=='CBD'):
            #        print("ID: "+str(od.ID)+" Demanda: "+str(od.demandaTotal)+", "
            #     if od.origen.ID=="PN1":
            #         dem0 += od.demandaTotal
            #print(r.macroZonas['PN'].microZonas[1].demandaO
            #print(dem0
            #print("DemandaAtraidaCBD= "+str(suma)
            #print("CostoOperacionTotal = "+str(r.CostoOperacion)
            #print("CostoViajeTotal = "+str(r.CostoTotaltViaje)
            #print("CostoEsperaTotal = "+str(r.CostoTotaltEspera)
            #print("CostoAccesoTotal = "+str(r.CostoTotaltAcceso)
            #print("CostoTransferenciaTotal = "+str(r.CostoTotaltTransferencia)
            #print("Espera Total = "+str(r.CostoTotaltTransferencia+r.CostoTotaltEspera)
            #print("Costo Total = "+str(r.CostoTotal)
            #print("Demanda Directa = "+str(directa)

            ##DATOS PARA GRAFICOS
            if j == 0:
                Varn.append(n)
            VarCT[j].append(r.CostoTotal)
            VarCO[j].append(r.CostoOperacion)
            VarTV[j].append(r.CostoTotaltViaje)
            VarTA[j].append(r.CostoTotaltAcceso)
            VarTE[j].append(r.CostoTotaltEspera)
            VarTT[j].append(r.CostoTotaltTransferencia)
            VarDT[j].append(r.demandaIndirecta)
            VarQT[j].append(r.Transferencias)
            VarTcD[j].append(r.TotaltTransferencia)
            VarTsD[j].append(r.TotaltTransferenciaSinDelta)
            VarFD[j].append(r.frecPorDistancia)
            VarTP[j].append(r.CostoTotaltParada)
            VarTM[j].append(r.CostoTotaltMovimiento)
            n += 1

    #Crear Graficos
    for nred in range(3, 3+len(city.red['Abierta'])):
        crearExcelRed(city.red['Abierta'][nred-3], 'Resultados_V4.0_sensibilidad_BaseNewQ&K_'+str(g)+'_Abierta_n'+str(len(city.red['Abierta'][nred-3].lineas)))
    for nred in range(3, 3+len(city.red['Cerrada'])):
        crearExcelRed(city.red['Cerrada'][nred-3], 'Resultados_V4.0_sensibilidad_BaseNewQ&K_'+str(g)+'_Cerrada_n'+str(len(city.red['Cerrada'][nred-3].lineas)))
    crearExcelnLineas('nLineasResultados_V4.0_Caso_BaseNewQ&K_'+str(g), ('n', Varn), VarCT, VarCO, VarTV, VarTA, VarTE, VarTT, VarDT, VarQT, VarTcD, VarTsD, VarFD, VarTP, VarTM)
    ciudades.append(city)
crearExcelCiudades(ciudades)

#TODO Resolver el Bug cuando el nCBD es relativamente muy grande. Al parecer el problema esta cuando se empiezan a parear las microzonas del CO.-> Para magnitudes modeladas no alcanza a ser problema. Se arreglara en casod e ser necesario.
#TODO Verificar de alguna forma que las cargas de pasajeros en buses se estan haciendo correctamente.
#TODO encontraar error por descuadre de rpk entre abierto y cerrado
#TODO Revisar calculo de factor de ocupacion. Segun Gschwender esta muy alto.->Si no, argumentar porque es tan alto.