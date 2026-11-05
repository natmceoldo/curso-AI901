# gerar_flux.py — gera uma imagem com o modelo FLUX.2-pro (API própria da Black Forest Labs)
import base64

import requests
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# 1) Endereço do recurso (termina em .cognitiveservices.azure.com, sem barra no fim)
ENDPOINT = "https://aula-ai901-natalia-ceol-resource.cognitiveservices.azure.com"

# 2) Nome da implantação do modelo, EM LETRAS MINÚSCULAS (ex.: flux.2-pro)
IMPLANTACAO = "flux.2-flex"

# 3) Token pelo az login (sem chave no código)
pegar_token = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

# 4) O caminho do FLUX.2-pro é próprio: não usa /images/generations
url = f"{ENDPOINT}/providers/blackforestlabs/v1/flux-2-flex?api-version=preview"

corpo = {
    "model": IMPLANTACAO,
    "prompt": "Uma banana madura sobre uma mesa de madeira, estilo aquarela",
    "num_images": 1,
    "width": 1024,
    "height": 1024,
    "output_format": "png",
}

resposta = requests.post(
    url,
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {pegar_token()}",
    },
    json=corpo,
    timeout=180,
)

# 5) Se der erro, mostra o motivo que o serviço devolveu
if not resposta.ok:
    raise SystemExit(f"Erro {resposta.status_code}: {resposta.text[:500]}")

# 6) A imagem volta em base64: salvamos em arquivo
dados = resposta.json()

# O formato da resposta não é descrito na documentação: tentamos os mais comuns
if dados.get("data") and "b64_json" in dados["data"][0]:
    imagem_b64 = dados["data"][0]["b64_json"]
elif "image" in dados:
    imagem_b64 = dados["image"]
else:
    raise SystemExit(f"Formato inesperado. Chaves recebidas: {list(dados.keys())}")

with open("imagem_gerada.png", "wb") as f:
    f.write(base64.b64decode(imagem_b64))
print("Imagem salva em imagem_gerada.png")