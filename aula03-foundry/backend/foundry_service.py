import logging
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.core.exceptions import ClientAuthenticationError

try:
    from backend.config import FOUNDRY_ENDPOINT, FOUNDRY_MODEL
except ImportError:
    from config import FOUNDRY_ENDPOINT, FOUNDRY_MODEL

logger = logging.getLogger(__name__)

class FoundryService:
    def __init__(self, endpoint: str = FOUNDRY_ENDPOINT, model: str = FOUNDRY_MODEL):
        self.endpoint = endpoint
        self.model = model
        self._project_client = None
        self._openai_client = None

    def _obter_cliente_openai(self):
        """Inicializa ou reaproveita o cliente OpenAI do projeto no Foundry."""
        if self._openai_client is None:
            logger.info(f"Conectando ao Foundry Endpoint: {self.endpoint}")
            self._project_client = AIProjectClient(
                endpoint=self.endpoint,
                credential=DefaultAzureCredential(),
            )
            self._openai_client = self._project_client.get_openai_client()
        return self._openai_client

    def _formatar_prompt(self, mensagem: str, historico: list = None) -> str:
        """
        Formata o histórico recente junto à nova mensagem
        para manter o contexto conversacional.
        """
        if not historico:
            return mensagem

        linhas = [
            "Você é um assistente prestativo e amigável da Microsoft Foundry.",
            "Considere o histórico da conversa abaixo para responder:\n"
        ]

        # Considera os últimos 6 turnos para economizar tokens mantendo o contexto
        turnos_recentes = historico[-6:]
        for item in turnos_recentes:
            papel = "Usuário" if item.get("role") == "user" else "Assistente"
            conteudo = item.get("content", "").strip()
            if conteudo:
                linhas.append(f"{papel}: {conteudo}")

        linhas.append(f"Usuário: {mensagem}")
        linhas.append("Assistente:")
        return "\n".join(linhas)

    def enviar_mensagem(self, mensagem: str, historico: list = None) -> dict:
        """
        Envia a mensagem para o modelo do Microsoft Foundry e retorna a resposta.
        """
        if not mensagem or not mensagem.strip():
            return {
                "success": False,
                "error": "A mensagem enviada está vazia."
            }

        try:
            cliente = self._obter_cliente_openai()
            prompt = self._formatar_prompt(mensagem.strip(), historico)

            # Utiliza a API de responses configurada no Foundry (conforme chat_interativo.py)
            resposta = cliente.responses.create(
                model=self.model,
                input=prompt,
            )

            texto_resposta = getattr(resposta, "output_text", None)
            if texto_resposta is None:
                # Caso a estrutura da resposta varie em diferentes versões
                texto_resposta = str(resposta)

            return {
                "success": True,
                "reply": texto_resposta,
                "model": self.model
            }

        except ClientAuthenticationError as auth_err:
            logger.error(f"Erro de autenticação Azure: {auth_err}")
            return {
                "success": False,
                "error": (
                    "Erro de autenticação no Azure. "
                    "Abra o terminal e execute 'az login' com as credenciais da sua aula "
                    "antes de iniciar o servidor."
                ),
                "details": str(auth_err)
            }
        except Exception as e:
            logger.error(f"Erro ao consultar Microsoft Foundry: {e}")
            return {
                "success": False,
                "error": f"Falha na comunicação com o Microsoft Foundry: {str(e)}",
                "details": str(e)
            }

# Instância singleton para uso nas rotas
foundry_service = FoundryService()

