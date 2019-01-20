__author__ = 'Pancho'
import xlsxwriter

def crearExcelnLineas(nombre, varIndependiente, CostoTotal, CostoOperacion, TViaje, TAcceso, TEspera, TTransferencia, DTransferencia, QTransferencia, CTransConDelta, CTransSinDelta, frecPorDistancia, TParada, TMovimiento):
    '''
    OBs: aca las listas puede ser de dos dimensiones para contener dentro de ellas una lista de valores para cada tipo de red. Por default, la primera lista es para red abierta y la segunda para red cerrada.
    :param nombre: nombre que tomara el workbook que se creara, no debe incluir el .xlsx
    :param varIndependiente: tupla con el nombre de la variable independiente en la primera celda, y lista con valores en la segunda celda.
    :param CostoTotal: lista con los valores que toma el costo total del sistema. Al igual que el resto de los indicadores, debe corresponder al orden de la lista dada por varIndependiente
    :param CostoOperacion: lista con la valores que toma el costo de operacion del sistema.
    :param TViaje: lista con los valores que toma el costo de viaje
    :param TAcceso: lista con los valores que toma el costo de acceso
    :param TEspera: lista con los valores que toma el costo de espera
    :param TTransferencia: lista con los valores que toma el costo de transferencia
    :return: no se retorna nada, simplemente se abre el excel que se acaba de crear.
    '''
    #Creamos un workbook para contener las salidas a graficar
    wb = xlsxwriter.Workbook(nombre+'.xlsx')
    #Dentro de ese workbook, habra un worksheet para cada grafico o set de graficos.
    wsMain = wb.add_worksheet('Main')
    wsTE   = wb.add_worksheet('TE y TT')
    wsCT   = wb.add_worksheet('CT y CO')
    wsTV   = wb.add_worksheet('TV y TA')
    wsTrans = wb.add_worksheet('Trans')
    #Creamos tambien los charts que se pegaran en sus respectivas hojas
    #Creamos los charts en el workbook
    chartMain = wb.add_chart({'type': 'line'})
    chartTE = wb.add_chart({'type': 'line'})
    chartCT = wb.add_chart({'type': 'line'})
    chartTV = wb.add_chart({'type': 'line'})
    charttrans1 = wb.add_chart({'type': 'line'})
    charttrans2 = wb.add_chart({'type': 'line'})

#En cada sheet crearemos una tabla con los resultados para cada una de las redes que se compararan

    nombresRedes = ('Abierta', 'Cerrada')
    tipoLineas = ('solid', 'dash_dot')
    nRedes = len(CostoTotal)
    largo = len(CostoTotal[0])
    for k in range(nRedes):
        #Partimos poniendo el nombre a cada una de las dos columnas
        wsMain.write(0 + k*(largo + 2), 0, varIndependiente[0])
        wsMain.write(0 + k*(largo + 2), 1, "Costo Total")
        wsMain.write(0 + k*(largo + 2), 2, "Costo Operacion")
        wsMain.write(0 + k*(largo + 2), 3, "Costo Tiempo de Viaje")
        wsMain.write(0 + k*(largo + 2), 4, "Costo Tiempo de Acceso")
        wsMain.write(0 + k*(largo + 2), 5, "Costo Tiempo de Espera")
        wsMain.write(0 + k*(largo + 2), 6, "Costo Tiempo de Transferencia")
        wsMain.write(0 + k*(largo + 2), 7, "Frecuencia*distancia")
        wsTE.write(0 + k*(largo + 2), 0, varIndependiente[0])
        wsTE.write(0 + k*(largo + 2), 1, "Costo Tiempo de Espera")
        wsTE.write(0 + k*(largo + 2), 2, "Costo Tiempo de Transferencia")
        wsCT.write(0 + k*(largo + 2), 0, varIndependiente[0])
        wsCT.write(0 + k*(largo + 2), 1, "Costo Total")
        wsCT.write(0 + k*(largo + 2), 2, "Costo de Operacion")
        wsTV.write(0 + k*(largo + 2), 0, varIndependiente[0])
        wsTV.write(0 + k*(largo + 2), 1, "Costo Tiempo de Viaje")
        wsTV.write(0 + k*(largo + 2), 2, "Costo Tiempo de Acceso")
        wsTV.write(0 + k*(largo + 2), 3, "Costo Tiempo en Parada")
        wsTV.write(0 + k*(largo + 2), 4, "Costo Tiempo de Movimiento")
        wsTrans.write(0 + k*(largo + 2), 0, varIndependiente[0])
        wsTrans.write(0 + k*(largo + 2), 1, "Demanda que transfiere")
        wsTrans.write(0 + k*(largo + 2), 2, "Cantidad de transferencias")
        wsTrans.write(0 + k*(largo + 2), 3, "Costo Trans sin penalizacion")
        wsTrans.write(0 + k*(largo + 2), 4, "Costo Trans con penalizacion")
        #Ahora comenzamos a pegar los resultados en ambas columnas
        for i in range(largo):
            wsMain.write(i + 1 + k*(largo + 2), 0, varIndependiente[1][i])
            wsMain.write(i + 1 + k*(largo + 2), 1, CostoTotal[k][i])
            wsMain.write(i + 1 + k*(largo + 2), 2, CostoOperacion[k][i])
            wsMain.write(i + 1 + k*(largo + 2), 3, TViaje[k][i])
            wsMain.write(i + 1 + k*(largo + 2), 4, TAcceso[k][i])
            wsMain.write(i + 1 + k*(largo + 2), 5, TEspera[k][i])
            wsMain.write(i + 1 + k*(largo + 2), 6, TTransferencia[k][i])
            wsMain.write(i + 1 + k*(largo + 2), 7, frecPorDistancia[k][i])
            wsTE.write(i + 1 + k*(largo + 2), 0, varIndependiente[1][i])
            wsTE.write(i + 1 + k*(largo + 2), 1, TEspera[k][i])
            wsTE.write(i + 1 + k*(largo + 2), 2, TTransferencia[k][i])
            wsCT.write(i + 1 + k*(largo + 2), 0, varIndependiente[1][i])
            wsCT.write(i + 1 + k*(largo + 2), 1, CostoTotal[k][i])
            wsCT.write(i + 1 + k*(largo + 2), 2, CostoOperacion[k][i])
            wsTV.write(i + 1 + k*(largo + 2), 0, varIndependiente[1][i])
            wsTV.write(i + 1 + k*(largo + 2), 1, TViaje[k][i])
            wsTV.write(i + 1 + k*(largo + 2), 2, TAcceso[k][i])
            wsTV.write(i + 1 + k*(largo + 2), 3, TParada[k][i])
            wsTV.write(i + 1 + k*(largo + 2), 4, TMovimiento[k][i])
            wsTrans.write(i + 1 + k*(largo + 2), 0, varIndependiente[1][i])
            wsTrans.write(i + 1 + k*(largo + 2), 1, DTransferencia[k][i])
            wsTrans.write(i + 1 + k*(largo + 2), 2, QTransferencia[k][i])
            wsTrans.write(i + 1 + k*(largo + 2), 3, CTransSinDelta[k][i])
            wsTrans.write(i + 1 + k*(largo + 2), 4, CTransConDelta[k][i])

        #Le agregamos los datos a los charts
        #                                [sheetname, first_row, first_col, last_row, last_col]
        chartMain.add_series({
            'categories':'=Main!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=Main!$B$'+str(2+k*(largo+2))+':$B$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'red'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Costo Total '+nombresRedes[k]
        })
        chartMain.add_series({
            'categories':'=Main!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=Main!$C$'+str(2+k*(largo+2))+':$C$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'lime'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Costo Operacion '+nombresRedes[k]
        })
        chartMain.add_series({
            'categories':'=Main!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=Main!$D$'+str(2+k*(largo+2))+':$D$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'green'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Tiempo de Viaje '+nombresRedes[k]
        })
        chartMain.add_series({
            'categories':'=Main!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=Main!$E$'+str(2+k*(largo+2))+':$E$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'purple'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Tiempo de Acceso '+nombresRedes[k]
        })
        chartMain.add_series({
            'categories':'=Main!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=Main!$F$'+str(2+k*(largo+2))+':$F$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'orange'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Tiempo de Espera '+nombresRedes[k]
        })
        chartMain.add_series({
            'categories':'=Main!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=Main!$G$'+str(2+k*(largo+2))+':$G$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'navy'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Tiempo de Transferencia '+nombresRedes[k]
        })
        chartTE.add_series({
            'categories':'=TE y TT!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=TE y TT!$B$'+str(2+k*(largo+2))+':$B$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'orange'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Tiempo de Espera '+nombresRedes[k]
        })
        chartTE.add_series({
            'categories':'=TE y TT!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=TE y TT!$C$'+str(2+k*(largo+2))+':$C$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'navy'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Tiempo de Transferencia '+nombresRedes[k]

        })
        chartCT.add_series({
            'categories':'=CT y CO!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=CT y CO!$B$'+str(2+k*(largo+2))+':$B$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'orange'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Costo Total '+nombresRedes[k]
        })
        chartCT.add_series({
            'categories':'=CT y CO!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=CT y CO!$C$'+str(2+k*(largo+2))+':$C$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'navy'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Costo de Operacion '+nombresRedes[k]
        })
        chartTV.add_series({
            'categories':'=TV y TA!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=TV y TA!$B$'+str(2+k*(largo+2))+':$B$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'orange'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Tiempo de Viaje '+nombresRedes[k]
        })
        chartTV.add_series({
            'categories':'=TV y TA!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=TV y TA!$C$'+str(2+k*(largo+2))+':$C$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'navy'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Tiempo de Acceso '+nombresRedes[k]
        })
        chartTV.add_series({
            'categories':'=TV y TA!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=TV y TA!$D$'+str(2+k*(largo+2))+':$D$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'red'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Tiempo de Parada '+nombresRedes[k]
        })
        chartTV.add_series({
            'categories':'=TV y TA!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=TV y TA!$E$'+str(2+k*(largo+2))+':$E$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'green'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Tiempo en Movimiento '+nombresRedes[k]
        })
        charttrans1.add_series({
            'categories':'=Trans!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=Trans!$B$'+str(2+k*(largo+2))+':$B$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'orange'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Demanda que transfiere '+nombresRedes[k]
        })
        charttrans1.add_series({
            'categories':'=Trans!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=Trans!$C$'+str(2+k*(largo+2))+':$C$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'navy'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Cantidad de Transferencias '+nombresRedes[k]
        })
        charttrans2.add_series({
            'categories':'=Trans!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=Trans!$D$'+str(2+k*(largo+2))+':$D$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'orange'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Costo Transferencias sin penalizacion '+nombresRedes[k]
        })
        charttrans2.add_series({
            'categories':'=Trans!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=Trans!$E$'+str(2+k*(largo+2))+':$E$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'navy'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Costo Transferencias con penalizacion '+nombresRedes[k]
        })


    #Finalmente insertamos el chart en la sheet donde queremos
    wsMain.insert_chart('I5', chartMain)
    wsTE.insert_chart('F5', chartTE)
    wsCT.insert_chart('F5', chartCT)
    wsTV.insert_chart('F5', chartTV)
    wsTrans.insert_chart('H5', charttrans1)
    wsTrans.insert_chart('H12', charttrans2)

    wb.close()

