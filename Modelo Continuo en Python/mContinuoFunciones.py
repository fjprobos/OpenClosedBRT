__author__ = 'Pancho'

#from gurobipy import*
from scipy.optimize import minimize
from math import*

def calcularDistanciaMovimiento(od):
    '''
    :param od: objeto de la clase OD. Estara pensado para Microzonas.
    :return: retorna una tupla de cuatro entredas con las distancias sobre periferia y  sobre corredor, ademas de los tiempos de parada sobre periferia y corredor.
    '''
    #TODO Ojo que hay distancias que podrian perfeccionarse. Por ejemplo, cuando se cruza el corredor de norte a sur, la distancia recorrida en aquella microzona se considera
    #TODO como la de este a oeste, y ademas dentro de distancia en corredor. Habra que definir bien estos casos borde.-> Por mejorar, no es algo tan relevante de todas formas.
    distanciaPeriferia = 0
    distanciaCorredor = 0
    #Tendremos que obtener las microzonas por donde pasa la ruta y guardarla sobre una lista. Luego calculamos distancias sobre esa lista.
    path = od.path
    #Primero vemos el caso en que el viajes es dentro de la misma microzona
    if od.origen == od.destino:
        if (od.origen.MZ == 'PN' or od.origen.MZ == 'PS'):
            distanciaPeriferia += od.origen.largo/3.0
        else:
            distanciaCorredor += od.origen.ancho/3.0
    #Luego el resto
    else:
        #Partimos agregando la distancia promedio sobre las zonas de origen y destino, para luego agregar el largo entero de las zonas intermedias.
        if (od.origen.MZ == 'PN' or od.origen.MZ == 'PS'):
            distanciaPeriferia += od.origen.largo/2.0
        else:
            distanciaCorredor += od.origen.ancho/2.0
        if (od.destino.MZ == 'PN' or od.destino.MZ == 'PS'):
            distanciaPeriferia += od.destino.largo/2.0
        else:
            distanciaCorredor += od.destino.ancho/2.0
        subpath = path[1:-1]
        for mz in subpath:
            if (mz.MZ == 'PN' or mz.MZ == 'PS'):
                distanciaPeriferia += mz.largo
            else:
                distanciaCorredor += mz.ancho

    return (distanciaPeriferia, distanciaCorredor)

def calcularTiempoParadas(od, tpVariable, tpp, tpc, sp, sc):
    '''
    Le devuelve todo el IVT por paradas para para un usuario cualquiera en ese OD.
    :param od:
    :return:
    '''
    #Primero tenemos el resultado del tiempo de parada total para el od incluyendo la porcion variable
    tParadaPeriferia = 0
    tParadaCorredor = 0

    #Tambien obtenemos aparte el tp fijo para poder analizar resultados en funcion de esto
    tParadaFijoPeriferia = 0
    tParadaFijoCorredor = 0

    #Tendremos que obtener las microzonas por donde pasa la ruta y guardarla sobre una lista. Luego calculamos distancias sobre esa lista.
    path = od.path

    ###Calculo del tiempo de parada total##
    #Primero vemos el caso en que el viajes es dentro de la misma microzona
    if od.origen == od.destino:
        if (od.origen.MZ == 'PN' or od.origen.MZ == 'PS'):
            tParadaPeriferia += promedioTparada(od, od.origen)/3.0 + od.origen.recorrido/sp*tpp/3.0
        else:
            tParadaCorredor += promedioTparada(od, od.origen)/3.0 + od.origen.recorrido/sc*tpc/3.0
    #Luego el resto
    else:
        #Partimos agregando la distancia promedio sobre las zonas de origen y destino, para luego agregar el largo entero de las zonas intermedias.
        if (od.origen.MZ == 'PN' or od.origen.MZ == 'PS'):
            tParadaPeriferia += promedioTparada(od, od.origen)/2.0 + od.origen.recorrido/sp*tpp/2.0
        else:
            tParadaCorredor += promedioTparada(od, od.origen)/2.0 + od.origen.largo/sc*tpc/2.0
        if (od.destino.MZ == 'PN' or od.destino.MZ == 'PS'):
            tParadaPeriferia += promedioTparada(od, od.destino)/2.0 + od.destino.recorrido/sp*tpp/2.0
        else:
            tParadaCorredor += promedioTparada(od, od.destino)/2.0 + od.destino.recorrido/sc*tpc/2.0
        subpath = path[1:-1]
        for mz in subpath:
            if (mz.MZ == 'PN' or mz.MZ == 'PS'):
                tParadaPeriferia += promedioTparada(od, mz)
            else:
                tParadaCorredor += promedioTparada(od, mz)

    ###Calculo del tiempo de parada fijo##
    #Primero vemos el caso en que el viajes es dentro de la misma microzona
    if od.origen == od.destino:
        if (od.origen.MZ == 'PN' or od.origen.MZ == 'PS'):
            tParadaFijoPeriferia += od.origen.recorrido/sp*tpp/3.0
        else:
            tParadaFijoCorredor += od.origen.recorrido/sc*tpc/3.0
    #Luego el resto
    else:
        #Partimos agregando la distancia promedio sobre las zonas de origen y destino, para luego agregar el largo entero de las zonas intermedias.
        if (od.origen.MZ == 'PN' or od.origen.MZ == 'PS'):
            tParadaFijoPeriferia += od.origen.recorrido/sp*tpp/2.0
        else:
            tParadaFijoCorredor += od.origen.largo/sc*tpc/2.0
        if (od.destino.MZ == 'PN' or od.destino.MZ == 'PS'):
            tParadaFijoPeriferia += od.destino.recorrido/sp*tpp/2.0
        else:
            tParadaFijoCorredor += od.destino.recorrido/sc*tpc/2.0
        subpath = path[1:-1]
        for mz in subpath:
            if (mz.MZ == 'PN' or mz.MZ == 'PS'):
                tParadaFijoPeriferia += mz.recorrido/sp*tpp
            else:
                tParadaFijoCorredor += mz.recorrido/sc*tpc

    return (tParadaPeriferia, tParadaCorredor, tParadaFijoPeriferia, tParadaFijoCorredor)

