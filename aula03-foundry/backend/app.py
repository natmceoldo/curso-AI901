import os
import sys
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Adiciona o diretório raiz e o diretório backend ao sys.path para garantir imports corretos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

try:
    from backend.config import FOUNDRY_ENDPOINT, FOUNDRY_MODEL, SERVER_HOST, SERVER_PORT
    from backend.foundry_service import foundry_service
except ImportError:
    from config import FOUNDRY_ENDPOINT, FOUNDRY_MODEL, SERVER_HOST, SERVER_PORT
    from foundry_service import foundry_service

app = Flask(__name__, static_folder=FRONTEND_DIR)
CORS(app)  # Permite requisições de outras origens (ex: Live Server)

@app.route("/")
def index():
    """Entrega a página principal do chat."""
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/<path:path>")
def static_files(path):
    """Entrega arquivos estáticos como CSS, JS e imagens da pasta frontend."""
    return send_from_directory(FRONTEND_DIR, path)

@app.route("/api/status", methods=["GET"])
def get_status():
    """Retorna o status do servidor e a configuração ativa do Foundry."""
    return jsonify({
        "status": "online",
        "model": FOUNDRY_MODEL,
        "endpoint": FOUNDRY_ENDPOINT,
        "message": "Servidor backend operacional e conectado às configurações do Foundry."
    })

@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Endpoint principal para receber mensagens do usuário,
    encaminhar ao agente do Microsoft Foundry e devolver a resposta.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "success": False,
            "error": "Corpo da requisição inválido. Esperado JSON com campo 'message'."
        }), 400

    mensagem = data.get("message", "").strip()
    historico = data.get("history", [])

    if not mensagem:
        return jsonify({
            "success": False,
            "error": "A mensagem não pode ser vazia."
        }), 400

    resultado = foundry_service.enviar_mensagem(mensagem, historico)

    if resultado.get("success"):
        return jsonify(resultado), 200
    else:
        # Retorna o erro com status 500 ou 401 caso seja autenticação
        status_code = 401 if "autenticação" in resultado.get("error", "").lower() else 500
        return jsonify(resultado), status_code

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Servidor Backend iniciado com sucesso!")
    print(f"🔗 Acesse o Chat no navegador: http://localhost:{SERVER_PORT}")
    print(f"🤖 Modelo configurado: {FOUNDRY_MODEL}")
    print(f"🌐 Endpoint: {FOUNDRY_ENDPOINT}")
    print("=" * 60)
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=True)

