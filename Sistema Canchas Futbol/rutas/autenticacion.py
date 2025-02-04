from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
from extensiones import obtener_conexion

bcrypt = Bcrypt()

# Crear Blueprint
autenticacion_bp = Blueprint('autenticacion_bp', __name__)

@autenticacion_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        usuario = request.form['usuario']
        email = request.form['email']
        contrasena = request.form['contrasena']

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        if cursor.fetchone():
            flash("El correo electrónico ya está registrado.", "error")
            cursor.close()
            conexion.close()
            return redirect(url_for('autenticacion_bp.registro'))

        hashed_password = bcrypt.generate_password_hash(contrasena).decode('utf-8')

        cursor.execute(
            "INSERT INTO usuarios (usuario, email, contrasena) VALUES (%s, %s, %s)",
            (usuario, email, hashed_password)
        )
        conexion.commit()

        cursor.close()
        conexion.close()

        session['usuario'] = usuario
        flash("Registro exitoso. ¡Bienvenido!", "success")
        return redirect(url_for('pagina_principal'))

    return render_template('register.html')

@autenticacion_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("SELECT * FROM usuarios WHERE usuario = %s", (usuario,))
        user = cursor.fetchone()

        cursor.close()
        conexion.close()

        if user and bcrypt.check_password_hash(user['contrasena'], contrasena):
            session['usuario'] = usuario
            flash("Inicio de sesión exitoso.", "success")
            return redirect(url_for('pagina_principal'))
        else:
            flash("Usuario o contraseña incorrectos.", "error")
            return render_template('login.html')

    return render_template('login.html')

@autenticacion_bp.route('/cambiar_contrasena', methods=['GET', 'POST'])
def cambiar_contrasena():
    if 'usuario' not in session:
        return redirect(url_for('autenticacion_bp.login'))

    if request.method == 'POST':
        contrasena_actual = request.form['contrasena_actual']
        nueva_contrasena = request.form['nueva_contrasena']
        confirmar_contrasena = request.form['confirmar_contrasena']

        if nueva_contrasena != confirmar_contrasena:
            flash("Las contraseñas no coinciden.", "error")
            return redirect(url_for('autenticacion_bp.cambiar_contrasena'))

        usuario = session['usuario']

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("SELECT contrasena FROM usuarios WHERE usuario = %s", (usuario,))
        user = cursor.fetchone()

        if not user or not bcrypt.check_password_hash(user['contrasena'], contrasena_actual):
            flash("La contraseña actual es incorrecta.", "error")
            cursor.close()
            conexion.close()
            return redirect(url_for('autenticacion_bp.cambiar_contrasena'))

        hashed_password = bcrypt.generate_password_hash(nueva_contrasena).decode('utf-8')

        cursor.execute(
            "UPDATE usuarios SET contrasena = %s WHERE usuario = %s",
            (hashed_password, usuario)
        )
        conexion.commit()

        cursor.close()
        conexion.close()

        flash("Tu contraseña ha sido actualizada con éxito.", "success")
        return redirect(url_for('autenticacion_bp.mi_perfil'))

    return render_template('cambiar_contrasena.html')

@autenticacion_bp.route('/logout')
def logout():
    session.pop('usuario', None)
    flash("Sesión cerrada correctamente.", "success")
    return redirect(url_for('autenticacion_bp.login'))

# Clave secreta para las sesiones
#app.secret_key = "advpjsh"