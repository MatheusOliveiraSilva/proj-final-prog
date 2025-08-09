# 🤖 Chat com Documentos - Sistema de IA Inteligente

## 📖 Sobre o Projeto

Este é um sistema avançado de inteligência artificial que permite fazer perguntas em linguagem natural sobre documentos enviados, utilizando tecnologias de ponta como OpenAI, Pinecone, LangChain e LangGraph.

### 🎯 O que o Sistema Faz

- 📄 Envio de Documentos: Envie arquivos PDF, Word, Excel, PowerPoint e texto
- 🧠 Processamento Inteligente: Extrai e analisa o conteúdo automaticamente
- 💬 Chat Natural: Converse com seus documentos como se estivesse falando com um especialista
- 🔍 Busca Semântica: Encontra informações relevantes mesmo que você não use as mesmas palavras
- 🎭 Múltiplas Conversas: Cada conversa mantém seu próprio contexto e documentos

### Demo

https://github.com/user-attachments/assets/fac6fb5d-e9d6-41cc-9bc3-6759b6a07069

---

## 🏗️ Arquitetura do Sistema

### 📁 Organização do Código

```
proj-final-prog/
├── backend/                    # Servidor Python (API + IA)
│   ├── api/                   # Endpoints REST
│   │   ├── routers/           # Rotas organizadas por funcionalidade
│   │   │   ├── agent.py       # Chat com IA
│   │   │   └── documents.py   # Upload e busca de documentos
│   │   └── schemas/           # Estruturas de dados da API
│   ├── agent/                 # Sistema de IA (LangGraph)
│   │   ├── graph.py           # Orquestração do agente
│   │   ├── nodes.py           # Lógica de processamento
│   │   └── agent_toolbox/     # Ferramentas do agente
│   │       └── tools/         # Busca em documentos
│   ├── vector_store/          # Integração com Pinecone
│   ├── utils/                 # Utilidades
│   │   ├── embeddings.py      # Geração de embeddings (OpenAI)
│   │   ├── text_chunking.py   # Fragmentação inteligente de texto
│   │   └── file_processing.py # Processamento de arquivos
│   └── settings.py            # Configuração
├── frontend/                   # Interface do usuário (React/TypeScript)
└── pyproject.toml             # Dependências e configurações
```

### 🔄 Como o Sistema Funciona

1. 📤 Upload de Documentos:
   - O usuário envia um arquivo (PDF, Word, etc.)
   - O sistema detecta automaticamente o tipo e extrai o conteúdo
   - O texto é dividido em trechos (chunks) inteligentes
   - Cada trecho vira um embedding (um vetor matemático)
   - Os embeddings são armazenados no Pinecone com metadados

2. 💬 Chat com IA:
   - O usuário faz uma pergunta
   - O sistema converte a pergunta em um embedding
   - Busca por trechos semelhantes no Pinecone
   - A IA analisa os trechos relevantes e a pergunta
   - Gera uma resposta contextualizada e natural

3. 🧠 Agente Inteligente:
   - Usa LangGraph para orquestrar o fluxo
   - OpenAI GPT-4 para processamento de linguagem natural
   - Ferramentas especializadas para busca em documentos
   - Contexto isolado por conversa (thread_id)

---

## 🚀 Instalação Completa (Para Iniciantes)

### Pré-requisitos

Certifique-se de ter instalado:

1. Python 3.12+ - [Baixar aqui](https://www.python.org/downloads/)
2. UV (gerenciador moderno de pacotes Python) - [Instruções de instalação](https://docs.astral.sh/uv/getting-started/installation/)

### 📥 1. Baixar o Projeto

```bash
# Clonar o repositório
git clone https://github.com/MatheusOliveiraSilva/proj-final-prog
cd proj-final-prog
```

### ⚙️ 2. Configurar o Backend (Servidor Python)

```bash
# Entrar na pasta do backend
cd backend

# Instalar dependências com UV (mais rápido que pip)
uv pip install -e .

# Voltar para a raiz do projeto
cd ..
```

### 🎨 3. Configurar o Frontend (Interface)

O repositório do frontend está [aqui](https://github.com/MatheusOliveiraSilva/ChatWithDocs-Front). Siga as instruções do README de lá.

### 🔑 4. Configurar Variáveis de Ambiente

Crie um arquivo chamado `.env` na pasta `backend/` com o seguinte conteúdo:

```bash
# Abra seu editor de texto e crie backend/.env
# Cole o conteúdo que será enviado separadamente
```

Importante: As chaves de API (OPENAI_API_KEY, PINECONE_API_KEY, etc.) serão enviadas separadamente para a Professora Clarisse por motivos de segurança. Cole-as no arquivo `.env` que você criou.

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

- Interface do usuário: http://localhost:5173
- API (documentação): http://localhost:8000/docs

---

## 🔧 Tecnologias Utilizadas

### Backend (Python)
- LangChain: Framework para aplicações de IA
- LangGraph: Orquestração de agentes inteligentes
- OpenAI: Modelos de linguagem (GPT-4) e embeddings
- Pinecone: Banco vetorial para busca semântica
- FastAPI: Framework web moderno e rápido
- PyPDF2: Processamento de arquivos PDF
- Pandas: Análise de dados (Excel/CSV)
- python-docx: Processamento de documentos Word

### Frontend (TypeScript/React)
- React: Biblioteca de UI
- TypeScript: JavaScript com tipagem estática
- Tailwind CSS: Framework de estilos
- Server-Sent Events: Streaming de respostas em tempo real

### Infraestrutura
- UV: Gerenciamento rápido de dependências Python
- Docker: Conteinerização (opcional)
- uvicorn: Servidor ASGI para FastAPI

---

## 📖 Como Usar o Sistema

### 1. 📤 Enviar Documentos
- Abra a interface web
- Clique em "Enviar Documento"
- Selecione seus arquivos (PDF, Word, Excel, etc.)
- Aguarde o processamento automático

### 2. 💬 Fazer Perguntas
- Digite sua pergunta na caixa de chat
- As perguntas podem ser sobre qualquer conteúdo dos documentos
- Exemplos:
  - "Qual é o resumo do documento de IA?"
  - "Quais são as principais conclusões da pesquisa?"
  - "Encontre informações sobre machine learning"

### 3. 🎯 Dicas para Melhores Resultados
- Seja específico: "Quais métricas de desempenho foram mencionadas?" é melhor do que "Como é o desempenho?"
- Use contexto: "No capítulo sobre redes neurais, qual algoritmo é recomendado?"
- Pergunte sobre relações: "Qual é a relação entre os conceitos X e Y no documento?"

---

## 🤝 Contribuição

Este projeto foi desenvolvido como trabalho final de mestrado. Sugestões e melhorias são bem-vindas!

---

## 🎓 Projeto Acadêmico

Este sistema foi desenvolvido como trabalho final de mestrado, demonstrando a aplicação prática de:

- Processamento de Linguagem Natural (PLN)
- Retrieval-Augmented Generation (RAG)
- Arquiteturas modernas de IA
- Desenvolvimento full-stack

O objetivo é mostrar como as tecnologias de IA podem ser aplicadas para resolver problemas reais de acesso à informação em documentos, criando uma experiência natural e intuitiva para os usuários.

---

🚀 Construído com ❤️ usando as tecnologias de IA mais modernas