def calcularTiempoEspera(od, k, transferencia):
    '''
    :param od: objeto de la clase OD. Para que represente bien la realidad, el OD debe ser de microzonas.
    :param k: constante de tiempo de espera de la ciudad
    :param transferencia: bool que indica si el tiempo de espera a calcular es el de inicial o transferencia
    :return: un double con el tiempo de espera promedio para el inicio del viaje en el OD indicado
    '''
    frecuenciaTotal = 0
    tEspera = 0
    if transferencia:
        for l in od.ruta[2]:
            frecuenciaTotal += float(l.f)
        tEspera = float(k)/frecuenciaTotal
        frecuenciaTotal = 0
        if not od.ruta[4] == None:
            for l in od.ruta[4]:
                frecuenciaTotal += float(l.f)
            tEspera += float(k)/frecuenciaTotal
    else:
        for l in od.ruta[0]:
            frecuenciaTotal += float(l.f)
        k = float(k)
        tEspera = float(k)/frecuenciaTotal
    return tEspera

def calcularTiempoAcceso(od, Va):
    '''
    :param od: objeto de la clase OD. Puede ser tanto de Macrozonas como Microzonas.
    :param Va: velocidad de acceso de los usuarios.
    :return: retorna el tiempo que toman los usuarios de un OD tanto en acceder como egresar del sistema en promedio.
    '''
    distanciaAcceso = 0
    distanciaEgreso = 0
    #Prinero el origen
    if (od.origen.MZ == 'PN' or od.origen.MZ == 'PS'):
        distanciaAcceso = od.origen.ancho/4.0 + od.origen.spacing/4.0
    else:
        distanciaAcceso = od.origen.largo/4.0 + od.origen.spacing/4.0
    #Luego la de egreso:
    if (od.destino.MZ == 'PN' or od.destino.MZ == 'PS'):
        distanciaEgreso = od.destino.ancho/4.0 + od.destino.spacing/4.0
    else:
        distanciaEgreso = od.destino.largo/4.0 + od.destino.spacing/4.0

    return (distanciaAcceso + distanciaEgreso)/Va

