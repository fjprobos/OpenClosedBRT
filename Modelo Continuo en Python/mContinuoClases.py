__author__ = 'Pancho'

from mContinuoFunciones import*
import copy

class macroZona(object):
    def __init__(self, densidadDemanda, ancho, largo, nombre):
        self.densidadDemanda = densidadDemanda
        self.anchoIndicado = ancho
        self.anchoEfectivo = 0
        self.largo = largo
        self.areaOriginal = ancho*largo
        self.lineas = []
        self.demandaO = ancho * largo * densidadDemanda
        self.demandaD = 0
        self.demandaDirecta = 0
        self.demandaIndirecta = 0
        self.tEspera = 0
        self.tTransferencia = 0
        self.nombre = nombre
        self.microZonas = []
        self.spacing = 0
        self.nMicroZonas = 0

    def agregarLinea(self, linea):
        self.lineas.append(linea)

    def agregartEspera(self, ods):
        tEsperaTotal = 0
        for od in ods:
            tEsperaTotal += od.tEspera
        self.tEspera = tEsperaTotal / float(len(ods))


class microZona(macroZona):
    def __init__(self, densidadDemanda, ancho, largo, MZ, lugar, lugarCorredor, vel, demandaD):
        self.densidadDemanda = densidadDemanda
        self.ancho = ancho
        self.largo = largo
        self.recorrido = 0
        if (MZ == "PN" or MZ == "PS"):
            self.recorrido = self.largo
        else:
            self.recorrido = self.ancho
        #El tiempo de recorrido solo contempla el tiempo de viaje en movimiento. Faltan las paradas.
        #El tiempo por paradas se asigna por cada linea ya que depende de la combinacion MZ/linea.
        self.tRecorrido = self.recorrido/vel
        self.lineas = []
        self.demandaO = ancho * largo * densidadDemanda
        self.demandaD = demandaD
        self.demandaDirecta = 0
        self.demandaIndirecta = 0
        self.tEspera = 0
        self.tTransferencia = 0
        self.MZ = MZ
        self.lugar = lugar
        self.ID = MZ + str(lugar)
        self.lugarCorredor = lugarCorredor
        self.spacing = 0
        self.paradas = 0
        self.MZ_corredor = False
        if MZ[0] == 'C':
            self.MZ_corredor = True
    # Aca definimos el operador les than "<" para microzona, a modo de comparar ubicaciones entre ellas.
    def __lt__(self, other):
        return self.lugarCorredor < other.lugarCorredor

    def __le__(self, other):
        return self.lugarCorredor <= other.lugarCorredor

    def __gt__(self, other):
        return self.lugarCorredor > other.lugarCorredor

    def setSpacing(self, s):
        self.spacing = s
        if self.MZ == 'PN' or self.MZ == 'PS':
            self.paradas = self.largo/self.spacing
        else:
            self.paradas = self.ancho/self.spacing


class OD(object):
    """
    Objeto definifo por dos zonas, se espera que los OD tengan sus lineas asignadas, de manera que se pueda definir el conjunto
    de elementos en comun, lo cual define las lineas que sirven para ir de una zona a otra de forma directa.
    Si no hya lineas directas, habra que buscar el mejor nodo de transferencia.
    El output es una lista con tres celdas: 1)Lista con las lineas que salen del origen (zonaA), 2)Nodo de transferencia
    3)Lista con las lineas que salen del nodo de transferencia al destino. Si hay viajes directos, celdas 2 y 3 estan en None.
    """

    def __init__(self, origen, destino, demandaTotalRed, Vp, Vc, Va, k, tpp, tpc, tipo, delta, k_troncal, brt_cerrado):
        self.origen = origen
        self.destino = destino
        self.Vp = Vp
        self.Vc = Vc
        self.Va = Va
        self.k = k
        self.k_troncal = k_troncal
        self.tpp = tpp
        self.tpc = tpc
        self.tipo = tipo
        self.deltaTT = delta
        self.ID = origen.ID + "/" + destino.ID
        self.demandaTotal = 0
        self.demandaDirecta = 0
        self.demandaIndirecta = 0
        self.demandaTotalRed = demandaTotalRed
        self.ruta = OD.ruta(self, origen, destino, tipo)#La ruta consiste en una lista de tres elementos con las lineas disponibles para el origen, el nodo de transferencia y laslineas de destino. Si hay lineas directas las celdas dos y tres quedan con 'None'
        self.path = obtenerPath(self)
        self.nTransferencias = 0
        if self.ruta[2]==None:
            self.demandaDirecta = self.demandaTotal
            self.nTransferencias = 0
        else:
            self.demandaIndirecta = self.demandaTotal
            if self.ruta[4] == None:
                self.nTransferencias = 1
            else:
                self.nTransferencias = 2
        if origen.MZ_corredor and brt_cerrado:
            self.tEspera = calcularTiempoEspera(self, k_troncal, False)
        else:
            self.tEspera = calcularTiempoEspera(self, k, False)
        if not self.nTransferencias == 0:
            if brt_cerrado:
                self.tTransferencia = calcularTiempoEspera(self, k_troncal, True)
            else:
                self.tTransferencia = calcularTiempoEspera(self, k, True)
        else:
            self.tTransferencia = 0
        self.tAcceso = calcularTiempoAcceso(self, Va)
        self.dist = calcularDistanciaMovimiento(self)
        self.distanciaPeriferia = self.dist[0]
        self.distanciaCorredor = self.dist[1]
        self.distanciaOD = self.distanciaPeriferia +self.distanciaCorredor
        self.distanciaTotal = self.demandaTotal*self.distanciaOD
        self.tParadas = None
        self.tParadaPeriferia = 0
        self.tParadaCorredor = 0
        self.tParadaFijo = 0
        self.tParadaVariable = 0
        self.tMovimientoPeriferia = self.distanciaPeriferia/self.Vp
        self.tMovimientoCorredor = self.distanciaCorredor/self.Vc
        self.tViaje = self.tMovimientoPeriferia + self.tMovimientoCorredor + self.tParadaCorredor + self.tParadaCorredor
        self.TotaltMovimiento = 0
        self.TotaltParada = 0
        self.TotaltParadaFijo = 0
        self.TotaltParadaVariable = 0
        self.TotaltViaje = 0
        self.TotaltAcceso = 0
        self.TotaltEspera = 0
        self.TotaltTransferencia = 0
        self.TotaltTransferenciaSinDelta = 0
        self.TotalNTransferencias = 0


    # Este primer metodo se ocupara para generar el conjunto de lineas que sirven para ir de un punto al otro.
    #n la practica, las lineas comunes se utilizan mas cuando estamos tratando un OD de microzonas.
    def lineasComunes(self, origen, destino):
        lineas = [l for l in origen.lineas if l in destino.lineas]
        return lineas


    def ruta(self, origen, destino, tipo):
        '''
        Este metodo sera el que entregara la ruta de los pasajeros, mediante las lineas comunes que llevan directamente, o bien
        mediante lineas entre los puntos de transferencia.
        return: [lineas 1er tramo, nodo 1er trans, lineas 2o tramo, nodo 2a trans, lineas 3er tramo]
        '''
        lineas = OD.lineasComunes(self, origen, destino)
        #Si no existen lineas directas, se procede a buscar el conjunto de lineas que generan una unica ruta. Para esta ruta, se define
        #uno o dos puntos de intercambio par ael caso de la red cerrada.
        if lineas == []:
            #Cuando hay transferencias tendremos que discriminar entre
            if tipo == 'Cerrada':
                lineast1 = []
                lineast2 = []
                if origen.MZ == 'PN' or origen.MZ == 'PS':
                    lineas.append(origen.lineas[0])
                    for n in origen.lineas[0].microZonas:
                        if n.MZ == 'CP' or (n.MZ == 'CBD' or n.MZ == 'CO'):
                            trans1 = n
                    for l in trans1.lineas:
                        for n in l.microZonas:
                            if n.lugarCorredor == destino.lugarCorredor:
                                lineast1.append(l)
                                if n == destino:
                                    return [lineas, trans1, lineast1, None, None]
                                else:
                                    trans2 = n
                                    lineast2.append(destino.lineas[0])
                                    return [lineas, trans1, lineast1, trans2, lineast2]
                else:#En este caso como el orgien esta en el corredor, habra a lo mas una transferencia.
                    for l in origen.lineas:
                        for n in l.microZonas:
                            if n.lugarCorredor == destino.lugarCorredor:
                                lineas.append(l)
                                trans1 = n
                                lineast1.append(destino.lineas[0])
                                return [lineas, trans1, lineast1, None, None]

            elif tipo == 'Abierta':
                nodosTrans = [n for l in origen.lineas for n in l.microZonas if tranferenciaRazonable(origen, destino, n)]
                #Ya que tenemos el set de nodos de transferencia factible, vemos cual sera en definitiva donde transbordaran los pasajeros.
                #Esto esta dado por el numero de lineas a destino que hayan en el nodo de transferencia.
                #Ojo que este criterio debiese ser el tiempo de espera, pero aun no sabemos la frecuencia que tendran los servicios.
                lineasMax = 0
                nodoTrans = None
                lineasTrans = []
                for n in nodosTrans:
                    count = 0
                    for l in n.lineas:
                        if l in destino.lineas:
                            count += 1
                    if count > lineasMax:
                        lineasMax = count
                        nodoTrans = n
                for l in nodoTrans.lineas:
                    if l in destino.lineas:
                        lineasTrans.append(l)
                for l in nodoTrans.lineas:
                    if l in origen.lineas:
                        lineas.append(l)
                return [lineas, nodoTrans, lineasTrans, None, None]
        else:
            return [lineas, None, None, None, None]


    def actualizarDemanda(self):
        '''
        Estem metodo se utiliza para actualizar parametros que quedearon seteados en cero en la creacion del OD.
        Como por ejemplo tras distribuir la demanda.
        '''
        if self.ruta[2] == None:
            self.demandaDirecta = self.demandaTotal
        else:
            self.demandaIndirecta = self.demandaTotal
        self.TotaltMovimiento = (self.tMovimientoPeriferia + self.tMovimientoCorredor)*self.demandaTotal
        self.TotaltParada = (self.tParadaPeriferia + self.tParadaCorredor)*self.demandaTotal
        self.TotaltViaje =self.tViaje*self.demandaTotal
        self.TotaltAcceso = self.tAcceso*self.demandaTotal
        self.TotaltEspera = self.tEspera*self.demandaTotal
        self.TotaltTransferencia = (self.tTransferencia+self.deltaTT*self.nTransferencias)*self.demandaIndirecta
        self.TotaltTransferenciaSinDelta = (self.tTransferencia)*self.demandaIndirecta
        self.TotalNTransferencias = self.demandaIndirecta*self.nTransferencias
        self.distanciaTotal = self.demandaTotal*self.distanciaOD


