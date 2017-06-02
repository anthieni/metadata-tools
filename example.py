__author__ = 'Ariel Anthieni'

#Definicion de Librerias
import os
import datetime
import time
import sys
import shutil
import zipfile
import zlib

#Incorporo las librerias de uso
from extractor import dataraster , generate_ql


#Establecimiento de variables
dir_origen = '/media/sf_prod24/nuevos/l8/'
dir_dest_xml = '/media/sf_prod24/nuevos/l8/product/'
dir_quicklook = '/media/sf_prod24/nuevos/l8/product/'
dir_back = '/media/sf_prod24/nuevos/l8/back/'
dir_metadatasrc = '/media/sf_prod24/nuevos/l8/'
dir_producto =  '/media/sf_prod24/nuevos/l8/product/'
base_ancho = 180
error_product = 0
error_count = 0


#Listo los archivos en el directorio
ficheros = os.listdir(dir_origen)


"""
El script se modificara para que tenga coherencia operativa, siendo que si existe el jpg se procesa
los siguientes datos que conforman el xml, en caso contrario se envia a un directorio de back

"""

for archivo in ficheros:

    ext = os.path.splitext(archivo)

    #verifico si es un producto
    if (( ext[1] == '.tif')or  ( ext[1] == '.img')):

        #seteo la variable de error a cero
        error_product = 0

        #recorto el nombre del producto a su nombre definitivo
        # nombre_producto = ext[0].split('_')
        # largo = len(nombre_producto)
        # nombre_subproducto = ''
        # for ele in nombre_producto[0:(largo-4)]:
        #     if (not nombre_subproducto == ''):
        #         nombre_subproducto = nombre_subproducto + '_' + ele
        #     else:
        #         nombre_subproducto = ele

        nombre_subproducto = ext[0]

        nombre_ql = nombre_subproducto + '.jpg'
        nombre_ql_origen = ext[0] + '.jpg'
        nombre_meta_txt = nombre_subproducto + '.txt'
        nombre_meta_xml = nombre_subproducto + '.xml'
        nombre_producto_f = nombre_subproducto + '.zip'

        #Adecuo el QL

        generate_ql(dir_origen + nombre_ql_origen, dir_quicklook + nombre_ql)

        #Genero los Metadatos

        #Verifico si no hay un error anterior
        if (error_product == 0):

            #genero los metadatos del producto

            try:
                #realiza la conversion del txt al xml
                #elemento = txttoxml()
                #elemento.toxml(dir_origen + nombre_meta_txt, dir_dest_xml + nombre_meta_xml, ':')

                #logSalida.write("Se convirtio el txt a xml el archivo: " + archivo + "\n")

                #Obtengo los metadatos de ciudades
                #metadatos_ciudades = getMetadata(ext[0])

                print("Se genero el metadato del archivo: " + archivo + "\n")

                #obtengo los datos raster de la imagen
                datos_imagen = dataraster(dir_origen + archivo)

                #incluimos los datos raster
                #elemento.metadataxml(dir_dest_xml + nombre_meta_xml, metadatos_ciudades, datos_imagen)

                #Muevo el archivo de metadatos
                #shutil.move(dir_origen + nombre_meta_txt, dir_metadatasrc + nombre_meta_txt)

                print("Se generaron los metadatos al archivo: " + archivo + "\n")
            except:
                print("ERROR [007]: No se ha podido generar los metadatos del archivo: " + archivo + "\n")
                error_product = 1
                continue


            #Genero los archivos para el producto terminado
            # try:
            #
            #     #Creamos el zip con todos los archivos extraidos
            #     os.chdir(dir_producto)  #cambiar al directorio donde quiero crear la carpeta zip
            #     #configuramos el metodo de compresion
            #     compresion = zipfile.ZIP_DEFLATED
            #
            #     zfilename = nombre_producto_f
            #     zf = zipfile.ZipFile(zfilename, "w")
            #     zf.write(os.path.join(dir_origen, archivo),arcname=archivo, compress_type=compresion)
            #     zf.close()
            #     #borro el archivo de origen
            #     #os.remove(os.path.join(dir_origen, archivo))
            #
            #     print("Se genero el producto del archivo: " + zfilename + " correctamente \n")
            #
            # except:
            #     print("ERROR [009]: No se ha podido manipular el archivo: " + archivo + "\n")


        else:
            #Muevo el tif a su lugar de back
            try:

                shutil.move(dir_origen + archivo, dir_back + archivo)
                print("ERROR [008]: No se ha podido generar el producto para el archivo: " + archivo + "\n")
                error_count = error_count +1

            except:
                print("ERROR [009]: No se ha podido manipular el archivo: " + archivo + "\n")
                continue


