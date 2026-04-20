<h1 align="center">🛒 Collect Prices</h1>

<p align="center">
  <strong>Monitoramento automatizado de preços em e-commerces brasileiros.</strong>
</p>

<p align="center">
  Collect Prices é um sistema que automatiza a coleta de preços de produtos em e-commerces brasileiros, permitindo que você acompanhe o histórico de preços de qualquer produto cadastrado, compare valores entre lojas e identifique o melhor momento para comprar — tudo em um único painel.
</p>

<p align="center">
  <a href="https://github.com/joaoMatusalen">
    <img src="https://img.shields.io/badge/GitHub-joaoMatusalen-181717?logo=github" alt="GitHub">
  </a>
  <a href="https://www.linkedin.com/in/joaomatusalen/">
    <img src="https://img.shields.io/badge/LinkedIn-joaomatusalen-0A66C2?logo=linkedin" alt="LinkedIn">
  </a>
</p>

## Por que Collect Prices?

O Collect Prices nasceu da necessidade de monitorar preços de produtos em diferentes e-commerces brasileiros. Eu queria uma solução que automatizasse meu processo de verificação de preços enquanto eu trabalhava e deixava meu computador ligado. Com o tempo, fui adicionando funcionalidades e melhorando a experiência do usuário.

## Rodando na máquina pessoal

O projeto foi pensado para rodar localmente, na máquina do próprio usuário, como uma solução self-hosted simples:

- O dashboard fica disponível no navegador;
- A API organiza o cadastro de produtos, URLs e analytics;
- O worker executa os scrapers em segundo plano;
- O scheduler agenda novas coletas ao longo do dia;
- O banco salva o histórico de preços entre reinicializações.

Esse modelo é ideal para quem quer deixar o sistema rodando em casa ou no computador de trabalho, acompanhando preços sem depender de um serviço externo.

## Funcionalidades

### Scraping automatizado

- Coleta de preços via Chrome headless com agendamento configurável via Ofelia (3x ao dia por padrão)
- Dispare o scraper pela interface ou deixe o agendador cuidar

### 14 lojas pré-configuradas e testadas

- Amazon, Kabum, Magazine Luiza, Mercado Livre, Americanas, Casas Bahia, Carrefour, Extra, Fast Shop, Netshoes, Ponto, Samsung e Casa das Cercas
- Padronização para facilitar a adição de novas lojas

### Dashboard interativo

- Gráficos de linha com histórico por loja, cards de métricas (atual, mínimo, máximo, média) e comparativo entre lojas
- Visualize dados dos últimos 7, 30, 60, 90 dias ou todo o histórico
- Isole métricas e gráficos de uma loja específica

<p align="center">
  <img src="docs/images/dashboard.png" alt="Dashboard interativo" width="800">
</p>

### CRUD de produtos

- Cadastre produtos, gerencie múltiplas URLs por produto e ative ou desative links individualmente

<p align="center">
  <img src="docs/images/crud-produtos.png" alt="CRUD de produtos" width="800">
</p>

### Logs de execução

- Acompanhe cada job do scraper em tempo real, com status, progresso e detalhes

<p align="center">
  <img src="docs/images/logs-scraper.png" alt="Logs do scraper" width="800">
</p>

## Como usar

### Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) e [Docker Compose](https://docs.docker.com/compose/)

### 1. Clone o repositório

```bash
git clone https://github.com/joaoMatusalen/collect-prices-in-web.git
cd collect-prices-in-web
```

### 2. Configure as variáveis de ambiente

```bash
cp .env.example .env
```

Edite o `.env` com seus valores:

```env
# Banco de dados
POSTGRES_DB=collect_prices
POSTGRES_USER=postgres
POSTGRES_PASSWORD=sua_senha_segura

# Conexão com frontend e API Flask
DATABASE_URL=postgresql://postgres:sua_senha_segura@db:5432/collect_prices
VITE_API_URL=http://localhost:5000
CORS_ORIGIN=http://localhost:5173
```

### 3. Suba todos os serviços

```bash
docker compose up -d
```

Isso inicializa o PostgreSQL, a API, o frontend, o worker do scraper e o agendador. As tabelas são criadas automaticamente na primeira execução.

### 4. Acesse o dashboard

