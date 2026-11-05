# chat_interativo.py  (extra: junta a Aula 02 com a Aula 03)
# Usa while, input, funções e try/except para conversar com o modelo.
# Cada pergunta é independente: o modelo não lembra das anteriores.

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

ENDPOINT = "https://aula-ai901-natalia-ceol-resource.services.ai.azure.com/api/projects/aula-ai901-natalia-ceoldo"   # Project endpoint da página Home
MODELO = "gpt-5-mini"               # nome da sua implantação


def criar_cliente():
    """Conecta ao projeto e devolve o cliente para chamar o modelo."""
    project = AIProjectClient(
        endpoint=ENDPOINT,
        credential=DefaultAzureCredential(),
    )
    return project.get_openai_client()


def perguntar(cliente, texto):
    """Envia a pergunta e devolve a resposta (ou None se der erro)."""
    try:
        resposta = cliente.responses.create(model=MODELO, input=texto)
        return resposta.output_text
    except Exception as erro:       # aqui um except geral é aceitável: só mostramos o erro
        print(f"Não foi possível obter a resposta: {erro}")
        return None


cliente = criar_cliente()

while True:
    pergunta = input("Você (ou 'sair'): ")
    if pergunta.lower() == "sair":
        break
    if not pergunta.strip():
        continue                    # ignora pergunta vazia

    texto = perguntar(cliente, pergunta)
    if texto is not None:
        print(f"Modelo: {texto}\n")

print("Até logo!")