def obtenerPath(od):
    '''

    :param od: objeto del tipo od. Debe ser de microzonas. Asume que el od ya ha seteado su parametro "ruta".
    :return: retorna el conjunto de microzonas contenidas en la ruta del od. Se utiliza un mergesort llamado routeSort para devolver la ruta ordenada.
    '''
    path = []
    path.append(od.origen)
    if(od.ruta[2] == None):
        for n in od.ruta[0][0].microZonas:
            if nodoEnRuta(od.origen, od.destino, n) and (not (n == od.origen or n == od.destino)):
                path.append(n)
    else:
        for n in od.ruta[0][0].microZonas:
            if nodoEnRuta(od.origen, od.destino, n) and (not (n == od.origen or n == od.destino)):
                path.append(n)
                #if n == od.ruta[1]:
                    #break
        for n in od.ruta[2][0].microZonas:
            if nodoEnRuta(od.origen, od.destino, n) and ((not (n == od.origen or n == od.destino)) and not n in path):
                path.append(n)
    path.append(od.destino)
    path = routeSortWrapper(path)
    return path

def nodoEnRuta(origen, destino, n):
    '''
    :param origen: origen de un OD dado por una microzona
    :param destino: destino de un OD dado poruna microzona
    :param n: objeto de la clase microzona
    :return: retorna un bool que indica si el nodo n esta dentro de la ruta entre el origen y el destino
    '''
    if (n == origen or n == destino):
        return True
    elif (n.MZ == 'PN' or n.MZ == 'PS'):
        return False
    else:
        return (origen <= n <= destino or destino <= n <= origen)


def tranferenciaRazonable(origen, destino, zonaTrans):
    '''
    :param origen:
    :param destino:
    :param zonaTrans:
    :return: Indica si el nodo zonaTrans es un nodo factible de ser lugar de transferencia para el par origen destino.
    Metodo que ve si la zonaC esta dentro del shortest path entre la zonaA y la zonaB. La idea es emular
    el razonamiento que ocupa Dial para la asignacion, en donde se parte en una primera etapa, definiendo
    rutas razonables. En este caso, el criterio de que un nodo de transferencia sea razonable, es que este dentro del
    shortest path entre dos nodos. Se utiliza para saber si un nodo esta dentro del shortest path para un OD.
    '''
    #Primero verificamos que el nodo no sea de periferia, ya que se asume que no se puede transferir ahi por el momento.
    if (zonaTrans.MZ == 'PN' or zonaTrans.MZ == 'PS'):
        return False
    #Luego vemos si el nodo de transferencias tiene al menos una linea que llegue al destino
    for l in  zonaTrans.lineas:
        if l in destino.lineas:
            #Ocupamos la definicion que ocupamos en la clase microzona para comparar que zonas son mayores:
            return (origen <= zonaTrans <= destino or destino <= zonaTrans <= origen)
    return False

def routeSortWrapper(path):
    '''
    :param path: se asume que es una lista de nodos que componen un path con el origen al principio y el destino al final.
    :return: retorna una lista ordenada del path
    '''
    origen = path[0]
    destino = path[-1]
    izqDer = origen < destino
    subpath = path[1:-1]
    result =[]
    result.append(origen)
    result += msort(subpath, izqDer)
    result.append(destino)

    return result


def msort(subpath, izqDer):
    '''
    corresponde a un mergeSort para ordenar los nodos entre el origen y destino no considerados aqui pero guardados en el wrapper.
    :param path:
    :return: retorna el path ordenado segun el lugar que ocupa cada microzona en el corredor
    Ojo que no discrimina si un nodo de periferia ocupa le mismo lugar que uno de corredor, por eso deben sacarse los nodos de periferia antes.
    '''
    result = []
    if izqDer:
        if len(subpath) < 2:
            return subpath
        mid = int(len(subpath)/2)
        y = msort(subpath[:mid], izqDer)
        z = msort(subpath[mid:], izqDer)
        while (len(y) > 0) or (len(z) > 0):
            if len(y) > 0 and len(z) > 0:
                if y[0] > z[0]:
                    result.append(z[0])
                    z.pop(0)
                else:
                    result.append(y[0])
                    y.pop(0)
            elif len(z) > 0:
                for i in z:
                    result.append(z[0])
                    z.pop(0)
            else:
                for i in y:
                    result.append(y[0])
                    y.pop(0)
    else:
        if len(subpath) < 2:
            return subpath
        mid = int(len(subpath)/2)
        y = msort(subpath[:mid], izqDer)
        z = msort(subpath[mid:], izqDer)
        while (len(y) > 0) or (len(z) > 0):
            if len(y) > 0 and len(z) > 0:
                if y[0] < z[0]:
                    result.append(z[0])
                    z.pop(0)
                else:
                    result.append(y[0])
                    y.pop(0)
            elif len(z) > 0:
                for i in z:
                    result.append(i)
                    z.pop(0)
            else:
                for i in y:
                    result.append(i)
                    y.pop(0)
    return result

