from flask import render_template
from . import cliente
from controller import *  # Importando mis Funciones
from bd import *  # Importando conexion BD
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import re
from flask import *
from flask import render_template
import controller


@cliente.route('/')
def index():
  productos = controller.datosMedicamentosHomeNoLogin()
  return render_template("inicio.html", productos=productos)



# ACTUALIZAR DATOS CLIENTE
@cliente.route("/actualizarDatosCliente", methods=["POST"])
def actualizarDatosCliente():
    id = request.form["id"]
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    correo = request.form["correo"]
    direccion = request.form["direccion"]
    telefono = request.form["telefono"]
    genero = request.form["genero"]
    controller.actualizarDatosCliente(nombre, apellido, correo, direccion, telefono, genero, id)
    return render_template("homecliente.html",dataLogin= dataLoginSesion())


# Home cliente
@cliente.route('/homecliente/')
def homecliente():
    noOfItems = 0
    conexion = obtener_conexion()
    correo = session['correo']
    cursor = conexion.cursor()
    cursor.execute("SELECT id FROM usuario WHERE correo = %s", (correo,))
    userId = cursor.fetchone()[0]
    cursor.fetchall()
    cursor.execute("SELECT count(id_producto) FROM carrito WHERE id = %s", (userId, ))
    noOfItems = cursor.fetchone()[0]    
    productos = controller.datosMedicamentosHome()
    return render_template("homecliente.html", productos=productos,dataLogin= dataLoginSesion(),noOfItems=noOfItems)


# Medicamentos cliente
@cliente.route('/medicamentoscliente/')
def medicamentoscliente():
  productos = controller.datosMedicamentos()
  return render_template("medicamentos.html", productos=productos,dataLogin= dataLoginSesion())


# Datos cliente
@cliente.route('/datoscliente/')
def datoscliente():
    return render_template('datoscliente.html', dataLogin= dataLoginSesion())


# Comprar producto
@cliente.route('/comprarproducto/')
def comprarproducto():
    noOfItems = 0
    conexion = obtener_conexion()
    correo = session['correo']
    cursor = conexion.cursor()
    cursor.execute("SELECT id FROM usuario WHERE correo = %s", (correo,))
    userId = cursor.fetchone()[0]
    cursor.fetchall()
    cursor.execute("SELECT count(id_producto) FROM carrito WHERE id = %s", (userId, ))
    noOfItems = cursor.fetchone()[0] 

    productId = request.args.get('id_producto')

    with conexion.cursor() as cursor:
        cursor.execute('SELECT id_producto, nombre, descripcion,cantidad, precio FROM producto WHERE id_producto = %s', (productId,))
        productData = cursor.fetchall()
    return render_template("comprarproducto.html",noOfItems=noOfItems,productData=productData,productId=productId)


# Cuidado personal
@cliente.route('/cuidadopersonalclient/')
def cuidadopersonalclient():
  productos = controller.datosCuidadoPersonal()
  return render_template("cuidadopersonalclient.html", productos=productos,dataLogin= dataLoginSesion())

# Dermacosmeticos
@cliente.route('/dermacosmetica/')
def dermacosmetica():
  productos = controller.datosDermacosmetica()
  return render_template("dermacosmetica.html", productos=productos,dataLogin= dataLoginSesion())


# Nutricionales
@cliente.route('/nutricionales/')
def nutricionales():
  productos = controller.datosNutricional()
  return render_template("nutricionales.html", productos=productos,dataLogin= dataLoginSesion())

# Bebe
@cliente.route('/bebemed/')
def bebemed():
  productos = controller.datosBebe()
  return render_template("bebemed.html", productos=productos,dataLogin= dataLoginSesion())


# Inicio cliente
@cliente.route('/inicio/')
def inicio():
    return render_template("inicio.html")


# PAGINACION 

#Pag. Medicamentos 
@cliente.route("/pag_medicamentos/<number_pag>")
def pag_medicamentos(number_pag):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    if number_pag == '1':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 5 LIMIT 0,12")
    if number_pag == '2':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 5 LIMIT 12,12")
    if number_pag == '3':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 5 LIMIT 24,12")
    if number_pag == '4':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 5 LIMIT 36,12")
        
    if number_pag == '5':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 5 LIMIT 48,12")
    if number_pag == '6':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 5 LIMIT 60,12")
    if number_pag == '7':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 5 LIMIT 72,12")
    if number_pag == '8':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 5 LIMIT 84,12")
    if number_pag == '9':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 5 LIMIT 96,12")
    if number_pag == '10':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 5 LIMIT 108,12")
    productos = cursor.fetchall()
    conexion.commit()
    return render_template('medicamentos.html', productos=productos) 

