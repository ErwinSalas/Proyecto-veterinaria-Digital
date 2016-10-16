__author__ = 'Erwin'
import mysql.connector
from DTOs import *
usuarios=[]
animales=[]
medicamentos=[]
enfermedades=[]
dosisList=[]
prescripciones=[]

class coneccion:
    def __init__(self):
        self.user='root'
        self.password=''
        self.host='127.0.0.1'
        self.database='veterinaria'
        self.conn=None
        self.cur=None
        self.registros=None

    def ejecutar(self,query,method):
        self.conn = mysql.connector.connect(user=self.user,
            password = self.password,
            host = self.host,
            database = self.database)
        self.cur = self.conn.cursor()
        self.cur.execute(query)
        if method == "GET":
            self.registros = self.cur.fetchall()
            self.conn.close()
            return self.registros
        self.conn.commit()
        self.conn.close()

class UsuarioController:

    def index(self):
        connt = coneccion()
        connt.ejecutar("select * from usuarios", "GET")

        usuariosBD = [usuario(row[0], row[1], row[2], row[3], row[4].decode('utf8')) for row in connt.registros]
        return usuariosBD

    def update(self, user):
        global usuarios
        filtro= list(filter(lambda x: x.login == user.login, usuarios))
        filtro2=list(filter(lambda x: x.login == user.login, self.index()))
        if len(filtro) != 0:
           temp = list(filter(lambda x: x.login != user.login, usuarios))
           usuarios=temp
           user.database=False
           usuarios.append(user)
        elif len(filtro2) != 0:
            query=("update usuarios set contraseña = '{}',nombre = '{}',permiso = '{}',foto ='{}'  Where login = '{}'".format(user.pasw,user.nombre,user.permiso,user.foto,user.login))
            connt = coneccion()
            connt.ejecutar(query,"POST")

    def create(self, user):
        if len(usuarios) == 0 and len(self.index()) == 0:
            user.database=False
            usuarios.append(user)
            return
        filtro = list(filter(lambda x: x.login == user.login, usuarios))
        filtro2 = list(filter(lambda x: x.login == user.login, self.index()))
        if len(filtro) != 0 or len(filtro2) != 0:
           return "Error del llave foranea"
        user.database=False
        usuarios.append(user)


    def delete(self, id):
        global usuarios
        filtro= list(filter(lambda x: x.login == id, usuarios))
        filtro2=list(filter(lambda x: x.login == id, self.index()))
        if len(filtro) != 0:
            temp =list(filter(lambda x: x.login != id, usuarios))
            usuarios.clear()
            usuarios=temp
            usuarios = [e for e in temp]
            return
        elif len(filtro2) != 0:
            conn = coneccion()
            conn.ejecutar( """
            DELETE FROM usuarios WHERE usuarios.login = '{}';
            """.format(id), "POST")
            return

    def guardarLista(self):
        generador = (e for e in usuarios )
        while True:
            try:
                user = generador.__next__()
                conn = coneccion()
                conn.ejecutar( """
                INSERT INTO usuarios (nombre,login,contraseña, permiso,foto) VALUES ('{}','{}','{}','{}','{}');
                """.format(user.nombre,user.login,user.pasw,user.permiso,user.foto), "POST")

            except StopIteration:
                usuarios.clear()
                break

    def borrarLista(self):
        usuarios.clear()
        return

    def registrosLogin(self):
        connt = coneccion()
        connt.ejecutar("select login,contraseña,permiso from usuarios ;", "GET")
        users = [usuario(0, row[0], row[1], row[2], 0) for row in connt.registros]
        return users



