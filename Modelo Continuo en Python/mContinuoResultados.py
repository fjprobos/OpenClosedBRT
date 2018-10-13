__author__ = 'Pancho'

from mContinuoClases import*
from mContinuoGraficos import*

####Aca vamos a poner de forma ordenada los metodos que nos permitiran generar distintos tipos de resultados.
####Sera una forma de ordenar lo que esta actualmente en el mail, e ir relacionando lo que se requiere, con los
##metodos internos del programa, y los metodos para guardar datos de resultados en excel

def resultadosNLineas(ciudad):
    '''

    :param ciudad: Ciudad a trabajar. Nos esta optimizada, simplemente creada en base a parametros de input.
    En principio, vamos a asumir que el n optimo para esta ciudad se encuentra entre 5 y 20.
    :return:No retorna nada. Carga distintas redes sobre la ciudad e identifica la optima. Adicionalmente genera
    un excel con los resultados en funcion de n.
    '''

    n = 3
    for i in range(n, 18):
        ciudad.agregarRedAbierta(i)
        ciudad.agregarRedCerrada(i)
        opA = optimiScipy(ciudad.red['Abierta'][i-n])
        opC = optimiScipy(ciudad.red['Cerrada'][i-n])
        ciudad.red['Abierta'][i-n].actualizarFrecuencias(opA[0], opA[1])
        ciudad.red['Cerrada'][i-n].actualizarFrecuencias(opC[0], opC[1])



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
        for r in ciudad.red[nombreRedes[j]]:
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
    crearExcelnLineas('resultadosNLineasReunionJCyGSCH', ('n', Varn), VarCT, VarCO, VarTV, VarTA, VarTE, VarTT, VarDT, VarQT, VarTcD, VarTsD, VarFD, VarTP, VarTM)

def resultadosRed(red, nombrePrueba):
    '''
    :param red:
    :return:No retorna nada. Simplemente obtiene todos los parametros de interes de esta red.
    Adicionalmente, muestra como van mejorando sus resultados al ir avanzando la optimizacion.
    '''

    #Primero optimizamos la red
    opA = optimiScipy(red)
    red.actualizarFrecuencias(opA[0], opA[1])

    #Luego Creamos excel con sus resultados
    crearExcelRed(red, nombrePrueba)

def resultadosDistribucion(ciudadBase):
    '''

    :param ciudadBase: Ciudad a partir de la cual se elaboran los resultados. Se optimiza para buscar su n optimo y luego
     se va variando el beta (para ambos lados) para ir optimizando estas nuevas ciudades. Luego con el arreglo de redes
     optimas se genera un excel.
    :return: Eventualmente puede retornar el arreglo de redes optimas segun el beta.
    '''
    #Primero obtenemos entonces el n optimo tanto para red abierta como cerrada del caso inicial de ciudad
    abiertasCasoBase = []
    cerradasCasoBase = []

    #Primero agregamos redes a la ciudad dentro de un rango de enes. Optimizamos cada una de esas redes
    for i in range(4, 15):
        ciudadBase.agregarRedAbierta(i)
        ciudadBase.agregarRedCerrada(i)
        opA = optimiScipy(ciudadBase.red['Abierta'][i-4])
        opC = optimiScipy(ciudadBase.red['Cerrada'][i-4])
        ciudadBase.red['Abierta'][i-4].actualizarFrecuencias(opA[0], opA[1])
        ciudadBase.red['Cerrada'][i-4].actualizarFrecuencias(opC[0], opC[1])

    #Obtenemos ambas listas de redes para el caso base.
    abiertasCasoBase = ciudadBase.red['Abierta']
    cerradasCasoBase = ciudadBase.red['Cerrada']

    #Buscamos la red optima y obtenemos su n
    cerradaMin = encontrarNOptimo(cerradasCasoBase)
    abiertaMin = encontrarNOptimo(abiertasCasoBase)
    nMinC = cerradaMin.n
    nMinA = abiertaMin.n

    #Ahora comenzaremos a crear nuevas ciudades.

    #Primero creamos el set de theta a probar
    thetaOriginal = ciudadBase.theta
    setTheta = []
    for i in range(1, 9):
        setTheta.append(thetaOriginal + (i - 4)*0.1)

    #Luego creamos las ciudades
    ciudades = []
    for i in range(9):
        if i < 4:
            ciudad = ciudad(ciudadBase.lambdap, ciudadBase.lambdac, ciudadBase.lambdaCBD, ciudadBase.R, ciudadBase.R1,
                            ciudadBase.beta, ciudadBase.beta1, ciudadBase.alpha, ciudadBase.alpha1, ciudadBase.Va,
                            ciudadBase.Vp, ciudadBase.Vc, ciudadBase.tpp, ciudadBase.tpc, ciudadBase.delta,
                            ciudadBase.gammaV, ciudadBase.gammaA, ciudadBase.gammaE, ciudadBase.k, ciudadBase.sMin,
                            ciudadBase.rhop, ciudadBase.rhoc, ciudadBase.rhoCBD, setTheta[i], ciudadBase.ad,
                            ciudadBase.bd, ciudadBase.at, ciudadBase.bt, ciudadBase.ts, ciudadBase.tpVariable)
            ciudades.append(ciudad)
        elif i == 4:
            ciudades.append(ciudadBase)
        else:
            ciudad = ciudad(ciudadBase.lambdap, ciudadBase.lambdac, ciudadBase.lambdaCBD, ciudadBase.R, ciudadBase.R1,
                            ciudadBase.beta, ciudadBase.beta1, ciudadBase.alpha, ciudadBase.alpha1, ciudadBase.Va,
                            ciudadBase.Vp, ciudadBase.Vc, ciudadBase.tpp, ciudadBase.tpc, ciudadBase.delta,
                            ciudadBase.gammaV, ciudadBase.gammaA, ciudadBase.gammaE, ciudadBase.k, ciudadBase.sMin,
                            ciudadBase.rhop, ciudadBase.rhoc, ciudadBase.rhoCBD, setTheta[i-1], ciudadBase.ad,
                            ciudadBase.bd, ciudadBase.at, ciudadBase.bt, ciudadBase.ts, ciudadBase.tpVariable)
    #Ahora las optimizamos
def resultadosDensidadDemanda(ciudadBase):
    '''

    :param ciudadBase: Ciudad a partir de la cual se elaboran los resultados. Se optimiza para buscar su n optimo y luego
     se va variando el beta (para ambos lados) para ir optimizando estas nuevas ciudades. Luego con el arreglo de redes
     optimas se genera un excel.
    :return: Eventualmente puede retornar el arreglo de redes optimas segun el beta.
    '''

def resultadosPenalidadTransbordo(ciudadBase):
    '''

    :param ciudadBase: Ciudad a partir de la cual se elaboran los resultados. Se optimiza para buscar su n optimo y luego
     se va variando el beta (para ambos lados) para ir optimizando estas nuevas ciudades. Luego con el arreglo de redes
     optimas se genera un excel.
    :return: Eventualmente puede retornar el arreglo de redes optimas segun el beta.
    '''


def encontrarNOptimo(redes):
    '''

    :param redes: lista de redes de una misma ciudad que varian en su n.
    :return: retorna la red de menor Costo Total
    '''
    CMin = 1000000000000000
    redMin = None
    for red in redes:
        if red.CostoTotal < CMin:
            CMin = red.CostoTotal
            redMin = red

    return redMin