#Pag. Cuidado personal

@cliente.route("/pag_cuidado_personal/<number_pag>")
def pag_cuidado_personal(number_pag):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    if number_pag == '1':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 1 LIMIT 0,12")
    if number_pag == '2':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 1 LIMIT 12,12")
    if number_pag == '3':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 1 LIMIT 24,12")
    if number_pag == '4':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 1 LIMIT 36,12")
        
    if number_pag == '5':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 1 LIMIT 48,12")
    if number_pag == '6':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 1 LIMIT 60,12")
    if number_pag == '7':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 1 LIMIT 72,12")
    if number_pag == '8':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 1 LIMIT 84,12")
    if number_pag == '9':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 1 LIMIT 96,12")
    if number_pag == '10':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 1 LIMIT 108,12")
    productos = cursor.fetchall()
    conexion.commit()
    return render_template('cuidadopersonalclient.html', productos=productos ,dataLogin= dataLoginSesion()) 

#Pag. Dermacosmética

@cliente.route("/pag_dermacosmetica/<number_pag>")
def pag_dermacosmetica(number_pag):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    if number_pag == '1':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 2 LIMIT 0,12")
    if number_pag == '2':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 2 LIMIT 12,12")
    if number_pag == '3':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 2 LIMIT 24,12")
    if number_pag == '4':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 2 LIMIT 36,12")
        
    if number_pag == '5':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 2 LIMIT 48,12")
    if number_pag == '6':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 2 LIMIT 60,12")
    if number_pag == '7':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 2 LIMIT 72,12")
    if number_pag == '8':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 2 LIMIT 84,12")
    if number_pag == '9':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 2 LIMIT 96,12")
    if number_pag == '10':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 2 LIMIT 108,12")
    productos = cursor.fetchall()
    conexion.commit()
    return render_template('dermacosmetica.html', productos=productos ,dataLogin= dataLoginSesion()) 

#Pag. Nutricionales

@cliente.route("/pag_nuticional/<number_pag>")
def pag_nuticional(number_pag):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    if number_pag == '1':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 3 LIMIT 0,12")
    if number_pag == '2':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 3 LIMIT 12,12")
    if number_pag == '3':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 3 LIMIT 24,12")
    if number_pag == '4':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 3 LIMIT 36,12")
        
    if number_pag == '5':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 3 LIMIT 48,12")
    if number_pag == '6':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 3 LIMIT 60,12")
    if number_pag == '7':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 3 LIMIT 72,12")
    if number_pag == '8':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 3 LIMIT 84,12")
    if number_pag == '9':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 3 LIMIT 96,12")
    if number_pag == '10':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 3 LIMIT 108,12")
    productos = cursor.fetchall()
    conexion.commit()
    return render_template('nutricionales.html', productos=productos ,dataLogin= dataLoginSesion()) 

#Pag. Bebé

@cliente.route("/pag_bebe/<number_pag>")
def pag_bebe(number_pag):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    if number_pag == '1':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 4 LIMIT 0,12")
    if number_pag == '2':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 4 LIMIT 12,12")
    if number_pag == '3':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 4 LIMIT 24,12")
    if number_pag == '4':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 4 LIMIT 36,12")
        
    if number_pag == '5':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 4 LIMIT 48,12")
    if number_pag == '6':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 4 LIMIT 60,12")
    if number_pag == '7':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 4 LIMIT 72,12")
    if number_pag == '8':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 4 LIMIT 84,12")
    if number_pag == '9':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 4 LIMIT 96,12")
    if number_pag == '10':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 4 LIMIT 108,12")
    productos = cursor.fetchall()
    conexion.commit()
    return render_template('nutricionales.html', productos=productos ,dataLogin= dataLoginSesion()) 


@cliente.route('/buscar', methods=['GET', 'POST'])
def buscar():
    if request.method == 'POST':
        # Obtener el término de búsqueda del usuario
        busqueda = request.form['busqueda']
        
        # Crear una consulta para buscar en la base de datos
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        consulta = "SELECT * FROM producto WHERE nombre LIKE '%{}%'".format(busqueda)
        cursor.execute(consulta)
        
        # Obtener los resultados de la consulta
        resultados = cursor.fetchall()
        
        if len(resultados) == 0:
            # Si no se encontraron resultados, mostrar un mensaje
            mensaje = "No se encontraron productos para '{}'. Intente con otra búsqueda.".format(busqueda)
            return render_template('base_cliente_registrado.html', mensaje=mensaje)
        else:
            # Si se encontraron resultados, mostrarlos
            return render_template('base_cliente_registrado.html', resultados=resultados)
    
    # Si la solicitud es GET, mostrar la página de búsqueda
    return render_template('base_cliente_registrado.html')


