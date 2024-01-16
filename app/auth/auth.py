from flask import render_template,abort
from . import autenticar
from flask import Flask,request,url_for,redirect

from datetime import date
from datetime import datetime

from bd import *  #Importando conexion BD
from controller import *  #Importando mis Funciones
from flask_babel import Babel, gettext, refresh; refresh()

import re
from werkzeug.security import generate_password_hash, check_password_hash
from flask_app import *
import babel.dates
from flask_mail import Mail
from flask_mail import Mail, Message
from email.utils import parseaddr



# Rutas para login y recuperacion de cuenta
@autenticar.route('/login/')
def login():
    translations = {
        'titlog': gettext('Registra tu cuenta y accede a nuestros servicios'),
        'welcome': gettext('Bienvenido de vuelta!'),
        'descwel': gettext('Para mantenerse conectado con nosotros, inicie sesión con su información personal'),
        'plhnom': gettext('Nombre'),
        'plhape': gettext('Apellido'),
        'plhcorr': gettext('Correo'),
        'plhdir': gettext('Direccion'),
        'plhtel': gettext('Telefono'),
        'plhpass': gettext('Contraseña'),
        'plhpass2': gettext('Repite contraseña'),
        'plhgen': gettext('Seleccione genero'),
        'plhgenm': gettext('Masculino'),
        'plhgenf': gettext('Femenino'),
        'sincu': gettext('Aun no tienes cuenta?'),
        'olvcon': gettext('Olvidaste tu contraseña?'),
        'txtlogin': gettext('Iniciar Sesión'),
        'textreg': gettext('Registrate'),
        'descreg': gettext('Para mantenerse conectado con nosotros, inicie sesión con su información personal'),
        'footdes': gettext('Descubre la comodidad de cuidar tu salud desde casa con FarmaCop'),
        'footnos': gettext('Nosotros'),
        'footqui': gettext('¿Quiénes somos?'),
        'footpreg': gettext('Preguntas Frecuentes'),
        'footpol': gettext('Políticas y Términos de Uso'),
        'footpole': gettext('Políticas de Envíos'),
        'foottrab': gettext('Trabaja con nosotros'),
        'footeni': gettext('Enlaces de interés'),
        'footsuper': gettext('Superintendencia de industria y comercio'),
        'footsuperf': gettext('Superintendencia financiera'),
        'footcped': gettext('Cómo hacer un pedido en TDV'),
        'foottitco': gettext('Contáctenos'),
        'footdir': gettext('Ipiales Nariño, CALLE 234A'),
        'footcorr': gettext('farmacop@farma.com.co'),
        'footnum1': gettext('+ 57 3217655433'),
        'footnum2': gettext(' + 57 3146785432'),
        'footsigred': gettext('Síguenos en nuestras redes sociales'),   
        'footderech': gettext('Todos los derechos reservados')     
       
        }

    return render_template('login.html',**dict(translations.items()))

@autenticar.route('/registro/')
def registro():
    return render_template("registro.html")

@autenticar.route('/recuperar_correo/')
def recuperarc():
    return render_template("cuenta.html")



@autenticar.route('/verificar/')
def verificar():
    return render_template("cuenta2.html")

@autenticar.route('/validar/')
def validar():
    return render_template("cuenta3.html")




