from flask import *
from . import carro
import hashlib, os
from werkzeug.utils import secure_filename
from bd import *  # Importando conexion BD
from reportlab.pdfgen import canvas
from flask_mail import Mail, Message
from flask import current_app
from flask import Flask, render_template, request, redirect, url_for, session, abort
from . import carro
from bd import obtener_conexion
from flask import Flask, render_template, request, current_app

from flask import current_app, render_template, request, redirect, url_for, session
from reportlab.lib.pagesizes import letter
import os


def enviar_correo_factura(detalle_compra, total, correo_destino):
    app = current_app._get_current_object()

    # Generar el PDF
    factura_pdf = generar_factura_pdf(detalle_compra, total)

    # Configuración del correo
    msg = Message('Factura de Compra', sender='tu_correo@example.com', recipients=[correo_destino])
    msg.body = "Gracias por tu compra. Adjunto encontrarás la factura."

    # Adjuntar el PDF
    with app.open_resource(factura_pdf) as pdf_file:
        msg.attach(factura_pdf, 'application/pdf', pdf_file.read())

    # Enviar el correo
    mail = Mail(app)
    mail.send(msg)

    # Eliminar el archivo PDF después de enviarlo
    os.remove(factura_pdf)

@carro.route("/agregar")
def agregar():
    conexion = obtener_conexion()
    if 'correo' not in session:
        return redirect(url_for('autenticar.login'))
    else:
        
        productId = int(request.args.get('productId'))
        with conexion.cursor() as cursor:
            
            cursor.execute("SELECT id FROM usuario WHERE correo = %s", (session['correo'], ))
            usuario = cursor.fetchone()[0]
            cursor.fetchall()
            # Buscar si el producto ya está en el carrito del usuario
            cursor.execute("SELECT cantidad FROM carrito WHERE id = %s AND id_producto = %s", (usuario, productId))
            result = cursor.fetchone()
            if result:
                # Si el producto ya está en el carrito, aumentar la cantidad en 1
                cantidad = result[0] + 1
                cursor.fetchall()
                cursor.execute("UPDATE carrito SET cantidad = %s WHERE id = %s AND id_producto = %s", (cantidad, usuario, productId))
            else:
                # Si el producto no está en el carrito, agregarlo con cantidad 1
                cursor.fetchall()
                cursor.execute("INSERT INTO carrito (id, id_producto, cantidad) VALUES (%s, %s, %s)", (usuario, productId, 1))
            conexion.commit() 
            msg = "Added successfully"
            # Reducir el stock del producto en la base de datos
            cursor.execute('''UPDATE producto SET cantidad = cantidad - 1 WHERE id_producto = %s''', (productId,))                
            conexion.commit()         
            
    conexion.close()
    return redirect(url_for('cliente.homecliente'))
    
@carro.route("/carrito")
def carrito():
    conexion = obtener_conexion()
    noOfItems = 0
    conexion = obtener_conexion()
    correo = session['correo']
    cursor = conexion.cursor()
    cursor.execute("SELECT id FROM usuario WHERE correo = %s", (correo,))
    userId = cursor.fetchone()[0]
    cursor.fetchall()
    cursor.execute("SELECT count(id_producto) FROM carrito WHERE id = %s", (userId, ))
    noOfItems = cursor.fetchone()[0]    
    if 'correo' not in session:
        return redirect(url_for('autenticar.login'))
   # loggedIn, firstName, noOfItems = getLoginDetails()
    correo = session['correo']
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id FROM usuario WHERE correo = %s", (correo, ))
        usuario = cursor.fetchone()[0]
        cursor.fetchall()
        cursor.execute("SELECT carrito.id, producto.id_producto, producto.nombre, producto.precio, producto.imagen, carrito.cantidad FROM producto, carrito WHERE producto.id_producto = carrito.id_producto AND carrito.id = %s", (usuario, ))
        
        productos = cursor.fetchall()
        
    totalPrice = 0
    for row in productos:
        totalPrice += row[3] * row[5]
    return render_template("cart.html", productos = productos, totalPrice=totalPrice, noOfItems=noOfItems)



