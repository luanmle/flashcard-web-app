# Flashcards SRS & Analytics Platform 🧠📊

Bem-vindo à documentação oficial da nossa plataforma de aprendizado por Repetição Espaçada (Spaced Repetition System - SRS). Este web app foi projetado do zero para oferecer alta performance na revisão de conteúdos complexos, agregando métricas de retenção de memória e telemetria através da análise de hesitação.

---

## 🎯 O que este Web App faz?
1. **Flashcard Studio**: Permite a criação estruturada de cartões de estudo (frente/verso e omissão de palavras - "cloze deletion") organizados rigidamente em **Tópicos > Subtópicos > Decks**.
2. **Estudo Focado (Filtros)**: Permite que os usuários escolham revisar todo o conteúdo atrasado ou foquem o estudo de hoje em um "Deck" específico.
3. **Motor SRS Sensível à Hesitação**: O coração do app. Diferente de algoritmos tradicionais, nosso cálculo de repetição avalia não apenas a nota (1 a 4) dada pelo usuário, mas o tempo (em milissegundos) que ele levou para virar a carta.
4. **Analytics com Pandas & Chart.js**: Processamento em tempo real do histórico do usuário, exibindo em um Dashboard as matérias com maior tempo de hesitação e a lista das cartas mais difíceis (menor rating histórico).

---

## 🏗️ Esquema da Infraestrutura

O projeto adota uma arquitetura modular em **Python**, focada em um fluxo unidirecional seguro: o Frontend HTML interage apenas com a API, que por sua vez tem o monopólio do acesso ao Banco de Dados Relacional.

```mermaid
graph TD
    %% Entidades Frontend
    subgraph Frontend [UI - Templates Jinja2 + Tailwind]
        Dash[Dashboard / Analytics<br/>index.html]
        Studio[Flashcard Studio<br/>studio.html]
        Study[Tela de Estudos<br/>study.html]
    end

    %% Entidades Backend
    subgraph Backend [FastAPI Backend]
        API_R[Routers<br/>/api/users, /decks, /reviews]
        Serv_SRS[Motor SRS<br/>services/srs.py]
        Serv_Ana[Motor de Analytics<br/>Pandas - services/analytics.py]
        CRUD[Camada de Repositório<br/>app/crud/]
        Schemas[Validação de Dados<br/>Pydantic V2]
    end

    %% Banco de Dados
    subgraph DB [Persistência]
        PG[(PostgreSQL)]
        Alembic[Alembic<br/>Migrações e Versionamento]
    end

    %% Relações Frontend -> Backend
    Dash -- "GET /api/analytics/{id}" --> API_R
    Studio -- "POST /api/cards/" --> API_R
    Study -- "GET /api/study/due" --> API_R
    Study -- "POST /api/reviews/" --> API_R

    %% Relações Internas Backend
    API_R --> Schemas
    Schemas --> CRUD
    API_R --> Serv_SRS
    API_R --> Serv_Ana

    %% Relações Backend -> DB
    CRUD -- "SQLAlchemy ORM" --> PG
    Serv_Ana -- "Consultas Textuais Complexas" --> PG
    Alembic -. "Gera/Atualiza Tabelas" .-> PG
```

### Otimização Arquitetural Crítica: `UserCardState`
Para evitar lentidão em escala (ex: recalcular milhares de registros de `/reviews` do passado toda vez que o usuário entra no app), implementamos uma tabela chamada `UserCardState`.

Quando o usuário submete um review na tela de **Study**, o **Motor SRS** calcula a nova dificuldade e salva a data da próxima revisão diretamente nesta tabela de estado. Assim, descobrir "quais cartas estudar hoje" vira uma busca `$O(1)$` no índice do PostgreSQL, garantindo velocidade máxima.

---

## 📂 Estrutura de Diretórios

```text
├── alembic/                # Arquivos de configuração e migrações do Banco de Dados
├── app/
│   ├── api/
│   │   ├── deps.py         # Injeção de dependências (Sessão do DB)
│   │   └── routers/        # Rotas FastAPI modularizadas (users, cards, study, analytics, etc.)
│   ├── core/               # Configuração do banco (`database.py`) e variáveis globais
│   ├── crud/               # Lógica de interação direta com o Banco (Create, Read, Update, Delete)
│   ├── models/             # Modelos ORM do SQLAlchemy (Tabelas: User, Topic, Card, UserCardState...)
│   ├── schemas/            # Classes Pydantic para validação (Create, Response, Base) de Input/Output
│   ├── services/           # Lógicas de negócios pesadas (Motor SRS e Pandas Analytics)
│   ├── templates/          # Arquivos HTML renderizados via Jinja2
│   └── main.py             # Ponto de inicialização do servidor FastAPI
├── data/
│   ├── seed.json           # Massa de dados pronta para testes didáticos
│   └── seed_db.py          # Script idempotente para carga inicial de dados
├── requirements.txt        # Dependências Python
└── README.md               # Esta documentação
```

---

## 🚀 Como Iniciar (Setup de Desenvolvimento)

### 1. Requisitos
- **Python 3.12+**
- Instância do **PostgreSQL** rodando (ou local, ou Docker).
  - *Dica para testes rápidos:* O sistema aceita rodar em SQLite para validações mudando a string de conexão.

### 2. Instalação

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd <diretorio>

# Crie seu ambiente virtual
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)

# Instale os pacotes necessários
pip install -r requirements.txt
```

### 3. Configuração do Banco de Dados

Aponte para o seu PostgreSQL exportando a variável de ambiente:
```bash
export DATABASE_URL="postgresql://user:password@localhost/flashcards"
```

A seguir, instancie as tabelas no banco de dados utilizando o Alembic:
```bash
alembic upgrade head
```

### 4. Carregando Massa de Testes (Opcional)
Temos um script pronto que injeta um ecossistema completo de testes focado em "Ciência de Dados" e "Legislação", perfeito para visualizar o dashboard ganhando vida:
```bash
PYTHONPATH=. python data/seed_db.py
```

### 5. Rodando a Aplicação
Inicie o servidor local FastAPI usando o `uvicorn`:
```bash
uvicorn app.main:app --reload
```

---

## 🧭 Utilizando a Plataforma

Assim que o servidor for iniciado, você terá dois portais principais:

1. **A Interface Web (Frontend MVP):**
   - Acesse `http://localhost:8000/` no navegador.
   - Digite o usuário "seed_user" (se rodou o script de carga) ou cadastre um novo.
   - Brinque com a interface, crie cartões, veja o timer funcionar na tela de Estudo e analise os gráficos de retenção.

2. **A Documentação API (Backend):**
   - Acesse `http://localhost:8000/docs` para ver o Swagger UI.
   - Lá você encontrará todas as rotas documentadas automaticamente, podendo testar o `POST` de Reviews, a extração dos metadados analíticos e filtros da API.
