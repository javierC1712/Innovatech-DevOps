import requests
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

BACKEND_DNS_INTERNO = "http://172.31.79.3:5000"

@app.route('/')
def home():
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>InnovaTech - Panel DevOps</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-900 text-slate-100 font-sans min-h-screen flex flex-col items-center justify-center p-4">
        
        <div class="bg-slate-800 p-8 rounded-2xl shadow-2xl border border-slate-700 w-full max-w-md">
            <header class="text-center mb-8">
                <span class="bg-green-500/10 text-green-400 text-xs font-semibold px-3 py-1 rounded-full border border-green-500/20">🔒 Red Interna AWS VPC Activa</span>
                <h1 class="text-2xl font-bold mt-3 text-white">InnovaTech Chile</h1>
                <p class="text-sm text-slate-400 mt-1">Demostración de DNS Interno en ECS</p>
            </header>
            
            <form id="taskForm" class="space-y-4">
                <div>
                    <label class="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">Requerimiento</label>
                    <input type="text" id="taskName" required placeholder="Ej: Validar políticas IAM" 
                           class="w-full bg-slate-950 border border-slate-700 rounded-lg px-4 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500 transition">
                </div>
                <div>
                    <label class="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">Descripción</label>
                    <textarea id="taskDesc" required placeholder="Detalles..." rows="2"
                              class="w-full bg-slate-950 border border-slate-700 rounded-lg px-4 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500 transition resize-none"></textarea>
                </div>
                <button type="submit" class="w-full bg-blue-600 hover:bg-blue-500 text-white text-sm font-semibold py-3 px-4 rounded-lg transition">
                    Enviar mediante DNS Interno
                </button>
            </form>

            <div id="statusMessage" class="mt-4 text-center text-xs font-medium py-2 rounded-lg hidden"></div>

            <div class="mt-6 pt-6 border-t border-slate-700">
                <div class="flex items-center justify-between mb-4">
                    <h2 class="text-sm font-bold text-white uppercase tracking-wider">📋 Datos desde el Backend</h2>
                    <button id="btnReload" class="text-xs text-blue-400 hover:text-blue-300 font-medium transition">🔄 Sincronizar</button>
                </div>
                <ul id="taskList" class="space-y-2.5 max-h-48 overflow-y-auto">
                    <li class="text-xs text-slate-500 italic text-center py-4">Cargando datos del cluster...</li>
                </ul>
            </div>
        </div>

        <script>
            // El navegador web ahora le habla a las rutas locales del PROPIO Frontend
            const form = document.getElementById('taskForm');
            const statusMsg = document.getElementById('statusMessage');
            const taskList = document.getElementById('taskList');
            const btnReload = document.getElementById('btnReload');

            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                const nombre = document.getElementById('taskName').value;
                const descripcion = document.getElementById('taskDesc').value;

                try {
                    const response = await fetch('/intermedio/tareas', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ nombre, descripcion })
                    });
                    if (response.ok) {
                        statusMsg.innerText = "¡Enviado al Frontend y procesado por DNS Interno!";
                        statusMsg.className = "mt-4 text-center text-xs font-medium py-2 rounded-lg bg-green-500/10 text-green-400 border border-green-500/20 block";
                        form.reset();
                        fetchTasks();
                    } else { throw new Error(); }
                } catch (err) {
                    statusMsg.innerText = "Error en la ruta puente.";
                    statusMsg.className = "mt-4 text-center text-xs font-medium py-2 rounded-lg bg-red-500/10 text-red-400 border border-red-500/20 block";
                }
            });

            async function fetchTasks() {
                try {
                    const response = await fetch('/intermedio/tareas');
                    const tareas = await response.json();
                    taskList.innerHTML = '';
                    if (tareas.length === 0) {
                        taskList.innerHTML = '<li class="text-xs text-slate-500 italic text-center py-4">Sin datos en la memoria del Backend.</li>';
                        return;
                    }
                    tareas.forEach(t => {
                        const li = document.createElement('li');
                        li.className = "bg-slate-950/50 border border-slate-800 p-3 rounded-xl text-xs";
                        li.innerHTML = `<div class="font-bold text-blue-400">#${t.id} - ${t.nombre}</div><div class="text-slate-300">${t.descripcion}</div>`;
                        taskList.appendChild(li);
                    });
                } catch (err) {
                    taskList.innerHTML = '<li class="text-xs text-red-400 text-center py-4">⚠️ El puente de Python no pudo resolver el DNS interno del Backend.</li>';
                }
            }

            btnReload.addEventListener('click', fetchTasks);
            fetchTasks();
        </script>
    </body>
    </html>
    """
    return render_template_string(html_content)

# === RUTAS PUENTE (PROXY) QUE OPERAN DENTRO DE LA VPC DE AWS ===

@app.route('/intermedio/tareas', methods=['GET'])
def proxy_get_tareas():
    try:
        # Python resuelve el DNS privado directamente en la red interna de AWS
        respuesta = requests.get(f"{BACKEND_DNS_INTERNO}/api/tareas", timeout=5)
        return jsonify(respuesta.json()), respuesta.status_code
    except Exception as e:
        return jsonify({"error": f"No se pudo conectar al Backend por DNS interno: {str(e)}"}), 500

@app.route('/intermedio/tareas', methods=['POST'])
def proxy_post_tareas():
    try:
        # Envía el JSON recibido del navegador hacia el contenedor backend por la red privada
        respuesta = requests.post(f"{BACKEND_DNS_INTERNO}/api/tareas", json=request.get_json(), timeout=5)
        return jsonify(respuesta.json()), respuesta.status_code
    except Exception as e:
        return jsonify({"error": f"Error al enviar datos por red privada: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)