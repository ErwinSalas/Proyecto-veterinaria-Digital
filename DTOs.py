__author__ = 'Erwin'

class usuario:
    def __init__(self, nombre, user, pasw, permiso, foto):
        self.nombre = nombre
        self.login = user
        self.pasw = pasw
        self.permiso = permiso
        self.foto=foto
        self.database=True

class medicamento:
    def __init__(self, nombre , descripcion, foto):
        self.nombre = nombre
        self.descripcion = descripcion
        self.foto = foto
        self.database=True
    def tipo(self):
            return 'medicamentos'
class animal:
    def __init__(self, nombre, descripcion, foto):
        self.nombre=nombre
        self.descripcion=descripcion
        self.foto=foto
        self.database=True
    def tipo(self):
        return 'animal'

class enfermedad:
     def __init__(self,nombre,descripcion,foto):
        self.nombre=nombre
        self.descripcion=descripcion
        self.foto=foto
        self.database=True

     def tipo(self):
        return 'enfermedad'
class Dosis:
    def __init__(self,id,animal,medicamento,enfermedad,max,min,dosis):
        self.id=id
        self.animal=animal
        self.enfermedad=enfermedad
        self.medicamento=medicamento
        self.pesoMax=max
        self.pesoMin=min
        self.dosis=dosis
        self.database=True
class prescripcion:
    def __init__(self,id,animal,usuario,enfermedad,rangoPeso,dosis):
        self.id=id
        self.animal=animal
        self.usuario=usuario
        self.enfermedad=enfermedad
        self.peso=rangoPeso
        self.dosis=dosis
        self.database=True
