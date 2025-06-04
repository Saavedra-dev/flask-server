from flask import Flask, request, jsonify, send_from_directory
import os
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Garante que a pasta existe mesmo após reinícios do Render
@app.before_request
def garantir_upload_folder():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

@app.route("/", methods=["GET"])
def index():
    return "Servidor Flask está no ar!"

@app.route("/upload", methods=["POST"])
def upload():
    rfid = request.form.get("rfid")
    photo = request.files.get("photo")

    if not rfid or not photo:
        return jsonify({"error": "Dados incompletos"}), 400

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{rfid}_{timestamp}.jpg"
    caminho_completo = os.path.join(UPLOAD_FOLDER, filename)
    photo.save(caminho_completo)

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

    logs.sort(key=lambda x: x["timestamp"], reverse=True)

    html = "<h1>Registos de Acessos (RFID)</h1><ul>"
    for log in logs:
        nome_img = f"{log['rfid']}_{log['timestamp']}.jpg"
        link_img = f"/uploads/{nome_img}"
        html += f"<li><strong>UID:</strong> {log['rfid']} | <strong>Hora:</strong> {log['timestamp']} | <a href='{link_img}' target='_blank'>📷 Ver imagem</a></li>"
    html += "</ul>"

    return html

@app.route("/uploads/<filename>")
def servir_imagem(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