def calcularSpacing(tp, gammaV, gammaA, lambdaa, largo, at, bt, Va, lineas, esCorredor):

    #Podemos actualizar la f promedio con las lineas del argumento. Para el Costo de detencion, ahora
    #Version en base a Modificacion Spacing del cuaderno amarillo.
    #Se actualiza al final del metodo asignarCarga, por lo que se ejecuta ademas cada vez que se actualiza frecuencia.

    #Primero calculamos parametros promedio para el spacing
    sumaCapacidades = 0
    sumaFrecuencias = 0
    sumaASK = 1
    sumaRPK = 0

    for l in lineas:
        sumaFrecuencias += l.f
        sumaCapacidades += l.cargaMaxima
        sumaASK += l.ASK
        sumaRPK += l.RPK

    if esCorredor:
        f = (sumaFrecuencias/len(lineas))*(len(lineas)+1)/2.0#Esta formula viene de la utilizada en modelo discreto.
        K = sumaCapacidades/len(lineas)
        Q = sumaRPK/sumaASK*K
#        Q = lambdaa*largo/(f*2.0) version old
        s = ((f*tp*(at + bt*K + gammaV*Q))/((gammaA*lambdaa)/(4*Va)))**(0.5)

    else:
        f = sumaFrecuencias/len(lineas)
        K = sumaCapacidades/len(lineas)
        Q = sumaRPK / sumaASK * K
#        Q = lambdaa*largo/(f*2.0) version old
        s = ((f*tp*(at + bt*K + gammaV*Q))/((gammaA*lambdaa)/(4*Va)))**(0.5)

    return s

def calcularCostoOperacion(red):
    '''

    :param red: objeto de la clase red.
    :return: retorna el costo total de operacion de un sistema definido por una red. Se van calculando los costos de operacion en cada
    una de las lineas y luego se suman.
    '''
    CostoLineas ={} #Diccionario con el costo de cada linea por id
    CostoTotal = 0
    lineas = red.lineas

    for l in lineas:
        #Se multiplica por dos ya que hay que considerar el ida y vuelta.
        costo = ((l.distanciaCorredor + l.distanciaPeriferia)*(red.ad + red.bd*l.cargaMaxima))*l.f*2 + (red.at + red.bt*l.cargaMaxima)*l.flota
        CostoLineas[l.ID] = costo
        CostoTotal += costo

    return (CostoTotal, CostoLineas)

def numeroMicrozonas(R1, beta, beta1, n):
    '''

    :param R1:
    :param beta:
    :param beta1:
    :param n:
    :return:
    '''
    #Numero teorico de microzonas segun proporcion geometrica de R1 respecto al ancho total.
    nTeoCBD = float(n)*float(R1)/float(beta)
    distMin = beta
    nEfectivoCBD = 0
    for i in range(1, int(n/2)):
        dist = ((i - nTeoCBD)**2)**(0.5)
        if dist < distMin:
            nEfectivoCBD = i
            distMin = dist
    nEfectivoCBD = max(nEfectivoCBD, 1)
    n0 = min(max(int(round(float(beta1)/float(beta)*float(n))), 1), n - nEfectivoCBD)
    nf = n-n0-nEfectivoCBD
    assert nf >= 0, 'nf o n0 es menor a 0'
    return n0, nEfectivoCBD, nf



