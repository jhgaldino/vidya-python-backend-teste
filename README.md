# Sales API (FastAPI + SQLite + MongoDB)

API backend em Python para ingestao, armazenamento e consulta de vendas.
A aplicacao suporta dois modos de execucao:
- Local (FastAPI + SQLite local + MongoDB local)
- Docker Compose (API + MongoDB em containers)

## Stack

- Python 3.11+
- FastAPI
- SQLite (dados estruturados de vendas)
- MongoDB (dados textuais relacionados as vendas)
- SQLAlchemy
- uv (gerenciamento de dependencias)
- Docker / Docker Compose (opcional)

## Estrutura do projeto

```text
app/
  api/routes/
  core/
  db/
  models/
  schemas/
  services/
```

## Requisitos funcionais atendidos

- CRUD de vendas (`POST`, `GET`, `PUT`, `DELETE` em `/sales`)
- Persistencia relacional em SQLite (tabela `sales`)
- Persistencia textual em MongoDB (colecao `sale_texts`)
- Consulta analitica (`/analytics/summary` e `/analytics/quantity-by-category`)
- Busca textual (`/search/text?q=...`) com retorno das vendas relacionadas

## Variaveis de ambiente

A aplicacao le as configuracoes de `.env`:

```env
APP_NAME=Sales API
SQLITE_URL=sqlite:///./data/sales.db
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=sales_db
MONGO_COLLECTION_NAME=sale_texts
```

## Como executar localmente

Pre-requisitos:
- Python 3.11+
- `uv` instalado
- MongoDB disponivel localmente (ou via Docker)

1. Instalar `uv` (caso nao tenha):
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

2. Instalar dependencias:
```powershell
uv sync
```

3. Criar arquivo de ambiente:
```powershell
Copy-Item .env.example .env
```

4. Garantir MongoDB ativo na porta `27017` (escolha uma opcao):

Opcao A - MongoDB instalado localmente (sem Docker):
```powershell
# Windows (servico)
Get-Service MongoDB
Start-Service MongoDB
```

Opcao B - MongoDB via Docker:
```powershell
docker run --name sales-mongo -p 27017:27017 -d mongo:7
```

Validacao rapida de conectividade:
```powershell
Test-NetConnection localhost -Port 27017
```

5. Iniciar API:
```powershell
uv run uvicorn app.main:app --reload
```

6. Acessar documentacao:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Como executar com Docker Compose

Pre-requisito:
- Docker Desktop (ou Docker Engine) em execucao

1. Subir API + MongoDB:
```powershell
docker compose up --build -d
```

2. Ver logs da API:
```powershell
docker compose logs -f api
```

3. Acessar documentacao:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

4. Parar containers:
```powershell
docker compose down
```

5. Parar e remover volumes (inclui dados do MongoDB):
```powershell
docker compose down -v
```

## Endpoints principais

- `GET /health`
- `POST /sales` cria venda (aceita `text_note` opcional para salvar no MongoDB)
- `GET /sales` lista vendas com filtros opcionais: `start_date`, `end_date`, `category`
- `GET /sales/{sale_id}` consulta uma venda por ID
- `PUT /sales/{sale_id}` atualiza campos de uma venda
- `DELETE /sales/{sale_id}` remove venda e textos relacionados
- `POST /sales/{sale_id}/texts` adiciona texto adicional para uma venda
- `GET /analytics/summary` resumo analitico (`total_sales`, `total_revenue`, `average_ticket`)
- `GET /analytics/quantity-by-category` soma `quantity` por categoria
- `GET /search/text?q=...` busca textual (regex case-insensitive) e retorna venda + texto

## Exemplos de uso

Criar venda:

```http
POST /sales
Content-Type: application/json

{
  "product_name": "Notebook X",
  "category": "Eletronicos",
  "quantity": 2,
  "unit_price": 3500.00,
  "sale_date": "2026-02-10",
  "text_note": "Cliente elogiou a entrega e a qualidade do produto"
}
```

Filtrar vendas por periodo e categoria:

```http
GET /sales?start_date=2026-02-01&end_date=2026-02-28&category=Eletronicos
```

Resumo analitico com filtro:

```http
GET /analytics/summary?start_date=2026-02-01&end_date=2026-02-28&category=Eletronicos
```

Busca textual:

```http
GET /search/text?q=elogiou
```

## Observacoes

- Valores monetarios (`unit_price`, `total_revenue`, `average_ticket`) usam decimal com 2 casas.
- Erros comuns:
  - `400`: regra de negocio invalida (`error_code: invalid_request`)
  - `404`: recurso nao encontrado
  - `422`: erro de validacao (`error_code: validation_error`)
  - `503`: indisponibilidade temporaria de banco (`sql_database_error` ou `mongo_database_error`)
  - `500`: erro interno nao tratado