class linea(object):
    """
    El objeto linea corresponde a un servicio. Es importante senalar que ocupa una relacion bidireccional con las zonas por las que
    pasa. Para generar esot mas facilmente, el constructor asigna la misma linea a las zonas que esta asignando.
    Habra que ver si funciona hacer esto en el mismo constructor.
    """
    ID = 0

    def __init__(self, macroZonas, microZonas, esTroncal):
        self.microZonas = microZonas
        self.macroZonas = macroZonas
        self.esTroncal = esTroncal
        #La info de carga debe estar separada segun direccion del servicio.
        #Esta tupla contiene cuatro diccionarios con la informacion de carga de pasajeros(0),
        # los que suben(1) y bajan(2) y el factor de ocupacion en ese punto(3) dentro del bus para la microzona dada por la llave.
        self.infoCarga = {}
        self.infoCarga["Ida"] = ({}, {}, {}, {})
        self.infoCarga["Vuelta"] = ({}, {}, {}, {})
        self.cargaMaxima = 0
        #Ocuparemos un diccionario parecido a infoCarga para ir registrando los tiempos de parada
        self.tiemposParada = {}
        self.tiemposParada["Ida"] = {}
        self.tiemposParada["Vuelta"] = {}
        self.tParada = 0  #Tiempo de parada total
        self.tCirculacion = 0  #Tiempo en movimiento
        if esTroncal:
            self.f = 10
        else:
            self.f = 10
        self.tCiclo = 0
        #Los tres siguientes indicadores se utilizan para medir la utilizacion de la capacidad del bus. Los tres se actualizan al terminar el metodo de asignar carga.
        self.ASK = 0
        self.RPK = 0
        self.FOPromedio = 0
        self.cargaPromedio = 0
        self.ID = linea.ID
        linea.ID += 1
        self.distanciaPeriferia = 0
        self.distanciaCorredor = 0
        self.paradasPeriferia = 0
        self.paradasCorredor = 0
        self.flota = self.f*self.tCiclo
        self.velocidadComercial = 0
        #Aca se agregan distancias tanto en periferia como corredor, y tiempos de viaje sobre las microzonas
        #Ojo que aca solo esta el tiempo en movimiento. Al asignar carga habra que sumar al tiempo de ciclo las paradas.
        for mz in microZonas:
            self.tCirculacion += mz.tRecorrido*2#Se multiplica por dos para considerar el recorrido ida y vuelta!
            if (mz.MZ == "PN" or mz.MZ == "PS"):
                self.distanciaPeriferia += mz.recorrido
            else:
                self.distanciaCorredor += mz.recorrido
        #Aca esperamos asignar la linea a las zonas que ella mismo se asigno.
        for z in microZonas:
            z.agregarLinea(self)
        for z in macroZonas:
            z.agregarLinea(self)

    def setParadas(self):
        for mz in self.microZonas:
            if (mz.MZ == "PN" or mz.MZ == "PS"):
                self.paradasPeriferia += mz.paradas
            else:
                self.paradasCorredor += mz.paradas

