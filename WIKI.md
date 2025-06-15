# Chat com Documentos - Sistema Inteligente de IA

## Breve Descrição

Este projeto implementa um **sistema avançado de inteligência artificial** com as seguintes características:

* **Principal função**: Sistema de chat inteligente que permite fazer perguntas em linguagem natural sobre documentos carregados, utilizando técnicas de Retrieval-Augmented Generation (RAG)

* **Funções específicas relevantes**: 
  - Upload e processamento automático de documentos (PDF, Word, Excel, PowerPoint, texto)
  - Extração e chunking inteligente de conteúdo
  - Geração de embeddings vetoriais com OpenAI
  - Busca semântica em banco de dados vetorial (Pinecone)
  - Chat contextualizado com agente de IA (LangGraph + GPT-4)
  - Isolamento de contexto por conversa (thread_id)

* **Usuários contemplados**: 
  - **Pesquisadores acadêmicos** que precisam analisar grandes volumes de documentos científicos
  - **Estudantes de pós-graduação** que trabalham com revisão bibliográfica e análise documental
  - **Professores universitários** que desejam criar assistentes para materiais didáticos
  - **Profissionais** que lidam com documentação técnica e relatórios

* **Natureza do programa**: 
  - **Prova de conceito completa** demonstrando aplicação prática de tecnologias modernas de IA
  - **Sistema funcional** com arquitetura full-stack (backend Python + frontend React)
  - **Ferramenta utilitária acabada** pronta para uso em ambiente acadêmico

* **Ressalvas**: 
  - Requer chaves de API pagas (OpenAI e Pinecone) para funcionamento completo
  - Processamento de documentos muito grandes (>50MB) pode ser lento
  - Qualidade das respostas depende da qualidade e relevância dos documentos carregados
  - Sistema otimizado para textos em português e inglês

## Visão de Projeto

### Cenário Positivo 1 (i.e. cenário que dá certo)

Maria é uma mestranda em Ciência da Computação pesquisando sobre "Aplicações de IA em Healthcare". Ela tem uma pasta com 15 artigos científicos em PDF sobre o tema. Maria acessa o sistema, faz upload de todos os PDFs de uma vez e aguarda o processamento automático. Em poucos minutos, todos os documentos estão indexados. Ela então pergunta: "Quais são as principais aplicações de machine learning mencionadas nos artigos para diagnóstico médico?". O sistema analisa todos os documentos e responde com uma lista estruturada citando técnicas como redes neurais convolucionais para análise de imagens médicas, algoritmos de classificação para diagnóstico diferencial, e processamento de linguagem natural para análise de prontuários. Maria continua refinando suas perguntas: "Quais datasets foram mais utilizados nos estudos?" e "Há menção a limitações éticas?". Para cada pergunta, recebe respostas contextualizadas que a ajudam a mapear o estado da arte em sua área de pesquisa, economizando horas de leitura manual.

### Cenário Positivo 2

Professor João está preparando uma disciplina sobre "Fundamentos de Inteligência Artificial" e tem diversos materiais: slides em PowerPoint, capítulos de livros em PDF, artigos complementares e suas próprias anotações em Word. Ele carrega todos esses materiais no sistema e cria uma conversa dedicada à disciplina. Durante a preparação das aulas, ele faz perguntas como: "Quais são os conceitos fundamentais de aprendizado supervisionado mencionados nos materiais?" e "Há exemplos práticos de algoritmos de busca?". O sistema consolida informações de todas as fontes, permitindo que João identifique lacunas no conteúdo, encontre exemplos complementares e prepare exercícios baseados no material disponível. Quando alunos fazem perguntas durante as aulas, João pode consultar rapidamente o sistema para dar respostas mais completas e referenciadas.

### Cenário Negativo 1 (i.e. cenário que expõe uma limitação conhecida e esperada do programa)

