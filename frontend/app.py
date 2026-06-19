from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <html>
        <head><title>InnovaTech Frontend</title></head>
        <body style="font-family: Arial, sans-serif; text-align: center; margin-top: 100px;">
            <h1 style="color: #004124;">¡Frontend de InnovaTech en ejecución!</h1>
            <p>El contenedor está vivo y escuchando correctamente.</p>
        </body>
    </html>
    """

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=80, debug=True)