def fo(red):
    '''

    :param red:
    :return:se retorna una funcion callable que ocupara scipy para evaluar la funcion objetivo respecto a las distintas frecuencias
    '''

    #Primero le pedimos a la red los objetos que ocuparemos para generar el modelo. En principio los OD y las lineas.
    k = red.k
    gammaE = red.gammaE
    gammaV = red.gammaV
    ODs=red.ODs
    lineas = red.lineas
    if red.tipo == "Cerrado":
        lineas.append(red.troncal)

    #Hacemos un diccionario que pase el ID de las lineas a numeracion interna
    #Tambien hacemos lo mismo para los OD
    dicLineas = {}
    i=0
    for l in red.lineas:
        dicLineas[l.ID] = i
        i += 1

    #Ahora creamos diccionarios con datos a utilizar en la funcion objetivo
    #Primero los costos de operacion que dependen de la distancia recorrida
    COd = {}
    for l in lineas:
        #((l.distanciaCorredor + l.distanciaPeriferia)*(red.ad + red.bd*l.cargaMaxima))*l.f*2 + (red.at + red.bt*l.cargaMaxima)*l.flota
        COd[l.ID] = (l.distanciaCorredor + l.distanciaPeriferia)*(red.ad + red.bd*l.cargaMaxima)*2

    #Luego los costos de operacion que dependen de las horas de operacion
    COt = {}
    for l in lineas:
        COt[l.ID] = (red.at + red.bt*l.cargaMaxima)*l.tCiclo

    #Esta es la demanda total de cada OD. Se utilizara para el tiempo de espera inicial
    DTotal = {}
    for od in ODs:
        DTotal[od.ID] = od.demandaTotal

    #Esta es la demanda indirecta de cada OD. Se utilizara para el tiempo de espera en transferencia
    DIndirecta = {}
    for od in ODs:
        DIndirecta[od.ID] = od.demandaIndirecta

    #Aca definimos la funcion que se entregara a scipy para ir probando la relacion Input/Output a optimizar. Lo que necesitamos que cambie durante la optimizacion,
    #debe cambiarse dentro de esta funcion.
    def f(x):
        #Primero, actualizamos las frecuencias con el input. Deberia cambiar solo el costo en cuanto al tamano de flota.
        #La flota y tamano de vehiculo deberian haber cambiado ya con el metodo actualizarfrecuencia.
        red.actualizarFrecuencias(x, dicLineas)
        CO = 0
        CE = 0
        CT = 0
        CP = 0

        suma = 0
        #Primero los costos de operacion
        for j in range(len(lineas)):
            suma += COd[lineas[j].ID]*x[dicLineas[lineas[j].ID]]+COt[lineas[j].ID]*x[dicLineas[lineas[j].ID]]
            CO += COd[lineas[j].ID]*x[dicLineas[lineas[j].ID]]+COt[lineas[j].ID]*x[dicLineas[lineas[j].ID]]

        #Luego espera al origen y en la transferencia
        for od in ODs:
            #Primero TEO
            #Rescatamos los ID de las lineas involucradas en este OD
            li = ()
            for l in od.ruta[0]:
                li = li + (dicLineas[l.ID],)
            #Luego agregamos los tiempos de espera iniciales
            feqi = 0
            for j in li:
                feqi += x[j]
            suma += gammaE*k*DTotal[od.ID]/feqi
            CE += gammaE*k*DTotal[od.ID]/feqi
            #En caso de que se amerite, consideramos las transferencias
            if not (od.ruta[1] == None):
                lt = ()
                for l in od.ruta[2]:
                    lt = lt + (dicLineas[l.ID],)
                feqt = 0
                for j in lt:
                    feqt += x[j]
                suma += gammaE*k*DIndirecta[od.ID]/feqt
                CT += gammaE*k*DIndirecta[od.ID]/feqt
                #Finalmente, tenemos que considerar tambien el caso en que haya dos transferencias para las redes cerradas.
                if not (od.ruta[3] == None):
                    ltt = ()
                    for l in od.ruta[4]:
                        ltt = ltt + (dicLineas[l.ID],)
                    feqtt = 0
                    for j in ltt:
                        feqtt += x[j]
                    suma += gammaE*k*DIndirecta[od.ID]/feqtt
                    CT += gammaE*k*DIndirecta[od.ID]/feqtt

            #Para el caso de tpvariable habra que sumar tambien tiempos de viaje
            suma += gammaV*DTotal[od.ID]*od.TotaltParada
            CP += gammaV*DTotal[od.ID]*od.TotaltParada

        #print 'Total:'+str(suma)+'-CO:'+str(CO)+"-CE:"+str(CE)+"-CT:"+str(CT)+"-CP:"+str(CP)
        #return suma
        #Probemos simplemente retornando el total del costo de la red
        print (red.iteracion)
        return red.CostoTotal

    return (f, dicLineas)

