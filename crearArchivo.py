import os
from os import remove

def generarArchivo(nombreTabla, nombreArchivo, contenidoArchivo):

    rutaNuevoArchivo = 'd:\\Clases\\' + nombreTabla + '\\APP\\' + nombreArchivo + ".cs"

    if (os.path.isdir(rutaNuevoArchivo)):
        remove(rutaNuevoArchivo)

    f = open (rutaNuevoArchivo,'w')
    f.write(contenidoArchivo)
    f.close()

    return

