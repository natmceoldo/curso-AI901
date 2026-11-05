import os

# Configurações do Microsoft Foundry (Azure AI Foundry)
# Pode ser configurado via variáveis de ambiente ou usar os padrões abaixo

# 1) Endpoint do projeto no Microsoft Foundry
FOUNDRY_ENDPOINT = os.getenv(
    "FOUNDRY_ENDPOINT",
    "https://aula-ai901-natalia-ceol-resource.services.ai.azure.com/api/projects/aula-ai901-natalia-ceoldo"
)

# 2) Nome da implantação (deployment) do modelo no portal
FOUNDRY_MODEL = os.getenv(
    "FOUNDRY_MODEL",
    "gpt-5-mini"
)

# 3) Porta e Host do servidor backend
SERVER_HOST = os.getenv("SERVER_HOST", "127.0.0.1")
SERVER_PORT = int(os.getenv("SERVER_PORT", "5000"))

