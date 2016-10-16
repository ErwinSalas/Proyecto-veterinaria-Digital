import base64

__author__ = 'Erwin'
#!flask/bin/python
from flask import Flask,request,render_template
import flask_login
from funciones import *
import funciones

usuarioController = UsuarioController()
ameController = AMEController()
dosisController=DosisController()
prescripcionController=PrescripcionController()
permiso=False

app = Flask(__name__)
app.secret_key = 'admin'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
    pass
@login_manager.request_loader
def request_loader(request):
    global permiso
    user = request.form.get('login')
    users = usuarioController.registrosLogin()
    for registro in users:
        if user == registro.login:
            reg = User()
            reg.id = user
            permiso = ("admin" == registro.permiso)
            return reg
    return

@login_manager.user_loader
def user_loader(user):
    users = usuarioController.registrosLogin()
    for registro in users:
        if user == registro.login:
            reg = User()
            reg.id = user
            return reg
    return

#------------------------------------------------------------------------------------
#Home
#-------------------------------------------------------------------------------------

@app.route('/')
def home():
    flask_login.logout_user()
    return render_template('login.html')






@app.route('/',methods=['POST'])
def login():
    global permiso
    nombre=request.form['user']
    passw=request.form['pass']

    users=list(filter(lambda x: x.login == nombre and x.pasw==passw, usuarioController.registrosLogin()))
    if len(users) !=0:
        registro= users[0]
        user= User()
        user.id = nombre
        permiso = ("admin" == registro.permiso)
        flask_login.login_user(user)
        return render_template('layout.html')
    # users=list(filter(lambda x: x.login == nombre and x.pasw==passw, usuarioController.index()))
    # if len(users) !=0:
    #    session=users[0]
    #    print(session.permiso)
    #    return render_template('layout.html')
    # return """" <h1>Credenciales invalidos</h1>"""

#---------------------------------------------------------------------------------------------
#usuarios
#Todos los end points de usuarios
#-----------------------------------------------------------------------------------------------
@app.route('/usuarios/registrar')
def mostrarFormularioUsuarios():
    if permiso==False:
        return render_template('error.html')
    return render_template('registro.html')


@app.route('/usuarios/edit/<string:id>')
def mostrarFormularioEditar(id):
    if permiso==False:
        return render_template('error.html')
    #Devuelve el formulario con los datos correspondientes
    # al usuario seleccionado
    lista=usuarioController.index()
    filtro=list(filter(lambda x: x.login == id,lista))
    filtro2 = list(filter(lambda x: x.login == id, usuarios))
    if len(filtro) !=0:
        #si esta en la lista temporal
        return render_template('edit.html', user=filtro[0])
    elif len(filtro2) !=0:
        #si esta en la Base de datos
        return render_template('edit.html', user=filtro2[0])

    return"Error"


@app.route('/usuarios/edit', methods=['POST'])
    #una vez editado el perfil del
    #usuario se envia el formulario con los nuevos datos
    #y son recibidos en este metodo

def editarUsuario():
    nomb = request.form['nombre']
    log= request.form['login']
    passw= request.form['contraseña']
    perm= request.form['permiso']
    foto= request.files['foto']
    encoded_string = base64.b64encode(foto.getvalue())
    result = encoded_string.decode('utf8')
    user = usuario(nomb,log,passw,perm,result)
    usuarioController.update(user)
    return mostrarUsuaios(0)


@app.route('/usuarios/guardar')
    #guarda la lista temporal en la base de datos
def guardarListaUsuarios():
    usuarioController.guardarLista()
    return mostrarUsuaios(0)


@app.route('/usuarios/registrar',methods=['POST'])
    #captura los datos del usuario
    #los almasena en un DTO y lo envia al controlador
def obtenerUsuario():
    nomb = request.form['nombre']
    log= request.form['login']
    passw= request.form['pass']
    perm= request.form['permiso']
    foto= request.files['foto']
    encoded_string = base64.b64encode(foto.getvalue())
    result = encoded_string.decode('utf8')
    user = usuario(nomb,log,passw,perm,result)
    usuarioController.create(user)
    return mostrarUsuaios(0)

@app.route('/usuarios/delete/<string:id>', methods=['POST', 'GET'])
    #captura en identificador del usuarioa eliminar
    #y realiza una invocacion al metodo delete del controlador
