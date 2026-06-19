from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

tareas_db = []

@app.route('/api/tareas', methods=['GET'])
def get_tareas():
    return jsonify(tareas_db), 200

@app.route('/api/tareas', methods=['POST'])
def add_tarea():
    data = request.get_json()
    if not data or 'nombre' not in data or 'descripcion' not in data:
        return jsonify({"error": "Datos inválidos"}), 400
    
    nueva_tarea = {
        "id": len(tareas_db) + 1,
        "nombre": data['nombre'],
        "descripcion": data['descripcion']
    }
    tareas_db.append(nueva_tarea)
    return jsonify({"message": "Guardado", "tarea": nueva_tarea}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)