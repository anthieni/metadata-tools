__author__ = 'Ariel Anthieni'

#Definicion de Librerias
import os
import json
import csv
import codecs


#Establecimiento de variables
dir_origen = '/opt/desarrollo/metadata-tools/convert-tools/data/in/'
dir_destino = '/opt/desarrollo/metadata-tools/convert-tools/data/out/'
geocampo = 'geojson'


#Listo los archivos en el directorio
ficheros = os.listdir(dir_origen)


"""
El script analiza el contenido del encabezado del csv y genera el array luego produciendo un geojson
"""

for archivo in ficheros:

    ext = os.path.splitext(archivo)

    #verifico si es un producto
    if (( ext[1] == '.csv')):

        #abro el csv
        filecsv = open(dir_origen+archivo)
        objcsv = csv.reader(filecsv)

        #Paso a un array la estructura
        arreglo = []
        geoarreglo = []
        propiedades = {}
        multigeo = []

        for elemento in objcsv:
            arreglo.append(elemento)

        filecsv.close()

        encabezado = arreglo[0]

        idgeo = encabezado.index(geocampo)

        i = 0
        for elemento in arreglo:
            #Recorro el encabezado

            if i == 0 :
                i=i+1
            else:
                j = 0
                propiedades = {}
                for col in encabezado:

                    if (j != idgeo):
                        propiedades[col] = elemento[j]
                    else:
                        multigeo = json.loads(elemento[j])

                    j=j+1

                #Almaceno las propiedades
                multigeo['properties'] = propiedades
                geoarreglo.append(multigeo)


        georesultado = { "type": "FeatureCollection", "features": [] }

        for value in geoarreglo:
            georesultado['features'].append(value)

        resultado = codecs.open(dir_destino+ext[0]+'.geojson', 'w','utf-8')
        resultado.write(json.dumps(georesultado))
        resultado.close()


