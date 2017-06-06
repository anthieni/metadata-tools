__author__ = 'Ariel Anthieni'

#Definicion de Librerias
import os
import json
import csv
import codecs


#Establecimiento de variables
dir_origen = '/opt/desarrollo/metadata-tools/convert-tools/data/in/'
dir_destino = '/opt/desarrollo/metadata-tools/convert-tools/data/out/'
geocampo = 'WKT'
tabla = 'calles_indec'

#Listo los archivos en el directorio
ficheros = os.listdir(dir_origen)


"""
El script analiza el contenido del encabezado del csv y genera el array luego produciendo el codigo sql
para crear la tabla e insertar los registros
"""

for archivo in ficheros:

    ext = os.path.splitext(archivo)

    #verifico si es un producto
    if (( ext[0] == '20161212calles_gba')):

        #abro el csv
        filecsv = open(dir_origen+archivo)
        objcsv = csv.reader(filecsv)

        #Paso a un array la estructura
        arreglo = []
        geoarreglo = []
        elementos_sql = {}
        multigeo = {}
        multiwkt = ''

        for elemento in objcsv:
            arreglo.append(elemento)

        filecsv.close()

        encabezado = arreglo[0]
        encabezado_col = ''


        #Genero el archivo de destino
        resultado = codecs.open(dir_destino+ext[0]+'.sql', 'w','utf-8')

        #jsongeo = json.dumps(georesultado, ensure_ascii=False).encode('utf8')

        #resultado.write(jsongeo.decode('utf-8'))



        #creamos la tabla necesario para la importacion
        createsql = 'CREATE TABLE '+tabla+' ('

        for col in encabezado:
            if col == geocampo:
                createsql = createsql + col + ' ' + 'geometry , '

            else:
                createsql = createsql + col + ' ' + 'character varying(255) , '

            encabezado_col = encabezado_col + col + ', '

        createsql = createsql[:-2]
        encabezado_col = encabezado_col[:-2]

        createsql = createsql + ');\n'

        #Escribo en el archivo
        resultado.write(createsql)


        idgeo = encabezado.index(geocampo)

        i = 0
        for elemento in arreglo:
            #Recorro el encabezado

            if i == 0 :
                i=i+1
            else:
                j = 0
                elementos_sql = []
                for col in encabezado:
                    elementos_sql.append(elemento[j])
                    j=j+1


                #Genero el registro de insercion
                insertsql = 'INSERT INTO '+tabla + ' (' + encabezado_col + ') VALUES ('

                for columna in elementos_sql:

                    insertsql = insertsql +"$$" + columna + "$$" + ', '


                insertsql = insertsql[:-2]

                insertsql = insertsql + ');\n'

                #Escribo en el archivo
                resultado.write(insertsql)


        resultado.close()