def borrarUsuario(id):
    if permiso==False:
        return render_template('error.html')
    usuarioController.delete(id)
    return mostrarUsuaios(0)

@app.route('/usuarios/<int:index>',methods=['GET'])
def mostrarUsuaios(index):
    #Este metodo no esta funcionando xq estoy trabajando en lo de paginacion
    users = usuarioController.index()
    lista = users+funciones.usuarios
    try:
        trozo=lista[index:index+3]
        return render_template('index.html', usuarios=trozo,tamaño=len(lista) )
    except :
        trozo=lista[index:len(lista)-1]
        return render_template('index.html', usuarios=trozo,tamaño=len(lista))




#-----------------------------------------------------------------------------------------------------------
#animales
#----------------------------------------------------------------------------------------------------------

@app.route('/animales/delete/<string:nombre>', methods=['POST', 'GET'])
     #captura en identificador del animal eliminar
    #y realiza una invocacion al metodo delete del controlador
def borrarAnimal(nombre):
    if permiso==False:
        return render_template('error.html')
    temp=ameController.delete(nombre,'animal',funciones.animales)
    funciones.animales=temp
    return mostrarAnimales(0)

@app.route('/animales/<int:index>')
def mostrarAnimales(index):
    anim = ameController.index('animal')
    lista = anim+funciones.animales
    try:
        trozo=lista[index:index+3]
        return render_template('indexAnimales.html', animales=trozo,tamaño=len(lista) )
    except :
        trozo=lista[index:len(lista)-1]
        return render_template('indexAnimales.html', animales=trozo,tamaño=len(lista))

@app.route('/animales/edit/<string:id>')
def mostrarFormularioEditarAnimales(id):
    if permiso==False:
        return render_template('error.html')
    lista= ameController.index('animal')
    filtro=list(filter(lambda x: x.nombre == id,lista))
    filtro2 = list(filter(lambda x: x.nombre == id, funciones.animales))
    if len(filtro) !=0:
        return render_template('editAnimales.html', anim=filtro[0])
    elif len(filtro2) !=0:
        return render_template('editAnimales.html', anim=filtro2[0])

    return"Error"


@app.route('/animales/edit', methods=['POST'])
     #una vez editado el perfil del
    #animal se envia el formulario con los nuevos datos
    #y son recibidos en este metodo
def editarAnimal():
    nomb = request.form['nombre']
    desc= request.form['descripcion']
    foto= request.files['foto']
    encoded_string = base64.b64encode(foto.getvalue())
    result = encoded_string.decode('utf8')
    anim = animal(nomb,desc,result)
    temp=ameController.update(anim,funciones.animales)
    funciones.animales=temp
    return mostrarAnimales(0)

@app.route('/animales/registrar')
def mostrarFormularioAnimales():
    if permiso==False:
        return render_template('error.html')
    return render_template('registroAnimales.html')

@app.route('/animales/registrar',methods=['POST'])
def obtenerAnimal():
    nomb = request.form['nombre']
    desc= request.form['descripcion']
    foto= request.files['foto']
    encoded_string = base64.b64encode(foto.getvalue())
    result=encoded_string.decode('utf8')
    anim=animal(nomb,desc,result)
    temp = ameController.create(anim,funciones.animales)
    funciones.animales = temp
    return mostrarAnimales(0)

@app.route('/animales/guardar')
def guardarListaAnimales():
    ameController.guardarLista(funciones.animales)
    funciones.animales.clear()

    return mostrarAnimales(0)

#-----------------------------------------------------------------------------------------------------------
#Medicamentos
#----------------------------------------------------------------------------------------------------------

@app.route('/medicamentos/delete/<string:nombre>', methods=['POST', 'GET'])
     #captura en identificador del medicamento eliminar
    #y realiza una invocacion al metodo delete del controlador
def borrarMedicamento(nombre):
    if permiso==False:
        return render_template('error.html')
    temp=ameController.delete(nombre,'medicamentos',funciones.medicamentos)
    funciones.medicamentos=temp
    return mostrarMedicamentos(0)


@app.route('/medicamentos/<int:index>')
def mostrarMedicamentos(index):
    med=ameController.index('medicamentos')
    lista = med+funciones.medicamentos
    try:
        trozo=lista[index:index+3]
        return render_template('indexMedicamentos.html', medicamentos=trozo,tamaño=len(lista) )
    except :
        trozo=lista[index:len(lista)-1]
        return render_template('indexMedicamentos.html', medicamentos=trozo,tamaño=len(lista))