#Registrando una cuenta de Usuario
@autenticar.route('/registro-usuario', methods=['GET', 'POST'])
def registerUser():
    
    translations = {
        'titlog': gettext('Registra tu cuenta y accede a nuestros servicios'),
        'welcome': gettext('Bienvenido de vuelta!'),
        'descwel': gettext('Para mantenerse conectado con nosotros, inicie sesión con su información personal'),
        'plhnom': gettext('Nombre'),
        'plhape': gettext('Apellido'),
        'plhcorr': gettext('Correo'),
        'plhdir': gettext('Direccion'),
        'plhtel': gettext('Telefono'),
        'plhpass': gettext('Contraseña'),
        'plhpass2': gettext('Repite contraseña'),
        'plhgen': gettext('Seleccione genero'),
        'plhgenm': gettext('Masculino'),
        'plhgenf': gettext('Femenino'),
        'sincu': gettext('Aun no tienes cuenta?'),
        'olvcon': gettext('Olvidaste tu contraseña?'),
        'txtlogin': gettext('Iniciar Sesión'),
        'textreg': gettext('Registrate'),
        'descreg': gettext('Para mantenerse conectado con nosotros, inicie sesión con su información personal'),
        'footdes': gettext('Descubre la comodidad de cuidar tu salud desde casa con FarmaCop'),
        'footnos': gettext('Nosotros'),
        'footqui': gettext('¿Quiénes somos?'),
        'footpreg': gettext('Preguntas Frecuentes'),
        'footpol': gettext('Políticas y Términos de Uso'),
        'footpole': gettext('Políticas de Envíos'),
        'foottrab': gettext('Trabaja con nosotros'),
        'footeni': gettext('Enlaces de interés'),
        'footsuper': gettext('Superintendencia de industria y comercio'),
        'footsuperf': gettext('Superintendencia financiera'),
        'footcped': gettext('Cómo hacer un pedido en TDV'),
        'foottitco': gettext('Contáctenos'),
        'footdir': gettext('Ipiales Nariño, CALLE 234A'),
        'footcorr': gettext('farmacop@farma.com.co'),
        'footnum1': gettext('+ 57 3217655433'),
        'footnum2': gettext(' + 57 3146785432'),
        'footsigred': gettext('Síguenos en nuestras redes sociales'),   
        'footderech': gettext('Todos los derechos reservados')    
       
        }
    
    msg = ''
    conexion = obtener_conexion()
    if request.method == 'POST':
        tipo_user                   =2
        nombre                      = request.form['nombre']
        apellido                    = request.form['apellido']
        correo                       = request.form['correo']
        direccion                       = request.form['direccion']
        telefono                       = request.form['telefono']
        password                    = request.form['password']
        repite_password             = request.form['repite_password']
        genero                        = request.form['genero']
        create_at                   = date.today()
        #current_time = datetime.datetime.now()
        # Comprobando si ya existe la cuenta de Usuario con respecto al correo
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute('SELECT * FROM usuario WHERE correo = %s', (correo,))
        account = cursor.fetchone()
        cursor.close() #cerrrando conexion SQL
          
        if account:
            msg = 'Ya existe el Email!'
        elif password != repite_password:
            msg = 'Disculpa, las clave no coinciden!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', correo):
            msg = 'Disculpa, formato de Email incorrecto!'
        elif not nombre or not apellido or not correo or not direccion or not telefono or not genero or not password or not repite_password:
            abort(400)
            msg = 'El formulario no debe estar vacio!'
        else:
            # La cuenta no existe y los datos del formulario son válidos,
            password_encriptada = generate_password_hash(password, method='sha256')
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute('INSERT INTO usuario (tipo_user, nombre, apellido, correo,direccion,telefono, password,genero, create_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (tipo_user, nombre, apellido, correo,direccion,telefono, password_encriptada, genero, create_at))
            conexion.commit()
            cursor.close()
            msg = 'Cuenta creada correctamente!'

           
# Envío del correo de bienvenida
        welcome_msg = Message('Bienvenido a nuestra aplicación', sender='tu_correo@example.com', recipients=[correo])
        welcome_msg.body = "¡Gracias por registrarte en nuestra aplicación!"
        html_content = render_template('correo_registro.html', username=nombre)
        welcome_msg.html = html_content

        try:
            mail.send(welcome_msg)
        except Exception as e:
            print(f"Error al enviar el correo de bienvenida: {str(e)}")

        return render_template('login.html', msjAlert='Cuenta creada correctamente y correo de bienvenida enviado.', typeAlert=1)

    return render_template('login.html', msjAlert='Registro de usuario no completado. ' + msg, typeAlert=0)
    
# Cerrar session del usuario
@autenticar.route('/logout')
def logout():
    translations = {
        'titlog': gettext('Registra tu cuenta y accede a nuestros servicios'),
        'welcome': gettext('Bienvenido de vuelta!'),
        'descwel': gettext('Para mantenerse conectado con nosotros, inicie sesión con su información personal'),
        'plhnom': gettext('Nombre'),
        'plhape': gettext('Apellido'),
        'plhcorr': gettext('Correo'),
        'plhdir': gettext('Direccion'),
        'plhtel': gettext('Telefono'),
        'plhpass': gettext('Contraseña'),
        'plhpass2': gettext('Repite contraseña'),
        'plhgen': gettext('Seleccione genero'),
        'plhgenm': gettext('Masculino'),
        'plhgenf': gettext('Femenino'),
        'sincu': gettext('Aun no tienes cuenta?'),
        'olvcon': gettext('Olvidaste tu contraseña?'),
        'txtlogin': gettext('Iniciar Sesión'),
        'textreg': gettext('Registrate'),
        'descreg': gettext('Para mantenerse conectado con nosotros, inicie sesión con su información personal'),
        'footdes': gettext('Descubre la comodidad de cuidar tu salud desde casa con FarmaCop'),
        'footnos': gettext('Nosotros'),
        'footqui': gettext('¿Quiénes somos?'),
        'footpreg': gettext('Preguntas Frecuentes'),
        'footpol': gettext('Políticas y Términos de Uso'),
        'footpole': gettext('Políticas de Envíos'),
        'foottrab': gettext('Trabaja con nosotros'),
        'footeni': gettext('Enlaces de interés'),
        'footsuper': gettext('Superintendencia de industria y comercio'),
        'footsuperf': gettext('Superintendencia financiera'),
        'footcped': gettext('Cómo hacer un pedido en TDV'),
        'foottitco': gettext('Contáctenos'),
        'footdir': gettext('Ipiales Nariño, CALLE 234A'),
        'footcorr': gettext('farmacop@farma.com.co'),
        'footsigred': gettext('Síguenos en nuestras redes sociales'),   
        'footderech': gettext('Todos los derechos reservados')     
       
        }
    msgClose = ''
    # Eliminar datos de sesión, esto cerrará la sesión del usuario
    session.pop('conectado', None)
    session.pop('id', None)
    session.pop('correo', None)
    msgClose ="La sesión fue cerrada correctamente"
    return render_template('./login.html', msjAlert = msgClose, typeAlert=1,**dict(translations.items()))



@autenticar.route('/dashboard', methods=['GET', 'POST'])
def loginUsser():
    conexion = obtener_conexion()
    noOfItems = 0
    translations = {
        'titlog': gettext('Registra tu cuenta y accede a nuestros servicios'),
        'welcome': gettext('Bienvenido de vuelta!'),
        'descwel': gettext('Para mantenerse conectado con nosotros, inicie sesión con su información personal'),
        'plhnom': gettext('Nombre'),
        'plhape': gettext('Apellido'),
        'plhcorr': gettext('Correo'),
        'plhdir': gettext('Direccion'),
        'plhtel': gettext('Telefono'),
        'plhpass': gettext('Contraseña'),
        'plhpass2': gettext('Repite contraseña'),
        'plhgen': gettext('Seleccione genero'),
        'plhgenm': gettext('Masculino'),
        'plhgenf': gettext('Femenino'),
        'sincu': gettext('Aun no tienes cuenta?'),
        'olvcon': gettext('Olvidaste tu contraseña?'),
        'txtlogin': gettext('Iniciar Sesión'),
        'textreg': gettext('Registrate'),
        'descreg': gettext('Para mantenerse conectado con nosotros, inicie sesión con su información personal'),
        'usrreg': gettext('Usuarios Registrados'),
        'titadm': gettext('Administradores'),
        'reg': gettext('Registrados'),
        'titcli': gettext('Clientes'),
        'footdes': gettext('Descubre la comodidad de cuidar tu salud desde casa con FarmaCop'),
        'footnos': gettext('Nosotros'),
        'footqui': gettext('¿Quiénes somos?'),
        'footpreg': gettext('Preguntas Frecuentes'),
        'footpol': gettext('Políticas y Términos de Uso'),
        'footpole': gettext('Políticas de Envíos'),
        'foottrab': gettext('Trabaja con nosotros'),
        'footeni': gettext('Enlaces de interés'),
        'footsuper': gettext('Superintendencia de industria y comercio'),
        'footsuperf': gettext('Superintendencia financiera'),
        'footcped': gettext('Cómo hacer un pedido en TDV'),
        'foottitco': gettext('Contáctenos'),
        'footdir': gettext('Ipiales Nariño, CALLE 234A'),
        'footcorr': gettext('farmacop@farma.com.co'),
        'footnum1': gettext('+ 57 3217655433'),
        'footnum2': gettext(' + 57 3146785432'),
        'footsigred': gettext('Síguenos en nuestras redes sociales'),   
        'footderech': gettext('Todos los derechos reservados'),  
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
        }
 
     
    if 'conectado' in session:
        
        
        
        correo = session['correo']
        cursor = conexion.cursor()
        cursor.execute("SELECT id FROM usuario WHERE correo = %s", (correo,))
        userId = cursor.fetchone()[0]
        cursor.fetchall()
        cursor.execute("SELECT count(id_producto) FROM carrito WHERE id = %s", (userId, ))
        noOfItems = cursor.fetchone()[0]  
    
        if session['tipo_user'] == 1:
            return render_template('./home.html', dataLogin = dataLoginSesion(),**dict(translations.items()))
        else:
            return render_template('./homecliente.html', dataLogin = dataLoginSesion(),noOfItems=noOfItems)
        
    else:
        msg = ''
        if request.method == 'POST' and 'correo' in request.form and 'password' in request.form:
            correo      = str(request.form['correo'])
            password   = str(request.form['password'])
            
            # Comprobando si existe una cuenta
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuario WHERE correo = %s", [correo])
            account = cursor.fetchone()

            if account:
                if check_password_hash(account['password'],password):
                    # Crear datos de sesión, para poder acceder a estos datos en otras rutas 
                    session['conectado']        = True
                    session['id']               = account['id']
                    session['tipo_user']        = account['tipo_user']
                    session['nombre']           = account['nombre']
                    session['apellido']         = account['apellido']
                    session['correo']           = account['correo']
                    session['direccion']        = account['direccion']
                    session['telefono']         = account['telefono']
                    session['genero']           = account['genero']
                    session['create_at']        = account['create_at'],
                    session['imagen']           = account['imagen']

                    msg = "Ha iniciado sesión correctamente."
                    if session['tipo_user'] == 1:
                        render_template('./home.html', msjAlert = msg, typeAlert=1, dataLogin = dataLoginSesion(),noOfItems=noOfItems,**dict(translations.items()))
                    else:
                        return render_template('./homecliente.html', msjAlert = msg, typeAlert=1, dataLogin = dataLoginSesion(),noOfItems=noOfItems) 
                else:
                    msg = 'Datos incorrectos, por favor verfique!'
                    return render_template('login.html', msjAlert = msg, typeAlert=0,**dict(translations.items()))
            else:
                return render_template('login.html', msjAlert = msg, typeAlert=0,**dict(translations.items()))
                
    return render_template('login.html', msjAlert = 'Debe iniciar sesión.', typeAlert=0,**dict(translations.items()))

