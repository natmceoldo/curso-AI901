# chat.py
# Aula 03: primeiro consumo de um modelo do Microsoft Foundry com Python

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# 1) Cole aqui o Project endpoint (portal Foundry > Home do projeto)
#    Formato: https://RECURSO.services.ai.azure.com/api/projects/PROJETO
ENDPOINT = "https://aula-ai901-natalia-ceol-resource.services.ai.azure.com/api/projects/aula-ai901-natalia-ceoldo"

# 2) Nome da implantação (deployment) do modelo, como aparece no portal
MODELO = "gpt-5-mini"

# Cria o cliente do projeto. DefaultAzureCredential usa o login do "az login"
project = AIProjectClient(
    endpoint=ENDPOINT,
    credential=DefaultAzureCredential(),
)

# Cliente para chamar os modelos implantados no projeto
openai = project.get_openai_client()

# Envia a pergunta para o modelo
response = openai.responses.create(
    model=MODELO,
    input="Quem foi Ada Lovelace?",
)

# Mostra só o texto da resposta
print(response.output_text)