@app.route('/medicamentos/registrar')
def mostrarFormularioMedicamentos():
    if permiso==False:
        return render_template('error.html')
    return render_template('registroMedicamentos.html')

@app.route('/medicamentos/registrar',methods=['POST'])
def obtenerMedicamento():
    nomb = request.form['nombre']
    desc= request.form['descripcion']
    foto= request.files['foto']
    encoded_string = base64.b64encode(foto.getvalue())
    result=encoded_string.decode('utf8')
    med=medicamento(nomb,desc,result)
    temp = ameController.create(med,funciones.medicamentos)
    funciones.medicamentos = temp
    return mostrarMedicamentos(0)


@app.route('/medicamentos/edit/<string:id>')
def mostrarFormularioEditarMedicamentos(id):
    if permiso==False:
        return render_template('error.html')
    lista= ameController.index('medicamentos')
    filtro=list(filter(lambda x: x.nombre == id,lista))
    filtro2 = list(filter(lambda x: x.nombre == id, funciones.medicamentos))
    if len(filtro) !=0:
        return render_template('editMedicamentos.html', med=filtro[0])
    elif len(filtro2) !=0:
        return render_template('editMedicamentos.html', med=filtro2[0])

    return"Error"


@app.route('/medicamentos/edit', methods=['POST'])
     #una vez editado el perfil del
    #medicamento se envia el formulario con los nuevos datos
    #y son recibidos en este metodo
def editarMedicamento():
    nomb = request.form['nombre']
    desc= request.form['descripcion']
    foto= request.files['foto']
    encoded_string = base64.b64encode(foto.getvalue())
    result = encoded_string.decode('utf8')
    med = medicamento(nomb,desc,result)
    temp=ameController.update(med,funciones.medicamentos)
    funciones.medicamentos=temp
    return mostrarMedicamentos(0)

@app.route('/medicamentos/guardar')
def guardarListaMedicamentos():
    ameController.guardarLista(funciones.medicamentos)
    funciones.medicamentos.clear()

    return mostrarMedicamentos(0)
#-----------------------------------------------------------------------------------------------------------
#Enfermedades
#----------------------------------------------------------------------------------------------------------

@app.route('/enfermedades/delete/<string:nombre>', methods=['POST', 'GET'])
def borrarEnfermedad(nombre):
     #captura en identificador de la enfermedad eliminar
    #y realiza una invocacion al metodo delete del controlador
    if permiso==False:
        return render_template('error.html')
    temp=ameController.delete(nombre,'enfermedad',funciones.enfermedades)
    funciones.enfermedades=temp
    return mostrarEnfermedades(0)


@app.route('/enfermedades/<int:index>')
def mostrarEnfermedades(index):
    enf=ameController.index('enfermedad')
    lista = enf+funciones.enfermedades
    try:
        trozo=lista[index:index+3]
        return render_template('indexEnfermedades.html', enfermedades=trozo,tamaño=len(lista) )
    except :
        trozo=lista[index:len(lista)-1]
        return render_template('indexEnfermedades.html', enfermedades=trozo,tamaño=len(lista))


@app.route('/enfermedades/registrar')
def mostrarFormularioEnfermedades():
    if permiso==False:
        return render_template('error.html')
    return render_template('registroEnfermedades.html')

@app.route('/enfermedades/registrar',methods=['POST'])
def obtenerEnfermedad():
    nomb = request.form['nombre']
    desc= request.form['descripcion']
    foto= request.files['foto']
    encoded_string = base64.b64encode(foto.getvalue())
    result=encoded_string.decode('utf8')
    enf=enfermedad(nomb,desc,result)
    temp = ameController.create(enf,funciones.enfermedades)
    funciones.enfermedades = temp
    return mostrarEnfermedades(0)


@app.route('/medicamentos/edit/<string:id>')
def mostrarFormularioEditarEnfermedad(id):
    if permiso==False:
        return render_template('error.html')
    lista= ameController.index('enfermedad')
    filtro=list(filter(lambda x: x.nombre == id,lista))
    filtro2 = list(filter(lambda x: x.nombre == id, funciones.enfermedades))
    if len(filtro) !=0:
        return render_template('editEnfermedades.html', med=filtro[0])
    elif len(filtro2) !=0:
        return render_template('editEnfermedades.html', med=filtro2[0])

    return"Error"


