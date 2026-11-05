# Aula 08: Visão Computacional e Geração de Imagens (Azure AI Foundry)

Esta pasta contém os códigos práticos para trabalhar com **compreensão visual multimodal** e **geração de imagens** utilizando os recursos do **Azure AI Foundry** e modelos avançados (como GPT multimodal e a família FLUX).

A autenticação é gerenciada via **Azure CLI (`az login`)** utilizando `DefaultAzureCredential`, o que dispensa o uso de chaves fixas expostas no código.

---

## 📁 Estrutura de Arquivos

| Arquivo | Descrição |
| --- | --- |
| `vision.py` | Script de **visão computacional multimodal**: envia uma imagem local e uma pergunta ao modelo (ex.: `gpt-5-mini`) via Azure AI Projects SDK |
| `gerar.py` | Script de **geração de imagem via SDK OpenAI**: consome o modelo de imagem (ex.: `FLUX.2-flex`) usando a interface de compatibilidade do Azure AI |
| `gerar_flux.py` | Script de **geração de imagem via API REST (Black Forest Labs)**: consome diretamente o endpoint do provedor com requisições HTTP autenticadas |
| `131.png` | Imagem de exemplo para testes de reconhecimento visual |
| `aero.png` | Imagem de exemplo para testes de reconhecimento visual |
| `requirements.txt` | Lista de bibliotecas Python necessárias para executar os scripts |
| `.gitignore` | Arquivos e pastas ignorados no versionamento Git |

---

## ⚙️ Pré-requisitos

1. **Python 3.10+** instalado.
2. **Azure CLI (`az`)** instalada no sistema.
3. Acesso a um projeto e recurso de **Azure AI Foundry** com:
   - Um modelo multimodal implantado (ex.: `gpt-5-mini` ou similar).
   - Um modelo de geração de imagem implantado (ex.: `FLUX.2-flex` / `FLUX.2-pro`).

---

## 🚀 Como Preparar o Ambiente

### 1. Navegar até a pasta da aula

Abra o terminal e entre no diretório:

```bash
cd aula08-visao-computacional
```

### 2. Criar e Ativar o Ambiente Virtual (`venv`)

Crie o ambiente virtual:
```bash
python -m venv venv
```

Ative o ambiente:
- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **Windows (CMD):**
  ```cmd
  venv\Scripts\activate.bat
  ```
- **Linux / macOS / Git Bash:**
  ```bash
  source venv/bin/activate
  ```

### 3. Instalar as Dependências

Com o ambiente virtual ativado, instale os pacotes:

```bash
pip install -r requirements.txt
```

### 4. Fazer Login no Azure

Os scripts utilizam a sua sessão da Azure CLI para autenticação segura. Conecte-se com sua conta de estudante/turma:

```bash
az login
```

---

## 💻 Como Executar os Scripts

### 1. Análise de Imagens com Visão Multimodal (`vision.py`)

O script recebe o caminho da imagem e opcionalmente uma pergunta através de argumentos de linha de comando:

```bash
python vision.py <caminho_da_imagem> "[sua pergunta]"
```

**Exemplos com as imagens incluídas:**

```bash
# Pergunta padrão ("O que você pode me dizer sobre isto?")
python vision.py 131.png

# Pergunta personalizada
python vision.py aero.png "Descreva detalhadamente o que você observa nesta imagem."
```

> 💡 **Configuração em `vision.py`:**
> Verifique se as variáveis `ENDPOINT` (Project endpoint do Foundry) e `model` correspondem aos nomes do seu projeto e da sua implantação no portal Azure.

---

### 2. Geração de Imagens via SDK OpenAI (`gerar.py`)

Gera uma imagem a partir de um prompt em linguagem natural utilizando o cliente OpenAI conectado ao Azure:

```bash
python gerar.py
```

- A imagem retornada é decodificada e salva automaticamente na raiz da pasta como **`imagem_gerada.png`**.
- Para alterar o que será desenhado, edite o texto do parâmetro `prompt` dentro do arquivo `gerar.py`.

---

### 3. Geração de Imagens via API FLUX (`gerar_flux.py`)

Gera uma imagem fazendo uma chamada HTTP direta à API da Black Forest Labs hospedada no Azure:

```bash
python gerar_flux.py
```

- A imagem resultante também é salva como **`imagem_gerada.png`**.
- Permite ajustar resolução (`width`, `height`), formato e prompt diretamente no payload da requisição.

---

## 🔧 Ajustando Endpoints e Modelos

Caso você esteja usando outro recurso ou projeto do Azure, abra os arquivos e atualize os seguintes campos:

- Em `vision.py`:
  - `ENDPOINT`: Endpoint do projeto (`https://<RECURSO>.services.ai.azure.com/api/projects/<PROJETO>`)
  - `model`: Nome da implantação do modelo multimodal (ex.: `gpt-5-mini`)
- Em `gerar.py`:
  - `ENDPOINT`: Endpoint do Azure OpenAI / Foundry
  - `model`: Nome da implantação do modelo de imagem (ex.: `FLUX.2-flex`)
- Em `gerar_flux.py`:
  - `ENDPOINT`: Endpoint do Cognitive Services (`https://<RECURSO>.cognitiveservices.azure.com`)
  - `IMPLANTACAO`: Nome da implantação em letras minúsculas (ex.: `flux.2-flex`)

---

## ❓ Se Der Erro

| Mensagem / Erro | Possível Causa | Como Resolver |
| --- | --- | --- |
| `az não é reconhecido...` | Azure CLI não está instalada ou não está no PATH | Instale a Azure CLI e reinicie o terminal |
| `DefaultAzureCredential failed...` / `ClientAuthenticationError` | Sessão expirada ou não autenticado | Execute `az login` novamente no terminal |
| `IndexError: list index out of range` em `vision.py` | Não foi passado o arquivo de imagem como argumento | Execute passando o arquivo: `python vision.py aero.png` |
| `DeploymentNotFound` / Erro 404 | O nome do modelo/implantação está incorreto | Confira o nome exato da implantação no portal do Azure AI Foundry |
| `ModuleNotFoundError: No module named 'azure.ai.projects'` | Dependências não instaladas ou venv inativo | Ative o `venv` e execute `pip install -r requirements.txt` |
| `FileNotFoundError` ao rodar `vision.py` | O arquivo de imagem informado não existe na pasta | Verifique se digitou o nome correto (ex.: `131.png` ou `aero.png`) |

---

## 🛡️ Segurança e Boas Práticas

- **Sem Chaves no Código:** Os scripts usam tokens de curta duração obtidos via `az login` com `DefaultAzureCredential`. Nunca insira chaves de API permanentes no código.
- **Não Versionar o `venv` nem Imagens:** A pasta `venv` e a imagem de saída `imagem_gerada.png` estão no `.gitignore` para manter o repositório limpo e leve.

