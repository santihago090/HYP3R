from flask import Flask, request, session, redirect, url_for, render_template, flash

app = Flask(__name__)
app.secret_key = 'cambia-esto-por-algo-muy-secreto-2026'

# Datos del producto (podes cambiarlos después)
PRODUCTO = "Camiseta Básica"
PRECIO = 12000.0
COLORES = ['Rojo', 'Azul', 'Verde', 'Negro']
TALLES = ['S', 'M', 'L', 'XL']

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        clave = request.form.get('clave')
        
        # Credenciales de prueba (cámbialas por las tuyas)
        if usuario == 'santiago' and clave == '123456':
            session['logueado'] = True
            session['usuario'] = usuario
            flash('¡Bienvenido!', 'exito')
            return redirect(url_for('productos'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    
    return render_template('login.html')

@app.route('/productos', methods=['GET', 'POST'])
def productos():
    if not session.get('logueado'):
        flash('Inicia sesión primero', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        color = request.form.get('color')
        talle = request.form.get('talle')
        
        try:
            cantidad = int(request.form.get('cantidad', 1))
            if cantidad < 1:
                cantidad = 1
        except:
            flash('Cantidad inválida', 'error')
            return redirect(url_for('productos'))
        
        if color not in COLORES or talle not in TALLES:
            flash('Opción no disponible', 'error')
            return redirect(url_for('productos'))
        
        if 'carrito' not in session:
            session['carrito'] = []
        
        item = {
            'titulo': PRODUCTO,
            'color': color,
            'talle': talle,
            'cantidad': cantidad,
            'precio': PRECIO,
            'subtotal': PRECIO * cantidad
        }
        
        session['carrito'].append(item)
        session.modified = True
        flash('Producto agregado al carrito', 'exito')
        return redirect(url_for('carrito'))
    
    return render_template('productos.html', colores=COLORES, talles=TALLES)

@app.route('/carrito')
def carrito():
    if not session.get('logueado'):
        flash('Inicia sesión primero', 'error')
        return redirect(url_for('login'))
    
    items = session.get('carrito', [])
    total = sum(item['subtotal'] for item in items)
    
    return render_template('carrito.html', items=items, total=total)

@app.route('/eliminar/<int:indice>', methods=['POST'])
def eliminar(indice):
    if not session.get('logueado'):
        return redirect(url_for('login'))
    
    carrito = session.get('carrito', [])
    if 0 <= indice < len(carrito):
        del carrito[indice]
        session['carrito'] = carrito
        session.modified = True
        flash('Producto eliminado', 'exito')
    
    return redirect(url_for('carrito'))

@app.route('/pagar', methods=['POST'])
def pagar():
    if not session.get('logueado'):
        flash('Inicia sesión primero', 'error')
        return redirect(url_for('login'))
    
    if not session.get('carrito'):
        flash('El carrito está vacío', 'error')
        return redirect(url_for('carrito'))
    
    # Simulación de pago (cuando tengas Mercado Pago, reemplaza esta parte)
    session['carrito'] = []
    session.modified = True
    flash('Pago simulado exitoso (pronto con Mercado Pago real)', 'exito')
    return redirect(url_for('exito'))

@app.route('/exito')
def exito():
    if not session.get('logueado'):
        return redirect(url_for('login'))
    return render_template('exito.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada', 'exito')
    return redirect(url_for('login'))

if __name__ == '__main__':
   app.run(debug=True)