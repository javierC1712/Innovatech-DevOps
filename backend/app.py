from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Permite que el Frontend se conecte al Backend sin bloqueos de seguridad

@app.route('/')
def index():
    return jsonify({
        "status": "ok",
        "message": "¡Backend de InnovaTech en ejecución!",
        "version": "1.0.0"
    })

# Ruta de prueba para verificar que la API responde datos
@app.route('/api/datos')
def get_datos():
    return jsonify({
        "proyecto": "InnovaTech",
        "integrantes": ["Equipo DevOps"],
        "estado": "Conectado exitosamente a AWS ECS"
    })

if __name__ == '__main__':
    # host='0.0.0.0' es OBLIGATORIO para AWS
    # port=5000 es el puerto típico para el backend (verifica si tu Dockerfile usa este mismo)
    app.run(host='0.0.0.0', port=5000, debug=True)