def optimiScipy(red):

    #obtenemos el diccionario a ocupar y la fo
    func = fo(red)
    f = func[0]
    dicLineas = func[1]
    x0 = ()
    for i in range(len(dicLineas)):
        x0 = x0 + (1.0,)

    res = minimize(f, x0, method='COBYLA')

    #print res.x
    #for l in red.lineas:
    #    print str(l.microZonas[0].ID)+"-"+str(l.microZonas[-1].ID)+", ",

    return (res.x, dicLineas)


def getSentido(origen, destino, linea):
    '''

    :param origen: Nodo origen desde donde comienza el viaje.
    :param destino: Nodo destino donde finaliza el viaje.
    :param linea: indica la linea sobre la cual se quiere saber el sentido del OD en cuestion.
    :return: retorna un string con 'Ida' si se cumplen parametros de ida, y 'Vuelta' en caso contrario. Para los viajes en la mizma zona se devuelve 'Ambos'
    '''
    for i in range(len(linea.microZonas)):
        if linea.microZonas[i].ID == origen.ID:
            o = i
        if linea.microZonas[i].ID == destino.ID:
            d = i

    if o == d:
        return "Ambos"
    elif o < d:#El origen esta a la izquierda en cuanto a su posicion del corredor
        return "Ida"
    elif o > d:
        return "Vuelta"

