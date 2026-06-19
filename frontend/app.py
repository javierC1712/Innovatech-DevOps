from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# IP Privada exacta de la tarea actual de tu Backend en AWS ECS Fargate
BACKEND_DNS_INTERNO = "http://172.31.79.3:5000"

@app.route('/')
def index():
    # Sirve la interfaz gráfica principal (index.html con Tailwind CSS)
    try:
        return render_template('index.html')
    except Exception:
        # Por si no tienes configurada la carpeta templates, evita que falle la carga inicial
        return "Frontend de InnovaTech Operativo. Asegúrate de compilar con tus archivos estáticos."

@app.route('/intermedio/tareas', methods=['POST'])
def guardar_tarea_intermedio():
    try:
        # 1. Recibir los datos enviados desde el formulario web (JavaScript / Fetch)
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No se recibieron datos en el Frontend"}), 400
        
        # Extraer los datos originales del formulario web
        requerimiento_web = data.get('requerimiento')
        descripcion_web = data.get('descripcion', '')

        # 2. SOLUCIÓN B: Mapear 'requerimiento' a 'nombre' para cumplir con el Backend
        payload_para_backend = {
            "nombre": requerimiento_web,
            "descripcion": descripcion_web
        }

        # 3. Enviar los datos estructurados al Backend por la red privada de la VPC
        # Se añade un timeout de 5 segundos para evitar que el contenedor quede congelado
        response = requests.post(
            f"{BACKEND_DNS_INTERNO}/api/tareas", 
            json=payload_para_backend,
            timeout=5
        )

        # 4. Retornar la respuesta exitosa del Backend directo a la interfaz web
        return jsonify(response.json()), response.status_code

    except requests.exceptions.ConnectionError:
        # Error controlado si el Security Group bloquea el puerto o la IP privada cambió
        return jsonify({
            "error": "Muro de red detectado: El puente de Python no pudo establecer conexión con la IP privada del Backend. Verifica las reglas del Security Group en el puerto 5000."
        }), 502
    except Exception as e:
        # Cualquier otro error interno de código se captura aquí sin romper el servidor
        return jsonify({"error": f"Error interno en el puente del Frontend: {str(e)}"}), 500

@app.route('/intermedio/tareas', methods=['GET'])
def obtener_tareas_intermedio():
    try:
        # Obtener el listado de requerimientos almacenados en la memoria del Backend
        response = requests.get(f"{BACKEND_DNS_INTERNO}/api/tareas", timeout=5)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": f"No se pudieron cargar los requerimientos del Backend: {str(e)}"}), 502

if __name__ == '__main__':
    # Escucha en todas las interfaces para que AWS ECS lo exponga correctamente a internet
    app.run(host='0.0.0.0', port=5000)