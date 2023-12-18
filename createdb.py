from flask import Flask, request
import os
import sqlite3
from datetime import datetime

app = Flask(__name__)

def createdb(type="tareas", reset=False):
    if reset:
        import shutil
        if os.path.exists(type):
            shutil.rmtree(type)

    conn = sqlite3.connect('tareas.db')
    cursor = conn.cursor()

    if type == "tareas":
        # Crea la carpeta de imágenes si no existe
        if not os.path.exists('imagenes'):
            os.makedirs('imagenes')

        # Crea la tabla si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                materia TEXT,
                respuesta TEXT,
                usuario TEXT,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                imagen_path TEXT
            )
        ''')

        # Manejar la imagen desde la solicitud POST
        if 'file' in request.files:
            imagen = request.files['file']
            if imagen.filename != '':
                # Asegúrate de tener un nombre único para la imagen
                imagen_path = os.path.join('imagenes', f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}.jpg")
                imagen.save(imagen_path)
            else:
                imagen_path = None
        else:
            imagen_path = None

        # Inserta la tarea en la base de datos
        cursor.execute('''
            INSERT INTO tareas (materia, respuesta, usuario, imagen_path) VALUES (?, ?, ?, ?)
        ''', (
            'Sistema',  # Ejemplo de materia
            'Bienvenido',  # Ejemplo de respuesta
            'Sistema',  # Ejemplo de usuario
            imagen_path
        ))

    # Guarda los cambios y cierra la conexión
    conn.commit()
    conn.close()