from controller import *  # Importando mis Funciones
from bd import *  # Importando conexion BD
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import re
from flask import *
from flask import render_template
from datetime import date
from flask import request, session
from . import administrador
import controller
from flask import Flask, url_for, redirect
import hashlib
import os
from flask_app import app
from datetime import date
from os import listdir
from flask import redirect
from flask import url_for

from flask import make_response
from flask import jsonify
from datetime import timedelta

from flask_babel import Babel, gettext, refresh; refresh()
import babel.dates



UPLOAD_FOLDER = os.path.abspath('static/uploads')
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@administrador.route('/home_admin/')
def home_admin():
    translations = {
        'usrreg': gettext('Usuarios Registrados'),
        'titadm': gettext('Administradores'),
        'reg': gettext('Registrados'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'infogen': gettext('A traves de esta seccion el administrador tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),

    }
    
    
    admin = controller.user_cant_admin()
    cliente = controller.user_cant_client()
    return render_template("home.html", admin=admin,cliente=cliente,dataLogin= dataLoginSesion(),
                           **dict(translations.items()))    


@administrador.route("/registrar_producto", methods=["POST"])
def registrar_producto():
    translations = {
        'usrreg': gettext('Usuarios Registrados'),
        'titadm': gettext('Administradores'),
        'reg': gettext('Registrados'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'infogen': gettext('A traves de esta seccion el administrador tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),

    }

    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    cantidad = request.form["cantidad"]
    precio = request.form["precio"]
    proveedor = request.form["proveedor"]
    fecha_vencimiento = request.form["fecha_vencimiento"]
    categoria = request.form["categoria"]
    
    imagen = request.files['imagen']
    imagename = None  # Inicializando imagename con un valor por defecto

    if imagen and allowed_file(imagen.filename):
        filename = secure_filename(imagen.filename)
        # Imprime la ruta para verificarla
        print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # Guardar la imagen en la ruta absoluta
        imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        imagename = filename

    

    controller.insertar_producto(nombre, descripcion, cantidad, precio, proveedor, fecha_vencimiento, imagename, categoria)
    
    return render_template("home.html", dataLogin=dataLoginSesion(), **dict(translations.items()))

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@administrador.route('/cuidado_personal/')
def cuidado_personal():
    translations = {
        'titadm': gettext('Administracion de productos de cuidado personal'),
        'descper': gettext('Esta sección permite operar sobre los productos de cuidado personal'),
        'menuprodl': gettext('Lista de productos'),
        'menuproda': gettext('Adicionar producto'),
        'adnom': gettext('Nombre'),
        'addes': gettext('Descripcion'),
        'adcant': gettext('Cantidad'),
        'adprec': gettext('Precio'),
        'adprov': gettext('Proveedor'),
        'adfech': gettext('Fecha Vencimiento'),
        'adimg': gettext('Imagen'),
        'btncan': gettext('Cancelar'),
        'btnsav': gettext('Guardar'),
        'tbnomp': gettext('Nombre'),
        'tbcan': gettext('Cantidad disponible'),
        'tbprec': gettext('Precio'),
        'tbfech': gettext('Fecha de Vencimiento'),
        'tbmod': gettext('Modificar'),
        'tbel': gettext('Eliminar'),
        'expl': gettext('Abrir Explorador'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'infogen': gettext('A traves de esta seccion el administrador tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),
        'titedit': gettext('Edicion de datos'),
        'desedit': gettext('Esta sección permite operar sobre los productos'),
    }
    productos = controller.producto_personal()
    return render_template("cuidadopersonal.html", productos=productos,dataLogin= dataLoginSesion(),**dict(translations.items()))

@administrador.route("/cuidado_personal_pag/<number_page>")
def page_cuidado_p(number_page):
    translations = {
        'titadm': gettext('Administracion de productos de cuidado personal'),
        'descper': gettext('Esta sección permite operar sobre los productos de cuidado personal'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'tbnomp': gettext('Nombre'),
        'tbcan': gettext('Cantidad disponible'),
        'tbprec': gettext('Precio'),
        'tbfech': gettext('Fecha de Vencimiento'),
        'tbmod': gettext('Modificar'),
        'tbel': gettext('Eliminar'),
        'menuprodl': gettext('Lista de productos'),
        'menuproda': gettext('Adicionar producto'),
        'infogen': gettext('A traves de esta seccion el administrador tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),

    }
    
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    if number_page == '1':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 1 LIMIT 0,10")
    if number_page == '2':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 1 LIMIT 10,10")
    if number_page == '3':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 1 LIMIT 20,10")
    if number_page == '4':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 1 LIMIT 30,10")
        
    if number_page == '5':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 1 LIMIT 40,10")
    if number_page == '6':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 1 LIMIT 50,10")
    if number_page == '7':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 1 LIMIT 60,10")
    if number_page == '8':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 1 LIMIT 70,10")
    if number_page == '9':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 1 LIMIT 80,10")
    if number_page == '10':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 1 LIMIT 90,10")
    productos = cursor.fetchall()
    conexion.commit()
    return render_template('cuidadopersonal.html', productos=productos ,dataLogin= dataLoginSesion(),**dict(translations.items()))   
  
@administrador.route('/dermacosmetico/')
def dermacosmetico():
    translations = {
        'titderm': gettext('Administracion de productos dermacosmeticos'),
        'desderma': gettext('Esta sección permite operar sobre los productos para el cuidado y tratamiento de la piel'),
        'menuprodl': gettext('Lista de productos'),
        'menuproda': gettext('Adicionar producto'),
        'adnom': gettext('Nombre'),
        'addes': gettext('Descripcion'),
        'adcant': gettext('Cantidad'),
        'adprec': gettext('Precio'),
        'adprov': gettext('Proveedor'),
        'adfech': gettext('Fecha Vencimiento'),
        'adimg': gettext('Imagen'),
        'expl': gettext('Abrir Explorador'),
        'btncan': gettext('Cancelar'),
        'btnsav': gettext('Guardar'),
        'tbnomp': gettext('Nombre'),
        'tbcan': gettext('Cantidad disponible'),
        'tbprec': gettext('Precio'),
        'tbfech': gettext('Fecha de Vencimiento'),
        'tbmod': gettext('Modificar'),
        'tbel': gettext('Eliminar'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'infogen': gettext('A traves de esta seccion el administrador tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),
        'titedit': gettext('Edicion de datos'),
        'desedit': gettext('Esta sección permite operar sobre los productos'),
    }
    productos = controller.producto_dermacosmetico()
    return render_template("dermacos.html", productos=productos,dataLogin= dataLoginSesion(),**dict(translations.items()))

@administrador.route("/dermacosmetico_pag/<number_pag>")
def dermacosmetico_pag(number_pag):
    translations = {
        'titderm': gettext('Administracion de productos dermacosmeticos'),
        'desderma': gettext('Esta sección permite operar sobre los productos para el cuidado y tratamiento de la piel'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'tbnomp': gettext('Nombre'),
        'tbcan': gettext('Cantidad disponible'),
        'tbprec': gettext('Precio'),
        'tbfech': gettext('Fecha de Vencimiento'),
        'tbmod': gettext('Modificar'),
        'tbel': gettext('Eliminar'),
        'menuprodl': gettext('Lista de productos'),
        'menuproda': gettext('Adicionar producto'),
        'infogen': gettext('A traves de esta seccion el administrador tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),

    }
    
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    if number_pag == '1':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 2 LIMIT 0,10")
    if number_pag == '2':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 2 LIMIT 10,10")
    if number_pag == '3':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 2 LIMIT 20,10")
    if number_pag == '4':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 2 LIMIT 30,10")
    if number_pag == '5':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 2 LIMIT 40,10")
    if number_pag == '6':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 2 LIMIT 50,10")
    if number_pag == '7':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 2 LIMIT 60,10")
    if number_pag == '8':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 2 LIMIT 70,10")
    if number_pag == '9':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 2 LIMIT 80,10")
    if number_pag == '10':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 2 LIMIT 90,10")
    productos = cursor.fetchall()
    conexion.commit()
    return render_template('dermacos.html', productos=productos ,dataLogin= dataLoginSesion(),**dict(translations.items())) 

@administrador.route('/nutricional/')
def nutricional():
    
    translations = {
        'titnut': gettext('Administracion de productos nutricionales'),
        'descnut': gettext('Esta sección permite operar sobre los productos nutricionales'),
        'menuprodl': gettext('Lista de productos'),
        'menuproda': gettext('Adicionar producto'),
        'adnom': gettext('Nombre'),
        'addes': gettext('Descripcion'),
        'adcant': gettext('Cantidad'),
        'adprec': gettext('Precio'),
        'adprov': gettext('Proveedor'),
        'adfech': gettext('Fecha Vencimiento'),
        'adimg': gettext('Imagen'),
        'btncan': gettext('Cancelar'),
        'btnsav': gettext('Guardar'),
        'tbnomp': gettext('Nombre'),
        'tbcan': gettext('Cantidad disponible'),
        'tbprec': gettext('Precio'),
        'tbfech': gettext('Fecha de Vencimiento'),
        'tbmod': gettext('Modificar'),
        'tbel': gettext('Eliminar'),
        'expl': gettext('Abrir Explorador'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'infogen': gettext('A traves de esta seccion el administrador tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),
        'titedit': gettext('Edicion de datos'),
        'desedit': gettext('Esta sección permite operar sobre los productos'),
    }    
    
    productos = controller.producto_nutricional()
    return render_template("nutricional.html", productos=productos,dataLogin= dataLoginSesion(),**dict(translations.items()))

@administrador.route("/nutricional_pag/<number_pag>")
def nutricional_pag(number_pag):

    translations = {
        'titnut': gettext('Administracion de productos nutricionales'),
        'descnut': gettext('Esta sección permite operar sobre los productos nutricionales'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'tbnomp': gettext('Nombre'),
        'tbcan': gettext('Cantidad disponible'),
        'tbprec': gettext('Precio'),
        'tbfech': gettext('Fecha de Vencimiento'),
        'tbmod': gettext('Modificar'),
        'tbel': gettext('Eliminar'),
        'menuprodl': gettext('Lista de productos'),
        'menuproda': gettext('Adicionar producto'),
        'infogen': gettext('A traves de esta seccion el administrador tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),

    }
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    if number_pag == '1':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 3 LIMIT 0,10")
    if number_pag == '2':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 3 LIMIT 10,10")
    if number_pag == '3':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 3 LIMIT 20,10")
    if number_pag == '4':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 3 LIMIT 30,10")
        
    if number_pag == '5':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 3 LIMIT 40,10")
    if number_pag == '6':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 3 LIMIT 50,10")
    if number_pag == '7':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 3 LIMIT 60,10")
    if number_pag == '8':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 3 LIMIT 70,10")
    if number_pag == '9':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 3 LIMIT 80,10")
    if number_pag == '10':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 3 LIMIT 90,10")
    productos = cursor.fetchall()
    conexion.commit()
    return render_template('nutricional.html', productos=productos ,dataLogin= dataLoginSesion(),**dict(translations.items()))
 
@administrador.route('/bebe/')
def bebe():
    
    translations = {
        'titbeb': gettext('Administracion de productos para bebé'),
        'descnut': gettext('Esta sección permite operar sobre los productos para el cuidado del bebé'),
        'menuprodl': gettext('Lista de productos'),
        'menuproda': gettext('Adicionar producto'),
        'adnom': gettext('Nombre'),
        'addes': gettext('Descripcion'),
        'adcant': gettext('Cantidad'),
        'adprec': gettext('Precio'),
        'adprov': gettext('Proveedor'),
        'adfech': gettext('Fecha Vencimiento'),
        'adimg': gettext('Imagen'),
        'btncan': gettext('Cancelar'),
        'btnsav': gettext('Guardar'),
        'tbnomp': gettext('Nombre'),
        'tbcan': gettext('Cantidad disponible'),
        'tbprec': gettext('Precio'),
        'tbfech': gettext('Fecha de Vencimiento'),
        'tbmod': gettext('Modificar'),
        'tbel': gettext('Eliminar'),
        'expl': gettext('Abrir Explorador'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'infogen': gettext('A traves de esta seccion el administrador tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),
        'titedit': gettext('Edicion de datos'),
        'desedit': gettext('Esta sección permite operar sobre los productos'),
    }       
    
    productos = controller.producto_bebe()
    return render_template("bebe.html", productos=productos,dataLogin= dataLoginSesion(),**dict(translations.items()))

@administrador.route("/bebe_pag/<number_pag>")
def page_bebe(number_pag):
    translations = {
        'titbeb': gettext('Administracion de productos para bebé'),
        'descnut': gettext('Esta sección permite operar sobre los productos para el cuidado del bebé'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'tbnomp': gettext('Nombre'),
        'tbcan': gettext('Cantidad disponible'),
        'tbprec': gettext('Precio'),
        'tbfech': gettext('Fecha de Vencimiento'),
        'tbmod': gettext('Modificar'),
        'tbel': gettext('Eliminar'),
        'menuprodl': gettext('Lista de productos'),
        'menuproda': gettext('Adicionar producto'),
        'infogen': gettext('A traves de esta seccion el administrador tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),

    }

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    if number_pag == '1':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 4 LIMIT 0,10")
    if number_pag == '2':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 4 LIMIT 10,10")
    if number_pag == '3':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 4 LIMIT 20,10")
    if number_pag == '4':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 4 LIMIT 30,10")
        
    if number_pag == '5':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 4 LIMIT 40,10")
    if number_pag == '6':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 4 LIMIT 50,10")
    if number_pag == '7':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 4 LIMIT 60,10")
    if number_pag == '8':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 4 LIMIT 70,10")
    if number_pag == '9':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 4 LIMIT 80,10")
    if number_pag == '10':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 4 LIMIT 90,10")
    productos = cursor.fetchall()
    conexion.commit()
    return render_template('bebe.html', productos=productos ,dataLogin= dataLoginSesion(),**dict(translations.items())) 

@administrador.route('/medicamento/')
def medicamento():
    translations = {
        'titmed': gettext('Administracion de medicamentos en general'),
        'descmed': gettext('Esta sección permite operar sobre medicamentos de diferentes tipos y/o presentaciones'),
        'menuprodl': gettext('Lista de productos'),
        'menuproda': gettext('Adicionar producto'),
        'adnom': gettext('Nombre'),
        'addes': gettext('Descripcion'),
        'adcant': gettext('Cantidad'),
        'adprec': gettext('Precio'),
        'adprov': gettext('Proveedor'),
        'adfech': gettext('Fecha Vencimiento'),
        'adimg': gettext('Imagen'),
        'btncan': gettext('Cancelar'),
        'btnsav': gettext('Guardar'),
        'tbnomp': gettext('Nombre'),
        'tbcan': gettext('Cantidad disponible'),
        'tbprec': gettext('Precio'),
        'tbfech': gettext('Fecha de Vencimiento'),
        'tbmod': gettext('Modificar'),
        'tbel': gettext('Eliminar'),
        'expl': gettext('Abrir Explorador'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'infogen': gettext('A traves de esta seccion el administrador tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),
        'titedit': gettext('Edicion de datos'),
        'desedit': gettext('Esta sección permite operar sobre los productos'),  
    }  
    productos = controller.producto_medicamento()
    return render_template("medicamento.html", productos=productos,dataLogin= dataLoginSesion(),**dict(translations.items()))

@administrador.route("/medicamentos_pag/<number_pag>")
def medicamentos_pag(number_pag):
    translations = {
        'titmed': gettext('Administracion de medicamentos en general'),
        'descmed': gettext('Esta sección permite operar sobre medicamentos de diferentes tipos y/o presentaciones'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'tbnomp': gettext('Nombre'),
        'tbcan': gettext('Cantidad disponible'),
        'tbprec': gettext('Precio'),
        'tbfech': gettext('Fecha de Vencimiento'),
        'tbmod': gettext('Modificar'),
        'tbel': gettext('Eliminar'),
        'menuprodl': gettext('Lista de productos'),
        'menuproda': gettext('Adicionar producto'),
        'infogen': gettext('A traves de esta seccion el administrador tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),

    }
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    if number_pag == '1':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 5 LIMIT 0,10")
    if number_pag == '2':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 5 LIMIT 10,10")
    if number_pag == '3':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 5 LIMIT 20,10")
    if number_pag == '4':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 5 LIMIT 30,10")
        
    if number_pag == '5':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 5 LIMIT 40,10")
    if number_pag == '6':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 5 LIMIT 50,10")
    if number_pag == '7':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 5 LIMIT 60,10")
    if number_pag == '8':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 5 LIMIT 70,10")
    if number_pag == '9':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 5 LIMIT 80,10")
    if number_pag == '10':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 5 LIMIT 90,10")
    productos = cursor.fetchall()
    conexion.commit()
    return render_template('medicamento.html', productos=productos ,dataLogin= dataLoginSesion(),**dict(translations.items()))


# Gestion de usuarios

@administrador.route('/gestionadmin/')
def gestionadmin():
    usuarios = controller.usuario_admin()
    translations = {
        'titgesadm': gettext('Panel de gestión de administradores'),
        'desgesadm': gettext('En este apartado esta diseñado para visualizar la informacion de los administrados registrados, asi como modificar y eliminar esta información'),
        'menuadm1': gettext('Lista de administradores'),
        'menuadm2': gettext('Adicionar administrador'),
        'adnom': gettext('Nombre'),
        'adape': gettext('Apellido'),
        'addire': gettext('Direccion'),
        'adtele': gettext('Telefono'),
        'adcorreo': gettext('Correo'),
        'adgener': gettext('Genero'),
        'adgenerm': gettext('Masculino'),
        'adgenefr': gettext('Femenino'),
        'adselopc': gettext('Seleccione una opcion'),
        'adimg': gettext('Imagen'),
        'adpass': gettext('Contraseña'),
        'adpass2': gettext('Repetir contraseña'),
        'btncan': gettext('Cancelar'),
        'btnsav': gettext('Guardar'),
        'tbmod': gettext('Modificar'),
        'tbel': gettext('Eliminar'),
        'expl': gettext('Abrir Explorador'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'infogen': gettext('A traves de esta seccion el administrador tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),
        
    } 
    return render_template("gestionadmin.html", usuarios=usuarios,dataLogin= dataLoginSesion(),**dict(translations.items()))

@administrador.route("/gestionadmin_pag/<number_pag>")
def gestionadmin_pag(number_pag):
    translations = {
        'titgesadm': gettext('Panel de gestión de administradores'),
        'desgesadm': gettext('En este apartado esta diseñado para visualizar la informacion de los administrados registrados, asi como modificar y eliminar esta información'),
        'menucl1': gettext('Lista de clientes'),
        'menucl2': gettext('Adicionar cliente'),
        'adnom': gettext('Nombre'),
        'adape': gettext('Apellido'),
        'addire': gettext('Direccion'),
        'adtele': gettext('Telefono'),
        'adcorreo': gettext('Correo'),
        'adgener': gettext('Genero'),
        'adgenerm': gettext('Masculino'),
        'adgenefr': gettext('Femenino'),
        'adselopc': gettext('Seleccione una opcion'),
        'adimg': gettext('Imagen'),
        'adpass': gettext('Contraseña'),
        'adpass2': gettext('Repetir contraseña'),
        'btncan': gettext('Cancelar'),
        'btnsav': gettext('Guardar'),
        'tbmod': gettext('Modificar'),
        'tbel': gettext('Eliminar'),
        'expl': gettext('Abrir Explorador'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'infogen': gettext('A traves de esta seccion el administrador tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),
        
    } 
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    if number_pag == '1':
        cursor.execute("SELECT * FROM usuario where tipo_user = 1 LIMIT 0,10")
    if number_pag == '2':
        cursor.execute("SELECT * FROM usuario where tipo_user = 1 LIMIT 10,10")
    if number_pag == '3':
        cursor.execute("SELECT * FROM usuario where tipo_user = 1 LIMIT 20,10")
    if number_pag == '4':
        cursor.execute("SELECT * FROM usuario where tipo_user = 1 LIMIT 30,10")
        
    if number_pag == '5':
        cursor.execute("SELECT * FROM usuario where tipo_user = 1 LIMIT 40,10")
    if number_pag == '6':
        cursor.execute("SELECT * FROM usuario where tipo_user = 1 LIMIT 50,10")
    if number_pag == '7':
        cursor.execute("SELECT * FROM usuario where tipo_user = 1 LIMIT 60,10")
    if number_pag == '8':
        cursor.execute("SELECT * FROM usuario where tipo_user = 1 LIMIT 70,10")
    if number_pag == '9':
        cursor.execute("SELECT * FROM usuario where tipo_user = 1 LIMIT 80,10")
    if number_pag == '10':
        cursor.execute("SELECT * FROM usuario where tipo_user = 1 LIMIT 90,10")
    usuarios = cursor.fetchall()
    conexion.commit()
    return render_template('gestionadmin.html', usuarios=usuarios ,dataLogin= dataLoginSesion(),**dict(translations.items()))


@administrador.route('/gestioncliente/')
def gestioncliente():
    translations = {
        'titgescl': gettext('Panel de gestión de clientes'),
        'desgescl': gettext('En este apartado esta diseñado para visualizar la informacion de los clientes, asi como modificar y eliminar la informacion almacenada'),
        'adnom': gettext('Nombre'),
        'adape': gettext('Apellido'),
        'addire': gettext('Direccion'),
        'adtele': gettext('Telefono'),
        'adcorreo': gettext('Correo'),
        'adgener': gettext('Genero'),
        'adimg': gettext('Imagen'),
        'tbmod': gettext('Modificar'),
        'tbel': gettext('Eliminar'),
        'expl': gettext('Abrir Explorador'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'infogen': gettext('A traves de esta seccion el administrador tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),
        
    }    
    
    usuarios = controller.usuario_cliente()
    return render_template("gestioncliente.html", usuarios=usuarios,dataLogin= dataLoginSesion(),**dict(translations.items()))

@administrador.route("/gestioncliente_pag/<number_pag>")
def gestioncliente_pag(number_pag):
    translations = {
        'titgescl': gettext('Panel de gestión de clientes'),
        'desgescl': gettext('En este apartado esta diseñado para visualizar la informacion de los clientes, asi como modificar y eliminar la informacion almacenada'),
        'adnom': gettext('Nombre'),
        'adape': gettext('Apellido'),
        'addire': gettext('Direccion'),
        'adtele': gettext('Telefono'),
        'adcorreo': gettext('Correo'),
        'adgener': gettext('Genero'),
        'adimg': gettext('Imagen'),
        'tbmod': gettext('Modificar'),
        'tbel': gettext('Eliminar'),
        'expl': gettext('Abrir Explorador'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'infogen': gettext('A traves de esta seccion el administrador tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),
        
    }  
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    if number_pag == '1':
        cursor.execute("SELECT * FROM usuario where tipo_user = 2 LIMIT 0,10")
    if number_pag == '2':
        cursor.execute("SELECT * FROM usuario where tipo_user = 2 LIMIT 10,10")
    if number_pag == '3':
        cursor.execute("SELECT * FROM usuario where tipo_user = 2 LIMIT 20,10")
    if number_pag == '4':
        cursor.execute("SELECT * FROM usuario where tipo_user = 2 LIMIT 30,10")
        
    if number_pag == '5':
        cursor.execute("SELECT * FROM usuario where tipo_user = 2 LIMIT 40,10")
    if number_pag == '6':
        cursor.execute("SELECT * FROM usuario where tipo_user = 2 LIMIT 50,10")
    if number_pag == '7':
        cursor.execute("SELECT * FROM usuario where tipo_user = 2 LIMIT 60,10")
    if number_pag == '8':
        cursor.execute("SELECT * FROM usuario where tipo_user = 2 LIMIT 70,10")
    if number_pag == '9':
        cursor.execute("SELECT * FROM usuario where tipo_user = 2 LIMIT 80,10")
    if number_pag == '10':
        cursor.execute("SELECT * FROM usuario where tipo_user = 2 LIMIT 90,10")
    usuarios = cursor.fetchall()
    conexion.commit()
    return render_template('gestioncliente.html', usuarios=usuarios ,dataLogin= dataLoginSesion(),**dict(translations.items()))


@administrador.route("/formulario_editar_producto/<int:id_producto>")
def editar_producto(id_producto):
    translations = {
        'titmed': gettext('Administracion de medicamentos en general'),
        'descmed': gettext('Esta sección permite operar sobre medicamentos de diferentes tipos y/o presentaciones'),
        'menuprodl': gettext('Lista de productos'),
        'menuproda': gettext('Adicionar producto'),
        'adnom': gettext('Nombre'),
        'addes': gettext('Descripcion'),
        'adcant': gettext('Cantidad'),
        'adprec': gettext('Precio'),
        'adprov': gettext('Proveedor'),
        'adfech': gettext('Fecha Vencimiento'),
        'adimg': gettext('Imagen'),
        'btncan': gettext('Cancelar'),
        'btnsav': gettext('Guardar'),
        'tbnomp': gettext('Nombre'),
        'tbcan': gettext('Cantidad disponible'),
        'tbprec': gettext('Precio'),
        'tbfech': gettext('Fecha de Vencimiento'),
        'tbmod': gettext('Modificar'),
        'tbel': gettext('Eliminar'),
        'expl': gettext('Abrir Explorador'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'infogen': gettext('A traves de esta seccion el administrador tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),
        'titedit': gettext('Edicion de datos'),
        'desedit': gettext('Esta sección permite operar sobre los productos'),  
    }  
    # Obtener el juego por ID
    productos = controller.obtener_producto_por_id(id_producto)
    return render_template("editar_producto.html", productos=productos,dataLogin= dataLoginSesion(),**dict(translations.items()))


@administrador.route("/formulario_editar_usuario/<int:id>")
def editar_usuario(id):
    translations = {
        'titgesadm': gettext('Panel de gestión de administradores'),
        'desgesadm': gettext('En este apartado esta diseñado para visualizar la informacion de los administrados registrados, asi como modificar y eliminar esta información'),
        'menuprodl': gettext('Lista de productos'),
        'menuproda': gettext('Adicionar producto'),
        'adnom': gettext('Nombre'),
        'adape': gettext('Apellido'),
        'addire': gettext('Direccion'),
        'adtele': gettext('Telefono'),
        'adcorreo': gettext('Correo'),
        'adgener': gettext('Genero'),
        'adgenerm': gettext('Masculino'),
        'adgenefr': gettext('Femenino'),
        'adselopc': gettext('Seleccione una opcion'),
        'adimg': gettext('Imagen'),
        'adpass': gettext('Contraseña'),
        'adpass2': gettext('Repetir contraseña'),
        'btncan': gettext('Cancelar'),
        'btnsav': gettext('Guardar'),
        'tbmod': gettext('Modificar'),
        'tbel': gettext('Eliminar'),
        'expl': gettext('Abrir Explorador'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'infogen': gettext('A traves de esta seccion el administrador tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),
        'titeditusu': gettext('Edicion de datos'),
        'deseditusu': gettext('En este apartado esta diseñado para modificar la informacion almacenada de los usuarios'),        
    } 
    # Obtener el juego por ID
    usuarios = controller.obtener_usuario_por_id(id)
    return render_template("editar_usuario.html", usuarios=usuarios,dataLogin= dataLoginSesion(),**dict(translations.items()))


@administrador.route("/actualizar_producto", methods=["POST"])
def actualizar_producto():
    translations = {
        'usrreg': gettext('Usuarios Registrados'),
        'titadm': gettext('Administradores'),
        'reg': gettext('Registrados'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'infogen': gettext('A traves de esta seccion el administrador tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),

    }
    id_producto = request.form["id_producto"]
    nombre = request.form["nombre"]
    cantidad = request.form["cantidad"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    fecha_vencimiento = request.form["fecha_vencimiento"]
    imagen = request.files["imagen"]
    if imagen and allowed_file(imagen.filename):
        filename = secure_filename(imagen.filename)
        
        imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        imagename = filename    
    controller.actualizar_producto(nombre, descripcion,cantidad ,precio,fecha_vencimiento,imagename,id_producto )
    return render_template("home.html",dataLogin= dataLoginSesion(),**dict(translations.items()))


@administrador.route("/actualizar_usuario", methods=["POST"])
def actualizar_usuario():
    translations = {
        'usrreg': gettext('Usuarios Registrados'),
        'titadm': gettext('Administradores'),
        'reg': gettext('Registrados'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'infogen': gettext('A traves de esta seccion el administrador tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),

    }
    translations = {
        'usrreg': gettext('Usuarios Registrados'),
        'titadm': gettext('Administradores'),
        'reg': gettext('Registrados'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'infogen': gettext('A traves de esta seccion el administrador tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),

    }    
    id = request.form["id"]
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    correo = request.form["correo"]
    direccion = request.form["direccion"]
    telefono = request.form["telefono"]
    genero = request.form["genero"]
    imagen = request.files["imagen"]
        

    if imagen and allowed_file(imagen.filename):
        filename = secure_filename(imagen.filename)
        
        imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        imagename = filename
    controller.actualizar_usuario(nombre, apellido, correo,direccion,telefono,genero,imagename,id)
    return render_template("home.html",dataLogin= dataLoginSesion(),**dict(translations.items()))


@administrador.route("/eliminar_producto", methods=["POST"])
def eliminar_producto():
    translations = {
        'usrreg': gettext('Usuarios Registrados'),
        'titadm': gettext('Administradores'),
        'reg': gettext('Registrados'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'infogen': gettext('A traves de esta seccion el administrador tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),

    }
    controller.eliminar_producto(request.form["id_producto"])
    return render_template("home.html",dataLogin= dataLoginSesion(),**dict(translations.items()))


@administrador.route("/eliminar_usuario", methods=["POST"])
def eliminar_usuario():
    controller.eliminar_usuario(request.form["id"])
    return render_template("home.html",dataLogin= dataLoginSesion())


@administrador.route('/registro_admin', methods=['GET', 'POST'])
def registerUser():
    msg = ''
    conexion = obtener_conexion()
    if request.method == 'POST':
        tipo_user = request.form['tipo_user']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        password = request.form['password']
        repite_password = request.form['repite_password']
        genero = request.form['genero']
        create_at = date.today()
        imagen = request.files['imagen']
        create_at = date.today()
        #current_time = datetime.datetime.now()

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute('SELECT * FROM usuario WHERE correo = %s', (correo,))
        account = cursor.fetchone()
        cursor.close()  # cerrrando conexion SQL

        if account:
            msg = 'Ya existe el Email!'
        elif password != repite_password:
            msg = 'Disculpa, las clave no coinciden!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', correo):
            msg = 'Disculpa, formato de Email incorrecto!'
        elif not correo or not password or not password or not repite_password:
            msg = 'El formulario no debe estar vacio!'
        else:
            # La cuenta no existe y los datos del formulario son válidos,
            password_encriptada = generate_password_hash(
                password, method='sha256')
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            if imagen and allowed_file(imagen.filename):
                filename = secure_filename(imagen.filename)
                
                rut= imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                imagename = str(UPLOAD_FOLDER+'/'+filename)           
            cursor.execute('INSERT INTO usuario (tipo_user, nombre, apellido, correo,direccion,telefono, password,genero, create_at,imagen) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (tipo_user, nombre, apellido, correo, direccion,telefono, password_encriptada, genero, create_at,imagename))
            conexion.commit()
            cursor.close()
            msg = 'Cuenta creada correctamente!'
    
        return render_template('login.html', msjAlert= msg, typeAlert=1)
    return render_template('login.html', dataLogin= dataLoginSesion(), msjAlert = msg, typeAlert=0)



@app.route('/imagen/<int:id>')
def mostrar_imagen(id):
    datalogin=dataLoginSesion
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = "SELECT imagen FROM usuario WHERE id = %s"
    values = (id,)
    cursor.execute(query, datalogin.id,)
    resultado = cursor.fetchone()
    cursor.close()
    if resultado is not None:
        ruta = resultado[0]
        return render_template('base_admin.html', ruta=ruta)
    else:
        return 'La imagen no existe'
    
@administrador.route('/gestionpedido/')
def gestionpedido():
    translations = {
        'titgesp': gettext('Administracion de pedidos'),
        'desges': gettext('A traves de esta seccion se visualiza la informacion de los pedidos realizados por los clientes'),
        'adnomp': gettext('Nombre'),
        'adapep': gettext('Apellido'),
        'addirep': gettext('Direccion'),
        'adtelep': gettext('Telefono'),
        'adcorreop': gettext('Correo'),
        'addirp': gettext('Direccion'),
        'adciudp': gettext('Ciudad'),
        'addeparp': gettext('Departamento'),
        'adpaisp': gettext('Pais'),
        'adestp': gettext('Estado'),
        'tbmod': gettext('Modificar'),
        'tbel': gettext('Eliminar'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'txthelp': gettext('Ayuda'),

        'infogen': gettext('A traves de esta seccion se visualiza la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),
        'titedit': gettext('Edicion de datos'),
        'desedit': gettext('Esta sección permite operar sobre los productos'),
    }
    pedidos = controller.gestion_pedido()
    return render_template("gestionpedido.html", pedidos=pedidos,dataLogin= dataLoginSesion(),**dict(translations.items()))

@administrador.route("/gestionpedido_pag/<number_pag>")
def gestionpedido_pag(number_pag):
    translations = {
        'titgesp': gettext('Administracion de pedidos'),
        'desges': gettext('A traves de esta seccion se visualiza la informacion de los pedidos realizados por los clientes'),
        'adnomp': gettext('Nombre'),
        'adapep': gettext('Apellido'),
        'addirep': gettext('Direccion'),
        'adtelep': gettext('Telefono'),
        'adcorreop': gettext('Correo'),
        'addirp': gettext('Direccion'),
        'adciudp': gettext('Ciudad'),
        'addeparp': gettext('Departamento'),
        'adpaisp': gettext('Pais'),
        'adestp': gettext('Estado'),
        'tbmod': gettext('Modificar'),
        'tbel': gettext('Eliminar'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'txthelp': gettext('Ayuda'),
        'infogen': gettext('A traves de esta seccion se visualiza la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),
        'titedit': gettext('Edicion de datos'),
        'desedit': gettext('Esta sección permite operar sobre los productos'),
    }
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    if number_pag == '1':
        cursor.execute("SELECT * FROM pedido LIMIT 0,10")
    if number_pag == '2':
        cursor.execute("SELECT * FROM pedido LIMIT 10,10")
    if number_pag == '3':
        cursor.execute("SELECT * FROM pedido LIMIT 20,10")
    if number_pag == '4':
        cursor.execute("SELECT * FROM pedido LIMIT 30,10")
        
    if number_pag == '5':
        cursor.execute("SELECT * FROM pedido LIMIT 40,10")
    if number_pag == '6':
        cursor.execute("SELECT * FROM pedido LIMIT 50,10")
    if number_pag == '7':
        cursor.execute("SELECT * FROM pedido LIMIT 60,10")
    if number_pag == '8':
        cursor.execute("SELECT * FROM pedido LIMIT 70,10")
    if number_pag == '9':
        cursor.execute("SELECT * FROM pedido LIMIT 80,10")
    if number_pag == '10':
        cursor.execute("SELECT * FROM pedido LIMIT 90,10")
    pedidos = cursor.fetchall()
    conexion.commit()
    return render_template('gestionpedido.html', pedidos=pedidos ,dataLogin= dataLoginSesion(),**dict(translations.items()))