class AMEController:

    def index(self,tabla):
        connt = coneccion()
        if tabla=='animal':
            connt.ejecutar("select * from animal", "GET")
            AnimalesBD = [animal(row[0], row[1], row[2].decode('utf8')) for row in connt.registros]
            return AnimalesBD
        elif tabla=='medicamentos':
            connt.ejecutar("select * from medicamentos", "GET")
            medicamentosBD = [medicamento(row[0], row[1], row[2].decode('utf8')) for row in connt.registros]
            return medicamentosBD
        elif tabla=='enfermedad':
            connt.ejecutar("select * from enfermedad", "GET")
            enfermedadBD = [enfermedad(row[0], row[1], row[2].decode('utf8')) for row in connt.registros]
            return enfermedadBD


    def update(self, obj,lista):

        filtro= list(filter(lambda x: x.nombre == obj.nombre, lista))
        filtro2=list(filter(lambda x: x.nombre == obj.nombre, self.index(obj.tipo())))
        if len(filtro) != 0:
           temp = list(filter(lambda x: x.nombre != obj.nombre, lista))
           lista=temp
           obj.database=False
           lista.append(obj)
           return lista
        elif len(filtro2) != 0:
            query=("update {} set descripcion = '{}',foto = '{}'  Where nombre = '{}'".format(obj.tipo(),obj.descripcion,obj.foto,obj.nombre))
            connt = coneccion()
            connt.ejecutar(query,"POST")
            return lista

    def create(self, obj,lista):
        if len(lista) == 0 and len(self.index(obj.tipo())) == 0:
            lista.append(obj)
            obj.database=False
            return lista
        filtro = list(filter(lambda x: x.nombre == obj.nombre, lista))
        filtro2 = list(filter(lambda x: x.nombre == obj.nombre, self.index(obj.tipo())))
        if len(filtro) != 0 or len(filtro2) != 0:
           return "Error del llave foranea"
        obj.database=False
        lista.append(obj)
        return lista



    def delete(self, id,tipo,lista):
        filtro =  list(filter(lambda x: x.nombre == id, lista))
        filtro2 = list(filter(lambda x: x.nombre == id, self.index(tipo)))
        if len(filtro) != 0:
            temp =list(filter(lambda x: x.nombre != id, lista))
            lista.clear()
            lista=temp
            return lista
        elif len(filtro2) != 0:
            conn = coneccion()
            conn.ejecutar( """
            DELETE FROM {} WHERE {}.nombre = '{}';
            """.format(tipo,tipo,id), "POST")
            return lista

    def guardarLista(self,lista):
        generador = (e for e in lista)
        while True:
            try:
                obj = generador.__next__()
                conn = coneccion()
                conn.ejecutar( """
                INSERT INTO {} (nombre,descripcion,foto) VALUES ('{}','{}','{}');
                """.format(obj.tipo(),obj.nombre,obj.descripcion,obj.foto), "POST")

            except StopIteration:
                return []

    def borrarLista(self):
        return []