@app.route('/enfermedades/edit', methods=['POST'])
     #una vez editado el perfil de la
    #enfermedad se envia el formulario con los nuevos datos
    #y son recibidos en este metodo
def editarEnfermedades():
    nomb = request.form['nombre']
    desc= request.form['descripcion']
    foto= request.files['foto']
    encoded_string = base64.b64encode(foto.getvalue())
    result = encoded_string.decode('utf8')
    enf = enfermedades(nomb,desc,result)
    temp=ameController.update(enf,funciones.enfermedades)
    funciones.enfermedades=temp
    return mostrarEnfermedades(0)

@app.route('/enfermedades/guardar')
def guardarListaEnfermedades():
    ameController.guardarLista(funciones.enfermedades)
    funciones.enfermedades.clear()
    return mostrarEnfermedades(0)

#-------------------------------------------------------------------------------------------------------------------
#dosis
#_______________________________________________________________________________________________________________________


@app.route('/dosis/registrar')
def mostrarFormularioDosis():
    if permiso==False:
        return render_template('error.html')
    anim=ameController.index('animal')+funciones.animales
    med=ameController.index('medicamentos')+funciones.medicamentos
    enf=ameController.index('enfermedad')+funciones.enfermedades
    return render_template('registroDosis.html',enfermedades=enf,animales=anim,medicamentos=med)


@app.route('/dosis/edit/<int:id>')
def mostrarFormularioEditarDosis(id):
    #Devuelve el formulario con los datos correspondientes
    # al usuario seleccionado
    if permiso==False:
        return render_template('error.html')
    lista=dosisController.index()
    anim=ameController.index('animal')+funciones.animales
    med=ameController.index('medicamentos')+funciones.medicamentos
    enf=ameController.index('enfermedad')+funciones.enfermedades
    filtro=list(filter(lambda x: x.id == id,lista))
    filtro2 = list(filter(lambda x: x.id == id, dosisList))
    if len(filtro) !=0:
        #si esta en la lista temporal
        return render_template('editDosis.html', dosis=filtro[0],enfermedades=enf,animales=anim,medicamentos=med)
    elif len(filtro2) !=0:
        #si esta en la Base de datos
        return render_template('editDosis.html', dosis=filtro2[0],enfermedades=enf,animales=anim,medicamentos=med,)

    return"Error"


@app.route('/dosis/edit', methods=['POST'])
    #una vez editado el perfil del
    #usuario se envia el formulario con los nuevos datos
    #y son recibidos en este metodo

def editarDosis():
    id = int(request.form['id'])
    anim= request.form['animal']
    med= request.form['medicamento']
    enf= request.form['enfermedad']
    dosis= request.form['dosis']
    pesoMax=request.form['pesoMax']
    pesoMin=request.form['pesoMin']

    dos = Dosis(id,anim,enf,med ,pesoMax,pesoMin,dosis)
    dosisController.update(dos)
    return mostrarDosis(0)


@app.route('/dosis/guardar')
    #guarda la lista temporal en la base de datos
def guardarListaDosis():
    dosisController.guardarLista()
    return mostrarDosis(0)


@app.route('/dosis/registrar',methods=['POST'])
    #captura los datos de la dosis
    #los almasena en un DTO y lo envia al controlador
def obtenerDosis():
    print(request.values)
    id = int(request.form['id'])
    anim= request.form['animal']
    med= request.form['medicamento']
    enf= request.form['enfermedad']
    dosis= request.form['dosis']
    pesoMax=request.form['pesoMax']
    pesoMin=request.form['pesoMin']
    dos = Dosis(id,anim,med,enf ,pesoMax,pesoMin,dosis)
    dosisController.create(dos)
    return mostrarDosis(0)

@app.route('/dosis/delete/<int:id>', methods=['POST', 'GET'])
    #captura en identificador del usuarioa eliminar
    #y realiza una invocacion al metodo delete del controlador
def borrarDosis(id):
    if permiso==False:
        return render_template('error.html')
    dosisController.delete(id)
    return mostrarDosis(0)

@app.route('/dosis/<int:index>',methods=['GET'])
def mostrarDosis(index):
    dosis = dosisController.index()
    lista = dosis+funciones.dosisList
    try:
        trozo=lista[index:index+6]
        return render_template('indexDosis.html', dosisList=trozo,tamaño=len(lista) )
    except :
        trozo=lista[index:len(lista)-1]
        return render_template('indexDosis.html', dosisList=trozo,tamaño=len(lista))