def distribucionDemanda(red):
    '''
    Este metodo distribuye los viajes generados y atraidos en las distintas zonas.
    :param red: Corresponde la red a distribuir. Se asume que las microzonas y los pares OD ya estan construidos. Ojo que los od son una lista simple llamada ODs. Hay que revisar cada origen y destino para ir sumando
    :return:
    '''
    #Primero organizamos los datos que vamos a utilizar: Oi, Dj, theta y fij
    #Nos conviene trabajar con diccionarios para ir haciendo calzar las sumas.
    #En el caso de las matrices, vamos a probar haciendo diccionarios bidimensionales, es decir un diccionario maestro que tiene un diccionario para cada zona de origen
    #y ese diccionario para cada zona tiene un valor por destino

    theta = red.theta
    Oi = {}#Demanda originada
    Dj = {}#Demanda atraida
    Oiobs = {}
    Djobs = {}
    Ai = {}#Coeficiente mod gravitacional
    Aiaux = {}#Auxiliar Ai
    Bjaux = {}#Auxiliar Bj
    Bj = {}#Coeficiente mod gravitacional
    fij = {}#funcion de costos para i y j. Depende de la distancia en ruta entre i y j.

    #Primero asignamos los valores a los diccionarios de un indice y creamos los diccionarios secundarios de las matrices.
    for macroz in red.macroZonas:
        for microz in red.macroZonas[macroz].microZonas:
            Oi[microz.ID] = microz.demandaO
            Dj[microz.ID] = microz.demandaD
            Oiobs[microz.ID] = 0
            Djobs[microz.ID] = 0
            Ai[microz.ID] = 1.0
            Bj[microz.ID] = 1.0
            Aiaux[microz.ID] = 1.0
            Bjaux[microz.ID] = 1.0
            fij[microz.ID] = {}
    #Ahora recorremos los OD para asignar los valores a la matriz Cij. La Vij solo necesita asignarse al final de la calibracion
    for od in red.ODs:
        fij[od.origen.ID][od.destino.ID] = exp(-theta*(od.distanciaPeriferia + od.distanciaCorredor))
    #Ahora podemos empezar a calibrar
        seguir = True
    while seguir:
        for i in Ai:
            Aiaux[i] = Ai[i]
            sumaAi = 0
            for j in Bj:
                sumaAi += Bj[j]*Dj[j]*fij[i][j]
            Ai[i] = 1/sumaAi

        for j in Bj:
            Bjaux[j] = Bj[j]
            sumaBj = 0
            for i in Ai:
                sumaBj += Ai[i]*Oi[i]*fij[i][j]
            Bj[j] = 1/sumaBj

        #Verificamos si cumplimos criterio de parada
        seguir = False
        for i in Ai:
            if fabs(Ai[i]-Aiaux[i])/Ai[i] > 0.005:
                seguir = True
                break
            if fabs(Bj[i]-Bjaux[i])/Bj[i] > 0.005:
                seguir = True
                break

    #Cuando sale del while, es porque ya estamos calibrados
    #Asi que podemos finalmente asignar los viajes
    #Ojo que tendremos que asignar la demanda directa e indirecta tambien mediante la funcion actualizarDemanda
    #Tambien sumaeremos viajes para corroborar que ande bien la cosa
    for od in red.ODs:
        #Para asignar la demanda ocupamos la funcion demanda definida en la clase OD
        od.demandaTotal = Ai[od.origen.ID]*Oi[od.origen.ID]*Bj[od.destino.ID]*Dj[od.destino.ID]*fij[od.origen.ID][od.destino.ID]
        od.actualizarDemanda()
        #Actualizamos aca la distancia total para la red ya que no sera necesairo volver a hacerlo
        red.distanciaTotal += od.distanciaTotal
        Oiobs[od.origen.ID] += od.demandaTotal
        Djobs[od.destino.ID] += od.demandaTotal

    #Finalmente actualizamos las variables de la red que dependen de la demanda.
    red.DatosTransferencias = red.getTransferencias()
    red.demandaIndirecta = red.DatosTransferencias[0]
    red.demandaDirecta = red.demandaTotal-red.demandaIndirecta
    red.Transferencias = red.DatosTransferencias[1]
    red.TiemposPersonas = red.getTiempoPersonas()
    red.TotaltViaje =red.TiemposPersonas[0]
    red.TotaltEspera =red.TiemposPersonas[1]
    red.TotaltAcceso =red.TiemposPersonas[2]
    red.TotaltTransferencia =red.TiemposPersonas[3]
    red.TotaltTransferenciaSinDelta = red.TiemposPersonas[4]
    red.TotaltMovimiento = red.TiemposPersonas[5]
    red.TotaltParada = red.TiemposPersonas[6]
    red.CostoTotaltMovimiento = red.TotaltMovimiento*red.gammaV
    red.CostoTotaltParada = red.TotaltParada*red.gammaV
    red.CostoTotaltViaje = red.TotaltViaje*red.gammaV
    red.CostoTotaltEspera = red.TotaltEspera*red.gammaE
    red.CostoTotaltAcceso = red.TotaltAcceso*red.gammaA
    red.CostoTotaltTransferencia = red.TotaltTransferencia*red.gammaE
    red.CostoTotal = red.CostoOperacion + red.CostoTotaltViaje + red.CostoTotaltEspera + red.CostoTotaltAcceso + red.CostoTotaltTransferencia
    red.tMovimientoPromedio = red.TotaltMovimiento/red.demandaTotal
    red.tParadaPromedio = red.TotaltParada/red.demandaTotal
    red.tViajePromedio = red.TotaltViaje/red.demandaTotal
    red.tEsperaPromedio = red.TotaltEspera/red.demandaTotal
    red.tAccesoPromedio = red.TotaltAcceso/red.demandaTotal
    red.tTransferenciaSinDeltaPromedio = red.TotaltTransferenciaSinDelta/red.demandaTotal
    red.tTransferenciaPromedio = red.TotaltTransferencia/red.demandaTotal
    red.CostoTotaltViajePromedio = red.CostoTotaltViaje/red.demandaTotal
    red.CostoTotaltMovimientoPromedio = red.CostoTotaltMovimiento/red.demandaTotal
    red.CostoTotaltParadaPromedio = red.CostoTotaltParada/red.demandaTotal
    red.CostoTotaltEsperaPromedio = red.CostoTotaltEspera/red.demandaTotal
    red.CostoTotaltAccesoPromedio = red.CostoTotaltAcceso/red.demandaTotal
    red.CostoTotaltTransferenciaPromedio = red.CostoTotaltTransferencia/red.demandaTotal
    red.CostoOperacionPromedio = red.CostoOperacion/red.demandaTotal
    red.CostoTotalPromedio = red.CostoTotal/red.demandaTotal
    red.transferenciasPromedio = red.Transferencias/red.demandaTotal
    red.largoViajePromedio = red.distanciaTotal/red.demandaTotal



    ###TESTEO Oi y Dj generados
    #dtotalobs = 0
    #dtotal = 0
    #for i in Oiobs:
    #    print Oiobs[i]
    #    print Oi[i]
    #    dtotal += Oi[i]
    #    dtotalobs += Oiobs[i]
    #print dtotalobs
    #print dtotal
    #print 'hola'


