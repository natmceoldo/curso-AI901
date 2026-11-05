# Curso AI-901: Inteligência Artificial no Microsoft Azure

Repositório de códigos práticos, exercícios de laboratório e projetos desenvolvidos ao longo do curso **AI-901**. Aqui você encontrará exemplos que vão desde a introdução ao desenvolvimento em Python até a integração com serviços cognitivos avançados da nuvem **Microsoft Azure (Azure AI Foundry e Azure Cognitive Services)**.

---

## 📚 Estrutura do Repositório

O conteúdo está organizado por aulas temáticas. Cada pasta possui seu próprio ambiente, dependências e guia detalhado:

| Módulo / Pasta | Tópicos Principais | Serviços Azure Utilizados | Tecnologias Principais |
| :--- | :--- | :--- | :--- |
| 📁 [**aula03-foundry**](./aula03-foundry/README.md) | Fundamentos de Python (Aula 02), integração com modelos de chat e aplicação web interativa Full-Stack | **Azure AI Foundry** (Projetos & Modelos LLM) | Python, Flask, Flask-CORS, Azure AI Projects SDK, HTML/CSS/JS |
| 📁 [**aula06-analise-texto**](./aula06-analise-texto/README.md) | Processamento de Linguagem Natural (NLP), detecção automática de idioma e redação/ocultação de PII | **Azure AI Language** (Text Analytics) | Python, Flask, Azure AI Text Analytics SDK, python-dotenv |
| 📁 [**aula08-visao-computacional**](./aula08-visao-computacional/README.md) | Visão Computacional multimodal (análise de imagem + texto) e geração de imagens a partir de prompts | **Azure AI Foundry** & **Black Forest Labs** (FLUX) | Python, Azure AI Projects, OpenAI SDK, Requests, Azure Identity |

---

## 🔎 Resumo de Cada Módulo

### 1. [Aula 03 — Microsoft Foundry](./aula03-foundry/README.md)
- **Objetivo:** Estabelecer a base de programação Python e conectar-se aos modelos de linguagem no Azure AI Foundry.
- **Destaques:**
  - Exemplos básicos de Python (`aula02-python/`).
  - Chamadas de chat pelo terminal (`chat.py` e `chat_interativo.py`).
  - Chat Interativo Web completo (`run.py`), com backend modular em Flask e interface web moderna.

### 2. [Aula 06 — Análise de Texto & Proteção de Dados (PII)](./aula06-analise-texto/README.md)
- **Objetivo:** Aplicar técnicas de NLP para analisar documentos textuais e garantir conformidade e privacidade (LGPD).
- **Destaques:**
  - Detecção do idioma e pontuação de confiança.
  - Reconhecimento e mascaramento automático de dados de identificação pessoal (*Personally Identifiable Information*).
  - Backend Flask com rota `/analisar` protegendo a chave de API e interface web em cartões e tabelas.

### 3. [Aula 08 — Visão Computacional & Geração de Imagens](./aula08-visao-computacional/README.md)
- **Objetivo:** Explorar capacidades multimodais (compreensão e geração visual).
- **Destaques:**
  - Script `vision.py`: Envio de imagens locais (ex.: `aero.png`, `131.png`) com perguntas para modelos multimodais como `gpt-5-mini`.
  - Scripts `gerar.py` e `gerar_flux.py`: Geração de ilustrações em alta resolução via modelo `FLUX.2-flex` utilizando o SDK da OpenAI e chamadas REST diretas.

---

## 🛠️ Pré-requisitos Gerais

Para rodar qualquer um dos projetos deste repositório, você precisará de:

1. **Python 3.10 ou superior:** [Download oficial do Python](https://www.python.org/downloads/)
2. **Azure CLI (`az`):** Necessária para autenticação sem chave nos módulos do Foundry. [Instruções de instalação da Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
3. **Conta no Microsoft Azure:** Acesso com permissões para criação de recursos no [Portal do Azure](https://portal.azure.com/) e no [Azure AI Foundry portal](https://ai.azure.com/).
4. **Git:** Para clonar e gerenciar versões do projeto.

---

## 🚀 Como Começar

Cada aula é independente e possui seu próprio arquivo `requirements.txt`. Siga o passo a passo abaixo para executar a aula desejada:

### 1. Clonar o repositório
```bash
git clone <URL_DO_REPOSITORIO>
cd curso-AI901
```

### 2. Escolher e acessar o diretório da aula
Por exemplo, para a Aula 06:
```bash
cd aula06-analise-texto
```

### 3. Criar e ativar o ambiente virtual isolado
- **No Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
- **No Windows (Prompt de Comando - CMD):**
  ```cmd
  python -m venv venv
  venv\Scripts\activate.bat
  ```
- **No Linux ou macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 4. Instalar as dependências da aula
```bash
pip install -r requirements.txt
```

### 5. Autenticação no Azure
Dependendo da aula:
- **Aulas com autenticação RBAC / Token (Aula 03 e Aula 08):**
  ```bash
  az login
  ```
- **Aulas com chave em arquivo `.env` (Aula 06):**
  - Copie o arquivo `.env.example` para `.env`.
  - Insira seu `LANGUAGE_ENDPOINT` e `LANGUAGE_KEY` obtidos no portal Azure.

---

## 🛡️ Segurança e Boas Práticas

- **Credenciais e Segredos:** Nunca envie arquivos `.env`, chaves de API, senhas ou tokens para o GitHub. O repositório já está configurado com um arquivo [`.gitignore`](./.gitignore) para evitar o rastreamento acidental de arquivos sensíveis.
- **Ambientes Virtuais:** Nunca versione pastas `venv/` ou `.venv/`. Sempre gere um novo ambiente virtual em sua máquina local a partir do arquivo `requirements.txt`.
- **Privacidade de Dados:** Nos testes de PII e Visão Computacional, utilize exclusivamente dados e imagens **fictícias** ou de domínio público.

---

## 🤝 Dúvidas e Suporte

Caso encontre dificuldades na execução, consulte a seção **"Se der erro"** presente no `README.md` específico de cada aula.