Carlos é um pesquisador que trabalha com documentos altamente técnicos em alemão sobre engenharia química. Ele faz upload de vários artigos científicos em alemão e tenta fazer perguntas em português sobre processos químicos específicos. O sistema processa os documentos, mas as respostas são inconsistentes e às vezes imprecisas. Isso acontece porque o modelo de embeddings foi otimizado principalmente para inglês e português, e a tradução automática de termos técnicos muito específicos em alemão pode perder nuances importantes. Carlos percebe que precisa traduzir os documentos para português antes do upload, ou fazer perguntas em inglês para obter melhores resultados. Alternativamente, ele pode usar o sistema apenas para documentos em português ou inglês, que são os idiomas para os quais o sistema foi otimizado.

### Cenário Negativo 2

Ana é uma estudante que está analisando um documento PDF de 200 páginas que foi escaneado (imagem), não sendo um PDF com texto selecionável. Ela faz upload do arquivo e aguarda o processamento. O sistema detecta que é um PDF, mas não consegue extrair texto significativo porque são apenas imagens. A ferramenta de extração de texto (PyPDF2) retorna conteúdo vazio ou caracteres sem sentido. Ana recebe uma mensagem indicando que o documento não pôde ser processado adequadamente. Ela precisa usar uma ferramenta de OCR (Optical Character Recognition) para converter o PDF escaneado em texto antes de fazer o upload, ou encontrar uma versão digital do mesmo documento que contenha texto selecionável.

## Documentação Técnica do Projeto

### Especificação de Requisitos Funcionais e Não-Funcionais

**Requisitos Funcionais:**
- RF01: Sistema deve aceitar upload de arquivos PDF, DOCX, XLSX, PPTX e TXT
- RF02: Sistema deve extrair texto automaticamente dos documentos carregados
- RF03: Sistema deve dividir textos em chunks otimizados para processamento
- RF04: Sistema deve gerar embeddings vetoriais usando OpenAI text-embedding-3-large
- RF05: Sistema deve armazenar embeddings no Pinecone com metadados
- RF06: Sistema deve permitir busca semântica por similaridade
- RF07: Sistema deve manter contexto isolado por thread_id
- RF08: Sistema deve gerar respostas usando LangGraph + GPT-4
- RF09: Sistema deve fornecer API REST documentada
- RF10: Sistema deve suportar streaming de respostas em tempo real

**Requisitos Não-Funcionais:**
- RNF01: Tempo de resposta para queries < 10 segundos
- RNF02: Suporte a documentos até 50MB
- RNF03: Arquitetura escalável com separação backend/frontend
- RNF04: Segurança: validação de tipos de arquivo e sanitização
- RNF05: Disponibilidade: sistema deve funcionar 24/7 em produção
- RNF06: Usabilidade: interface intuitiva para usuários não-técnicos

### Descrição da Arquitetura do Software

**Arquitetura em Camadas:**

1. **Camada de Apresentação (Frontend)**:
   - React + TypeScript + Tailwind CSS
   - Interface responsiva e moderna
   - Comunicação via HTTP/SSE com backend

2. **Camada de API (FastAPI)**:
   - Endpoints RESTful para upload e chat
   - Validação de dados com Pydantic
   - Documentação automática com Swagger

3. **Camada de Processamento (Agent)**:
   - LangGraph para orquestração de fluxo
   - Nodes especializados para diferentes tarefas
   - Toolbox com ferramentas de busca

4. **Camada de Dados**:
   - Pinecone: armazenamento vetorial
   - Metadados: informações de documentos e chunks
   - Isolamento por namespace (thread_id)

5. **Camada de Utilitários**:
   - Processamento de arquivos multi-formato
   - Geração de embeddings OpenAI
   - Chunking inteligente de texto

### Modelo Funcional do Software

**Fluxo Principal - Upload de Documento:**
```
Usuário → Upload Arquivo → Detecção Tipo → Extração Texto → 
Chunking → Geração Embeddings → Armazenamento Pinecone → Confirmação
```

**Fluxo Principal - Chat:**
```
Usuário → Pergunta → Embedding Query → Busca Similaridade → 
Recuperação Chunks → LangGraph Agent → GPT-4 → Resposta Streaming
```

**Componentes Principais:**
- `FileProcessor`: Detecção e extração de conteúdo
- `TextChunker`: Divisão inteligente de texto
- `EmbeddingGenerator`: Interface com OpenAI
- `VectorStore`: Abstração do Pinecone
- `ChatAgent`: Orquestração com LangGraph
- `DocumentSearchTool`: Ferramenta de busca semântica

