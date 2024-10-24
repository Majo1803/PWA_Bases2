import os
from flask import Flask, flash, render_template, request, redirect, url_for
from register import register_client
from recarga_monedero import recarga_monedero , descarga_monedero
from promociones import mostrar_promociones
from compras import procesar_compra
# Crear la aplicación de Flask
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '../frontend/templates'))

# Ruta principal de la app
@app.route('/')
def home():
    return render_template('index.html')

# Ruta para el registro de usuarios
@app.route('/registrar_usuario', methods=['GET', 'POST'])
def registrar_usuario():
    if request.method == 'POST':
        result = register_client(request.form)
        if "successfully" in result:
            return redirect(url_for('home', message=result))
        return render_template('registrar_usuario.html', message=result)
    return render_template('registrar_usuario.html')

# Ruta para recarga del monedero
# Ruta para la recarga de monedero
@app.route('/recarga_monedero', methods=['GET', 'POST'])
def recarga():
    print(os.listdir('frontend/templates')) 
    if request.method == 'POST':
        id_usuario = request.form['id_cliente']
        id_monedero = request.form['id_monedero']
        monto = float(request.form['monto'])  # Asegúrate de que sea un número

        # Llamar a la función de recarga
        recarga_monedero(id_usuario, id_monedero, monto)
        
        return redirect(url_for('home'))  # Redirigir a la página principal después de la recarga

    return render_template('recarga_monedero.html')  # Mostrar el formulario de recargarar el formulario de recarga

#Ruta para la descarga del monedero
@app.route('/descargar_monedero', methods=['GET', 'POST'])
def descarga():
    if request.method == 'POST':
        id_usuario = request.form['id_cliente']
        id_monedero = request.form['id_monedero']
        monto = float(request.form['monto'])
        descarga_monedero(id_usuario, id_monedero, monto)
        return redirect(url_for('home'))
    return render_template('descargar_monedero.html')

# Ruta para promocion
@app.route('/promociones')
def promocion():
    promociones = mostrar_promociones()  # Llama a la función que obtiene las promociones
    return render_template('promociones.html', promociones=promociones)  # Pasa las promociones a la plantilla

@app.route('/compras', methods=['GET', 'POST'])
def compras():
    if request.method == 'POST':
        id_cliente = request.form.get('id_cliente')
        id_producto = request.form.get('id_producto')
        cantidad = request.form.get('cantidad')
        id_nodo = request.form.get('id_nodo')

        # Llama a procesar_compra con los datos obtenidos
        procesar_compra(id_cliente, id_producto, cantidad, id_nodo)

        # Redirige o muestra un mensaje
        flash("Compra procesada con éxito.")  # O maneja errores de alguna manera
        return redirect(url_for('compras'))  # Redirige de nuevo a la página de compras

    return render_template('comprar.html')  # Muestra el formulario si es un GET




if __name__ == "__main__":
    app.run(debug=True)
