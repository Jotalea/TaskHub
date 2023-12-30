from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
import sqlite3
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'imagenes'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Función para obtener la conexión a la base de datos
def get_db_connection():
    return sqlite3.connect('tareas.db')

# Ruta principal
@app.route('/', methods=['GET'])
def index():
    archivo = "tareas.db"

    if not os.path.exists(archivo):
        from createdb import createdb as cdb
        cdb("tareas")

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM tareas ORDER BY fecha DESC
        ''')
        tareas_recientes = cursor.fetchall()

    return render_template('index.html', tareas_nuevas=[(item[0], item[1], item[2], item[3], item[4][:-9], item[5]) for item in tareas_recientes])

@app.route('/tarea/<int:id_tarea>')
def tarea_detalle(id_tarea):
    # Obtener detalles de la tarea por ID
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tareas WHERE id = ?', (id_tarea,))
        tarea = cursor.fetchone()

    # Verificar si la tarea existe
    if tarea:
        # Ajustar el orden del usuario y la fecha
        usuario = tarea[2]
        fecha = tarea[4][:-9]

        return render_template('tarea.html', tarea=tarea, usuario=usuario, fecha_formateada=fecha)
    else:
        # Redirigir a la página principal si la tarea no existe
        return redirect(url_for('index'))

@app.route('/reset')
def reset():
    return render_template('reset.html')

@app.route('/post')
def postpage():
    return render_template('post.html')

#https://iplogger.org/es/logger/uuKm4B1uYE8L/
@app.route('/api/logger')
def logger():
    site = """<html><head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><title>IP Logger</title></head><body><a href="https://iplogger.org/es/logger/uuKm4B1uYE8L/">IP Logger</a></body></html>"""
    return site

@app.route('/api/upload', methods=['POST'])
def api_upload():
    if request.method == 'POST':
        materia = request.form['materia']
        respuesta = request.form['respuesta']
        username = request.form['username']

        conn = get_db_connection()
        cursor = conn.cursor()

        # Obtener el último ID de manera más eficiente
        current_id = cursor.execute("SELECT seq FROM sqlite_sequence WHERE name='tareas'").fetchone()[0]

        # Manejar la imagen desde la solicitud POST
        filename = "none.png"
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '' and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], f"{current_id}.{filename.rsplit('.', 1)[1].lower()}"))
            else:
                pass
        cursor.execute('''
          INSERT INTO tareas (materia, respuesta, usuario, imagen_path) VALUES (?, ?, ?, ?)
      ''', (materia, respuesta, username, f"{current_id}.{filename.rsplit('.', 1)[1].lower()}" if 'file' in locals() else None))

        conn.commit()
        conn.close()
        return redirect(url_for('index'))
      
@app.route('/api/reset', methods=['POST', 'GET'])
def resetdata():
    if request.method == 'POST':
        rpass = request.form['password']

        # AUTH
        if rpass == os.environ['PASSWORD']:
            pass
        else:
            return render_template('reset.html', result="Contraseña incorrecta.")
          
        print(f'Contraseña recibida en el servidor: {rpass}')
      
        # Reiniciar la base de datos
        os.remove("tareas.db")
        return render_template('reset.html', result="Base de datos reiniciada.")
    elif request.method == 'GET':
        return render_template('reset.html', result="")

@app.route('/api/delete/<int:id_tarea>', methods=['POST'])
def borrar_tarea(id_tarea):
    contrasena_ingresada = request.form['contrasena']
    print("STAGE 1")

    # Conecta con la base de datos
    conn = get_db_connection()
    cursor = conn.cursor()

    # Verifica la contraseña antes de borrar la tarea
    contrasena_tarea = os.environ['PASSWORD']
    print("STAGE 2")
    
    print(f'Contraseña ingresada: {contrasena_ingresada}')
    print(f'Contraseña tarea: {contrasena_tarea}')

    if contrasena_ingresada == contrasena_tarea:
        print("STAGE 2-1")
    else:
        print("STAGE 2-2")

    if contrasena_tarea:
        print("STAGE 2-3")
    else:
        print("STAGE 2-4")

    if contrasena_tarea == contrasena_ingresada:
        print("STAGE 3")
        cursor.execute('DELETE FROM tareas WHERE id = ?', (int(id_tarea),))
        conn.commit()
        conn.close()
        flash('Tarea borrada con éxito', 'success')
    else:
        print("STAGE 4 - bad")
        flash('Contraseña incorrecta. No se pudo borrar la tarea', 'error')
    
    print("STAGE 5")

    return redirect(url_for('index'))

@app.route('/imagenes/<filename>')
def mostrar_imagen(filename):
    return send_from_directory('imagenes', filename) 

@app.route('/assets/<filename>')
def asset(filename):
    return send_from_directory('assets', filename) 
  
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=81)
