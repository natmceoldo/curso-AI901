# gerar.py — gera uma imagem a partir de um prompt
import base64
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# Azure OpenAI endpoint (termina em /openai/v1/), da página Home do projeto.
# Atenção: é diferente do Project endpoint usado no vision.py
ENDPOINT = "https://aula-ai901-natalia-ceol-resource.services.ai.azure.com/api/projects/aula-ai901-natalia-ceoldo"

# Autenticação pelo az login: gera um token no lugar da chave
token = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)
cliente = OpenAI(base_url=ENDPOINT, api_key=token)

resultado = cliente.images.generate(
    model="FLUX.2-flex",  # nome da implantação do modelo de imagem
    prompt="Uma banana madura sobre uma mesa de madeira, estilo aquarela",
    n=1,
    size="1024x1024",
)

# A imagem volta em base64: salvamos em arquivo
with open("imagem_gerada.png", "wb") as f:
    f.write(base64.b64decode(resultado.data[0].b64_json))
print("Imagem salva em imagem_gerada.png")