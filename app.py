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
