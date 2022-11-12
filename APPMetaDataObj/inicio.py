from inicioObjetos import generarObjetos

def generarObjetos():
    nombreTabla = "AcdCampus"
    clase = generarObjetos(nombreTabla)
    clase.generarObjetosBankEnd()
    return 