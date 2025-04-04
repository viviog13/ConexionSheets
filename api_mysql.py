from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)
CORS(app) # permite solicitudes desde Google Sheets

# Configuración de la base de datos (usa variables de entorno para seguridad)
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'sunafil'),
    'password': os.getenv('DB_PASSWORD', 'Sunafil2025*'),
    'database': os.getenv('DATABASE', 'SUNAFIL')
}

# Ruta para ejecutar consultas SQL (POST por seguridad)
@app.route('/query', methods=['POST'])
def execute_query():
    try:
        data = request.get_json()
        query = data.get('query')

        if not query:
            return jsonify({"error": "No se proporcionó una consulta SQL"}), 400
        
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({"data" : results})
    except Error as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Error interno del servidor"}), 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)