class DosisController:

    def index(self):
        connt = coneccion()
        connt.ejecutar("select * from dosis ;", "GET")
        dosisBD = [Dosis(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in connt.registros]
        return dosisBD

    def update(self, dosis):
        global dosisList
        filtro= list(filter(lambda x: x.id == dosis.id, dosisList))
        filtro2=list(filter(lambda x: x.id == dosis.id, self.index()))
        if len(filtro) != 0:
           temp = list(filter(lambda x: x.id != dosis.id, dosisList))
           dosisList=temp
           dosis.database=False
           dosisList.append(dosis)
        elif len(filtro2) != 0:
            query = """update dosis set animal = '{}',enfermedad = '{}',
            medicamento ='{}',pesoMax ={},pesoMin ={}, dosis={}   Where id = {}""".format(dosis.animal,dosis.enfermedad,dosis.medicamento,dosis.pesoMax,dosis.pesoMin,dosis.id)
            connt = coneccion()
            connt.ejecutar(query,"POST")

    def create(self, dosis):
        if len(dosisList) == 0 and len(self.index()) == 0:
            dosis.database=False
            dosisList.append(dosis)
            return
        filtro = list(filter(lambda x: x.id == dosis.id, dosisList))
        filtro2 = list(filter(lambda x: x.id == dosis.id, self.index()))
        if len(filtro) != 0 or len(filtro2) != 0:
           return "Error del llave foranea"
        dosis.database=False
        dosisList.append(dosis)


    def delete(self, id):
        global dosisList
        filtro= list(filter(lambda x: x.id == id, dosisList))
        filtro2=list(filter(lambda x: x.id == id, self.index()))
        if len(filtro) != 0:
            temp =list(filter(lambda x: x.login != id, dosisList))
            dosisList.clear()
            dosisList = [e for e in temp]
            return
        elif len(filtro2) != 0:
            conn = coneccion()
            conn.ejecutar( """
            DELETE FROM dosis WHERE dosis.id = '{}';
            """.format(id), "POST")
            return

    def guardarLista(self):
        generador = (e for e in dosisList )
        while True:
            try:
                dosis = generador.__next__()
                conn = coneccion()
                conn.ejecutar( """
                INSERT INTO dosis (id,animal,enfermedad, medicamento,pesoMax,pesoMin,dosis)
                 VALUES ('{}','{}','{}','{}', {}, {}, {});
                """.format(dosis.id,dosis.animal,dosis.enfermedad,dosis.medicamento,dosis.pesoMax,dosis.pesoMin,dosis.dosis), "POST")

            except StopIteration:
                dosisList.clear()
                break

    def borrarLista(self):
        dosisList.clear()
        return

class PrescripcionController:



    def setDosis(self,presc):
        connt = coneccion()
        connt.ejecutar("""select id from dosis where dosis.animal = '{}'  and dosis.enfermedad = '{}'  ;""".format(presc.animal,presc.enfermedad) , "GET")
        if len(connt.registros) > 0 :
            connt.registros[0][0]
            presc.dosis=connt.registros[0][0]
            return presc
        presc.dosis=None
        return presc



    def index(self):
        connt = coneccion()
        connt.ejecutar("select * from prescripcion ;", "GET")
        prescBD = [prescripcion(row[0], row[2], row[1], row[3], row[4],row[5]) for row in connt.registros]
        return prescBD

    def update(self, presc):
        global prescripciones
        filtro= list(filter(lambda x: x.id == presc.id, prescripciones))
        filtro2=list(filter(lambda x: x.id == presc.id, self.index()))
        if len(filtro) != 0:
           temp = list(filter(lambda x: x.id != presc.id, prescripciones))
           prescripciones=temp
           presc.database=False
           prescripciones.append(presc)
        elif len(filtro2) != 0:
            query = """update prescripcion set animal = '{}',enfermedad = '{}',
            usuario ='{}',peso ={}, dosis={}   Where id = {}""".format(presc.animal,presc.enfermedad,presc.usuario,presc.peso,presc.dosis,presc.id)
            connt = coneccion()
            connt.ejecutar(query,"POST")

    def create(self, presc):
        if len(prescripciones) == 0 and len(self.index()) == 0:
            presc.database=False
            presc = self.setDosis(presc)
            prescripciones.append(presc)
            return
        filtro = list(filter(lambda x: x.id == presc.id, prescripciones))
        filtro2 = list(filter(lambda x: x.id == presc.id, self.index()))
        if len(filtro) != 0 or len(filtro2) != 0:
           return "Error del llave foranea"
        presc.database=False
        temp = self.setDosis(presc)
        presc=temp
        prescripciones.append(presc)


    def delete(self, id):
        global prescripciones
        filtro= list(filter(lambda x: x.id == id, prescripciones))
        filtro2=list(filter(lambda x: x.id == id, self.index()))
        if len(filtro) != 0:
            temp =list(filter(lambda x: x.id != id, prescripciones))
            prescripciones.clear()
            prescripciones = [e for e in temp]
            return
        elif len(filtro2) != 0:
            conn = coneccion()
            conn.ejecutar( """
            DELETE FROM prescripcion WHERE id = {};
            """.format(id), "POST")
            return

    def guardarLista(self):
        generador = (e for e in prescripciones )
        while True:
            try:
                presc  = generador.__next__()
                conn = coneccion()
                conn.ejecutar( """
                INSERT INTO prescripcion (id,animal,enfermedad, usuario,peso,dosis)
                 VALUES ({},'{}','{}','{}', {}, {});
                """.format(presc.id,presc.animal,presc.enfermedad,presc.usuario,presc.peso,presc.dosis), "POST")

            except StopIteration:
                prescripciones.clear()
                break

    def borrarLista(self):
        prescripciones.clear()
        return