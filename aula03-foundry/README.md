# Aula 03: Microsoft Foundry (pasta dos alunos)

Esta pasta traz o que você precisa para a **Parte 4 da Aula 03** (primeiro código
com o Foundry), os programas da **Aula 02** (Python) e o **Chat Interativo Completo (Front-end e Back-end)**.

## O que tem aqui

| Arquivo / Pasta | Para quê |
| --- | --- |
| `run.py` | Inicia o servidor backend e o chat interativo web |
| `backend/` | Servidor Flask (`app.py`), serviço do Foundry (`foundry_service.py`) e configurações (`config.py`) |
| `frontend/` | Interface web separada em `index.html`, `style.css` e `script.js` |
| `chat.py` | Primeiro programa que chama o modelo do Foundry via terminal (Aula 03, Parte 4) |
| `chat_interativo.py` | Conversa em loop via terminal |
| `requirements.txt` | Lista dos pacotes necessários (inclui Flask e Flask-CORS) |
| `aula02-python/` | Códigos da Aula 02: `ola.py`, `cadastro_aluno.py`, `calculadora.py`, `tabela.py` |

---

## 🚀 Como rodar o Chat Interativo Web (Front-end + Back-end)

### 1. Pré-requisitos
Certifique-se de que o ambiente virtual está ativo e as dependências instaladas:
```bash
# Ativar o ambiente virtual (se ainda não estiver ativo):
# Windows (CMD):
venv\Scripts\activate
# Windows (PowerShell):
venv\Scripts\Activate.ps1
# Git Bash:
source venv/Scripts/activate

# Instalar dependências:
pip install -r requirements.txt
```

### 2. Autenticação no Azure
Faça login com a conta da aula:
```bash
az login
```

### 3. Iniciar o Servidor
Execute o arquivo inicializador:
```bash
python run.py
```
*(ou `python backend/app.py`)*

### 4. Abrir no Navegador
Abra o navegador no endereço:
👉 **[http://localhost:5000](http://localhost:5000)**

> **Nota:** Caso prefira usar a extensão **Live Server** do VS Code para editar o front-end, basta abrir a pasta `frontend/index.html` com o Live Server (porta 5500). O script já está preparado com CORS para se comunicar automaticamente com o backend na porta 5000.

---

## Passo a passo original (Parte 4 - Terminal)

1. Abra o **VS Code**, depois **File > Open Folder** e escolha esta pasta (`aula03-foundry`).
2. Abra o terminal do VS Code (`Ctrl` + crase).
3. Crie e ative o ambiente virtual.
4. Entre no Azure pelo terminal: `az login`.
5. Abra o `chat.py` e confira o `ENDPOINT` e `MODELO`.
6. Rode:
   ```bash
   python chat.py
   ```

## Se der erro

| Mensagem | O que fazer |
| --- | --- |
| `python não é reconhecido` | Tente `py` (Windows) ou `python3` (Mac e Linux) |
| `az não é reconhecido` | A CLI do Azure não está instalada: avise o professor |
| Erro de autenticação (401) | Rode `az login` de novo, com a mesma conta do portal |
| Implantação não encontrada | O `MODELO` no `backend/config.py` precisa ser igual ao nome da implantação no portal |
| Erro de método ou atributo inexistente | Versão antiga do SDK: `pip install -U azure-ai-projects` |
| `ModuleNotFoundError` | O venv não está ativo ou faltou o `pip install -r requirements.txt` |

## Cuidados

- **Nunca** coloque API key em arquivo, print ou grupo de conversa.
- Não envie esta pasta com a pasta `venv` dentro: ela é pesada e só funciona no seu computador.