### Sobre o Código

**Linguagem e Frameworks:**
- **Backend**: Python 3.12+ com FastAPI, LangChain, LangGraph
- **Frontend**: TypeScript com React 18+ e Vite
- **Gerenciamento de Dependências**: UV (Python) e npm (Node.js)

**Estratégia de Comentários:**
- Docstrings em todas as funções públicas seguindo padrão Google
- Comentários inline para lógica complexa
- Type hints obrigatórios em todas as funções
- Logging estruturado para debugging e monitoramento

**Estrutura de Diretórios:**
```
backend/
├── api/          # Endpoints e schemas
├── agent/        # Sistema de IA
├── utils/        # Utilitários reutilizáveis
├── vector_store/ # Integração Pinecone
└── settings.py   # Configurações centralizadas
```

**Padrões de Código:**
- Arquitetura hexagonal com separação de responsabilidades
- Dependency injection para testabilidade
- Error handling com exceções customizadas
- Configuração via variáveis de ambiente
- Logging estruturado com contexto de thread_id

## Manual de Utilização para Usuários Contemplados

### Para Pesquisadores e Estudantes de Pós-Graduação

#### Guia de Instruções:

**Para CARREGAR DOCUMENTOS DE PESQUISA faça:**
1. Acesse a interface web em http://localhost:5173
2. Clique no botão "Upload de Documentos" 
3. Selecione um ou múltiplos arquivos (PDF, Word, Excel, PowerPoint)
4. Aguarde a barra de progresso indicar "Processamento concluído"
5. Verifique na lista de documentos que seus arquivos aparecem com status "Processado"

**Para FAZER PERGUNTAS SOBRE OS DOCUMENTOS faça:**
1. Na caixa de chat, digite sua pergunta em linguagem natural
2. Seja específico: "Quais metodologias de pesquisa são mencionadas?" em vez de "Como pesquisar?"
3. Pressione Enter ou clique em "Enviar"
4. Aguarde a resposta ser gerada (pode levar 5-10 segundos)
5. Para perguntas de follow-up, continue na mesma conversa para manter contexto

**Exceções ou potenciais problemas:**

Se [Documento não foi processado corretamente]
{
Então faça: 
- Verifique se o arquivo não está corrompido
- Confirme que é um dos formatos suportados (PDF, DOCX, XLSX, PPTX, TXT)
- Para PDFs escaneados, use OCR antes do upload
- Tente arquivos menores que 50MB
}

Se [Resposta está imprecisa ou incompleta]
{
Então faça:
- Reformule a pergunta sendo mais específico
- Verifique se os documentos contêm informação relevante
- Tente perguntas em português ou inglês (idiomas otimizados)
- Divida perguntas complexas em várias perguntas simples
}

### Para Professores Universitários

#### Guia de Instruções:

**Para CRIAR MATERIAL DIDÁTICO INTERATIVO faça:**
1. Organize todos os materiais da disciplina (slides, PDFs, artigos)
2. Crie uma nova conversa com nome da disciplina
3. Faça upload de todos os materiais de uma vez
4. Teste com perguntas que os alunos costumam fazer
5. Use o sistema durante as aulas para consultas rápidas

**Para PREPARAR EXERCÍCIOS E AVALIAÇÕES faça:**
1. Pergunte: "Quais são os conceitos principais abordados nos materiais?"
2. Solicite: "Liste exemplos práticos mencionados sobre [tópico específico]"
3. Questione: "Há exercícios ou problemas propostos nos documentos?"
4. Explore: "Quais são as referências bibliográficas citadas?"

**Exceções ou potenciais problemas:**

Se [Sistema não encontra informações específicas]
{
É porque: O conteúdo pode não estar nos documentos carregados, ou a pergunta precisa ser reformulada com termos mais próximos aos usados nos textos originais
}

Se [Respostas são muito genéricas]
{
Então faça: Use perguntas mais específicas como "No capítulo 3 do livro X, qual algoritmo é recomendado?" em vez de "Qual o melhor algoritmo?"
} 