@carro.route("/eliminar")
def eliminar():
    conexion = obtener_conexion()
    if 'correo' not in session:
        return redirect(url_for('autenticar.login'))
    correo = session['correo']
    productId = int(request.args.get('productId'))
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id FROM usuario WHERE correo = %s", (correo, ))
        id = cursor.fetchone()[0]
        cursor.fetchall()
        try:
            # Buscar si el producto ya está en el carrito del usuario
            cursor.execute("SELECT cantidad FROM carrito WHERE id = %s AND id_producto = %s AND cantidad > 0", (id, productId))
            result = cursor.fetchone()
            if result:
                            
                cursor.execute("UPDATE carrito SET cantidad = cantidad - 1 WHERE id = %s AND id_producto = %s AND cantidad > 0", (id, productId))
                cursor.fetchall()
                conexion.commit()
                cursor.execute('''UPDATE producto SET cantidad = cantidad + 1 WHERE id_producto = %s''', (productId,))  
                cursor.fetchall()
                conexion.commit()
            else:
                 cursor.execute("DELETE FROM carrito WHERE id = %s AND id_producto = %s", (id, productId))
                 conexion.commit()

        except:
            conexion.rollback()
            msg = "error occured"
    conexion.close()
    return redirect(url_for('cliente.homecliente'))

@carro.route("/checkout")
def checkout():
    id = request.args.get('id')
    return render_template("checkout.html",id=id)


@carro.route('/pasarelacompra', methods=['POST'])
def pasarelacompra():
    # Obtener datos del formulario
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    correo = request.form.get('correo')
    telefono = request.form.get('telefono')
    direccion = request.form.get('direccion')
    departamento = request.form.get('departamento')
    ciudad = request.form.get('ciudad')
    pais = request.form.get('pais')
    id_user = session.get('id')  # Obtener el ID de usuario de la sesión

    # Realizar la inserción en la base de datos
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        query = "INSERT INTO pedido (nombre, apellido, telefono, correo, direccion, ciudad, departamento, pais, estado, id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (nombre, apellido, telefono, correo, direccion, ciudad, departamento, pais, 'Pendiente', id_user)
        cursor.execute(query, values)
        conexion.commit()

    # Obtener detalles de la compra
    detalle_compra = obtener_detalles_compra(id_user)
    total_compra = calcular_total_compra(detalle_compra)

    # Enviar correo electrónico con la factura adjunta
    enviar_correo_factura(detalle_compra, total_compra, correo)

    return render_template('checkout.html', id_user=id_user)

def generar_factura_pdf(detalle_compra, total):
    filename = "factura.pdf"
    document_title = "Factura de Compra"
    
    # Crear el documento PDF
    c = canvas.Canvas(filename, pagesize=letter)
    c.setTitle(document_title)
    
    # Agregar contenido al PDF
    c.drawString(100, 750, "Factura de Compra")
    c.drawString(100, 730, f"Total: ${total}")
    c.drawString(100, 710, "Detalles de la Compra:")
    
    y_position = 690
    for producto in detalle_compra:
        # Verificar si 'producto' es una tupla antes de tratar de acceder a sus elementos
        if isinstance(producto, tuple):
            producto = dict(zip(['nombre', 'descripcion', 'cantidad', 'precio', 'proveedor', 'fecha_vencimiento', 'imagen', 'categoria'], producto))
            
        c.drawString(120, y_position, f"{producto['nombre']}: ${producto['precio']} x {producto['cantidad']}")
        y_position -= 15
    
    # Guardar el PDF
    c.save()
    return filename


def obtener_detalles_compra(usuario):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT producto.nombre, producto.precio, carrito.cantidad
            FROM producto
            INNER JOIN carrito ON producto.id_producto = carrito.id_producto
            WHERE carrito.id = %s
        """, (usuario,))
        detalle_compra = cursor.fetchall()
    
    # Convertir los resultados a un formato consistente (diccionarios)
    detalle_compra_format = [
        {'nombre': row[0], 'precio': row[1], 'cantidad': row[2]}
        for row in detalle_compra
    ]

    conexion.close()
    return detalle_compra_format        

def calcular_total_compra(detalle_compra):
    total = sum(producto[3] * producto[5] if len(producto) > 5 else 0 for producto in detalle_compra)

    return total


def enviar_correo_factura(detalle_compra, total_compra, correo_destino):
    app = current_app._get_current_object()

    # Generar el PDF
    factura_pdf = generar_factura_pdf(detalle_compra, total_compra)

    # Configuración del correo
    msg = Message('Factura de Compra', sender='tu_correo@example.com', recipients=[correo_destino])
    msg.body = "Gracias por tu compra. Adjunto encontrarás la factura."

    # Adjuntar el PDF
    with app.open_resource(factura_pdf) as pdf_file:
        msg.attach(factura_pdf, 'application/pdf', pdf_file.read())

    # Enviar el correo
    mail = Mail(app)
    mail.send(msg)

    # Eliminar el archivo PDF después de enviarlo
    os.remove(factura_pdf)