def crearExcelRed(red, nombre):
    '''
    Excel con la informacion de la red entregada. Se asume que esta la informacion respecto a distintos valores de f.
    Muestra:
    1) Costos Agregados (con porcentajes respecto a total)
    2) Costos por Macrozona
    3) Carga de los vehiculos
    4) Tamano de vehiculo
    5) Histograma de tiempos
    6) Costos por persona transportada
    7) Capacidad de buses
    8) Flota optima
    9) Espaciamiento paraderos optimo
    10) ASK, RPK y FO
    11) Transferencias totales y por persona
    Obs: Estos indicadores se muestran para distintos valores de f.

    :param red: Esta es la red a analizar y para la cual se creara el excel
    :return:no retorna nada, solo crea un archivo excel con toda la info de esta red.
    '''
    #Paramostrar los costos podemos ocupar el esquema que tenemos para el Excel respecto a distintas n, pero respecto a los distintos f.
    #Como no es un solo f, podemos ir mostrando los distintos valores que ocupa el solver para el vector f. Le asignamos un id a cada par f-red.

    #Partimos rescatando de la red de input, toda la informacion necesaria.
    varIndependiente = [[]]
    CostoTotal = [[]]
    CostoOperacion = [[]]
    TViaje = [[]]
    TAcceso = [[]]
    TEspera = [[]]
    TTransferencia = [[]]
    DTransferencia = [[]]
    QTransferencia = [[]]
    CTransSinDelta = [[]]
    CTransConDelta = [[]]
    fPromedio = [[]]
    fPorDist = [[]]
    FOPromedio = [[]]
    flota = [[]]
    KPromedio = [[]]
    KOciosaTotal = [[]]
    sc =[[]]
    sp = [[]]
    vComercial = [[]]
    largoViajePromedio = [[]]
    tViajeMovimiento = [[]]
    tParadaFijo = [[]]
    tParadaVariable = [[]]
    infoCargaL1 = [[]]
    mzL1 = [[]]

    for i in range(red.iteracion):
        varIndependiente[0].append(i)
        CostoTotal[0].append(red.resultadosPorFrecuencia[i].CostoTotal)
        CostoOperacion[0].append(red.resultadosPorFrecuencia[i].CostoOperacion)
        TViaje[0].append(red.resultadosPorFrecuencia[i].CostoTotaltViaje)
        TAcceso[0].append(red.resultadosPorFrecuencia[i].CostoTotaltAcceso)
        TEspera[0].append(red.resultadosPorFrecuencia[i].CostoTotaltEspera)
        TTransferencia[0].append(red.resultadosPorFrecuencia[i].CostoTotaltTransferencia)
        DTransferencia[0].append(red.resultadosPorFrecuencia[i].demandaIndirecta)
        QTransferencia[0].append(red.resultadosPorFrecuencia[i].Transferencias)
        CTransSinDelta[0].append(red.resultadosPorFrecuencia[i].TotaltTransferencia)
        CTransConDelta[0].append(red.resultadosPorFrecuencia[i].TotaltTransferenciaSinDelta)
        fPromedio[0].append(red.resultadosPorFrecuencia[i].frecuenciaPromedio)
        fPorDist[0].append(red.resultadosPorFrecuencia[i].frecPorDistancia)
        FOPromedio[0].append(red.resultadosPorFrecuencia[i].FOPromedio)
        flota[0].append(red.resultadosPorFrecuencia[i].FlotaTotal)
        KPromedio[0].append(red.resultadosPorFrecuencia[i].CapacidadPromedio)
        KOciosaTotal[0].append(red.resultadosPorFrecuencia[i].CapacidadOciosaTotal)
        sc[0].append(red.resultadosPorFrecuencia[i].sc)
        sp[0].append(red.resultadosPorFrecuencia[i].sp)
        vComercial[0].append(red.resultadosPorFrecuencia[i].vComercialPromedio)
        largoViajePromedio[0].append(red.resultadosPorFrecuencia[i].largoViajePromedio)
        tViajeMovimiento[0].append(red.resultadosPorFrecuencia[i].TotaltMovimiento)
        tParadaFijo[0].append(red.resultadosPorFrecuencia[i].TotaltParadaFijo)
        tParadaVariable[0].append(red.resultadosPorFrecuencia[i].TotaltParadaVariable)
        infoCargaL1[0].append(red.resultadosPorFrecuencia[i].lineas[0].infoCarga["Ida"])
        mzL1[0].append(red.resultadosPorFrecuencia[i].lineas[0].microZonas)


    #Creamos un workbook para contener las salidas a graficar
    redtipo = red.tipo
    n = str(len(red.lineas))
    wb = xlsxwriter.Workbook("Red"+redtipo+'n'+n+nombre+'.xlsx')
    #Dentro de ese workbook, habra un worksheet para cada grafico o set de graficos.
    wsMain = wb.add_worksheet('Main')
    wsTE   = wb.add_worksheet('TE y TT')
    wsCT   = wb.add_worksheet('CT y CO')
    wsTV   = wb.add_worksheet('TV y TA')
    wsTrans = wb.add_worksheet('Trans')
    wsFKB = wb.add_worksheet('Frec y K')
    wsInfoC = wb.add_worksheet('InfoC')
    wsCLineas = wb.add_worksheet('CompLineas')

    #Creamos tambien los charts que se pegaran en sus respectivas hojas
    #Creamos los charts en el workbook
    chartMain = wb.add_chart({'type': 'line'})
    chartTE = wb.add_chart({'type': 'line'})
    chartCT = wb.add_chart({'type': 'line'})
    chartTV = wb.add_chart({'type': 'line'})
    charttrans1 = wb.add_chart({'type': 'line'})
    charttrans2 = wb.add_chart({'type': 'line'})
    chartfrecLineas = wb.add_chart({'type': 'column'})
    chartVelCom = wb.add_chart({'type': 'column'})
    chartK = wb.add_chart({'type': 'column'})
    chartFlota = wb.add_chart({'type': 'column'})
    chartFO = wb.add_chart({'type': 'column'})

    #En cada sheet crearemos una tabla con los resultados para cada una de las redes que se compararan

    nombresRedes = ('Abierta', 'Cerrada')
    tipoLineas = ('solid', 'dash_dot')
    sentido = ('Ida', 'Vuelta')
    nRedes = 1
    largo = red.iteracion
    for k in range(nRedes):
        #Partimos poniendo el nombre a cada una de las dos columnas
        wsMain.write(0 + k*(largo + 2), 0, "Iteracion")
        wsMain.write(0 + k*(largo + 2), 1, "Costo Total")
        wsMain.write(0 + k*(largo + 2), 2, "Costo Operacion")
        wsMain.write(0 + k*(largo + 2), 3, "Costo Tiempo de Viaje")
        wsMain.write(0 + k*(largo + 2), 4, "Costo Tiempo de Acceso")
        wsMain.write(0 + k*(largo + 2), 5, "Costo Tiempo de Espera")
        wsMain.write(0 + k*(largo + 2), 6, "Costo Tiempo de Transferencia")
        wsTE.write(0 + k*(largo + 2), 0, "Iteracion")
        wsTE.write(0 + k*(largo + 2), 1, "Costo Tiempo de Espera")
        wsTE.write(0 + k*(largo + 2), 2, "Costo Tiempo de Transferencia")
        wsCT.write(0 + k*(largo + 2), 0, "Iteracion")
        wsCT.write(0 + k*(largo + 2), 1, "Costo Total")
        wsCT.write(0 + k*(largo + 2), 2, "Costo de Operacion")
        wsTV.write(0 + k*(largo + 2), 0, "Iteracion")
        wsTV.write(0 + k*(largo + 2), 1, "Costo Tiempo de Viaje")
        wsTV.write(0 + k*(largo + 2), 2, "Costo Tiempo de Acceso")
        wsTrans.write(0 + k*(largo + 2), 0, "Iteracion")
        wsTrans.write(0 + k*(largo + 2), 1, "Demanda que transfiere")
        wsTrans.write(0 + k*(largo + 2), 2, "Cantidad de transferencias")
        wsTrans.write(0 + k*(largo + 2), 3, "Costo Trans sin penalizacion")
        wsTrans.write(0 + k*(largo + 2), 4, "Costo Trans con penalizacion")
        wsFKB.write(0 + k*(largo + 2), 0, "Iteracion")
        wsFKB.write(0 + k*(largo + 2), 1, "Frecuencia Promedio")
        wsFKB.write(0 + k*(largo + 2), 2, "Frecuencia por Distancia")
        wsFKB.write(0 + k*(largo + 2), 3, "FO Promedio")
        wsFKB.write(0 + k*(largo + 2), 4, "Flota Total")
        wsFKB.write(0 + k*(largo + 2), 5, "Capacidad Promedio")
        wsFKB.write(0 + k*(largo + 2), 6, "Capacidad Ociosa Total")
        wsFKB.write(0 + k*(largo + 2), 7, "Spacing Corredor")
        wsFKB.write(0 + k*(largo + 2), 8, "Spacing Periferia")
        wsFKB.write(0 + k*(largo + 2), 9, "Velocidad Comercial Promedio")
        wsFKB.write(0 + k*(largo + 2), 10, "Largo de Viaje Promedio")
        wsFKB.write(0 + k*(largo + 2), 11, "Total tiempo en movimiento")
        wsFKB.write(0 + k*(largo + 2), 12, "Total tiempo parada fijo")
        wsFKB.write(0 + k*(largo + 2), 14, "Total tiempo parada variable")
        wsCLineas.write(0 + k*(largo + 2), 0, "Linea")
        wsCLineas.write(0 + k*(largo + 2), 1, "Frecuencia")
        wsCLineas.write(0 + k*(largo + 2), 2, "Velocidad Comercial")
        wsCLineas.write(0 + k*(largo + 2), 3, "Tamano Vehiculo")
        wsCLineas.write(0 + k*(largo + 2), 4, "Flota")
        wsCLineas.write(0 + k*(largo + 2), 5, "ASK")
        wsCLineas.write(0 + k*(largo + 2), 6, "RPK")
        wsCLineas.write(0 + k*(largo + 2), 7, "Factor de Ocupacion")

        #Ahora comenzamos a pegar los resultados en ambas columnas
        for i in range(largo):
            wsMain.write(i + 1 + k*(largo + 2), 0, varIndependiente[k][i])
            wsMain.write(i + 1 + k*(largo + 2), 1, CostoTotal[k][i])
            wsMain.write(i + 1 + k*(largo + 2), 2, CostoOperacion[k][i])
            wsMain.write(i + 1 + k*(largo + 2), 3, TViaje[k][i])
            wsMain.write(i + 1 + k*(largo + 2), 4, TAcceso[k][i])
            wsMain.write(i + 1 + k*(largo + 2), 5, TEspera[k][i])
            wsMain.write(i + 1 + k*(largo + 2), 6, TTransferencia[k][i])
            wsTE.write(i + 1 + k*(largo + 2), 0, varIndependiente[k][i])
            wsTE.write(i + 1 + k*(largo + 2), 1, TEspera[k][i])
            wsTE.write(i + 1 + k*(largo + 2), 2, TTransferencia[k][i])
            wsCT.write(i + 1 + k*(largo + 2), 0, varIndependiente[k][i])
            wsCT.write(i + 1 + k*(largo + 2), 1, CostoTotal[k][i])
            wsCT.write(i + 1 + k*(largo + 2), 2, CostoOperacion[k][i])
            wsTV.write(i + 1 + k*(largo + 2), 0, varIndependiente[k][i])
            wsTV.write(i + 1 + k*(largo + 2), 1, TViaje[k][i])
            wsTV.write(i + 1 + k*(largo + 2), 2, TAcceso[k][i])
            wsTrans.write(i + 1 + k*(largo + 2), 0, varIndependiente[k][i])
            wsTrans.write(i + 1 + k*(largo + 2), 1, DTransferencia[k][i])
            wsTrans.write(i + 1 + k*(largo + 2), 2, QTransferencia[k][i])
            wsTrans.write(i + 1 + k*(largo + 2), 3, CTransSinDelta[k][i])
            wsTrans.write(i + 1 + k*(largo + 2), 4, CTransConDelta[k][i])
            wsFKB.write(i + 1 + k*(largo + 2), 0, varIndependiente[k][i])
            wsFKB.write(i + 1 + k*(largo + 2), 1, fPromedio[k][i])
            wsFKB.write(i + 1 + k*(largo + 2), 2, fPorDist[k][i])
            wsFKB.write(i + 1 + k*(largo + 2), 3, FOPromedio[k][i])
            wsFKB.write(i + 1 + k*(largo + 2), 4, flota[k][i])
            wsFKB.write(i + 1 + k*(largo + 2), 5, KPromedio[k][i])
            wsFKB.write(i + 1 + k*(largo + 2), 6, KOciosaTotal[k][i])
            wsFKB.write(i + 1 + k*(largo + 2), 7, sc[k][i])
            wsFKB.write(i + 1 + k*(largo + 2), 8, sp[k][i])
            wsFKB.write(i + 1 + k*(largo + 2), 9, vComercial[k][i])
            wsFKB.write(i + 1 + k*(largo + 2), 10, largoViajePromedio[k][i])
            wsFKB.write(i + 1 + k*(largo + 2), 11, tViajeMovimiento[k][i])
            wsFKB.write(i + 1 + k*(largo + 2), 12, tParadaFijo[k][i])
            wsFKB.write(i + 1 + k*(largo + 2), 13, tParadaVariable[k][i])


        #Y los resultados de Infocarga y lineas
        nlineas = len(red.resultadosPorFrecuencia[red.iteracion-1].lineas)#Numero de lineas de la ultima red de esta ciudad
        largoCiclo = 0
        #Primero los encabezados
        for l in range(nlineas):

            for s in range(len(sentido)):
                wsInfoC.write(0 + largoCiclo, 0, "Linea"+str(l)+"-"+sentido[s])
                wsInfoC.write(0 + largoCiclo, 1, "f"+str(l))
                wsInfoC.write(1 + largoCiclo, 1, "vComercial"+str(l))
                wsInfoC.write(2 + largoCiclo, 1, "K"+str(l))
                wsInfoC.write(3 + largoCiclo, 1, "B"+str(l))
                wsInfoC.write(4 + largoCiclo, 1, "ASK"+str(l))
                wsInfoC.write(5 + largoCiclo, 1, "RPK"+str(l))
                wsInfoC.write(6 + largoCiclo, 1, "FO"+str(l))
                wsInfoC.write(7 + largoCiclo, 1, "MZ-ID")
                wsInfoC.write(8 + largoCiclo, 1, "Carga")
                wsInfoC.write(9 + largoCiclo, 1, "Subidas")
                wsInfoC.write(10 + largoCiclo, 1, "Bajadas")
                wsInfoC.write(11 + largoCiclo, 1, "Ocupacion")

                #Luego los datos
                wsInfoC.write(0 + largoCiclo, 2, red.resultadosPorFrecuencia[red.iteracion-1].lineas[l].f)
                wsInfoC.write(1 + largoCiclo, 2, red.resultadosPorFrecuencia[red.iteracion-1].lineas[l].velocidadComercial)
                wsInfoC.write(2 + largoCiclo, 2, red.resultadosPorFrecuencia[red.iteracion-1].lineas[l].cargaMaxima)
                wsInfoC.write(3 + largoCiclo, 2, red.resultadosPorFrecuencia[red.iteracion-1].lineas[l].flota)
                wsInfoC.write(4 + largoCiclo, 2, red.resultadosPorFrecuencia[red.iteracion-1].lineas[l].ASK)
                wsInfoC.write(5 + largoCiclo, 2, red.resultadosPorFrecuencia[red.iteracion-1].lineas[l].RPK)
                wsInfoC.write(6 + largoCiclo, 2, red.resultadosPorFrecuencia[red.iteracion-1].lineas[l].FOPromedio)
                wsCLineas.write(1 + l, 0, 'Linea '+str(red.resultadosPorFrecuencia[red.iteracion-1].lineas[l].ID))
                wsCLineas.write(1 + l, 1, red.resultadosPorFrecuencia[red.iteracion-1].lineas[l].f)
                wsCLineas.write(1 + l, 2, red.resultadosPorFrecuencia[red.iteracion-1].lineas[l].velocidadComercial)
                wsCLineas.write(1 + l, 3, red.resultadosPorFrecuencia[red.iteracion-1].lineas[l].cargaMaxima)
                wsCLineas.write(1 + l, 4, red.resultadosPorFrecuencia[red.iteracion-1].lineas[l].flota)
                wsCLineas.write(1 + l, 5, red.resultadosPorFrecuencia[red.iteracion-1].lineas[l].ASK)
                wsCLineas.write(1 + l, 6, red.resultadosPorFrecuencia[red.iteracion-1].lineas[l].RPK)
                wsCLineas.write(1 + l, 7, red.resultadosPorFrecuencia[red.iteracion-1].lineas[l].FOPromedio)

                #Seteamos el ancho de las microzonas
                ancho = len(red.resultadosPorFrecuencia[red.iteracion-1].lineas[l].microZonas)

                #Se inicializa la primera columna con la info de salida del terminal
                wsInfoC.write(7 + largoCiclo, 2, 'Inicio')
                wsInfoC.write(8 + largoCiclo, 2, 0)
                wsInfoC.write(9 + largoCiclo, 2, 0)
                wsInfoC.write(10 + largoCiclo, 2, 0)
                wsInfoC.write(11 + largoCiclo, 2, 0)

                #Luego las microzonas
                for j in range(ancho):
                    if sentido[s] == "Ida":
                        id = red.resultadosPorFrecuencia[red.iteracion - 1].lineas[l].microZonas[j].ID
                    else:
                        id = red.resultadosPorFrecuencia[red.iteracion - 1].lineas[l].microZonas[-1-j].ID
                    wsInfoC.write(7 + largoCiclo, 3 + j, id)
                    wsInfoC.write(8 + largoCiclo, 3 + j, red.resultadosPorFrecuencia[red.iteracion-1].lineas[l].infoCarga[sentido[s]][0][id])
                    wsInfoC.write(9 + largoCiclo, 3 + j, red.resultadosPorFrecuencia[red.iteracion-1].lineas[l].infoCarga[sentido[s]][1][id])
                    wsInfoC.write(10 + largoCiclo, 3 + j, red.resultadosPorFrecuencia[red.iteracion-1].lineas[l].infoCarga[sentido[s]][2][id])
                    wsInfoC.write(11 + largoCiclo, 3 + j, red.resultadosPorFrecuencia[red.iteracion-1].lineas[l].infoCarga[sentido[s]][3][id])

                #Creamos un chart para ir viendo la carga de la linea
                chartCarga = wb.add_chart({'type': 'line'})
                chartCarga.add_series({
                'categories': ['InfoC', 7 + largoCiclo, 2, 7 + largoCiclo, 3 + ancho],
                'values':     ['InfoC', 8 + largoCiclo, 2, 8 + largoCiclo, 3 + ancho],
                'line':       {'color': 'red'},
                'name': 'Carga'
                })

                chartCarga.add_series({
                'categories': ['InfoC', 7 + largoCiclo, 2, 7 + largoCiclo, 3 + ancho],
                'values':     ['InfoC', 9 + largoCiclo, 2, 9 + largoCiclo, 3 + ancho],
                'line':       {'color': 'green'},
                'name': 'Subidas'
                })

                chartCarga.add_series({
                'categories': ['InfoC', 7 + largoCiclo, 2, 7 + largoCiclo, 3 + ancho],
                'values':     ['InfoC', 10 + largoCiclo, 2, 10 + largoCiclo, 3 + ancho],
                'line':       {'color': 'blue'},
                'name': 'Bajadas'
                })

                wsInfoC.insert_chart(largoCiclo, 4 + ancho, chartCarga)

                largoCiclo += 14



        #Le agregamos los datos a los charts normales
        #                                [sheetname, first_row, first_col, last_row, last_col]
        chartMain.add_series({
            'categories':'=Main!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=Main!$B$'+str(2+k*(largo+2))+':$B$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'red'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Costo Total '+nombresRedes[k]
        })
        chartMain.add_series({
            'categories':'=Main!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=Main!$C$'+str(2+k*(largo+2))+':$C$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'lime'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Costo Operacion '+nombresRedes[k]
        })
        chartMain.add_series({
            'categories':'=Main!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=Main!$D$'+str(2+k*(largo+2))+':$D$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'green'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Tiempo de Viaje '+nombresRedes[k]
        })
        chartMain.add_series({
            'categories':'=Main!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=Main!$E$'+str(2+k*(largo+2))+':$E$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'purple'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Tiempo de Acceso '+nombresRedes[k]
        })
        chartMain.add_series({
            'categories':'=Main!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=Main!$F$'+str(2+k*(largo+2))+':$F$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'orange'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Tiempo de Espera '+nombresRedes[k]
        })
        chartMain.add_series({
            'categories':'=Main!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=Main!$G$'+str(2+k*(largo+2))+':$G$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'navy'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Tiempo de Transferencia '+nombresRedes[k]
        })
        chartTE.add_series({
            'categories':'=TE y TT!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=TE y TT!$B$'+str(2+k*(largo+2))+':$B$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'orange'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Tiempo de Espera '+nombresRedes[k]
        })
        chartTE.add_series({
            'categories':'=TE y TT!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=TE y TT!$C$'+str(2+k*(largo+2))+':$C$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'navy'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Tiempo de Transferencia '+nombresRedes[k]

        })
        chartCT.add_series({
            'categories':'=CT y CO!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=CT y CO!$B$'+str(2+k*(largo+2))+':$B$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'orange'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Costo Total '+nombresRedes[k]
        })
        chartCT.add_series({
            'categories':'=CT y CO!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=CT y CO!$C$'+str(2+k*(largo+2))+':$C$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'navy'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Costo de Operacion '+nombresRedes[k]
        })
        chartTV.add_series({
            'categories':'=TV y TA!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=TV y TA!$B$'+str(2+k*(largo+2))+':$B$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'orange'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Tiempo de Viaje '+nombresRedes[k]
        })
        chartTV.add_series({
            'categories':'=TV y TA!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=TV y TA!$C$'+str(2+k*(largo+2))+':$C$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'navy'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Tiempo de Acceso '+nombresRedes[k]
        })
        charttrans1.add_series({
            'categories':'=Trans!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=Trans!$B$'+str(2+k*(largo+2))+':$B$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'orange'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Demanda que transfiere '+nombresRedes[k]
        })
        charttrans1.add_series({
            'categories':'=Trans!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=Trans!$C$'+str(2+k*(largo+2))+':$C$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'navy'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Cantidad de Transferencias '+nombresRedes[k]
        })
        charttrans2.add_series({
            'categories':'=Trans!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=Trans!$D$'+str(2+k*(largo+2))+':$D$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'orange'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Transferencias sin Delta '+nombresRedes[k]
        })
        charttrans2.add_series({
            'categories':'=Trans!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=Trans!$E$'+str(2+k*(largo+2))+':$E$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'navy'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Transferencias con Delta '+nombresRedes[k]
        })
        chartfrecLineas.add_series({
            'categories':'=CompLineas!$A$2:$A$'+str(nlineas + 1),
            'values':    '=CompLineas!$B$2:$B$'+str(nlineas + 1),
            'line':       {'color': 'red'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Frecuencias'
        })
        chartVelCom.add_series({
            'categories':'=CompLineas!$A$2:$A$'+str(nlineas + 1),
            'values':    '=CompLineas!$C$2:$C$'+str(nlineas + 1),
            'line':       {'color': 'red'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Velocidad Comercial'
        })
        chartK.add_series({
            'categories':'=CompLineas!$A$2:$A$'+str(nlineas + 1),
            'values':    '=CompLineas!$D$2:$D$'+str(nlineas + 1),
            'line':       {'color': 'red'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Tamano Vehiculo'
        })
        chartFlota.add_series({
            'categories':'=CompLineas!$A$2:$A$'+str(nlineas + 1),
            'values':    '=CompLineas!$E$2:$E$'+str(nlineas + 1),
            'line':       {'color': 'red'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Flota'
        })
        chartFO.add_series({
            'categories':'=CompLineas!$A$2:$A$'+str(nlineas + 1),
            'values':    '=CompLineas!$H$2:$H$'+str(nlineas + 1),
            'line':       {'color': 'red'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Factor de Ocupacion'
        })

    #Finalmente insertamos el chart en la sheet donde queremos
    wsMain.insert_chart('I5', chartMain)
    wsTE.insert_chart('F5', chartTE)
    wsCT.insert_chart('F5', chartCT)
    wsTV.insert_chart('F5', chartTV)
    wsTrans.insert_chart('H5', charttrans1)
    wsTrans.insert_chart('H12', charttrans2)
    wsCLineas.insert_chart('J2', chartfrecLineas)
    wsCLineas.insert_chart('J18', chartVelCom)
    wsCLineas.insert_chart('R2', chartK)
    wsCLineas.insert_chart('R18', chartFlota)
    wsCLineas.insert_chart('J33', chartFO)

    wb.close()


def crearExcelCiudades(ciudades):
    '''
    Vamos a hacer lo mismo que en nRedes, pero con nCiudades ocupando una sola red por ciudad. Esa red por ciudad puede ser una optima o alguna a comparar.
    Tambien vamos a tender a comparar valores de costos promedio entre ciudades, ya que no tiene sentido comparar costos totales.
    Se asume que la red a comparar esta en la posicion 0 de la lista de la ciudad.
    :param redes: Toma como parametros distintas ciudades definidas por geometria y densidad de demanda. Asume que cada ciudad tiene varias posibles redes cargadas
    :return: No retarna nada al modelo. Crea un excel que compara indicadores entre distintas ciudades. Por ej.: frec* v/s densidad de demanda.
    '''

    #Partimos rescatando de la red de input, toda la informacion necesaria.
    varIndependiente = [[], []]
    LambdaP = [[], []]
    LambdaC = [[], []]
    LambdaCBD = [[], []]
    demandaTotal = [[], []]
    CostoTotal = [[], []]
    CostoOperacion = [[], []]
    TViaje = [[], []]
    TAcceso = [[], []]
    TEspera = [[], []]
    TTransferencia = [[], []]
    DTransferencia = [[], []]
    QTransferencia = [[], []]
    CTransSinDelta = [[], []]
    CTransConDelta = [[], []]
    frecuenciaL1 = [[], []]
    sizeL1 = [[], []]
    flotaL1 = [[], []]
    infoCargaL1 = [[], []]
    mzL1 = [[], []]

    nombreRedes = ["Abierta", "Cerrada"]
    for k in range(len(nombreRedes)):
        for i in range(len(ciudades)):
            varIndependiente[k].append(i)
            LambdaP[k].append(ciudades[i].lambdap)
            LambdaC[k].append(ciudades[i].lambdac)
            LambdaCBD[k].append(ciudades[i].lambdaCBD)
            demandaTotal[k].append(ciudades[i].red[nombreRedes[k]][0].demandaTotal)
            CostoTotal[k].append(ciudades[i].red[nombreRedes[k]][0].CostoTotalPromedio)
            CostoOperacion[k].append(ciudades[i].red[nombreRedes[k]][0].CostoOperacionPromedio)
            TViaje[k].append(ciudades[i].red[nombreRedes[k]][0].CostoTotaltViajePromedio)
            TAcceso[k].append(ciudades[i].red[nombreRedes[k]][0].CostoTotaltAccesoPromedio)
            TEspera[k].append(ciudades[i].red[nombreRedes[k]][0].CostoTotaltEsperaPromedio)
            TTransferencia[k].append(ciudades[i].red[nombreRedes[k]][0].CostoTotaltTransferenciaPromedio)
            DTransferencia[k].append(ciudades[i].red[nombreRedes[k]][0].demandaIndirecta/ciudades[i].red[nombreRedes[k]][0].demandaTotal)
            QTransferencia[k].append(ciudades[i].red[nombreRedes[k]][0].Transferencias/ciudades[i].red[nombreRedes[k]][0].demandaTotal)
            CTransSinDelta[k].append(ciudades[i].red[nombreRedes[k]][0].TotaltTransferencia/ciudades[i].red[nombreRedes[k]][0].demandaTotal)
            CTransConDelta[k].append(ciudades[i].red[nombreRedes[k]][0].TotaltTransferenciaSinDelta/ciudades[i].red[nombreRedes[k]][0].demandaTotal)
            frecuenciaL1[k].append(ciudades[i].red[nombreRedes[k]][0].lineas[0].f)
            sizeL1[k].append(ciudades[i].red[nombreRedes[k]][0].lineas[0].cargaMaxima)
            flotaL1[k].append(ciudades[i].red[nombreRedes[k]][0].lineas[0].flota)
            infoCargaL1[k].append(ciudades[i].red[nombreRedes[k]][0].lineas[0].infoCarga["Ida"])
            mzL1[k].append(ciudades[i].red[nombreRedes[k]][0].lineas[0].microZonas)

    #Creamos un workbook para contener las salidas a graficar
    wb = xlsxwriter.Workbook("CiudadesN10prueba2"+'.xlsx')
    #Dentro de ese workbook, habra un worksheet para cada grafico o set de graficos.
    wsMain = wb.add_worksheet('Main')
    wsTE   = wb.add_worksheet('TE y TT')
    wsCT   = wb.add_worksheet('CT y CO')
    wsTV   = wb.add_worksheet('TV y TA')
    wsTrans = wb.add_worksheet('Trans')
    wsFKB = wb.add_worksheet('Frec y K')
    wsInfoC = []
    #Creamos tambien los charts que se pegaran en sus respectivas hojas
    #Creamos los charts en el workbook
    chartMain = wb.add_chart({'type': 'line'})
    chartTE = wb.add_chart({'type': 'line'})
    chartCT = wb.add_chart({'type': 'line'})
    chartTV = wb.add_chart({'type': 'line'})
    charttrans1 = wb.add_chart({'type': 'line'})
    charttrans2 = wb.add_chart({'type': 'line'})

#En cada sheet crearemos una tabla con los resultados para cada una de las redes que se compararan

    nombresRedes = ('Abierta', 'Cerrada')
    tipoLineas = ('solid', 'dash_dot')
    nRedes = len(CostoTotal)
    largo = len(CostoTotal[0])
    largok = 0
    for k in range(nRedes):
        #Partimos poniendo el nombre a cada una de las dos columnas
        wsMain.write(0 + k*(largo + 2), 0, "Iteracion")
        wsMain.write(0 + k*(largo + 2), 1, "Costo Total")
        wsMain.write(0 + k*(largo + 2), 2, "Costo Operacion")
        wsMain.write(0 + k*(largo + 2), 3, "Costo Tiempo de Viaje")
        wsMain.write(0 + k*(largo + 2), 4, "Costo Tiempo de Acceso")
        wsMain.write(0 + k*(largo + 2), 5, "Costo Tiempo de Espera")
        wsMain.write(0 + k*(largo + 2), 6, "Costo Tiempo de Transferencia")
        wsMain.write(0 + k*(largo + 2), 7, "lambdap")
        wsMain.write(0 + k*(largo + 2), 8, "lambdac")
        wsMain.write(0 + k*(largo + 2), 9, "lambdaCBD")
        wsTE.write(0 + k*(largo + 2), 0, "Iteracion")
        wsTE.write(0 + k*(largo + 2), 1, "Costo Tiempo de Espera")
        wsTE.write(0 + k*(largo + 2), 2, "Costo Tiempo de Transferencia")
        wsCT.write(0 + k*(largo + 2), 0, "Iteracion")
        wsCT.write(0 + k*(largo + 2), 1, "Costo Total")
        wsCT.write(0 + k*(largo + 2), 2, "Costo de Operacion")
        wsTV.write(0 + k*(largo + 2), 0, "Iteracion")
        wsTV.write(0 + k*(largo + 2), 1, "Costo Tiempo de Viaje")
        wsTV.write(0 + k*(largo + 2), 2, "Costo Tiempo de Acceso")
        wsTrans.write(0 + k*(largo + 2), 0, "Iteracion")
        wsTrans.write(0 + k*(largo + 2), 1, "Demanda que transfiere")
        wsTrans.write(0 + k*(largo + 2), 2, "Cantidad de transferencias")
        wsTrans.write(0 + k*(largo + 2), 3, "Costo Trans sin penalizacion")
        wsTrans.write(0 + k*(largo + 2), 4, "Costo Trans con penalizacion")
        wsFKB.write(0 + k*(largo + 2), 0, "Iteracion")
        wsFKB.write(0 + k*(largo + 2), 1, "Frecuencia Linea 1")
        wsFKB.write(0 + k*(largo + 2), 2, "Capacidad Vehiculo L1")
        wsFKB.write(0 + k*(largo + 2), 3, "Flota L1")
        wsFKB.write(0 + k*(largo + 2), 4, "lambdap")
        wsFKB.write(0 + k*(largo + 2), 5, "lambdac")
        wsFKB.write(0 + k*(largo + 2), 6, "lambdaCBD")
        wsFKB.write(0 + k*(largo + 2), 7, "DemandaTotal")


        #Ahora comenzamos a pegar los resultados en ambas columnas
        for i in range(largo):
            wsMain.write(i + 1 + k*(largo + 2), 0, varIndependiente[1][i])
            wsMain.write(i + 1 + k*(largo + 2), 1, CostoTotal[k][i])
            wsMain.write(i + 1 + k*(largo + 2), 2, CostoOperacion[k][i])
            wsMain.write(i + 1 + k*(largo + 2), 3, TViaje[k][i])
            wsMain.write(i + 1 + k*(largo + 2), 4, TAcceso[k][i])
            wsMain.write(i + 1 + k*(largo + 2), 5, TEspera[k][i])
            wsMain.write(i + 1 + k*(largo + 2), 6, TTransferencia[k][i])
            wsMain.write(i + 1 + k*(largo + 2), 7, LambdaP[k][i])
            wsMain.write(i + 1 + k*(largo + 2), 8, LambdaC[k][i])
            wsMain.write(i + 1 + k*(largo + 2), 9, LambdaCBD[k][i])
            wsTE.write(i + 1 + k*(largo + 2), 0, varIndependiente[1][i])
            wsTE.write(i + 1 + k*(largo + 2), 1, TEspera[k][i])
            wsTE.write(i + 1 + k*(largo + 2), 2, TTransferencia[k][i])
            wsCT.write(i + 1 + k*(largo + 2), 0, varIndependiente[1][i])
            wsCT.write(i + 1 + k*(largo + 2), 1, CostoTotal[k][i])
            wsCT.write(i + 1 + k*(largo + 2), 2, CostoOperacion[k][i])
            wsTV.write(i + 1 + k*(largo + 2), 0, varIndependiente[1][i])
            wsTV.write(i + 1 + k*(largo + 2), 1, TViaje[k][i])
            wsTV.write(i + 1 + k*(largo + 2), 2, TAcceso[k][i])
            wsTrans.write(i + 1 + k*(largo + 2), 0, varIndependiente[1][i])
            wsTrans.write(i + 1 + k*(largo + 2), 1, DTransferencia[k][i])
            wsTrans.write(i + 1 + k*(largo + 2), 2, QTransferencia[k][i])
            wsTrans.write(i + 1 + k*(largo + 2), 3, CTransSinDelta[k][i])
            wsTrans.write(i + 1 + k*(largo + 2), 4, CTransConDelta[k][i])
            wsFKB.write(i + 1 + k*(largo + 2), 0, varIndependiente[1][i])
            wsFKB.write(i + 1 + k*(largo + 2), 1, frecuenciaL1[k][i])
            wsFKB.write(i + 1 + k*(largo + 2), 2, sizeL1[k][i])
            wsFKB.write(i + 1 + k*(largo + 2), 3, flotaL1[k][i])
            wsFKB.write(i + 1 + k*(largo + 2), 4, LambdaP[k][i])
            wsFKB.write(i + 1 + k*(largo + 2), 5, LambdaC[k][i])
            wsFKB.write(i + 1 + k*(largo + 2), 6, LambdaCBD[k][i])
            wsFKB.write(i + 1 + k*(largo + 2), 7, demandaTotal[k][i])
            #Por cada ciudad crearemos una hoja con la info de las lineas. Solo lo creamos para el primer k, luego solo agregamos al existente.
            if k == 0:
                wsInfoC.append(wb.add_worksheet('Info Carga-'+str(i)))
            #Luego la poblamos
            nlineas = len(ciudades[0].red[nombreRedes[k]][0].lineas)#Numero de lineas de la red 0 de esta ciudad
            largoCiclo = 0
            #Primero los encabezados
            for l in range(nlineas):
                wsInfoC[i].write(0 + largoCiclo + k*(largok + 2), 0, "Linea"+str(l))
                wsInfoC[i].write(0 + largoCiclo + k*(largok + 2), 1, "f"+str(l))
                wsInfoC[i].write(1 + largoCiclo + k*(largok + 2), 1, "K"+str(l))
                wsInfoC[i].write(2 + largoCiclo + k*(largok + 2), 1, "B"+str(l))
                wsInfoC[i].write(3 + largoCiclo + k*(largok + 2), 1, "ASK"+str(l))
                wsInfoC[i].write(4 + largoCiclo + k*(largok + 2), 1, "RPK"+str(l))
                wsInfoC[i].write(5 + largoCiclo + k*(largok + 2), 1, "FO"+str(l))
                wsInfoC[i].write(6 + largoCiclo + k*(largok + 2), 1, "MZ-ID")
                wsInfoC[i].write(7 + largoCiclo + k*(largok + 2), 1, "Carga")
                wsInfoC[i].write(8 + largoCiclo + k*(largok + 2), 1, "Subidas")
                wsInfoC[i].write(9 + largoCiclo + k*(largok + 2), 1, "Bajadas")
                wsInfoC[i].write(10 + largoCiclo + k*(largok + 2), 1, "Ocupacion")
                largoCiclo += 11
            #Generamos el largo de filas que se ocupan por tipo de red para las hojas de info de linea
            if k==0:
                largok += largoCiclo

            #Luego los datos
            largoCiclo = 0
            for l in range(nlineas):
                wsInfoC[i].write(0 + largoCiclo + k*(largok + 2), 2, ciudades[i].red[nombreRedes[k]][0].lineas[l].f)
                wsInfoC[i].write(1 + largoCiclo + k*(largok + 2), 2, ciudades[i].red[nombreRedes[k]][0].lineas[l].cargaMaxima)
                wsInfoC[i].write(2 + largoCiclo + k*(largok + 2), 2, ciudades[i].red[nombreRedes[k]][0].lineas[l].flota)
                wsInfoC[i].write(3 + largoCiclo + k*(largok + 2), 2, ciudades[i].red[nombreRedes[k]][0].lineas[l].ASK)
                wsInfoC[i].write(4 + largoCiclo + k*(largok + 2), 2, ciudades[i].red[nombreRedes[k]][0].lineas[l].RPK)
                wsInfoC[i].write(5 + largoCiclo + k*(largok + 2), 2, ciudades[i].red[nombreRedes[k]][0].lineas[l].FOPromedio)
                for j in range(len(ciudades[i].red[nombreRedes[k]][0].lineas[l].microZonas)):
                    id = ciudades[i].red[nombreRedes[k]][0].lineas[l].microZonas[j].ID
                    wsInfoC[i].write(6 + largoCiclo + k*(largok + 2), 2 + j, id)
                    wsInfoC[i].write(7 + largoCiclo + k*(largok + 2), 2 + j, ciudades[i].red[nombreRedes[k]][0].lineas[l].infoCarga['Ida'][0][id])
                    wsInfoC[i].write(8 + largoCiclo + k*(largok + 2), 2 + j, ciudades[i].red[nombreRedes[k]][0].lineas[l].infoCarga['Ida'][1][id])
                    wsInfoC[i].write(9 + largoCiclo + k*(largok + 2), 2 + j, ciudades[i].red[nombreRedes[k]][0].lineas[l].infoCarga['Ida'][2][id])
                    wsInfoC[i].write(10 + largoCiclo + k*(largok + 2), 2 + j, ciudades[i].red[nombreRedes[k]][0].lineas[l].infoCarga['Ida'][3][id])
                largoCiclo += 11
        #Le agregamos los datos a los charts
        #                                [sheetname, first_row, first_col, last_row, last_col]
        chartMain.add_series({
            'categories':'=Main!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=Main!$B$'+str(2+k*(largo+2))+':$B$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'red'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Costo Total '+nombresRedes[k]
        })
        chartMain.add_series({
            'categories':'=Main!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=Main!$C$'+str(2+k*(largo+2))+':$C$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'lime'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Costo Operacion '+nombresRedes[k]
        })
        chartMain.add_series({
            'categories':'=Main!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=Main!$D$'+str(2+k*(largo+2))+':$D$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'green'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Tiempo de Viaje '+nombresRedes[k]
        })
        chartMain.add_series({
            'categories':'=Main!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=Main!$E$'+str(2+k*(largo+2))+':$E$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'purple'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Tiempo de Acceso '+nombresRedes[k]
        })
        chartMain.add_series({
            'categories':'=Main!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=Main!$F$'+str(2+k*(largo+2))+':$F$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'orange'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Tiempo de Espera '+nombresRedes[k]
        })
        chartMain.add_series({
            'categories':'=Main!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=Main!$G$'+str(2+k*(largo+2))+':$G$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'navy'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Tiempo de Transferencia '+nombresRedes[k]
        })
        chartTE.add_series({
            'categories':'=TE y TT!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=TE y TT!$B$'+str(2+k*(largo+2))+':$B$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'orange'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Tiempo de Espera '+nombresRedes[k]
        })
        chartTE.add_series({
            'categories':'=TE y TT!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=TE y TT!$C$'+str(2+k*(largo+2))+':$C$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'navy'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Tiempo de Transferencia '+nombresRedes[k]

        })
        chartCT.add_series({
            'categories':'=CT y CO!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=CT y CO!$B$'+str(2+k*(largo+2))+':$B$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'orange'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Costo Total '+nombresRedes[k]
        })
        chartCT.add_series({
            'categories':'=CT y CO!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=CT y CO!$C$'+str(2+k*(largo+2))+':$C$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'navy'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Costo de Operacion '+nombresRedes[k]
        })
        chartTV.add_series({
            'categories':'=TV y TA!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=TV y TA!$B$'+str(2+k*(largo+2))+':$B$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'orange'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Tiempo de Viaje '+nombresRedes[k]
        })
        chartTV.add_series({
            'categories':'=TV y TA!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=TV y TA!$C$'+str(2+k*(largo+2))+':$C$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'navy'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Tiempo de Acceso '+nombresRedes[k]
        })
        charttrans1.add_series({
            'categories':'=Trans!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=Trans!$B$'+str(2+k*(largo+2))+':$B$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'orange'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Demanda que transfiere '+nombresRedes[k]
        })
        charttrans1.add_series({
            'categories':'=Trans!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=Trans!$C$'+str(2+k*(largo+2))+':$C$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'navy'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Cantidad de Transferencias '+nombresRedes[k]
        })
        charttrans2.add_series({
            'categories':'=Trans!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=Trans!$D$'+str(2+k*(largo+2))+':$D$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'orange'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Costo Transferencias sin penalizacion '+nombresRedes[k]
        })
        charttrans2.add_series({
            'categories':'=Trans!$A$'+str(2+k*(largo+2))+':$A$'+str(1+(k+1)*largo+2*k),
            'values':    '=Trans!$E$'+str(2+k*(largo+2))+':$E$'+str(1+(k+1)*largo+2*k),
            'line':       {'color': 'navy'},
            'line':   {'dash_type': tipoLineas[k]},
            'name':'Costo Transferencias con penalizacion '+nombresRedes[k]
        })


    #Finalmente insertamos el chart en la sheet donde queremos
    wsMain.insert_chart('I5', chartMain)
    wsTE.insert_chart('F5', chartTE)
    wsCT.insert_chart('F5', chartCT)
    wsTV.insert_chart('F5', chartTV)
    wsTrans.insert_chart('H5', charttrans1)
    wsTrans.insert_chart('H12', charttrans2)

    wb.close()
