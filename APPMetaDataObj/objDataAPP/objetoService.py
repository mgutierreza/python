from objDataAPP.iObjetoAplicacion import iObjetoAplicacion
from util.utilitario import gestionArchivos
from objConexionBD.consultasBD import obtenerData

class objetoRepository(iObjetoAplicacion):

    def __init__(self, nombreTabla, claseObjeto):
        self.__nombreTabla = nombreTabla
        self.__claseObjeto = claseObjeto
        self.__nombreClase = ''
        self.TAB = '\t'
        self.ENTER = '\n'

    def generarArchivo(self):
        nuevoArchivo = gestionArchivos(self.__nombreTabla, self.__claseObjeto)
        self.__nombreClase = nuevoArchivo.generarNombreArchivo()
        contenidoClase = self.__generarClase()
        nuevoArchivo.generarArchivo(contenidoClase)
        return

    def __generarClase(self):
        clase = ""
        clase += self.__generarCabeceraClase()
        clase += "namespace EP_AcademicMicroservice.Service" + self.ENTER 
        clase += "{"  + self.ENTER    
        clase += self.__generarCuerpoClase()
        clase += "}"
        
        return clase
    
    def __generarCabeceraClase(self):
        cabeceraClase = ""
        cabeceraClase += "using EP_AcademicMicroservice.Domain;" + self.ENTER 
        cabeceraClase += "using EP_AcademicMicroservice.Entities;" + self.ENTER 
        cabeceraClase += "using EP_AcademicMicroservice.Exceptions;" + self.ENTER
        cabeceraClase += "using System;" + self.ENTER 
        cabeceraClase += "using System.Collections.Generic;" + self.ENTER
        cabeceraClase += "using System.Linq;" + self.ENTER
        cabeceraClase += "using System.Text;" + self.ENTER
        cabeceraClase += "using System.Threading.Tasks;" + 2*self.ENTER

        return cabeceraClase
    
    def __generarCuerpoClase(self):
        cuerpoClase = ""
        cuerpoClase = cuerpoClase + self.TAB + "public class " + self.__nombreClase + self.ENTER
        cuerpoClase = cuerpoClase + self.TAB + "{" + self.ENTER 
        cuerpoClase = cuerpoClase + 2*self.TAB + "#region Public Methods" + self.ENTER 
        cuerpoClase = cuerpoClase + self.__generarMetodoExecute() + 2*self.ENTER 
        cuerpoClase = cuerpoClase + self.__generarMetodoGet() + 2*self.ENTER 
        cuerpoClase = cuerpoClase + self.__generarMetodoLstItemResponse() + self.ENTER 
        cuerpoClase = cuerpoClase + 2*self.TAB + "#endregion" + 2*self.ENTER 
        cuerpoClase = cuerpoClase + self.TAB + "}" + self.ENTER
        
        return cuerpoClase
    
    def __generarMetodoExecute(self):
        metodoExecute = ""
        campoClavePrincipal = ""

        data = obtenerData(self.__nombreTabla)
        dictData = data.metaDataClavePrincipal()
        for valor in dictData:
            campoClavePrincipal = valor["nombreCampo"]

        metodoExecute += 2*self.TAB + "public " + self.__nombreTabla + "Response Execute(" + self.__nombreTabla + "Request request)" + self.ENTER
        metodoExecute += 2*self.TAB + "{" + self.ENTER 
        metodoExecute += 3*self.TAB + self.__nombreTabla + "Response response = new " + self.__nombreTabla + "Response();" + self.ENTER 
        metodoExecute += 3*self.TAB + "response.InitializeResponse(request);" + self.ENTER 
        metodoExecute += 3*self.TAB + "try" + self.ENTER 
        metodoExecute += 3*self.TAB + "{" + self.ENTER 
        metodoExecute += 4*self.TAB + "if (response.LstError.Count == 0)" + self.ENTER 
        metodoExecute += 4*self.TAB + "{" + self.ENTER 
        metodoExecute += 5*self.TAB + "switch (request.Operation)" + self.ENTER 
        metodoExecute += 5*self.TAB + "{" + self.ENTER 
        metodoExecute += 6*self.TAB + "case Operation.Undefined:" + self.ENTER 
        metodoExecute += 7*self.TAB + "break;" + self.ENTER 
        metodoExecute += 6*self.TAB + "case Operation.Add:" + self.ENTER 
        metodoExecute += 7*self.TAB + "response.Resultado = new " + self.__nombreTabla + "Domain().Create" + self.__nombreTabla + "(request.Item);" + self.ENTER 
        metodoExecute += 7*self.TAB + "break;" + self.ENTER 
        metodoExecute += 6*self.TAB + "case Operation.Edit:" + self.ENTER 
        metodoExecute += 7*self.TAB + "response.Item = new " + self.__nombreTabla + "Domain().Edit" + self.__nombreTabla + "(request.Item);" + self.ENTER 
        metodoExecute += 7*self.TAB + "break;" + self.ENTER 
        metodoExecute += 6*self.TAB + "case Operation.Delete:" + self.ENTER 
        metodoExecute += 7*self.TAB + "response.Item = new " + self.__nombreTabla + "Domain().Delete" + self.__nombreTabla + "(request.Item." + campoClavePrincipal + ");" + self.ENTER 
        metodoExecute += 7*self.TAB + "break;" + self.ENTER 
        metodoExecute += 6*self.TAB + "default:" + self.ENTER 
        metodoExecute += 7*self.TAB + "break;" + self.ENTER 
        metodoExecute += 5*self.TAB + "}" + self.ENTER 
        metodoExecute += 5*self.TAB + "response.IsSuccess = true;" + self.ENTER 
        metodoExecute += 4*self.TAB + "}" + self.ENTER 
        metodoExecute += 3*self.TAB + "}" + self.ENTER
        metodoExecute += 3*self.TAB + "catch (CustomException ex)" + self.ENTER
        metodoExecute += 3*self.TAB + "{" + self.ENTER
        metodoExecute += 4*self.TAB + "response.LstError.Add(ex.CustomMessage);" + self.ENTER
        metodoExecute += 3*self.TAB + "}" + self.ENTER
        metodoExecute += 3*self.TAB + "catch (Exception ex)" + self.ENTER
        metodoExecute += 3*self.TAB + "{" + self.ENTER
        metodoExecute += 4*self.TAB + "response.LstError.Add(\"Server Error\");" + self.ENTER
        metodoExecute += 3*self.TAB + "}" + self.ENTER
        metodoExecute += 3*self.TAB + "return response;" + self.ENTER 
        metodoExecute += 2*self.TAB + "}" + self.ENTER 

        return metodoExecute
    
    def __generarMetodoGet(self):
        metodoGet = ""
        campoClavePrincipal = ""

        data = obtenerData(self.__nombreTabla)
        dictData = data.metaDataClavePrincipal()
        for valor in dictData:
            campoClavePrincipal = valor["nombreCampo"]

        metodoGet += 2*self.TAB + "public " + self.__nombreTabla + "ItemResponse Get" + self.__nombreTabla + "(" + self.__nombreTabla + "ItemRequest request)" + self.ENTER
        metodoGet += 2*self.TAB + "{" + self.ENTER 
        metodoGet += 3*self.TAB + self.__nombreTabla + "ItemResponse response = new " + self.__nombreTabla + "ItemResponse();" + self.ENTER 
        metodoGet += 3*self.TAB + "response.InitializeResponse(request);" + self.ENTER 
        metodoGet += 3*self.TAB + "try" + self.ENTER 
        metodoGet += 3*self.TAB + "}" + self.ENTER 
        metodoGet += 4*self.TAB + "if (response.LstError.Count == 0)" + self.ENTER 
        metodoGet += 4*self.TAB + "{" + self.ENTER 
        metodoGet += 5*self.TAB + "switch (request.FilterType)" + self.ENTER
        metodoGet += 5*self.TAB + "{" + self.ENTER     
        metodoGet += 6*self.TAB + "case " + self.__nombreTabla + "FilterItemType.ById:" + self.ENTER     
        metodoGet += 7*self.TAB + "response.Item = new " + self.__nombreTabla + "Domain().GetById(request.Filter." + campoClavePrincipal + ");" + self.ENTER
        metodoGet += 7*self.TAB + "break;" + self.ENTER 
        metodoGet += 6*self.TAB + "default:" + self.ENTER 
        metodoGet += 7*self.TAB + "break;" + self.ENTER 
        metodoGet += 5*self.TAB + "}" + self.ENTER 
        metodoGet += 5*self.TAB + "response.IsSuccess = true;" + self.ENTER 
        metodoGet += 4*self.TAB + "}" + self.ENTER 
        metodoGet += 3*self.TAB + "}" + self.ENTER 
        metodoGet += 3*self.TAB + "catch (CustomException ex)" + self.ENTER
        metodoGet += 3*self.TAB + "{" + self.ENTER
        metodoGet += 4*self.TAB + "response.LstError.Add(ex.CustomMessage);" + self.ENTER
        metodoGet += 3*self.TAB + "}" + self.ENTER
        metodoGet += 3*self.TAB + "catch (Exception ex)" + self.ENTER
        metodoGet += 3*self.TAB + "{" + self.ENTER
        metodoGet += 4*self.TAB + "response.LstError.Add(\"Server Error\");" + self.ENTER
        metodoGet += 3*self.TAB + "}" + self.ENTER
        metodoGet += 3*self.TAB + "return response;" + self.ENTER 
        metodoGet += 2*self.TAB + "}" + self.ENTER 

        return metodoGet

    def __generarMetodoLstItemResponse(self):
        metodoLstItemResponse = ""

        metodoLstItemResponse += 2*self.TAB + "public " + self.__nombreTabla + "LstItemResponse GetLst" + self.__nombreTabla + "(" + self.__nombreTabla + "LstItemRequest request)" + self.ENTER
        metodoLstItemResponse += 2*self.TAB + "{" + self.ENTER 
        metodoLstItemResponse += 3*self.TAB + self.__nombreTabla + "LstItemResponse response = new " + self.__nombreTabla + "LstItemResponse();" + self.ENTER 
        metodoLstItemResponse += 3*self.TAB + "response.InitializeResponse(request);" + self.ENTER 
        metodoLstItemResponse += 3*self.TAB + "try" + self.ENTER 
        metodoLstItemResponse += 3*self.TAB + "{" + self.ENTER 
        metodoLstItemResponse += 4*self.TAB + "if (response.LstError.Count == 0)" + self.ENTER 
        metodoLstItemResponse += 4*self.TAB + "{" + self.ENTER 
        metodoLstItemResponse += 5*self.TAB + "switch (request.FilterType)" + self.ENTER
        metodoLstItemResponse += 5*self.TAB + "{" + self.ENTER     
        metodoLstItemResponse += 6*self.TAB + "case " + self.__nombreTabla + "FilterLstItemType.ByPagination:" + self.ENTER     
        metodoLstItemResponse += 7*self.TAB + "response.Item = new " + self.__nombreTabla + "Domain().GetByPagination(request.Filter, request.FilterType, request.Pagination);" + self.ENTER
        metodoLstItemResponse += 7*self.TAB + "break;" + self.ENTER 
        metodoLstItemResponse += 6*self.TAB + "default:" + self.ENTER 
        metodoLstItemResponse += 7*self.TAB + "break;" + self.ENTER 
        metodoLstItemResponse += 5*self.TAB + "}" + self.ENTER 
        metodoLstItemResponse += 5*self.TAB + "response.IsSuccess = true;" + self.ENTER 
        metodoLstItemResponse += 4*self.TAB + "}" + self.ENTER 
        metodoLstItemResponse += 3*self.TAB + "}" + self.ENTER 
        metodoLstItemResponse += 3*self.TAB + "catch (CustomException ex)" + self.ENTER
        metodoLstItemResponse += 3*self.TAB + "{" + self.ENTER
        metodoLstItemResponse += 4*self.TAB + "response.LstError.Add(ex.CustomMessage);" + self.ENTER
        metodoLstItemResponse += 3*self.TAB + "}" + self.ENTER
        metodoLstItemResponse += 3*self.TAB + "catch (Exception ex)" + self.ENTER
        metodoLstItemResponse += 3*self.TAB + "{" + self.ENTER
        metodoLstItemResponse += 4*self.TAB + "response.LstError.Add(ex.Message);" + self.ENTER
        metodoLstItemResponse += 3*self.TAB + "}" + self.ENTER
        metodoLstItemResponse += 3*self.TAB + "return response;" + self.ENTER 
        metodoLstItemResponse += 2*self.TAB + "}" + self.ENTER 

        return metodoLstItemResponse