Abra [http://localhost:5173](http://localhost:5173) no navegador.

## Como funciona no dia a dia

1. Você cadastra um produto e adiciona links de lojas.
2. O scheduler enfileira execuções automáticas nos horários configurados.
3. O worker processa os jobs do scraper em segundo plano.
4. Os preços coletados são salvos no PostgreSQL.
5. O dashboard exibe histórico, métricas e comparativos entre lojas.

## Configurações opcionais e uso

### Cadastrar um produto

1. Clique em **"Adicionar produto"** na interface.
2. Informe o nome do produto e um grupo opcional.
3. Adicione URLs das lojas que deseja monitorar.

### Cadastrar uma nova loja

1. Vá até `scraper/app/scrapers/` e crie um novo arquivo `nome_da_loja.py`.
2. Siga a formatação padrão dos outros arquivos.
3. Adicione o nome da loja no arquivo `scraper/app/runner.py`.

Exemplo:

```python
from selenium.webdriver.common.by import By
from .base import BaseScraper


class MinhaLojaScraper(BaseScraper):
    store_name = "Minha Loja"

    def extract(self, url):
        self.browser.get(url)
        self.wait_for_document_ready()
        price = self.wait_for_non_empty_text(By.CSS_SELECTOR, ".price-selector")
        return {"name": "", "price": price}
```

### Executar o scraper

1. Clique em **"Executar scraper"** no header do dashboard.
2. Selecione os produtos que deseja raspar.
3. Clique em **"Executar scraper"**.

### Agendamento automático

Por padrão, o Ofelia agenda a coleta para as **12h, 15h e 20h** (horário de Brasília). Edite `ofelia.ini` para alterar.

Repositório do agendador: [Ofelia](https://github.com/mcuadros/ofelia)

```ini
[job-exec "scraper-enqueue"]
# segundo | minuto | hora | dia-do-mês | mês | dia-da-semana
# Exemplo: 0 0 12,15,20 * * * -> 12h, 15h e 20h
schedule = 0 0 12,15,20 * * *
container = scraper-worker
command = python enqueue_job.py --trigger scheduled
```

### Variáveis de ambiente opcionais

```env
# Frontend
CORS_ORIGIN=http://localhost:5173

# Zona de tempo para agrupamento diário
ANALYTICS_TIMEZONE=America/Sao_Paulo

# Controles do scraper
SCRAPER_PAGE_LOAD_STRATEGY=eager     # padrão: eager
SCRAPER_PAGE_LOAD_TIMEOUT_SECONDS=30 # padrão: 30
SCRAPER_IMPLICIT_WAIT_SECONDS=4      # padrão: 4
SCRAPER_WORKER_POLL_SECONDS=5        # padrão: 5
```

## Persistência de dados

Os dados ficam salvos no volume Docker `postgres_data`, usado pelo PostgreSQL. Isso significa que:

- Recriar os containers não apaga o histórico de preços;
- Parar e subir o projeto novamente mantém os dados;
- Remover o volume explicitamente apaga o banco.

Se você quiser reiniciar tudo do zero, aí sim precisará remover os volumes Docker manualmente.

## Arquitetura

O projeto segue uma arquitetura de microsserviços, orquestrada com Docker Compose:

```text
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Frontend   │────▶│   API Flask  │────▶│  PostgreSQL  │
│  React/Vite  │     │   :5000      │     │    :5432     │
│   :5173      │     └──────────────┘     └──────┬───────┘
└──────────────┘                                 │
                      ┌──────────────┐           │
                      │  Scheduler   │           │
                      │   (Ofelia)   │           │
                      └──────┬───────┘           │
                             │ enqueue           │
                      ┌──────▼───────┐           │
                      │   Scraper    │───────────┘
                      │   Worker     │
                      └──────────────┘
```

| Serviço | Stack | Porta | Descrição |
| --- | --- | --- | --- |
| **db** | PostgreSQL 16 Alpine | 5432 | Banco de dados com volume persistente |
| **api** | Python 3.11 / Flask | 5000 | API REST com CRUD de produtos, URLs, analytics e scraper jobs |
| **frontend** | React 19 / Vite 8 | 5173 | SPA com dashboard de preços, gráficos Plotly e tema dark/light |
| **scraper-worker** | Python 3.11 / Selenium / Chromium | — | Worker que processa jobs de scraping com Chrome headless |
| **scheduler** | Ofelia | — | Agendador cron que enfileira jobs automaticamente |

## Estrutura do Projeto

```text
collect-prices-in-web/
├── backend/
│   └── api/
│       ├── app.py              # Factory da aplicação Flask
│       ├── db.py               # Pool de conexões e schema bootstrap
│       ├── routes/
│       │   ├── products.py     # CRUD de produtos
│       │   ├── urls.py         # CRUD de URLs por produto
│       │   ├── analytics.py    # Histórico de preços e estatísticas
│       │   ├── stores.py       # Lista de lojas
│       │   └── scraper.py      # Gerenciamento de jobs do scraper
│       └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # Componente raiz
│   │   ├── components/         # MetricCard, ProductChart, StoreCard, modais...
│   │   ├── sections/           # HeroPanel, MetricsSection, StoreComparisonSection
│   │   ├── hooks/              # useProductList, useProductAnalytics, useTheme...
│   │   ├── styles/             # theme.css, layout.css, ui.css, modals.css
│   │   └── utils/              # Formatação de moeda e inferência de loja
│   └── Dockerfile
├── scraper/
│   ├── main.py                 # Entrypoint de execução direta
│   ├── worker.py               # Worker loop para processar jobs
│   ├── enqueue_job.py          # CLI para enfileirar jobs
│   ├── app/
│   │   ├── database.py         # Conexão PostgreSQL, queries do scraper
│   │   ├── runner.py           # Orquestrador de scraping
│   │   ├── jobs.py             # Gerenciamento de jobs (enqueue, claim, execute)
│   │   └── scrapers/           # Um módulo por loja (Amazon, Kabum, etc.)
│   └── Dockerfile
├── shared/
│   ├── schema.py               # DDL das tabelas (products, stores, price_history, jobs)
│   └── scraper_jobs.py         # CRUD de jobs compartilhado entre API e scraper
├── docker-compose.yml          # Orquestração dos 5 serviços
├── ofelia.ini                  # Agendamento cron do scraper
├── requirements.txt            # Dependências Python
└── .env.example                # Template de variáveis de ambiente
```

## API

Base URL: `http://localhost:5000`

### Produtos

| Método | Rota | Descrição |
| --- | --- | --- |
| `GET` | `/api/products` | Lista produtos (aceita `?active=true\|false`) |
| `POST` | `/api/products` | Cria produto com nome, grupo e URLs opcionais |
| `PUT` | `/api/products/:id` | Atualiza nome, grupo ou status ativo |
| `DELETE` | `/api/products/:id` | Remove o produto e o histórico relacionado |

### URLs

| Método | Rota | Descrição |
| --- | --- | --- |
| `GET` | `/api/products/:id/urls` | Lista URLs do produto |
| `POST` | `/api/products/:id/urls` | Adiciona URL ao produto |
| `PUT` | `/api/urls/:id` | Atualiza URL ou status ativo |
| `DELETE` | `/api/urls/:id` | Remove URL permanentemente |

### Analytics

| Método | Rota | Descrição |
| --- | --- | --- |
| `GET` | `/api/analytics/:product_id` | Histórico de preços + stats (`?days=30&store=all`) |

### Scraper

| Método | Rota | Descrição |
| --- | --- | --- |
| `POST` | `/api/scraper/jobs` | Enfileira um novo job |
| `GET` | `/api/scraper/jobs` | Lista jobs recentes |
| `GET` | `/api/scraper/jobs/latest` | Retorna o job mais recente |
| `GET` | `/api/scraper/jobs/:id` | Detalhes e logs de um job |

### Lojas

| Método | Rota | Descrição |
| --- | --- | --- |
| `GET` | `/api/stores` | Lista todas as lojas cadastradas |

## Banco de Dados

PostgreSQL 16 com as seguintes tabelas:

```text
products          → id, name, group_name, active, created_at, updated_at
product_urls      → id, product_id (FK), url, active, created_at
stores            → id, name
price_history     → id, product_id (FK), store_id (FK), price, url, scraped_at
scraper_jobs      → id, status, trigger_type, requested_by, timestamps, counters
scraper_job_logs  → id, job_id (FK), level, event_type, message, details (JSONB)
```

O schema é criado e migrado automaticamente na inicialização (idempotente).

## Limitações conhecidas

- Como todo projeto de scraping, o funcionamento depende da estrutura HTML das lojas. Se o site mudar, o scraper correspondente pode quebrar.
- Algumas lojas podem aplicar mecanismos anti-bot, CAPTCHAs ou bloqueios temporários.
- O projeto foi pensado para uso pessoal e local, não como uma plataforma SaaS multiusuário.
- O consumo de recursos pode variar conforme a quantidade de produtos, a frequência das coletas e o comportamento dos sites monitorados.
- O scraper depende de Chromium e ambiente gráfico virtual dentro do container.

## Como atualizar o projeto

Para atualizar sua instalação local com a versão mais recente do repositório:

```bash
git pull
docker compose up -d --build
```

Isso recompila as imagens necessárias e reaplica a configuração atual sem apagar os dados persistidos no volume do banco.

## Contribuições

Contribuições são bem-vindas. Esse projeto tem como objetivo ajudar pessoas que enfrentam o mesmo problema ao consultar preços de produtos em diferentes lojas. Sinta-se livre para contribuir.