class red(object):
    '''
    La red contiene toda la informacion necesaria para generar nuestro modelo, es decir, tiene la informacion de la ciudad a traves
    de las macrozonas, mas la informacion del servicio de tp dado por las lineas.
    La idea es que tanto las lineas como las macrozonas sean unicas para esta red, es decir, se generen como tipos aparte y no referencias
    a otros ya existentes.
    La variable tipo indica el tipo de red (ej: cerrada, abierta, etc..)
    La variable troncal es una var de tipo linea que referencia al troncal para casos de redes cerradas.
    '''

    def __init__(self, lineas, troncal, tipo, macroZ, Vp, Vc, Va, k, gammaV, gammaA, gammaE, sp, sc, tpp, tpc, delta,
                 theta, ad, bd, at, bt, tsp, tsc, tbp, alpha, alpha1, alpha2, beta, beta1, beta2, R, lambdap, lambdac,
                 lambdaCBD, tpVariable, n, k_troncal):
        self.lineas = lineas
        self.troncal = troncal
        self.brt_cerrado = False
        if tipo == 'Cerrada':
            self.lineas.append(self.troncal)
            self.brt_cerrado = True
        self.tipo = tipo
        self.macroZonas = macroZ
        self.Vp = Vp
        self.Vc = Vc
        self.Va = Va
        self.k = k
        self.gammaV = gammaV
        self.gammaA = gammaA
        self.gammaE = gammaE
        self.sp = sp
        self.sc = sc
        self.tpp =tpp
        self.tpc =tpc
        self.delta = delta
        self.theta = theta
        self.ad = ad
        self.bd = bd
        self.at = at
        self.bt = bt
        self.tsp = tsp
        self.tsc = tsc
        self.tbp = tbp
        self.alpha = alpha
        self.alpha1 = alpha1
        self.alpha2 = alpha2
        self.beta = beta
        self.beta1 = beta1
        self.beta2 = beta2
        self.R = R
        self.lambdap = lambdap
        self.lambdac = lambdac
        self.lambdaCBD = lambdaCBD
        self.tpVariable = tpVariable
        self.n = n #No es el numero de lineas, sino el n que lo creo.
        self.demandaTotal = 0
        for j in self.macroZonas:
            self.demandaTotal += self.macroZonas[j].demandaO
        # Generamos en este punto todos los OD de la red, como conjunto de microzonas y no a nivel de macrozonas.
        #Quizas despues podemos agregar otra lista de OD a nivel de macrozonas.
        self.ODs = []
        for mazO in self.macroZonas:
            for mizO in self.macroZonas[mazO].microZonas:
                for mazD in self.macroZonas:
                    for mizD in self.macroZonas[mazD].microZonas:
                        od = OD(mizO, mizD, self.demandaTotal, Vp, Vc, Va, k, tpp, tpc, tipo, delta, k_troncal, self.brt_cerrado)
                        self.ODs.append(od)
        self.DatosTransferencias = self.getTransferencias()
        self.demandaIndirecta = self.DatosTransferencias[0]
        self.demandaDirecta = self.demandaTotal-self.demandaIndirecta
        self.Transferencias = self.DatosTransferencias[1]
        self.TiemposPersonas = self.getTiempoPersonas()
        self.TotaltViaje = self.TiemposPersonas[0]
        self.TotaltEspera = self.TiemposPersonas[1]
        self.TotaltAcceso = self.TiemposPersonas[2]
        self.TotaltTransferencia = self.TiemposPersonas[3]
        self.TotaltTransferenciaSinDelta = self.TiemposPersonas[4]
        self.TotaltMovimiento = self.TiemposPersonas[5]
        self.TotaltParada = self.TiemposPersonas[6]
        self.TotaltParadaFijo = self.TiemposPersonas[7]
        self.TotaltParadaVariable = self.TiemposPersonas[8]
        self.CostoTotaltMovimiento = self.TotaltMovimiento*gammaV
        self.CostoTotaltParada = self.TotaltParada*gammaV
        self.CostoTotaltViaje = self.TotaltViaje*gammaV
        self.CostoTotaltEspera = self.TotaltEspera*gammaE
        self.CostoTotaltAcceso = self.TotaltAcceso*gammaA
        self.CostoTotaltTransferencia = self.TotaltTransferencia*gammaE
        self.Costos = 0
        self.CostosLineas = 0
        self.CostoOperacion = 0
        self.CostoTotal = self.CostoOperacion + self.CostoTotaltViaje + self.CostoTotaltEspera + self.CostoTotaltAcceso + self.CostoTotaltTransferencia
        self.tMovimientoPromedio = self.TotaltMovimiento/self.demandaTotal
        self.tParadaPromedio = self.TotaltParada/self.demandaTotal
        self.tViajePromedio = self.TotaltViaje/self.demandaTotal
        self.tEsperaPromedio = self.TotaltEspera/self.demandaTotal
        self.tAccesoPromedio = self.TotaltAcceso/self.demandaTotal
        self.tTransferenciaSinDeltaPromedio = self.TotaltTransferenciaSinDelta/self.demandaTotal
        self.tTransferenciaPromedio = self.TotaltTransferencia/self.demandaTotal
        self.CostoTotaltViajePromedio = self.CostoTotaltViaje/self.demandaTotal
        self.CostoTotaltMovimientoPromedio = self.CostoTotaltMovimiento/self.demandaTotal
        self.CostoTotaltParadaPromedio = self.CostoTotaltParada/self.demandaTotal
        self.CostoTotaltEsperaPromedio = self.CostoTotaltEspera/self.demandaTotal
        self.CostoTotaltAccesoPromedio = self.CostoTotaltAcceso/self.demandaTotal
        self.CostoTotaltTransferenciaPromedio = self.CostoTotaltTransferencia/self.demandaTotal
        self.CostoOperacionPromedio = self.CostoOperacion/self.demandaTotal
        self.CostoTotalPromedio = self.CostoTotal/self.demandaTotal
        self.transferenciasPromedio = self.Transferencias/self.demandaTotal
        self.FOPromedio = 0 #Factor de ocupacion promedio de los buses de la red.
        self.FlotaTotal = 0
        self.CapacidadPromedio = 0
        self.CapacidadOciosaTotal = 0
        self.frecuenciaPromedio = 0
        self.vComercialPromedio = 0
        self.distanciaTotal = 0
        self.largoViajePromedio = 0
        #Crearemos un diccionario que ira guardando los indicadores de la red para cada valor de F que se tome. De esta manera podremos graficar cambios respecto a F.
        #Quizas simplemente podemos hacer un clon de la red(aunque eso puede tardar mucho).
        self.resultadosPorFrecuencia = {}#La llave corresponde a un id dado por la iteracion
        self.iteracion = 0#Contador de iteraciones del optimizador
        self.frecPorDistancia = 0


    def getTiempoPersonas(self):
        TotaltViaje = 0
        TotaltEspera = 0
        TotaltAcceso = 0
        TotaltTransferencia = 0
        TotaltTransferenciaSinDelta = 0
        TotaltMovimiento = 0
        TotaltParada = 0
        TotaltParadaFijo = 0
        TotaltParadaVariable = 0

        for od in self.ODs:
            TotaltViaje += od.TotaltViaje
            TotaltEspera += od.TotaltEspera
            TotaltAcceso += od.TotaltAcceso
            TotaltTransferencia += od.TotaltTransferencia
            TotaltTransferenciaSinDelta += od.TotaltTransferenciaSinDelta
            TotaltMovimiento += od.TotaltMovimiento
            TotaltParada += od.TotaltParada
            TotaltParadaFijo += od.TotaltParadaFijo
            TotaltParadaVariable += od.TotaltParadaVariable
        return (TotaltViaje, TotaltEspera, TotaltAcceso, TotaltTransferencia, TotaltTransferenciaSinDelta, TotaltMovimiento, TotaltParada, TotaltParadaFijo, TotaltParadaVariable)

    def getTransferencias(self):
        DemandaIndirecta = 0
        Transferencias = 0

        for od in self.ODs:
            DemandaIndirecta += od.demandaIndirecta
            Transferencias += od.TotalNTransferencias
        return (DemandaIndirecta, Transferencias)

    def actualizarFrecuencias(self, f, dicLineas):
        '''

        :param f: lista con las frecuencias ordenadas por el id del metodo de optimizacion.
        :param dicLineas: diccionario ocupado en el solver para relacionar id del solver ocn id de la linea en el modelo.
        :return:Nada, simplemente actualiza las frecuencias y los parametros asociados a ella.
        '''
        #Antes de comenzar a actualizar, clonamos la red actual y la guardamos en el diccionario de esta.
        red = copy.copy(self)
        self.resultadosPorFrecuencia[self.iteracion] = red
        self.iteracion += 1
        self.frecPorDistancia = 0
        self.FOPromedio = 0
        self.FlotaTotal = 0
        self.CapacidadPromedio = 0
        self.CapacidadOciosaTotal = 0
        self.frecuenciaPromedio = 0
        self.vComercialPromedio = 0

        #Primero actualizamos las frecuencias de las lineas y la flota requerida(y la frac*dist para efectos de resultados)
        for l in self.lineas:
            i = dicLineas[l.ID]
            l.f = f[i]
            l.flota = l.f*l.tCiclo
            self.frecPorDistancia += l.f*(l.distanciaCorredor+l.distanciaPeriferia)

        #Luego debemos reasignar la carga para poder calcular los indicadores de costos par ausuarios y operacion.
        self.asignarCarga()

        #Con la carga reasignada, podemos recalcular los indicadores que dependen de ella.
        sumaFO = 0
        sumaCapacidadPromedio = 0
        sumaFrecuencia = 0
        sumavComercial = 0
        for l in self.lineas:
            sumaFO += l.FOPromedio*l.f*(l.distanciaCorredor+l.distanciaPeriferia)
            sumaCapacidadPromedio += l.cargaMaxima*l.f*(l.distanciaCorredor+l.distanciaPeriferia)
            sumaFrecuencia += l.f*l.f*(l.distanciaCorredor+l.distanciaPeriferia)
            sumavComercial += l.velocidadComercial*l.f*(l.distanciaCorredor+l.distanciaPeriferia)
            self.CapacidadOciosaTotal += l.ASK-l.RPK
            self.FlotaTotal += l.flota
        self.FOPromedio = sumaFO/self.frecPorDistancia
        self.CapacidadPromedio = sumaCapacidadPromedio/self.frecPorDistancia
        self.frecuenciaPromedio = sumaFrecuencia/self.frecPorDistancia
        self.vComercialPromedio = sumavComercial/self.frecPorDistancia

        #Luego actualizamos los costos de operacion
        self.Costos = calcularCostoOperacion(self)
        self.CostosLineas = self.Costos[1]
        self.CostoOperacion = self.Costos[0]

        #Tambien actualizamos tiempos de espera en paradero, en transferencias y de viajes(por tiempo parada)
        #En estos casos tendremos que actualizar los tiempos de cada OD
        self.TotaltParada = 0
        self.TotaltParadaFijo = 0
        self.TotaltParadaVariable = 0
        self.TotaltViaje = 0
        self.TotaltEspera = 0
        self.TotaltTransferencia = 0
        self.TotaltTransferenciaSinDelta = 0
        self.TotaltAcceso = 0
        for od in self.ODs:
            od.tParadas = calcularTiempoParadas(od, self.tpVariable, self.tpp, self.tpc, self.sp, self.sc)
            od.tParadaPeriferia = od.tParadas[0]
            od.tParadaCorredor = od.tParadas[1]
            od.tParadaFijo = od.tParadas[2] + od.tParadas[3]
            od.tParadaVariable = od.tParadaCorredor + od.tParadaPeriferia - od.tParadaFijo
            od.tViaje = od.tMovimientoPeriferia + od.tParadaPeriferia + od.tMovimientoCorredor + od.tParadaCorredor
            od.tAcceso = calcularTiempoAcceso(od, self.Va)

            if od.origen.MZ_corredor and self.brt_cerrado:
                od.tEspera = calcularTiempoEspera(od, od.k_troncal, False)
            else:
                od.tEspera = calcularTiempoEspera(od, od.k, False)
            if not od.nTransferencias == 0:
                if self.brt_cerrado:
                    od.tTransferencia = calcularTiempoEspera(od, od.k_troncal, True)
                else:
                    od.tTransferencia = calcularTiempoEspera(od, od.k, True)
            else:
                od.tTransferencia = 0

            od.TotaltParada = (od.tParadaCorredor + od.tParadaPeriferia)*od.demandaTotal
            od.TotaltParadaFijo = od.tParadaFijo*od.demandaTotal
            od.TotaltParadaVariable = od.tParadaVariable*od.demandaTotal
            od.TotaltViaje = od.tViaje*od.demandaTotal
            od.TotaltEspera = od.tEspera*od.demandaTotal
            od.TotaltTransferencia = (od.tTransferencia+od.deltaTT*od.nTransferencias)*od.demandaIndirecta
            od.TotaltTransferenciaSinDelta = (od.tTransferencia)*od.demandaIndirecta
            od.TotaltAcceso = od.tAcceso*od.demandaTotal
            self.TotaltEspera += od.TotaltEspera
            self.TotaltTransferencia += od.TotaltTransferencia
            self.TotaltTransferenciaSinDelta += od.TotaltTransferenciaSinDelta
            self.TotaltViaje += od.TotaltViaje
            self.TotaltParada += od.TotaltParada
            self.TotaltParadaFijo += od.TotaltParadaFijo
            self.TotaltParadaVariable += od.TotaltParadaVariable
            self.TotaltAcceso += od.TotaltAcceso

        self.CostoTotaltViaje = self.TotaltViaje*self.gammaV
        self.CostoTotaltParada = self.TotaltParada*self.gammaV
        self.CostoTotaltEspera = self.TotaltEspera*self.gammaE
        self.CostoTotaltTransferencia = self.TotaltTransferencia*self.gammaE
        self.CostoTotaltAcceso = self.TotaltAcceso*self.gammaA
        #Finalmente se actualiza el costo Total
        self.CostoTotal = self.CostoOperacion + self.CostoTotaltViaje + self.CostoTotaltEspera + self.CostoTotaltAcceso + self.CostoTotaltTransferencia
        #Tambien hay que actualizar los promedios.
        self.tViajePromedio = self.TotaltViaje/self.demandaTotal
        self.tParadaPromedio = self.TotaltParada/self.demandaTotal
        self.tEsperaPromedio = self.TotaltEspera/self.demandaTotal
        self.tTransferenciaSinDeltaPromedio = self.TotaltTransferenciaSinDelta/self.demandaTotal
        self.tTransferenciaPromedio = self.TotaltTransferencia/self.demandaTotal
        self.tAccesoPromedio = self.TotaltAcceso/self.demandaTotal
        self.CostoTotaltViajePromedio = self.CostoTotaltViaje/self.demandaTotal
        self.CostoTotaltParadaPromedio = self.CostoTotaltParada/self.demandaTotal
        self.CostoTotaltEsperaPromedio = self.CostoTotaltEspera/self.demandaTotal
        self.CostoTotaltTransferenciaPromedio = self.CostoTotaltTransferencia/self.demandaTotal
        self.CostoOperacionPromedio = self.CostoOperacion/self.demandaTotal
        self.CostoTotalPromedio = self.CostoTotal/self.demandaTotal
        self.transferenciasPromedio = self.Transferencias/self.demandaTotal



    def actualizarTParadas(self):
        '''
        Metodo que actualiza el tiempo de paradas para la creacion de la primera red, y para cada vez que se quiera actualizar este tiempo
        fuera del metodo de actualizacion de frecuencias. Requiere que se haya cargado la red.
        :return:
        '''

        self.TotaltViaje = 0
        self.TotaltParada = 0
        self.TotaltParadaFijo = 0
        self.TotaltParadaVariable = 0
        for od in self.ODs:
            od.tParadas = calcularTiempoParadas(od, self.tpVariable, self.tpp, self.tpc, self.sp, self.sc)
            od.tParadaPeriferia = od.tParadas[0]
            od.tParadaCorredor = od.tParadas[1]
            od.tParadaFijo = od.tParadas[2] + od.tParadas[3]
            od.tParadaVariable = od.tParadaCorredor + od.tParadaPeriferia - od.tParadaFijo
            od.tViaje = od.distanciaPeriferia/od.Vp + od.tParadaPeriferia + od.distanciaCorredor/od.Vc + od.tParadaCorredor
            od.TotaltViaje = od.tViaje*od.demandaTotal
            od.TotaltParada = (od.tParadaCorredor + od.tParadaPeriferia)*od.demandaTotal
            od.TotaltParadaFijo = od.tParadaFijo*od.demandaTotal
            od.TotaltParadaVariable = od.tParadaVariable*od.demandaTotal
            self.TotaltViaje += od.TotaltViaje
            self.TotaltParada += od.TotaltParada
            self.TotaltParadaFijo += od.TotaltParadaFijo
            self.TotaltParadaVariable += od.TotaltParadaVariable

        self.CostoTotaltViaje = self.TotaltViaje*self.gammaV
        self.CostoTotaltParada =self.TotaltParada*self.gammaV
        #Finalmente se actualiza el costo Total
        self.CostoTotal = self.CostoOperacion + self.CostoTotaltViaje + self.CostoTotaltEspera + self.CostoTotaltAcceso + self.CostoTotaltTransferencia
        #Tambien hay que actualizar los promedios.
        self.tViajePromedio = self.TotaltViaje/self.demandaTotal
        self.tParadaPromedio =self.TotaltParada/self.demandaTotal
        self.CostoTotaltViajePromedio = self.CostoTotaltViaje/self.demandaTotal
        self.CostoTotaltParadaPromedio = self.CostoTotaltParada/self.demandaTotal
        self.CostoTotalPromedio = self.CostoTotal/self.demandaTotal


    def asignarCarga(self):
        '''
        Este metodo no retorna nada. Lo que hace es tomar la red con la demanda ya asignada y dadas las frecuencias, asignar carga a cada bus.
        Se espera que este metodo pueda ser llamado dentro de la rutina del Scipy para incluir los costos de flota en la optimizacion.
        En este metodo se calculan los tiempos de parada para cada linea/mz.
        infocarga[sentido][0]:Corresponde a las personas que quedan dentro del bus al final de la microzona
        infocarga[sentido][1]:Corresponde a las personas que se suben al servicio dentro de la microzona
        infocarga[sentido][2]:Corresponde a las personas que se bajan del servicio dentro de la microzona
        infocarga[sentido][3]:FO, solo a nivel de linea general por el momento.
        :return: Nada
        '''
        #TODO Verificar bugs en asignacion de carga. Cuando comenzamos a optimizar, cargas en microzonas de la misma periferia son distintas, cuando deberian ser iguales? Quizas no por distinta frecuencia!
        #TODO ->Revisado, al parecer se produce por diferencias en cuanto a donde se da la carga maxima y que tan plana es la demanda a lo largo del recorrido.
        #Primero reseteamos la info de carga para no sumar sobre lo que se tenia antes. Tambien reseteamos la carga maxima.
        #Tambien reseteamos los tiempos de parada y el tiempo de ciclo a solo el tiempo de circulacion.
        for l in self.lineas:
            l.cargaMaxima = 0
            l.RPK = 0
            l.ASK = 0
            for mz in l.microZonas:
                l.infoCarga['Ida'][0][mz.ID] = 0
                l.infoCarga['Ida'][1][mz.ID] = 0
                l.infoCarga['Ida'][2][mz.ID] = 0
                l.infoCarga['Vuelta'][0][mz.ID] = 0
                l.infoCarga['Vuelta'][1][mz.ID] = 0
                l.infoCarga['Vuelta'][2][mz.ID] = 0
                l.tiemposParada["Ida"][mz.ID] = 0
                l.tiemposParada["Vuelta"][mz.ID] = 0
            l.tCiclo = l.tCirculacion
            l.tParada = 0

        #El loop principal de este metodo corresponde a una vuelta por los OD. Para cada OD, se repartira la demanda en las lineas que correspondan segun su "ruta".
        for od in self.ODs:
            ruta = od.ruta

            #Diferenciamos las distintas lineas que participan en los viajes del OD en cuestion.
            #Tambien diferenciamos los nodos de transferencias y las direcciones de cada segmento sobre las lineas.
            lineasSuben = ruta[0]#Nodo donde se sube la gente
            if not ruta[1] == None:  #Caso en que hay una o dos transferencias
                nodoTrans1 = ruta[1]
                if not ruta[3] == None:  #Caso en que hay dos transferencias
                    nodoTrans2 = ruta[3]
                    lineasBajan = ruta[4]
                    lineasTransOut1 = ruta[0]
                    lineasTransIn1 = ruta[2]
                    lineasTransOut2 = ruta[2]
                    lineasTransIn2 = ruta[4]
                    dirSuben = getSentido(od.origen, nodoTrans1, lineasSuben[0])
                    dirTrans1 = getSentido(nodoTrans1, nodoTrans2, lineasTransIn1[0])
                    dirTrans2 = getSentido(nodoTrans2, od.destino, lineasTransIn2[0])
                else:  #Caso en que hay una transferencia
                    lineasBajan = ruta[2]
                    lineasTransOut1 = ruta[0]
                    lineasTransIn1 = ruta[2]
                    dirSuben = getSentido(od.origen, nodoTrans1, lineasSuben[0])
                    dirTrans1 = getSentido(nodoTrans1, od.destino, lineasTransIn1[0])
            else:  #Caso en que no haya transferencias
                dirSuben = getSentido(od.origen, od.destino, lineasSuben[0])
                lineasBajan = ruta[0]

            #El caso en que el origen y el destino son el mismo, debe tratarse aparte,
            #  ya que la direccion "ambos" incluye ida y vuelta, y es necesario dividir el flujo directamente.
            if dirSuben == "Ambos":
                fTotal = sum(l.f for l in lineasSuben)
                for l in lineasSuben:
                    l.infoCarga['Ida'][1][od.origen.ID] += (od.demandaTotal/2)*(l.f/fTotal)/l.f
                    l.infoCarga['Vuelta'][1][od.origen.ID] += (od.demandaTotal/2)*(l.f/fTotal)/l.f
                fTotal = sum(l.f for l in lineasBajan)
                for l in lineasBajan:
                    l.infoCarga['Ida'][2][od.destino.ID] += (od.demandaTotal/2)*(l.f/fTotal)/l.f
                    l.infoCarga['Vuelta'][2][od.destino.ID] += (od.demandaTotal/2)*(l.f/fTotal)/l.f
            #Luego el resto de los OD
            else:
                #A cada una de las lineas debo asignarle demanda en proporcion a su frecuencia.
                fTotal = sum(l.f for l in lineasSuben)
                for l in lineasSuben:
                    l.infoCarga[dirSuben][1][od.origen.ID] += (od.demandaTotal*l.f/fTotal)/l.f
                if not ruta[1] == None:
                    if not ruta[3] == None:
                        fTotal = sum(l.f for l in lineasBajan)
                        for l in lineasBajan:
                            l.infoCarga[dirTrans2][2][od.destino.ID] += (od.demandaTotal*l.f/fTotal)/l.f
                        fTotal = sum(l.f for l in lineasTransOut1)
                        for l in lineasTransOut1:
                            l.infoCarga[dirSuben][2][nodoTrans1.ID] += (od.demandaTotal*l.f/fTotal)/l.f
                        fTotal = sum(l.f for l in lineasTransIn1)
                        for l in lineasTransIn1:
                            l.infoCarga[dirTrans1][1][nodoTrans1.ID] += (od.demandaTotal*l.f/fTotal)/l.f
                        fTotal = sum(l.f for l in lineasTransOut2)
                        for l in lineasTransOut2:
                            l.infoCarga[dirTrans1][2][nodoTrans2.ID] += (od.demandaTotal*l.f/fTotal)/l.f
                        fTotal = sum(l.f for l in lineasTransIn2)
                        for l in lineasTransIn2:
                            l.infoCarga[dirTrans2][1][nodoTrans2.ID] += (od.demandaTotal*l.f/fTotal)/l.f
                    else:
                        fTotal = sum(l.f for l in lineasBajan)
                        for l in lineasBajan:
                            l.infoCarga[dirTrans1][2][od.destino.ID] += (od.demandaTotal*l.f/fTotal)/l.f
                        fTotal = sum(l.f for l in lineasTransOut1)
                        for l in lineasTransOut1:
                            l.infoCarga[dirSuben][2][nodoTrans1.ID] += (od.demandaTotal*l.f/fTotal)/l.f
                        fTotal = sum(l.f for l in lineasTransIn1)
                        for l in lineasTransIn1:
                            l.infoCarga[dirTrans1][1][nodoTrans1.ID] += (od.demandaTotal*l.f/fTotal)/l.f
                else:
                    fTotal = sum(l.f for l in lineasBajan)
                    for l in lineasBajan:
                        l.infoCarga[dirSuben][2][od.destino.ID] += (od.demandaTotal*l.f/fTotal)/l.f

        #Finalmente calculamos la carga para cada linea en cada microzona segun subidas y bajadas, y aprovechamos de ver cual es la carga maxima de la linea.
        #Como la asignacion es simetrica en cuanto a ida y vuelta, solo revisaremos un sentido.
        #Aprovechamos aca tambien de ir contando los Revenue Passenger Kilometer(RPK)
        for l in self.lineas:
            #Ida
            l.infoCarga['Ida'][0][l.microZonas[0].ID] = l.infoCarga['Ida'][1][l.microZonas[0].ID]-l.infoCarga['Ida'][2][l.microZonas[0].ID]#En la primera microzona se considera que el bus viene vacio.
            l.RPK += l.microZonas[0].recorrido*(l.infoCarga['Ida'][0][l.microZonas[0].ID]/2.0)
            if l.cargaMaxima < l.infoCarga['Ida'][0][l.microZonas[0].ID]:
                l.cargaMaxima = l.infoCarga['Ida'][0][l.microZonas[0].ID]
            for i in range(1, len(l.microZonas)):
                l.infoCarga['Ida'][0][l.microZonas[i].ID] = l.infoCarga['Ida'][1][l.microZonas[i].ID]-l.infoCarga['Ida'][2][l.microZonas[i].ID] + l.infoCarga['Ida'][0][l.microZonas[i-1].ID]
                l.RPK += l.microZonas[i].recorrido*(l.infoCarga['Ida'][0][l.microZonas[i].ID]+l.infoCarga['Ida'][0][l.microZonas[i-1].ID])/2.0
                if l.cargaMaxima < l.infoCarga['Ida'][0][l.microZonas[i].ID]:
                    l.cargaMaxima = l.infoCarga['Ida'][0][l.microZonas[i].ID]

            #Vuelta. Para la vuelta es lo mismo pero justo al reves
            l.infoCarga['Vuelta'][0][l.microZonas[-1].ID] = l.infoCarga['Vuelta'][1][l.microZonas[-1].ID]-l.infoCarga['Vuelta'][2][l.microZonas[-1].ID]#En la primera microzona se considera que el bus viene vacio.
            l.RPK += l.microZonas[-1].recorrido*(l.infoCarga['Vuelta'][0][l.microZonas[-1].ID]/2.0)
            if l.cargaMaxima < l.infoCarga['Vuelta'][0][l.microZonas[-1].ID]:
                l.cargaMaxima = l.infoCarga['Vuelta'][0][l.microZonas[-1].ID]
            for i in range(len(l.microZonas)-2, -1, -1):#TODO Verificar que la lista de microzonas de una lineas este en orden. ->Revisado, para el caso de ciudad parecida a Valdivia, esta todo ok.
                l.infoCarga['Vuelta'][0][l.microZonas[i].ID] = l.infoCarga['Vuelta'][1][l.microZonas[i].ID]-l.infoCarga['Vuelta'][2][l.microZonas[i].ID] + l.infoCarga['Vuelta'][0][l.microZonas[i+1].ID]
                l.RPK += l.microZonas[i].recorrido*(l.infoCarga['Vuelta'][0][l.microZonas[i].ID]+l.infoCarga['Vuelta'][0][l.microZonas[i+1].ID])/2.0
                if l.cargaMaxima < l.infoCarga['Vuelta'][0][l.microZonas[i].ID]:
                    l.cargaMaxima = l.infoCarga['Vuelta'][0][l.microZonas[i].ID]

            #Finalmente obtenemos los Available Seat Kilometer(ASK) y Factor de Ocupacion(FO)
            l.ASK = 2*(l.distanciaPeriferia + l.distanciaCorredor)*l.cargaMaxima*l.f
            l.RPK = l.RPK*l.f
            l.FOPromedio = l.RPK/l.ASK
            l.cargaPromedio = l.FOPromedio*l.cargaMaxima

            #Por ultimo hacemos un ultimo loop a las microzonas de la linea para ver el factor de ocupacion al terminar cada microzona.
            for i in range(0, len(l.microZonas)):
                l.infoCarga['Ida'][3][l.microZonas[i].ID] = l.infoCarga['Ida'][0][l.microZonas[i].ID]/l.cargaMaxima
                l.infoCarga['Vuelta'][3][l.microZonas[i].ID] = l.infoCarga['Vuelta'][0][l.microZonas[i].ID]/l.cargaMaxima


        #En adicion a la carga, aprovechamos el metodo para actualizar primero los spacing, y luego los tiempos de parada y tiempos de ciclo.
        #Para la periferia, es importante sacar del cálculo al troncal ya que su alta frecuencia genera mucha distorción en los promedios.
        lineas_periferia = []
        for l in self.lineas:
            lineas_periferia.append(l)
        if self.tipo == 'Cerrada':
            lineas_periferia.remove(self.troncal)
        #Calculo del espaciamiento en periferia, aplica lo mismo para BRT Abierto y Cerrado
        sp = calcularSpacing(self.tpp, self.gammaV, self.gammaA, self.lambdap*self.beta/(len(self.macroZonas['PN'].microZonas)), (self.alpha1+self.alpha2)/2.0, self.at, self.bt, self.Va, lineas_periferia, False,)
        #En el corredor es necesario hacer la diferencia: para el abierto se ocupan todas las lineas, para el cerrado solo el troncal
        if self.tipo == 'Abierta':
            sc = calcularSpacing(self.tpc, self.gammaV, self.gammaA, self.lambdac*self.R, (self.beta1+self.beta2)/2.0, self.at, self.bt, self.Va, self.lineas, True)
        else:
            sc = calcularSpacing(self.tpc, self.gammaV, self.gammaA, self.lambdac*self.R, (self.beta1+self.beta2)/2.0, self.at, self.bt, self.Va, [self.troncal], True)
        #print 'sp= '+str(sp)+" "+'sc= '+str(sc)
        self.sc = sc
        self.sp = sp
        for maz in self.macroZonas:
            if maz == 'PN' or maz == 'PS':
                for miz in self.macroZonas[maz].microZonas:
                    miz.setSpacing(sp)
            else:
                for miz in self.macroZonas[maz].microZonas:
                    miz.setSpacing(sc)


        #Una version para tpvariables y otra para tpfijos
        #Primero la de tiempos variables
        if self.tpVariable:
            for l in self.lineas:
                for mz in l.microZonas:
                    if mz.MZ =='PN' or mz.MZ == 'PS':
                        l.tiemposParada["Ida"][mz.ID] = max(l.infoCarga['Ida'][1][mz.ID]*self.tsp, l.infoCarga['Ida'][2][mz.ID]*self.tbp)\
                                                        + mz.recorrido/self.sp*self.tpp
                        l.tiemposParada["Vuelta"][mz.ID] = max(l.infoCarga['Vuelta'][1][mz.ID]*self.tsp, l.infoCarga['Vuelta'][2][mz.ID]*self.tbp)\
                                                           + mz.recorrido/self.sp*self.tpp
                    else:
                        l.tiemposParada["Ida"][mz.ID] = (l.infoCarga['Ida'][1][mz.ID] + l.infoCarga['Ida'][2][mz.ID])*self.tsc\
                                                        + mz.recorrido/self.sc*self.tpc
                        l.tiemposParada["Vuelta"][mz.ID] = (l.infoCarga['Vuelta'][1][mz.ID] + l.infoCarga['Vuelta'][2][mz.ID])*self.tsc\
                                                           + mz.recorrido/self.sc*self.tpc
                    l.tParada += l.tiemposParada["Ida"][mz.ID] + l.tiemposParada["Vuelta"][mz.ID]
                l.tCiclo += l.tParada
                #Pero como se modifica el tiempo de ciclo, debe modificarse tambien la flota requerida.
                l.flota = l.tCiclo*l.f
                l.velocidadComercial = 2*(l.distanciaPeriferia + l.distanciaCorredor)/l.tCiclo

        #Ahora la de tiempos fijos
        else:
            for l in self.lineas:
                for mz in l.microZonas:
                    if mz.MZ =='PN' or mz.MZ == 'PS':
                        l.tiemposParada["Ida"][mz.ID] = mz.recorrido/self.sp*self.tpp
                        l.tiemposParada["Vuelta"][mz.ID] = mz.recorrido/self.sp*self.tpp
                    else:
                        l.tiemposParada["Ida"][mz.ID] = mz.recorrido/self.sc*self.tpc
                        l.tiemposParada["Vuelta"][mz.ID] = mz.recorrido/self.sc*self.tpc
                    l.tParada += l.tiemposParada["Ida"][mz.ID] + l.tiemposParada["Vuelta"][mz.ID]
                l.tCiclo += l.tParada
                #Pero como se modifica el tiempo de ciclo, debe modificarse tambien la flota requerida.
                l.flota = l.tCiclo*l.f
                l.velocidadComercial = 2*(l.distanciaPeriferia + l.distanciaCorredor)/l.tCiclo



