#enconding: utf-8
__author__ = 'Ariel Anthieni'

#Cargo librerias
from PIL import Image
from osgeo import gdal, osr


"""
Libreria de funciones para obtener datos de las imagenes raster
 a partir de GDAL
"""

def GetExtent(gt,cols,rows):
    """ Retorna la lista de corner para geotransform

        @type gt:   C{tuple/list}
        @param gt: geotransform
        @type cols:   C{int}
        @param cols: nro de columnas del dataset
        @type rows:   C{int}
        @param rows: nro de filas del dataset
        @rtype:    C{[float,...,float]}
        @return:   coordenadas de los esquinas
    """

    ext=[]
    xarr=[0,cols]
    yarr=[0,rows]

    for px in xarr:
        for py in yarr:
            x=gt[0]+(px*gt[1])+(py*gt[2])
            y=gt[3]+(px*gt[4])+(py*gt[5])
            ext.append([x,y])

        yarr.reverse()
    return ext

def ReprojectCoords(coords,src_srs,tgt_srs):
    """ Reprojecta una lista de cordenadas x,y

        @type geom:     C{tuple/list}
        @param geom:    Lista de  [[x,y],...[x,y]] coordenadas
        @type src_srs:  C{osr.SpatialReference}
        @param src_srs: OSR SpatialReference object
        @type tgt_srs:  C{osr.SpatialReference}
        @param tgt_srs: OSR SpatialReference object
        @rtype:         C{tuple/list}
        @return:        Lista trasnformada [[x,y],...[x,y]] de coordenadas
    """
    trans_coords=[]
    transform = osr.CoordinateTransformation( src_srs, tgt_srs)
    for x,y in coords:
        x,y,z = transform.TransformPoint(x,y)
        trans_coords.append([x,y])
    return trans_coords

####DEVUELVE LOS DATOS DEL RASTER QUE SE PASA POR PARAMETRO###############

def dataraster(archivo):

    """
    Analiza el archivo pasado por referencia para obtener los metadatos del mismo

    :param archivo: ruta del archivo a analizar
    :return: arreglo con metadatos
    """


    #Generamos un diccionario para devolver los datos del Raster

    resultado = {}

    #Abrimos el archivo
    datafile = gdal.Open(archivo)

    #Datos de grid
    cols = datafile.RasterXSize
    rows = datafile.RasterYSize
    bands = datafile.RasterCount

    resultado["cols"] = str(cols)
    resultado["rows"] = str(rows)
    resultado["bands"] = str(bands)

    #Obtener informacion Geografica

    geoinformation = datafile.GetGeoTransform()

    #Accedemos primero a la proyeccion en formato WKT

    projInfo = datafile.GetProjection()

    #Creamos el objeto espacial

    spatialRef = osr.SpatialReference()

    #Importamos el WKT al objeto espacial

    spatialRef.ImportFromWkt(projInfo)

    #Usamos ExportToProj4() metodo para devolver el estilo en string del objeto espacial

    spatialRefProj = spatialRef.ExportToProj4()

    srs = spatialRefProj
    resultado["srs"] = str(srs)

    #Generacion del extent

    ext = GetExtent(geoinformation,cols,rows)

    #generamos un objeto espacial

    tgt_srs = spatialRef.CloneGeogCS()


    geo_ext = ReprojectCoords(ext,spatialRef,tgt_srs)


    #valores de la imagen

    resultado["UL"] = str(geo_ext[0])
    resultado["UR"] = str(geo_ext[3])
    resultado["LR"] = str(geo_ext[2])
    resultado["LL"] = str(geo_ext[1])

    #valores del extent

    resultado["CORNER_UL_LON_PRODUCT"] = str(geo_ext[0][0])
    resultado["CORNER_UR_LON_PRODUCT"] = str(geo_ext[3][0])
    resultado["CORNER_LR_LAT_PRODUCT"] = str(geo_ext[2][1])
    resultado["CORNER_UL_LAT_PRODUCT"] = str(geo_ext[0][1])

    return resultado


def generate_ql(source, destination, base_ancho = 180):

    """
    Funcion que dimensiona un QL a partir de un jpg
    :param source: ruta completa de donde se aloja el archivo jpg
    :param destination: ruta completa de donde dejar el ql generado
    :param base_ancho: ancho del ql generado en pixeles
    :return: restona 0 si se realizo correctamente, 1 en caso contrario
    """

    try:
        #Reduzco la imagen para la miniatura

        #Abrimos el archivo
        img = Image.open(source)

        #Calculamos el ancho conservando el aspecto
        anchoPercent = (base_ancho / float(img.size[0]))
        alto = int((float(img.size[1]) * float(anchoPercent)))

        #Reduccion
        img = img.resize((base_ancho,alto), Image.BILINEAR)

        #guardamos imagen
        img.save(destination)

        print("Se genero la miniatura del archivo: " + source + "\n")

        return 0

    except:

        print("ERROR [006]: No se ha podido generar el QL del archivo: " + source + "\n")
        return 1