@app.route('/busqueda/<int:index>', methods=['POST'])
def buscar(index):
    valor = request.form['busqueda']
    lista=dosisController.index()+funciones.dosisList
    filtro= list(filter(lambda x: x.animal.find(valor) != -1, lista))
    filtro2= list(filter(lambda x: x.enfermedad.find(valor) != -1, lista))
    lista=filtro+filtro2
    try:
        trozo=lista[index:index+6]
        return render_template('indexDosis.html', dosisList=trozo,tamaño=len(lista) )
    except :
        trozo=lista[index:len(lista)-1]
        return render_template('indexDosis.html', dosisList=trozo,tamaño=len(lista))

#-------------------------------------------------------------------------------------------------------------------
#Prescripcion
#_______________________________________________________________________________________________________________________


@app.route('/prescripciones/registrar')
def mostrarFormularioPrescripcion():
    anim=ameController.index('animal')+funciones.animales
    user=usuarioController.index()+funciones.usuarios
    enf=ameController.index('enfermedad')+funciones.enfermedades
    return render_template('registroPrescripcion.html',enfermedades=enf,animales=anim,usuarios=user)


@app.route('/prescripciones/edit/<int:id>')
def mostrarFormularioEditarPrescripcion(id):
    #Devuelve el formulario con los datos correspondientes
    # al usuario seleccionado
    lista=prescripcionController.index()
    anim=ameController.index('animal')+funciones.animales
    user=usuarioController.index()+funciones.usuarios
    enf=ameController.index('enfermedad')+funciones.enfermedades
    filtro=list(filter(lambda x: x.id == id,lista))
    filtro2 = list(filter(lambda x: x.id == id, funciones.prescripciones))
    if len(filtro) !=0:
        #si esta en la lista temporal
        return render_template('editPrescripciones.html', presc=filtro[0],enfermedades=enf,animales=anim,usuarios=user)
    elif len(filtro2) !=0:
        #si esta en la Base de datos
        return render_template('editPrescripciones.html', presc=filtro2[0],enfermedades=enf,animales=anim,usuarios=user,)

    return"Error"


@app.route('/prescripciones/edit', methods=['POST'])
    #una vez editado el perfil del
    #usuario se envia el formulario con los nuevos datos
    #y son recibidos en este metodo

def editarPrescripcion():
    id = int(request.form['id'])
    anim= request.form['animal']
    user= request.form['usuario']
    enf= request.form['enfermedad']
    peso=request.form['peso']
    presc = prescripcion(id,anim ,user,enf ,peso,None)
    prescripcionController.update(presc)
    return mostrarPrescripcion(0)


@app.route('/prescripciones/guardar')
    #guarda la lista temporal en la base de datos
def guardarListaPrescripcion():
    prescripcionController.guardarLista()
    return mostrarPrescripcion(0)


@app.route('/prescripciones/registrar',methods=['POST'])
    #captura los datos de la dosis
    #los almasena en un DTO y lo envia al controlador
def obtenerPrescripcion():
    id = int(request.form['id'])
    anim= request.form['animal']
    user= request.form['usuario']
    enf= request.form['enfermedad']
    peso=request.form['peso']
    presc = prescripcion(id,anim ,user,enf ,peso,None)
    prescripcionController.create(presc)
    return mostrarPrescripcion(0)

@app.route('/prescripciones/delete/<int:id>', methods=['POST', 'GET'])
    #captura en identificador del usuarioa eliminar
    #y realiza una invocacion al metodo delete del controlador
def borrarPrescripcion(id):

    prescripcionController.delete(id)
    return mostrarPrescripcion(0)

@app.route('/prescripciones/<int:index>',methods=['GET'])
def mostrarPrescripcion(index):
    presc = prescripcionController.index()
    lista = presc + funciones.prescripciones
    try:
        trozo=lista[index:index+6]
        return render_template('indexPrescripciones.html', prescripciones=trozo,tamaño=len(lista) )
    except :
        trozo=lista[index:len(lista)]
        return render_template('indexPrescripciones.html', prescripciones=trozo,tamaño=len(lista))


if __name__ == '__main__':
    app.run(debug=True)
home()