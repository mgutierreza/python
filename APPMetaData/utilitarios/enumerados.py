from enum import Enum, unique

@unique
class tipoObjeto(Enum):
    BaseDatos = 1
    Aplicacion = 2

@unique
class claseObjeto(Enum):
    entity = 1
    exception = 2
    filter = 3
    filterType = 4
    request = 5
    response = 6
    requestValidation = 7
    service = 8
    repository = 9
    iRepository = 10
    domain = 11
    controller = 12
    select = 13
    insert = 14
    update = 15
    delete = 16

@unique
class tipoConsulta(Enum):
    TodosCampos = 1
    CamposSinPK = 2
    SoloPKFK = 3
    SoloPK = 4