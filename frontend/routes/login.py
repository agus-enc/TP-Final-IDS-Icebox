from flask import Blueprint, render_template, redirect, url_for, session, flash, request

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Validación provisoria local
        if username == 'fiuba' and password == 'ids':
            
            session.permanent = True
            
            session['usuario_id'] = 100
            flash('Sesión iniciada correctamente', 'success')
            return redirect(url_for('imanes.mostrar_heladera'))
        else:
            flash('Credenciales inválidas.', 'error')

    return render_template('login.html')

@login_bp.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada.', 'success')
    return redirect(url_for('login.login'))