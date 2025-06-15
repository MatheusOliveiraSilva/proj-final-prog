# 🤖 Chat com Documentos - Sistema Inteligente de IA

## 📖 Sobre o Projeto

Este é um **sistema avançado de inteligência artificial** que permite fazer **perguntas em linguagem natural** sobre documentos carregados, usando tecnologias de ponta como OpenAI, Pinecone, LangChain e LangGraph.

### 🎯 O que o Sistema Faz

- 📄 **Upload de Documentos**: Carregue PDFs, Word, Excel, PowerPoint e arquivos de texto
- 🧠 **Processamento Inteligente**: Extrai e analisa automaticamente o conteúdo dos documentos
- 💬 **Chat Natural**: Converse com seus documentos como se fosse uma pessoa especialista
- 🔍 **Busca Semântica**: Encontra informações relevantes mesmo quando você não usa as palavras exatas
- 🎭 **Múltiplas Conversas**: Cada conversa mantém seu próprio contexto e documentos

### Demonstração

(vou por video aqui)

---

## 🏗️ Arquitetura do Sistema

### 📁 Organização do Código

```
proj-final-prog/
├── backend/                    # 🔧 Servidor Python (API + IA)
│   ├── api/                   # 🌐 Endpoints da API REST
│   │   ├── routers/           # 📍 Rotas organizadas por funcionalidade
│   │   │   ├── agent.py       # 🤖 Chat com IA
│   │   │   └── documents.py   # 📄 Upload e busca de documentos
│   │   └── schemas/           # 📋 Estruturas de dados da API
│   ├── agent/                 # 🧠 Sistema de IA (LangGraph)
│   │   ├── graph.py           # 🕸️ Orquestração do agente
│   │   ├── nodes.py           # ⚙️ Lógica de processamento
│   │   └── agent_toolbox/     # 🔨 Ferramentas do agente
│   │       └── tools/         # 🛠️ Busca em documentos
│   ├── vector_store/          # 🗄️ Integração com Pinecone
│   ├── utils/                 # 🔧 Utilitários
│   │   ├── embeddings.py      # 🧮 Geração de embeddings (OpenAI)
│   │   ├── text_chunking.py   # ✂️ Divisão inteligente de texto
│   │   └── file_processing.py # 📁 Processamento de arquivos
│   └── settings.py            # ⚙️ Configurações
├── frontend/                   # 🎨 Interface do usuário (React/TypeScript)
└── pyproject.toml             # 📦 Dependências e configurações
```

### 🔄 Como o Sistema Funciona

1. **📤 Upload de Documento**:
   - Usuário faz upload de um arquivo (PDF, Word, etc.)
   - Sistema detecta automaticamente o tipo e extrai o conteúdo
   - Texto é dividido em chunks inteligentes
   - Cada chunk vira um embedding (vetor matemático)
   - Embeddings são salvos no Pinecone com metadados

2. **💬 Chat com IA**:
   - Usuário faz uma pergunta
   - Sistema converte pergunta em embedding
   - Busca chunks similares no Pinecone
   - IA analisa chunks relevantes + pergunta
   - Gera resposta contextualizada e natural

3. **🧠 Agente Inteligente**:
   - Usa **LangGraph** para orquestrar o fluxo
   - **OpenAI GPT-4** para processamento de linguagem
   - **Ferramentas especializadas** para busca de documentos
   - **Contexto isolado** por conversa (thread_id)

---

## 🚀 Instalação Completa (Para Iniciantes)

### Pré-requisitos

Você precisa ter instalado em seu computador:

1. **Python 3.12+** - [Download aqui](https://www.python.org/downloads/)
2. **UV** (gerenciador moderno do Python) - [Instruções de instalação](https://docs.astral.sh/uv/getting-started/installation/)

### 📥 1. Baixar o Projeto

```bash
# Clone o repositório
git clone https://github.com/MatheusOliveiraSilva/proj-final-prog
cd proj-final-prog
```

### ⚙️ 2. Configurar o Backend (Servidor Python)

```bash
# Entre na pasta do backend
cd backend

# Instale as dependências com UV (mais rápido que pip)
uv pip install -e .

# Volte para a raiz do projeto
cd ..
```

### 🎨 3. Configurar o Frontend (Interface)

O repositório do front-end está [aqui](https://github.com/MatheusOliveiraSilva/ChatWithDocs-Front) e suas instruções no readme.

### 🔑 4. Configurar Variáveis de Ambiente

Crie um arquivo chamado `.env` na pasta `backend/` com o seguinte conteúdo:

```bash
# Abra seu editor de texto favorito e crie o arquivo backend/.env
# Cole o conteúdo que eu vou te enviar separadamente
```

**📧 IMPORTANTE**: Vou enviar as chaves de API (OPENAI_API_KEY, PINECONE_API_KEY, etc.) separadamente para professora Clarisse, por questões de segurança. Cole-as no arquivo `.env` que você criar.

### ▶️ 5. Executar o Sistema

#### Terminal 1 - Backend (API):
```bash
cd backend
uv run uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

#### Terminal 2 - Frontend (Interface):
```bash
cd frontend
npm run dev
```

### 🌐 6. Acessar o Sistema

- **Interface do usuário**: http://localhost:5173
- **API (documentação)**: http://localhost:8000/docs

---

## 🔧 Tecnologias Utilizadas

### Backend (Python)
- **🔗 LangChain**: Framework para aplicações de IA
- **🕸️ LangGraph**: Orquestração de agentes inteligentes
- **🤖 OpenAI**: Modelos de linguagem (GPT-4) e embeddings
- **🗄️ Pinecone**: Banco de dados vetorial para busca semântica
- **⚡ FastAPI**: Framework web moderno e rápido
- **📄 PyPDF2**: Processamento de arquivos PDF
- **📊 Pandas**: Análise de dados (Excel/CSV)
- **📝 python-docx**: Processamento de documentos Word

### Frontend (TypeScript/React)
- **⚛️ React**: Biblioteca para interfaces de usuário
- **📘 TypeScript**: JavaScript com tipagem estática
- **🎨 Tailwind CSS**: Framework de estilização
- **🔄 Server-Sent Events**: Streaming de respostas em tempo real

### Infraestrutura
- **📦 UV**: Gerenciamento rápido de dependências Python
- **🐳 Docker**: Containerização (opcional)
- **⚙️ uvicorn**: Servidor ASGI para FastAPI

---

## 📖 Como Usar o Sistema

### 1. 📤 Carregar Documentos
- Acesse a interface web
- Clique em "Upload de Documento"
- Selecione seus arquivos (PDF, Word, Excel, etc.)
- Aguarde o processamento automático

### 2. 💬 Fazer Perguntas
- Digite sua pergunta na caixa de chat
- Perguntas podem ser sobre qualquer conteúdo dos documentos
- Exemplos:
  - "Qual o resumo do documento sobre IA?"
  - "Quais são as principais conclusões da pesquisa?"
  - "Encontre informações sobre machine learning"

### 3. 🎯 Dicas para Melhores Resultados
- **Seja específico**: "Quais métricas de performance foram mencionadas?" é melhor que "Como está o desempenho?"
- **Use contexto**: "No capítulo sobre redes neurais, qual algoritmo é recomendado?"
- **Pergunte sobre relações**: "Qual a relação entre os conceitos X e Y no documento?"

---

## 🤝 Contribuição

Este projeto foi desenvolvido como trabalho final de mestrado. Sugestões e melhorias são bem-vindas!


---

## 🎓 Projeto Acadêmico

Este sistema foi desenvolvido como **projeto final de mestrado**, demonstrando a aplicação prática de:

- **Processamento de Linguagem Natural (NLP)**
- **Retrieval-Augmented Generation (RAG)**
- **Arquiteturas de IA Modernas**
- **Desenvolvimento Full-Stack**

O objetivo é mostrar como tecnologias de IA podem ser aplicadas para resolver problemas reais de acesso à informação em documentos, criando uma experiência natural e intuitiva para os usuários.

---

**🚀 Desenvolvido com ❤️ usando as mais modernas tecnologias de IA**