def promedioTparada(od, mz):
    '''
    Se aplica cuando el tiempo de parada es variable!!
    Por lo pesado que es calcular algo sobre cada od, resulta mejor ir guardando el resultado de este metodo en cada objeto od.
    Este metodo debe correrse al actualizar frecuencia, luego de haber cargado los buses.
    :param od: od al que pertenecen los viajeros a los que se les quiere calcular el in vehicle time por paradas en la microzona mz
    :param mz: microzona donde se quiere obtener el tparada promedio para los viajeros del OD od.
    :return: tiempo promedio de parada promedio de los viajeros del od en mz.
    '''
    #Primero debemos identificar en que porcion del viaje esta el mz para encontrar las lineas que estan utilizando los usuarios ahi.
    path = od.path
    nt1 = 0  #posicion dentro del path del nodo de transferencia 1. Si no existe queda como 0
    nt2 = 0  #posicion dentro del path del nodo de transferencia 2. Si no existe queda como 0
    nmz = 0  #posicion dentro del path del nodo a analizar mz.

    for i in range(len(path)):
        if path[i].ID == mz.ID:
            nmz = i
        if (not od.ruta[1] == None) and path[i].ID == od.ruta[1].ID:
            nt1 = i
        if (not od.ruta[3] == None) and path[i].ID == od.ruta[3].ID:
            nt2 = i

    #Vamos a asumir que si un mz es nodo de transferencia, las lineas a las que se suben los usuarios tras la transfe-
    #rencia son las que se utilizan en ese mz. Aprovechamos tambien de guardar el nodo a donde se subio al bus actual.
    nodoSubida = None

    if od.ruta[1] == None:
        #Caso en que son viajes directos
        lineas = od.ruta[0]
        nodoSubida = od.origen
    else:
        if od.ruta[3] == None:
            #Caso en que hay una transferencia
            if nmz < nt1:
                lineas = od.ruta[0]
                nodoSubida = od.origen
            else:
                lineas = od.ruta[2]
                nodoSubida = od.ruta[1]
        else:
            #Caso en que hay dos transferencias
            if nmz < nt1:
                lineas = od.ruta[0]
                nodoSubida = od.origen
            elif nmz < nt2:
                lineas = od.ruta[2]
                nodoSubida = od.ruta[1]
            else:
                lineas = od.ruta[4]
                nodoSubida = od.ruta[3]

    #Ok, ya tenemos las lineas que necesitamos. Ahora debemos obtener el tiempo de parada promedio en esa microzona
    #Nos falta saber en que sentido van esas lineas en esa microzona para ese od, pero eso se hara en el loop de lineas
    sumaTiempos = 0 #Suma de los tiempos de parada ponderados por frecuencia
    sumaFrecuencias = 0 #Suma de las frecuencias

    for l in lineas:
        sentido = getSentido(nodoSubida, mz, l)

        #En el caso de que vaya partiendo el viaje, nodoSubida puede ser igual a mz. En ese caso se asume el sentido
        #ocupando el siguiente nodo de la linea(a menos de que el destino sea ese mismo nodo, claro).
        if sentido == 'Ambos' and not(od.origen.ID == od.destino.ID):
            sentido = getSentido(nodoSubida, path[nmz + 1], l)

        #En el caso de viajes interzona(origen = destino), debemos hacer un promedio simple entre tiempos de ambos
        #sentidos, ya que el numero de personas en una direccions es igual al numero en la otra. Y luego ponderamos
        #Por la frecuencia para sumar este promedio simple con el de otras lineas.
        if sentido == 'Ambos':
            sumaTiempos += l.f*(l.tiemposParada['Ida'][mz.ID]+l.tiemposParada['Vuelta'][mz.ID])/2
            sumaFrecuencias += l.f #Como frecuencia es la misma ida y vuelta, solo ponemos l.f
        #Luego el resto de los casos
        else:
            sumaTiempos += l.f*l.tiemposParada[sentido][mz.ID]
            sumaFrecuencias += l.f

    #Finalmente el promedio es el cociente entre ambas sumas
    return sumaTiempos/sumaFrecuencias
















