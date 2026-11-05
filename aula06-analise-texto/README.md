# Aula 06: Análise de Texto (Azure AI Language)

Este projeto demonstra como utilizar o serviço **Azure AI Language** (Text Analytics) para detecção de idioma e reconhecimento/ocultação de informações de identificação pessoal (PII - *Personally Identifiable Information*). 

A aplicação possui um **backend em Flask** seguro (que protege a chave de API no servidor) e um **front-end web interativo** em HTML/CSS/JavaScript.

---

## 📁 Estrutura de Arquivos

| Arquivo / Pasta | Descrição |
| --- | --- |
| `app.py` | Servidor Flask com as rotas web (`/`) e de API (`/analisar`), integrando com o SDK da Azure |
| `static/index.html` | Interface web para digitação de texto, envio da requisição e exibição dos resultados |
| `requirements.txt` | Lista de dependências Python (`flask`, `azure-ai-textanalytics`, `python-dotenv`) |
| `.env.example` | Modelo para criação do arquivo `.env` com as variáveis necessárias |
| `.env` | Arquivo local com suas credenciais do Azure (*não versionado no Git*) |
| `.gitignore` | Configuração para ignorar arquivos sensíveis e temporários (como `.env` e `venv/`) |

---

## 🛠️ O que a aplicação faz

1. **Detecção de Idioma:** Identifica o idioma predominante do texto e a pontuação de confiança (0 a 100%).
2. **Ocultação de PII (Redação):** Substitui automaticamente dados pessoais identificáveis (nomes, telefones, e-mails, endereços, etc.) por asteriscos (`*`).
3. **Extração Estruturada de Entidades:** Lista cada dado pessoal encontrado com sua respectiva categoria, nível de confiança, posição (*offset*) e comprimento no texto.

---

## 🚀 Como Executar o Projeto

### 1. Pré-requisitos

- Python 3.10 ou superior instalado.
- Um recurso do **Azure AI Services** ou **Azure AI Language** criado no [Portal do Azure](https://portal.azure.com/).

### 2. Criar e Ativar o Ambiente Virtual (`venv`)

No terminal, navegue até a pasta `aula06-analise-texto`:

```bash
cd aula06-analise-texto
```

Crie o ambiente virtual (caso ainda não tenha criado):
```bash
python -m venv venv
```

Ative o ambiente virtual:
- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **Windows (Prompt de Comando / CMD):**
  ```cmd
  venv\Scripts\activate.bat
  ```
- **Linux / macOS / Git Bash:**
  ```bash
  source venv/bin/activate
  ```

### 3. Instalar as Dependências

Com o ambiente virtual ativado, instale os pacotes necessários:

```bash
pip install -r requirements.txt
```

### 4. Configurar as Chaves no `.env`

1. Crie uma cópia do arquivo `.env.example` com o nome `.env`:
   - No Windows PowerShell: `Copy-Item .env.example .env`
   - Ou crie manualmente o arquivo `.env` na raiz desta pasta.

2. Abra o arquivo `.env` e preencha com as credenciais do seu recurso no Portal do Azure:
   ```env
   LANGUAGE_ENDPOINT=https://SEU-RECURSO.cognitiveservices.azure.com/
   LANGUAGE_KEY=sua_chave_de_acesso_aqui
   ```

> ⚠️ **Importante:** Você encontra o **Endpoint** e as **Chaves (Keys)** no Portal do Azure na seção **Chaves e Ponto de Extremidade** (*Keys and Endpoint*) do seu recurso.

### 5. Iniciar o Servidor Flask

Execute o arquivo principal:

```bash
python app.py
```

### 6. Acessar a Aplicação

Abra seu navegador e acesse:
👉 **[http://localhost:5000](http://localhost:5000)**

---

## 🧪 Exemplo de Teste

No campo de texto, insira uma frase fictícia com dados pessoais (por exemplo):

```text
Olá, meu nome é Carlos Alberto e meu telefone é (11) 98765-4321. Meu e-mail de contato é carlos.teste@exemplo.com.
```

Clique em **Analisar** para visualizar:
- O idioma detectado (ex: Português / `pt` com ~100% de confiança).
- O texto redigido com as informações sensíveis ocultadas.
- A tabela discriminando cada entidade encontrada (`Person`, `PhoneNumber`, `Email`, etc.).

---

## ⚠️ Boas Práticas e Segurança

- **Apenas Dados Fictícios:** Nunca utilize dados pessoais ou sensíveis reais durante testes de aula ou laboratórios.
- **Segurança da Chave:** Nunca compartilhe sua chave de API (`LANGUAGE_KEY`), não a inclua diretamente no código e jamais envie o arquivo `.env` para repositórios públicos (GitHub/GitLab). O backend foi projetado para ler a chave do `.env` e nunca expô-la ao navegador.

---

## ❓ Se Der Erro

| Mensagem / Sintoma | Causa Mais Comum | O que Fazer |
| --- | --- | --- |
| `Faltam LANGUAGE_ENDPOINT e LANGUAGE_KEY no arquivo .env` | O arquivo `.env` não existe ou as variáveis estão vazias | Copie `.env.example` para `.env` e preencha o endpoint e a chave |
| `Falha ao falar com o Azure Language...` (Erro 500) | Endpoint incorreto, chave inválida ou recurso desativado | Verifique se a URL termina com barra `/` e se a chave copiada do Portal está exata |
| `ModuleNotFoundError: No module named 'flask'` | Dependências não instaladas ou venv inativo | Ative o `venv` e execute `pip install -r requirements.txt` |
| `python não é reconhecido como um comando interno...` | Python não adicionado ao PATH | Tente executar com `py app.py` ou reinstale o Python marcando a opção "Add Python to PATH" |
| Página não carrega (`ERR_CONNECTION_REFUSED`) | Servidor não foi iniciado | Certifique-se de que o comando `python app.py` está rodando no terminal |

