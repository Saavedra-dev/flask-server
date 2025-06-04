from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET"])
def index():
    return "Servidor Flask está no ar!"

@app.route("/upload", methods=["POST"])
def upload():
    # Receber RFID
    rfid = request.form.get("rfid")
    
    # Receber imagem
    photo = request.files.get("photo")
    if not rfid or not photo:
        return jsonify({"error": "Dados incompletos"}), 400

    # Salvar imagem com timestamp e rfid
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{UPLOAD_FOLDER}/{rfid}_{timestamp}.jpg"
    photo.save(filename)

    return jsonify({"message": "Recebido com sucesso", "rfid": rfid}), 200

@app.route("/logs", methods=["GET"])
def logs():
    logs = []
    for filename in os.listdir(UPLOAD_FOLDER):
        if filename.endswith(".jpg"):
            parts = filename.replace(".jpg", "").split("_")
            if len(parts) >= 2:
                rfid = parts[0]
                timestamp = "_".join(parts[1:])
                logs.append({"rfid": rfid, "timestamp": timestamp})

    # Ordenar por data (mais recente primeiro)
    logs.sort(key=lambda x: x["timestamp"], reverse=True)

    # Gerar HTML simples
    html = "<h1>Registos de Acessos (RFID)</h1><ul>"
    for log in logs:
        html += f"<li><strong>UID:</strong> {log['rfid']} | <strong>Hora:</strong> {log['timestamp']}</li>"
    html += "</ul>"

    return html
