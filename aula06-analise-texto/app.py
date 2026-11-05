# app.py — Backend do analisador de texto (Azure Language)
# O navegador chama este servidor; só o servidor conhece a chave.

import os

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory

# 1) Lê o arquivo .env e coloca os valores nas variáveis de ambiente
load_dotenv()
ENDPOINT = os.environ.get("LANGUAGE_ENDPOINT")
CHAVE = os.environ.get("LANGUAGE_KEY")

if not ENDPOINT or not CHAVE:
    raise SystemExit("Faltam LANGUAGE_ENDPOINT e LANGUAGE_KEY no arquivo .env")

# 2) Cliente do Azure Language: endpoint + chave (sem az login)
cliente = TextAnalyticsClient(endpoint=ENDPOINT, credential=AzureKeyCredential(CHAVE))

app = Flask(__name__, static_folder="static")

LIMITE = 5000  # o analisador aceita até 5000 caracteres por texto


# 3) Rota da página: entrega o index.html
@app.get("/")
def pagina():
    return send_from_directory("static", "index.html")


# 4) Rota da análise: recebe o texto e devolve JSON estruturado
@app.post("/analisar")
def analisar():
    dados = request.get_json(silent=True) or {}
    texto = (dados.get("texto") or "").strip()

    if not texto:
        return jsonify({"erro": "Digite um texto para analisar."}), 400
    if len(texto) > LIMITE:
        return jsonify({"erro": f"Texto muito longo (máximo {LIMITE} caracteres)."}), 400

    try:
        # 4a) Detecção de idioma
        idioma = cliente.detect_language([texto])[0]
        if idioma.is_error:
            return jsonify({"erro": "Não foi possível detectar o idioma."}), 502
        lingua = idioma.primary_language

        # 4b) Detecção e ocultação de PII (usa o idioma detectado, se conhecido)
        codigo = lingua.iso6391_name if lingua.iso6391_name != "(Unknown)" else None
        pii = cliente.recognize_pii_entities([texto], language=codigo)[0]
        if pii.is_error:
            return jsonify({"erro": "Não foi possível analisar dados pessoais."}), 502

        # 4c) Monta a resposta: cada campo é um dado estruturado
        return jsonify({
            "idioma": {
                "nome": lingua.name,
                "codigo": lingua.iso6391_name,
                "confianca": lingua.confidence_score,
            },
            "texto_redigido": pii.redacted_text,
            "entidades": [
                {
                    "texto": e.text,
                    "tipo": e.category,
                    "confianca": e.confidence_score,
                    "offset": e.offset,
                    "tamanho": e.length,
                }
                for e in pii.entities
            ],
        })
    except Exception:
        # Não devolvemos o erro bruto: ele pode conter detalhes da conexão
        return jsonify({"erro": "Falha ao falar com o Azure Language. Confira o endpoint e a chave no .env."}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
