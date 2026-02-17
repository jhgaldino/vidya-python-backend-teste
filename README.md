# Sales API (FastAPI + SQLite + MongoDB)

API backend em Python para ingestao, armazenamento e consulta de vendas.
Esta aplicacao pode ser executada de duas formas:
- Localmente (FastAPI + SQLite local + MongoDB local)
- Docker Compose (API + MongoDB em containers)

## Stack

- Python 3.11+
- FastAPI
- SQLite (dados estruturados de vendas)
- MongoDB (dados textuais relacionados as vendas)
- uv (gerenciamento de ambiente/dependencias)
- Docker / Docker Compose (opcional, para execucao conteinerizada)

## Estrutura

```
app/
  api/routes/
  core/
  db/
  models/
  schemas/
  services/
```

## Como executar (local)

Pre-requisitos:
- Python 3.11+
- `uv` instalado
- MongoDB rodando localmente (ou em container)

1. Instale o `uv` (caso ainda nao tenha):
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

2. Instale as dependencias:
```powershell
uv sync
```

3. Configure variaveis de ambiente:
```powershell
Copy-Item .env.example .env
```

4. Suba um MongoDB local (exemplo com Docker):
```powershell
docker run --name sales-mongo -p 27017:27017 -d mongo:7
```
exemplo com instalacao nativa no windows
Baixe o instalador: Vá ao site oficial do MongoDB e baixe o MSI do Community Server.
Instale: Execute o instalador, escolha "Complete" e, na tela de serviço, marque "Install MongoDB as a Service" para que ele inicie automaticamente com o Windows.
Instale o Compass (Opcional, mas recomendado): O instalador perguntará se deseja instalar o MongoDB Compass, uma interface gráfica para gerenciar seu banco.
Verifique: Abra o terminal (cmd) e digite mongosh (ou mongo em versões antigas) para acessar o shell. 

Método 3: macOS (Nativo)
Utilizando Homebrew:
Atualize e instale:
bash
brew tap mongodb/brew
brew install mongodb-community
Inicie o serviço:
bash
brew services start mongodb-community
Verifique:
bash
mongosh

5. Rode a API:
```powershell
uv run uvicorn app.main:app --reload
```

6. Documentacao interativa:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Como executar (Docker)

Pre-requisitos:
- Docker Desktop (ou Docker Engine) ativo

1. Suba API + MongoDB:
```powershell
docker compose up --build -d
```

2. Verifique os logs da API:
```powershell
docker compose logs -f api
```

3. Acesse a documentacao:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

4. Parar os containers:
```powershell
docker compose down
```

5. Parar e remover volumes (inclui dados do Mongo):
```powershell
docker compose down -v
```

## Teste rapido (qualquer modo)

1. `GET /health`
- `http://127.0.0.1:8000/health`
- resposta esperada: `{"status":"ok"}`

2. Criar uma venda (`POST /sales`) com o payload de exemplo abaixo

3. Validar consultas:
- `GET /sales`
- `GET /analytics/summary`
- `GET /search/text?q=elogiou`

## Endpoints principais

- `POST /sales` cria venda (com `text_note` opcional para MongoDB)
- `GET /sales` lista vendas com filtros `start_date`, `end_date`, `category`
- `GET /sales/{sale_id}` consulta uma venda
- `PUT /sales/{sale_id}` atualiza uma venda
- `DELETE /sales/{sale_id}` remove venda e textos relacionados
- `POST /sales/{sale_id}/texts` adiciona texto relacionado a venda
- `GET /analytics/summary` resumo analitico (`total_revenue`, `average_ticket`, `total_sales`)
- `GET /analytics/quantity-by-category` quantidade vendida por categoria
- `GET /search/text?q=...` busca textual no Mongo e retorna vendas relacionadas

## Observacao sobre valores monetarios

- `unit_price`, `total_revenue` e `average_ticket` usam precisao decimal (2 casas).
- A API evita ponto flutuante para dinheiro; em algumas respostas JSON os valores monetarios podem vir como string decimal.

## Tratamento de erros HTTP

- `404`: recurso nao encontrado (ex.: venda inexistente).
- `422`: erro de validacao de payload/query (`error_code: validation_error`).
- `400`: erro de regra de negocio baseado em `ValueError` (`error_code: invalid_request`).
- `503`: falha temporaria de banco SQL ou Mongo (`error_code: sql_database_error` / `mongo_database_error`).
- `500`: erro interno inesperado (`error_code: internal_server_error`).

## Exemplo de payload para criar venda

```json
{
  "product_name": "Notebook X",
  "category": "Eletronicos",
  "quantity": 2,
  "unit_price": 3500.0,
  "sale_date": "2026-02-10",
  "text_note": "Cliente elogiou a entrega e a qualidade do produto"
}
```