class ciudad(object):
    """
    Es la clase que contiene las distintas redes a evaluar para una determinada configuracion de ciudad.

    """

    def __init__(self, lambdap, lambdac, lambdaCBD, R, R1, beta, beta1, alpha, alpha1, Va, Vp, Vc, tpp, tpc, delta,
                 gammaV, gammaA, gammaE, k, sMin, rhop, rhoc, rhoCBD, theta, ad, bd, at, bt, tsp, tsc, tbp, tpVariable,
                 k_troncal):
        assert R < R1, "R1 debe ser al menos del tamano de R"
        #assert beta - beta1 - R1 >= R1
        assert rhop + rhoc +rhoCBD == 1, "La suma de las atracctividades por macrozona debe ser 1"
        self.lambdap = lambdap
        self.lambdac = lambdac
        self.lambdaCBD = lambdaCBD
        self.R = R
        self.R1 = R1
        self.beta = beta
        self.beta1 = beta1
        self.beta2 = beta - beta1 - R1
        self.alpha = alpha
        self.alpha1 = alpha1
        self.alpha2 = alpha - alpha1 - R
        self.Va = Va
        self.Vp = Vp
        self.Vc = Vc
        self.tpp = tpp
        self.tpc = tpc
        self.delta = delta
        self.gammaV = gammaV
        self.gammaA = gammaA
        self.gammaE = gammaE
        self.k = k
        self.k_troncal = k_troncal
        self.sMin = sMin#A nivel de ciudad se establecera una restriccion respecto al numero minimo de lineas que deben haber. Esto dependera de las dimensiones minimas de la ciudad.
        self.rhop =rhop
        self.rhoc = rhoc
        self.rhoCBD = rhoCBD
        self.theta = theta
        self.ad = ad
        self.bd = bd
        self.at = at
        self.bt = bt
        self.tsp = tsp
        self.tsc = tsc
        self.tbp = tbp
        self.tpVariable = tpVariable

        # Este diccionario contiene dos listas de redes, cada una con distinta cantidad de lineas.
        self.red = {'Abierta': [], 'Cerrada': []}
        #Estas macrozonas no tienen una red asociada, y se ocuparan solo como referencia para tener algunos indicadores facilmente.
        self.macroZonas = {}
        self.macroZonas['PN'] = macroZona(lambdap, beta, alpha1, 'Periferia Norte')
        self.macroZonas['PS'] = macroZona(lambdap, beta, self.alpha2, 'Periferia Sur')
        self.macroZonas['CP'] = macroZona(lambdac, beta1, R, 'Corredor Poniente')
        self.macroZonas['CBD'] = macroZona(lambdaCBD, R1, R, 'CBD')
        self.macroZonas['CO'] = macroZona(lambdac, self.beta2, R, 'Corredor Oriente')

        #Ahora se suma la demanda de todas las macrozonas para obtener su demanda total
        self.demandaTotal = self.macroZonas['PN'].demandaO + self.macroZonas['PS'].demandaO + self.macroZonas['CP'].demandaO + self.macroZonas['CBD'].demandaO + self.macroZonas['CO'].demandaO
        #Luego agregamos la demanda atraida por cada macrozona. Ojo que en el caso de las periferias, la demanda se repartira segun el area original de la macrozona.
        self.macroZonas['PN'].demandaD = self.demandaTotal*self.rhop*self.macroZonas['PN'].areaOriginal/(self.macroZonas['PN'].areaOriginal + self.macroZonas['PS'].areaOriginal)
        self.macroZonas['PS'].demandaD = self.demandaTotal*self.rhop*self.macroZonas['PS'].areaOriginal/(self.macroZonas['PN'].areaOriginal + self.macroZonas['PS'].areaOriginal)
        self.macroZonas['CP'].demandaD = self.demandaTotal*self.rhoc*self.macroZonas['CP'].areaOriginal/(self.macroZonas['CP'].areaOriginal + self.macroZonas['CO'].areaOriginal)
        self.macroZonas['CBD'].demandaD = self.demandaTotal*self.rhoCBD
        self.macroZonas['CO'].demandaD = self.demandaTotal*self.rhoc*self.macroZonas['CO'].areaOriginal/(self.macroZonas['CP'].areaOriginal + self.macroZonas['CO'].areaOriginal)

    # Aca creamos las redes y las asignamos a la ciudad. En estos dos metodos se define como se asignan
    # las lineas a las microzonas.

    def agregarMicrozonas(self, n, macroZ):
        '''
        A pesar de que probamos la idea de ir generando un ancho efectivo, para cada microzona, buscando mantener el mismo ancho para todas las microzona,
        se llego a la conclusion que hacer eso distorciona mucho los resultados ya que se ve alterada la demanda.
        Es por esto que se optara por mantener los anchos fijos, y angostar el espaciamiento en los lugares mas estrechos como el CBD o CO.
        :param n: numero de lineas en la red
        :param macroZ: conjunto de macrozonas de la Red(Ojo, es la propia de la red y no ciudad) Sobre ella se asignan las microzonas.
        :return: No tiene return, ya que las microzonas se agregan a las macrozonas.
        '''

        #Buscamos el numero de microzonas a asignar a cada macrozona. Para ello ocupamos el metodo numeroMicrozonas definido en el archivo mContinuoFunciones
        numeroZonas = numeroMicrozonas(self.R1, self.beta, self.beta1, n)
        n0 = numeroZonas[0]
        nCBD = numeroZonas[1]#Aca ocurre muchas veces que el centro es muy pequeno por lo que no caben lineas. en ese caso se pone una por default.
        nf = numeroZonas[2]
        anchoMZ = self.beta/float(n)

        #Antes de comenzar a crear las microzonas, recalcularemos la densidad de demanda del CBD, de modo que absorva las variaciones y la demanda total permanezca constante.
        demandaOriginalCP = self.beta1*self.R*self.lambdac
        demandaOriginalCO = self.beta2*self.R*self.lambdac
        demandaOriginalCBD = self.R1*self.R*self.lambdaCBD
        lambdaCBDnueva = (demandaOriginalCP + demandaOriginalCBD + demandaOriginalCO - n0*self.R*anchoMZ*self.lambdac - nf*self.R*anchoMZ*self.lambdac)/(float(float(nCBD)*anchoMZ*self.R))

        #Con los parametros anteriores se tienen ya los anchos definitivos de cada macrozona
        macroZ['PN'].anchoEfectivo = macroZ['PN'].anchoIndicado
        macroZ['PS'].anchoEfectivo = macroZ['PS'].anchoIndicado
        macroZ['CP'].anchoEfectivo = anchoMZ*n0
        macroZ['CBD'].anchoEfectivo = anchoMZ*nCBD
        macroZ['CO'].anchoEfectivo = anchoMZ*nf
        macroZ['CBD'].densidadDemanda = lambdaCBDnueva

        #Hacemos un ajuste parecido en para la demanda atraida. Aca simplemente, si se saco una macrozona del corredor,
        #Habra que agregar esa demanda atraida al CBD.
        if n0 == 0:
            macroZ['CBD'].demandaD += macroZ['CP'].demandaD
            macroZ['CP'].demandaD = 0
        if nf == 0:
            macroZ['CBD'].demandaD += macroZ['CO'].demandaD
            macroZ['CO'].demandaD = 0

        #Agregamos las microzonas a sus respectivas macrozonas
        #Hay que hacer notar que las microzonas perifericas ocupan el ancho de sus macrozonas de corredor respectivas.

        #Partimos por el poniente
        for i in range(n0):
            mn = microZona(self.lambdap, anchoMZ, self.alpha1, 'PN', i, i, self.Vp, macroZ['PN'].demandaD/n)
            m = microZona(self.lambdac, anchoMZ, self.R, 'CP', i, i, self.Vc, macroZ['CP'].demandaD/n0)
            ms = microZona(self.lambdap, anchoMZ, self.alpha2, 'PS', i, i, self.Vp, macroZ['PS'].demandaD/n)
            macroZ['PN'].microZonas.append(mn)
            macroZ['CP'].microZonas.append(m)
            macroZ['PS'].microZonas.append(ms)
            macroZ['PN'].nMicroZonas += 1
            macroZ['CP'].nMicroZonas += 1
            macroZ['PS'].nMicroZonas += 1

        #Las de CBD
        for i in range(nCBD):
            mn = microZona(self.lambdap, anchoMZ, self.alpha1, 'PN', i+n0, i+n0, self.Vp, macroZ['PN'].demandaD/n)
            m = microZona(lambdaCBDnueva, anchoMZ, self.R, 'CBD', i, i+n0, self.Vc, macroZ['CBD'].demandaD/nCBD)
            ms = microZona(self.lambdap, anchoMZ, self.alpha2, 'PS', i+n0, i+n0, self.Vp, macroZ['PS'].demandaD/n)
            macroZ['PN'].microZonas.append(mn)
            macroZ['CBD'].microZonas.append(m)
            macroZ['PS'].microZonas.append(ms)
            macroZ['PN'].nMicroZonas += 1
            macroZ['CBD'].nMicroZonas += 1
            macroZ['PS'].nMicroZonas += 1

        #Y por ultimo las microzonas de CO
        for i in range(nf):
            mn = microZona(self.lambdap, anchoMZ, self.alpha1, 'PN', i+n0+nCBD, i+n0+nCBD, self.Vp, macroZ['PN'].demandaD/n)
            m = microZona(self.lambdac, anchoMZ, self.R, 'CO', i, i+n0+nCBD, self.Vc, macroZ['CO'].demandaD/nf)
            ms = microZona(self.lambdap, anchoMZ, self.alpha2, 'PS', i+n0+nCBD, i+n0+nCBD, self.Vp, macroZ['PS'].demandaD/n)
            macroZ['PN'].microZonas.append(mn)
            macroZ['CO'].microZonas.append(m)
            macroZ['PS'].microZonas.append(ms)
            macroZ['PN'].nMicroZonas += 1
            macroZ['CO'].nMicroZonas += 1
            macroZ['PS'].nMicroZonas += 1

    def agregarRedCerrada(self, n):
        #En esta lista se iran guardando las lineas pertenecientes a la red cerrada
        lineas = []
        #Creamos una copia de las macrozonas de la ciudad para hacerlas propias de la red.
        macroZ = {'PN': macroZona(self.lambdap, self.beta, self.alpha1, 'Periferia Norte'),
                  'PS': macroZona(self.lambdap, self.beta, self.alpha2, 'Periferia Sur'),
                  'CP': macroZona(self.lambdac, self.beta1, self.R, 'Corredor Poniente'),
                  'CBD': macroZona(self.lambdaCBD, self.R1, self.R, 'CBD'),
                  'CO': macroZona(self.lambdac, self.beta2, self.R, 'Corredor Oriente')}

        #Luego agregamos la demanda atraida por cada macrozona. Ojo que en el caso de las periferias, la demanda se repartira segun el area original de la macrozona.
        macroZ['PN'].demandaD = self.demandaTotal*self.rhop*macroZ['PN'].areaOriginal/(macroZ['PN'].areaOriginal + macroZ['PS'].areaOriginal)
        macroZ['PS'].demandaD = self.demandaTotal*self.rhop*macroZ['PS'].areaOriginal/(macroZ['PN'].areaOriginal + macroZ['PS'].areaOriginal)
        macroZ['CP'].demandaD = self.demandaTotal*self.rhoc*macroZ['CP'].areaOriginal/(macroZ['CP'].areaOriginal + macroZ['CO'].areaOriginal)
        macroZ['CBD'].demandaD = self.demandaTotal*self.rhoCBD
        macroZ['CO'].demandaD = self.demandaTotal*self.rhoc*macroZ['CO'].areaOriginal/(macroZ['CP'].areaOriginal + macroZ['CO'].areaOriginal)

        #Agregamos las microzonas segun la cantidad de lineas con la que definimos la red.
        self.agregarMicrozonas(n, macroZ)

        #recuperamos los rangos de las macrozonas del corredor:
        n0 = macroZ['CP'].nMicroZonas
        nCBD = macroZ['CBD'].nMicroZonas
        nf = macroZ['CO'].nMicroZonas

        #Ahora generamos las lineas una a una y las agregamos a la lista. Ocuparemos los rangos recien definidos para ir asignandoles macro y microzonas.
        for i in range(n):
            if i < n0:
                maz = [macroZ['PN'], macroZ['CP'], macroZ['PS']]
                miz = [macroZ['PN'].microZonas[i], macroZ['CP'].microZonas[i], macroZ['PS'].microZonas[i]]
                l = linea(maz, miz, False)
                lineas.append(l)
            elif i < n0 + nCBD:
                maz = [macroZ['PN'], macroZ['CBD'], macroZ['PS']]
                miz = [macroZ['PN'].microZonas[i], macroZ['CBD'].microZonas[i - n0], macroZ['PS'].microZonas[i]]
                l = linea(maz, miz, False)
                lineas.append(l)
            elif i < n0 + nCBD + nf:
                maz = [macroZ['PN'], macroZ['CO'], macroZ['PS']]
                miz = [macroZ['PN'].microZonas[i], macroZ['CO'].microZonas[i - n0 - nCBD], macroZ['PS'].microZonas[i]]
                l = linea(maz, miz, False)
                lineas.append(l)

        #Finalmente agregamos la linea troncal
        maz = [macroZ['CP'], macroZ['CBD'], macroZ['CO']]
        miz = macroZ['CP'].microZonas + macroZ['CBD'].microZonas + macroZ['CO'].microZonas
        ltroncal = linea(maz, miz, True)

        #Antes de crear la red debemos asignar el spacing optimo a las microzonas. Habia que esperar hasta este momento para poder tener las lineas.
        sp = calcularSpacing(self.tpp, self.gammaV, self.gammaA, self.lambdap*(self.beta/len(lineas)/2), (self.alpha1+self.alpha2)/2.0, self.at, self.bt, self.Va, lineas, False)
        sc = calcularSpacing(self.tpc, self.gammaV, self.gammaA, self.lambdac*self.R, self.beta, self.at, self.bt, self.Va, [ltroncal], True)
        red.sc = sc
        red.sp = sp
        for maz in macroZ:
            if maz == 'PN' or maz == 'PS':
                for miz in macroZ[maz].microZonas:
                    miz.setSpacing(sp)
            else:
                for miz in macroZ[maz].microZonas:
                    miz.setSpacing(sc)
        #Con las paradas asignadas a las microzonas, podemos calcular el numero de paradas en una linea
        for l in lineas:
            l.setParadas()

        x = red(lineas, ltroncal, 'Cerrada', macroZ, self.Vp, self.Vc, self.Va, self.k, self.gammaV, self.gammaA, self.gammaE,
                sp, sc, self.tpp, self.tpc, self.delta, self.theta, self.ad, self.bd, self.at, self.bt, self.tsp, self.tsc, self.tbp, self.alpha,
                self.alpha1, self.alpha2, self.beta, self.beta1, self.beta2, self.R, self.lambdap, self.lambdac, self.lambdaCBD, self.tpVariable, n, self.k_troncal)
        #Calibramos la distribucion
        distribucionDemanda(x)
        #Asignamos la carga a los buses
        x.asignarCarga()#Se asigna la carga a las lineas antes del append
        x.actualizarTParadas()
        self.red['Cerrada'].append(x)



    #Lo mismo que antes pero para redes abiertas
    def agregarRedAbierta(self, n):
    #TODO Cuando hay nodo impar en el CBD ponemos una linea central, mientras que cuando hay un numero par ponemos dos lineas de dos nodos en el nodo central(n1CBD)->Ok, ver si pasa para nuestro experimiento. Si es asi, arreglar.
        lineas = []#En esta lista se iran guardando las lineas de la red
        #Creamos una copia de las macrozonas de la ciudad para hacerlas propias de la red.
        macroZ = {'PN': macroZona(self.lambdap, self.beta, self.alpha1, 'Periferia Norte'),
                  'PS': macroZona(self.lambdap, self.beta, self.alpha2, 'Periferia Sur'),
                  'CP': macroZona(self.lambdac, self.beta1, self.R, 'Corredor Poniente'),
                  'CBD': macroZona(self.lambdaCBD, self.R1, self.R, 'CBD'),
                  'CO': macroZona(self.lambdac, self.beta2, self.R, 'Corredor Oriente')}

        #Luego agregamos la demanda atraida por cada macrozona. Ojo que en el caso de las periferias, la demanda se repartira segun el area original de la macrozona.
        macroZ['PN'].demandaD = self.demandaTotal*self.rhop*macroZ['PN'].areaOriginal/(macroZ['PN'].areaOriginal + macroZ['PS'].areaOriginal)
        macroZ['PS'].demandaD = self.demandaTotal*self.rhop*macroZ['PS'].areaOriginal/(macroZ['PN'].areaOriginal + macroZ['PS'].areaOriginal)
        macroZ['CP'].demandaD = self.demandaTotal*self.rhoc*macroZ['CP'].areaOriginal/(macroZ['CP'].areaOriginal + macroZ['CO'].areaOriginal)
        macroZ['CBD'].demandaD = self.demandaTotal*self.rhoCBD
        macroZ['CO'].demandaD = self.demandaTotal*self.rhoc*macroZ['CO'].areaOriginal/(macroZ['CP'].areaOriginal + macroZ['CO'].areaOriginal)

        self.agregarMicrozonas(n, macroZ)#Agregamos las microzonas segun la cantidad de lineas con la que definimos la red.

        #recuperamos los rangos de las macrozonas del corredor:
        n0 = macroZ['CP'].nMicroZonas
        nCBD = macroZ['CBD'].nMicroZonas
        n1CBD = int(nCBD/2) + 1#Este numero se ocupa como auxiliar para ver los rangos de emparejamiento
        n2CBD = nCBD - n1CBD#Este numero se ocupa como auxiliar para ver los rangos de emparejamiento
        nf = macroZ['CO'].nMicroZonas

        #Ahora generamos las lineas una a una y las agregamos a la lista. Ocuparemos los rangos recien definidos para ir asignandoles macro y microzonas.
        #Ojo que tenemos que hacer lo mismo tanto para las que parten del norte como las del sur.
        for i in range(n):
            #Primero, conectamos todas las lineas al poniente de la mitad del CBD, hasta la mitad mas uno del centro del CBD.
            if i < n0:#Lineas que parten en el poniente
                mazN = [macroZ['PN'], macroZ['CP'], macroZ['CBD']]
                mizN = [macroZ['PN'].microZonas[i]]
                mazS = [macroZ['PS'], macroZ['CP'], macroZ['CBD']]
                mizS = [macroZ['PS'].microZonas[i]]
                for j in range(i, n0):
                    mizN.append(macroZ['CP'].microZonas[j])
                    mizS.append(macroZ['CP'].microZonas[j])
                for j in range(n1CBD):
                    mizN.append(macroZ['CBD'].microZonas[j])
                    mizS.append(macroZ['CBD'].microZonas[j])

            elif i < n0 + n1CBD:#Lineas que parten en CBD
                mazN = [macroZ['PN'], macroZ['CBD']]
                mizN = [macroZ['PN'].microZonas[i]]
                for j in range(i-n0, n1CBD):
                    mizN.append(macroZ['CBD'].microZonas[j])

                ##Para el caso en que haya un numero de nodos impar en el CBD, se considera solo una linea justo por la mitad. Lamentablemente por eso tendremos que preguntarnos cada vez si estamos justo en la mitad.
                if not nCBD%2 ==0 and i == n0 + n1CBD - 1:
                    mazN.append(macroZ['PS'])
                    mizN.append(macroZ['PS'].microZonas[i])
                else:#Para el resto de los casos se construye tambien la linea simetrica del sur.
                    mazS = [macroZ['PS'], macroZ['CBD']]
                    mizS = [macroZ['PS'].microZonas[i]]
                    for j in range(i-n0, n1CBD):
                        mizS.append(macroZ['CBD'].microZonas[j])

            #Finalmente si i corresponde a una linea no pareada al oriente del CBD, se conecta hasta la mitad mas uno del CBD.
            elif i < n0 + nCBD + nf:
                if nf > n0 + nCBD/2 and (i - n0 - nCBD) < (nf - n0 - nCBD/2):
                    mazN = [macroZ['PN'], macroZ['CO'], macroZ['CBD']]
                    mizN = [macroZ['PN'].microZonas[i]]
                    mazS = [macroZ['PS'], macroZ['CO'], macroZ['CBD']]
                    mizS = [macroZ['PS'].microZonas[i]]
                    for j in range((i - n0 - nCBD)+1):
                        mizN.append(macroZ['CO'].microZonas[j])
                        mizS.append(macroZ['CO'].microZonas[j])
                    for j in range(n1CBD - 1, min(i + 1 - n0, nCBD)):
                        mizN.append(macroZ['CBD'].microZonas[j])
                        mizS.append(macroZ['CBD'].microZonas[j])


            #Ahora se conectan las microzonas al oriente de la mitad del CBD mas uno a algunas de las lineas que hemos generado hasta el momento.
            #Se ocupa la estrategia de lineas largas, es decir, las que parten mas al poniente van agregando las microzonas mas al oriente.
            if i < nf + n2CBD and i < n0 +n1CBD - 1:#La condicion es que queden lineas libres al oriente y que estemos en una linea que parta al poniente de la linea central.
                #En este caso se le parean tanto zonas oriente del CBD como del CO mismo
                if i < nf:
                    #Se le agregan primero las zonas que le faltaron dentro del CBD
                    for j in range(min(n2CBD-(i + 1 - n0 - n1CBD), n2CBD)):
                        mizN.append(macroZ['CBD'].microZonas[j+n1CBD])
                        mizS.append(macroZ['CBD'].microZonas[j+n1CBD])
                    #Luego las del CO si aplica.
                    mazN.append(macroZ['CO'])
                    mazS.append(macroZ['CO'])
                    for j in range(nf - i):
                        mizN.append(macroZ['CO'].microZonas[j])
                        mizS.append(macroZ['CO'].microZonas[j])

                #Este es el caso en que la zona s eparea con una al oriente de la mitad del CBD pero no alcanza ninguna de CO
                else:
                    #Tambien se le conecta el resto del CBD si es que aplica
                    for j in range(nf + n2CBD - i):
                        mizN.append(macroZ['CBD'].microZonas[j+n1CBD])
                        mizS.append(macroZ['CBD'].microZonas[j+n1CBD])
                #Tambien se le conecta la periferia final
                mazN.append(macroZ['PS'])
                mizN.append(macroZ['PS'].microZonas[n - i - 1])
                mazS.append(macroZ['PN'])
                mizS.append(macroZ['PN'].microZonas[n - i - 1])

            #Finalmente generamos las dos lineas del caso y las metemos en la lista.
            if not mizN == None:
                lN = linea(mazN, mizN, False)
                lineas.append(lN)
            if not mizS == None:
                lS = linea(mazS, mizS, False)
                lineas.append(lS)

            #Seteamos en None las listas de zonas para la proxima iteracion
            mazN = None
            mizN = None
            mazS = None
            mizS = None

        #Antes de crear la red debemos asignar el spacing optimo a las microzonas. Habia que esperar hasta este momento para poder tener las lineas.
        sp = calcularSpacing(self.tpp, self.gammaV, self.gammaA, self.lambdap*(self.beta/len(lineas)/2), (self.alpha1+self.alpha2)/2.0, self.at, self.bt, self.Va, lineas, False)
        sc = calcularSpacing(self.tpc, self.gammaV, self.gammaA, self.lambdac*self.R, self.beta, self.at, self.bt, self.Va, lineas, True)
        red.sc = sc
        red.sp = sp
        for maz in macroZ:
            if maz == 'PN' or maz =='PS':
                for miz in macroZ[maz].microZonas:
                    miz.setSpacing(sp)
            else:
                for miz in macroZ[maz].microZonas:
                    miz.setSpacing(sc)
        #Con las paradas asignadas a las microzonas, podemos calcular el numero de paradas en una linea
        for l in lineas:
            l.setParadas()

        x = red(lineas, None, 'Abierta', macroZ,  self.Vp, self.Vc, self.Va, self.k, self.gammaV, self.gammaA, self.gammaE,
                sp, sc, self.tpp, self.tpc, self.delta, self.theta, self.ad, self.bd, self.at, self.bt, self.tsp, self.tsc, self.tbp, self.alpha,
                self.alpha1, self.alpha2, self.beta, self.beta1, self.beta2, self.R, self.lambdap, self.lambdac, self.lambdaCBD, self.tpVariable, n, self.k_troncal)
        #Calibramos la distribucion
        distribucionDemanda(x)
        #Asignamos la carga a los buses
        x.asignarCarga()#Se asigna la carga a las lineas antes del append
        x.actualizarTParadas()
        self.red['Abierta'].append(x)

