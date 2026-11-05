"""
Ponto de entrada prático para iniciar o backend e abrir o chat interativo.
Execute com:
    python run.py
"""
import os
import sys

# Garante que o diretório atual está no PATH
diretorio_raiz = os.path.dirname(os.path.abspath(__file__))
if diretorio_raiz not in sys.path:
    sys.path.insert(0, diretorio_raiz)

from backend.app import app
from backend.config import SERVER_HOST, SERVER_PORT, FOUNDRY_MODEL, FOUNDRY_ENDPOINT

if __name__ == "__main__":
    print("=" * 65)
    print("🤖 Chat Interativo - Microsoft Foundry (Azure AI)")
    print("=" * 65)
    print(f"👉 Acesse no navegador: http://localhost:{SERVER_PORT}")
    print(f"📦 Modelo Ativo: {FOUNDRY_MODEL}")
    print(f"🎯 Endpoint: {FOUNDRY_ENDPOINT}")
    print("=" * 65)
    print("Dica: Certifique-se de ter feito 'az login' antes de enviar mensagens.")
    print("Pressione CTRL+C para encerrar o servidor.\n")
    
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=True)

