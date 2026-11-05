# vision.py — envia uma imagem local e uma pergunta ao modelo multimodal
import base64
import mimetypes
import sys

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Project endpoint: https://RECURSO.services.ai.azure.com/api/projects/PROJETO
ENDPOINT = "https://aula-ai901-natalia-ceol-resource.services.ai.azure.com/api/projects/aula-ai901-natalia-ceoldo"

# 1) Lê o caminho da imagem e a pergunta na linha de comando
caminho = sys.argv[1]
pergunta = sys.argv[2] if len(sys.argv) > 2 else "O que você pode me dizer sobre isto?"

# 2) Converte a imagem em base64 (texto) para enviar junto com a pergunta
tipo, _ = mimetypes.guess_type(caminho)
with open(caminho, "rb") as arquivo:
    dados = base64.b64encode(arquivo.read()).decode("utf-8")
imagem_em_base64 = f"data:{tipo or 'image/jpeg'};base64,{dados}"

# 3) Conecta ao projeto (autenticação pelo az login, sem chave no código)
projeto = AIProjectClient(endpoint=ENDPOINT, credential=DefaultAzureCredential())
openai = projeto.get_openai_client()

# 4) Mensagem com dois blocos: texto + imagem
entrada = [{
    "role": "user",
    "content": [
        {"type": "input_text", "text": pergunta},
        {"type": "input_image", "image_url": imagem_em_base64},
    ],
}]

# 5) Chama o modelo e mostra a resposta
resposta = openai.responses.create(model="gpt-5-mini", input=entrada)
print(resposta.output_text)