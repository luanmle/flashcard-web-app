# 🧠 Flashcard Analytics Web App

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red.svg)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791.svg)
![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-orange.svg)

Uma plataforma web de flashcards focada em repetição espaçada (*Spaced Repetition*) e recuperação ativa (*Active Recall*), desenhada com a robustez e capilaridade de filtros dos grandes bancos de questões para concursos. 

Mais do que um aplicativo de estudos, este projeto é um laboratório de **Ciência e Análise de Dados**, projetado para coletar logs detalhados de retenção de conhecimento e tempo de resposta para modelagem estatística.

---

## 🎯 Visão Geral e O Problema

Estudantes que enfrentam editais densos (como legislações complexas e disciplinas técnicas) sofrem com a "curva de esquecimento". Ferramentas tradicionais de flashcards frequentemente carecem de uma estruturação hierárquica eficiente que permita filtrar os estudos por nichos específicos, além de não fornecerem métricas granulares sobre o comportamento de aprendizado.

**A Solução:** Uma API RESTful desacoplada que não apenas agenda as revisões de forma inteligente (via algoritmo de repetição espaçada), mas que categoriza os estudos e processa telemetria avançada em um banco de dados relacional.

---

## ⚙️ Escopo e Funcionalidades

### 🚀 MVP (Minimum Viable Product)
- **Motor de Repetição Espaçada:** Algoritmo de agendamento (inspirado no SM-2/Anki) processado no backend para otimização de retenção a longo prazo.
- **Sistema Avançado de Filtros:** Criação de baralhos dinâmicos e sessões de estudo segmentadas. A estrutura hierárquica suportada inclui:
  | Estrutura de Filtros (Tópicos e Subtópicos) |
  | :--- |
  | Tópico: Ciência de Dados |
  | Subtópico: Pandas |
  | Subtópico: Machine Learning |
  | Tópico: Legislação |
  | Subtópico: Lei Orgânica |
  | Subtópico: Código de Ética |
- **Modelos de Cartão Múltiplos:** Suporte nativo a cartões no formato *Básico* (Frente/Verso) e *Cloze Deletion* (Omissão de palavras, ideal para "lei seca").
- **Estatísticas Analíticas (Dashboard):** Processamento de dados via Pandas para exibir taxa de retenção, tempo médio de resposta e volume de estudos filtráveis por dia, mês, ano e matéria.

### 🔮 Implementações Futuras (Arquitetura Preparada)
O banco de dados foi modelado prevendo escalabilidade horizontal para funções de comunidade e *Machine Learning*:
- **Módulo Social:** Comentários em cartões (para resolução colaborativa) e sistema de *likes* em comentários.
- **Micro-Análises de Cartão:** Estatísticas do histórico de revisão individual de cada flashcard (taxa de acerto global vs. individual).
- **Modelagem Preditiva:** Utilização do histórico de revisões (banco de logs) para treinar modelos preditivos capazes de antecipar o esquecimento com base no tempo de hesitação (*duration_ms*).

---

## 🏗️ Arquitetura e Engenharia de Dados

O projeto utiliza o ecossistema do **GitHub Student Developer Pack** (Codespaces para desenvolvimento cloud-native) e é impulsionado por uma stack moderna em Python. A aplicação segue o padrão de repositório, mantendo o frontend totalmente desacoplado para futuras implementações em React/Next.js.

### Diagrama Entidade-Relacionamento (Core de Dados)

```mermaid
erDiagram
    USERS ||--o{ DECKS : "cria"
    USERS ||--o{ REVIEWS : "gera"
    TOPICS ||--o{ SUBTOPICS : "possui"
    SUBTOPICS ||--o{ CARDS : "categoriza"
    DECKS ||--|{ CARDS : "agrupa"
    CARDS ||--o{ REVIEWS : "histórico de"
    
    CARDS {
        string type "basic, cloze"
        string front_content
        string back_content
    }
    
    REVIEWS {
        int rating "1 a 4 (Errei a Fácil)"
        int duration_ms "Telemetria de hesitação"
        datetime reviewed_at
    }
