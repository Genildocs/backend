# API Vidraçaria dos Anjos - Documentação

## Índice

1. [Visão Geral](#1-visão-geral)
2. [Configuração](#2-configuração)
3. [Autenticação](#3-autenticação)
4. [Endpoints](#4-endpoints)
5. [Modelos de Dados](#5-modelos-de-dados)
6. [Exemplos de Uso](#6-exemplos-de-uso)

## 1. Visão Geral

A API da Vidraçaria dos Anjos é um sistema RESTful desenvolvido com FastAPI para gerenciar vendas, orçamentos e clientes. A API utiliza PostgreSQL como banco de dados e implementa autenticação JWT.

### Tecnologias Principais

- FastAPI
- SQLAlchemy (ORM)
- PostgreSQL
- JWT (Autenticação)
- Pydantic (Validação de dados)

## 2. Configuração

### Variáveis de Ambiente (.env)

```env
# Configurações do Banco de Dados
DATABASE_URL=postgresql://usuario:senha@localhost:5432/nome_do_banco

# Configurações de Segurança
SECRET_KEY=sua_chave_secreta_aqui
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Configurações do Servidor
HOST=0.0.0.0
PORT=8000
```

### Instalação

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Iniciar servidor
uvicorn app.main:app --reload
```

## 3. Autenticação

A API utiliza autenticação JWT (JSON Web Token). Todas as rotas, exceto login, requerem um token válido.

### Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "seu_email@exemplo.com", "senha": "sua_senha"}'
```

Resposta:

```json
{
  "access_token": "seu_token_jwt",
  "token_type": "bearer"
}
```

### Uso do Token

Inclua o token no header de todas as requisições:

```
Authorization: Bearer seu_token_jwt
```

## 4. Endpoints

### 4.1 Clientes

#### Criar Cliente

```bash
curl -X POST "http://localhost:8000/clientes/" \
     -H "Authorization: Bearer seu_token_jwt" \
     -H "Content-Type: application/json" \
     -d '{
         "nome": "Nome do Cliente",
         "email": "cliente@exemplo.com",
         "telefone": "1234567890"
     }'
```

#### Listar Clientes

```bash
curl -X GET "http://localhost:8000/clientes/" \
     -H "Authorization: Bearer seu_token_jwt"
```

#### Obter Cliente

```http
GET /clientes/{cliente_id}
```

#### Atualizar Cliente

```http
PATCH /clientes/{cliente_id}
```

### 4.2 Vendedores

#### Criar Vendedor

```bash
curl -X POST "http://localhost:8000/vendedores/" \
     -H "Authorization: Bearer seu_token_jwt" \
     -H "Content-Type: application/json" \
     -d '{
         "nome": "Nome do Vendedor",
         "email": "vendedor@exemplo.com",
         "senha": "senha_segura"
     }'
```

#### Listar Vendedores

```bash
curl -X GET "http://localhost:8000/vendedores/" \
     -H "Authorization: Bearer seu_token_jwt"
```

#### Obter Vendedor

```http
GET /vendedores/{vendedor_id}
```

#### Atualizar Vendedor

```http
PATCH /vendedores/{vendedor_id}
```

### 4.3 Vendas

#### Criar Venda/Orçamento

```bash
curl -X POST "http://localhost:8000/vendas/" \
     -H "Authorization: Bearer seu_token_jwt" \
     -H "Content-Type: application/json" \
     -d '{
         "cliente_id": "uuid_do_cliente",
         "vendedor_id": "uuid_do_vendedor",
         "valor_total": 1000.00,
         "itens": [
             {
                 "produto": "Nome do Produto",
                 "quantidade": 2,
                 "valor_unitario": 500.00
             }
         ]
     }'
```

#### Listar Vendas

```bash
curl -X GET "http://localhost:8000/vendas/" \
     -H "Authorization: Bearer seu_token_jwt"
```

#### Obter Venda

```http
GET /vendas/{venda_id}
```

#### Atualizar Status

```http
PATCH /vendas/{venda_id}/status
```

**Request:**

```json
{
  "status": "APPROVED"
}
```

## 5. Modelos de Dados

### 5.1 Cliente

- id: UUID
- nome: string
- cpf: string (único)
- telefone: string
- endereco: string
- numero: string
- bairro: string
- cidade: string
- cep: string
- created_at: datetime
- updated_at: datetime

### 5.2 Vendedor

- id: UUID
- nome: string
- email: string (único)
- telefone: string
- senha: string (hash)
- ativo: boolean
- created_at: datetime
- updated_at: datetime

### 5.3 Venda

- id: UUID
- numero_documento: string (único)
- tipo: string (BUDGET|ORDER)
- status: string (PENDING|APPROVED|REJECTED|CANCELLED)
- cliente_id: UUID
- vendedor_id: UUID
- total: decimal
- created_at: datetime
- updated_at: datetime

### 5.4 Item

- id: UUID
- venda_id: UUID
- quantidade: integer
- material: string
- medidas: string
- cor: string
- espessura: string
- unitario: decimal
- subtotal: decimal
- created_at: datetime

## 6. Exemplos de Uso

### 6.1 Fluxo Básico

1. Login do vendedor
2. Cadastro do cliente
3. Criação do orçamento
4. Aprovação do orçamento
5. Conversão em venda

### 6.2 Curl Examples

**Login:**

```bash
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "seu_email@exemplo.com", "senha": "sua_senha"}'
```

**Criar Cliente:**

```bash
curl -X POST "http://localhost:8000/clientes/" \
     -H "Authorization: Bearer seu_token_jwt" \
     -H "Content-Type: application/json" \
     -d '{
         "nome": "Nome do Cliente",
         "email": "cliente@exemplo.com",
         "telefone": "1234567890"
     }'
```

**Criar Orçamento:**

```bash
curl -X POST "http://localhost:8000/vendas/" \
     -H "Authorization: Bearer seu_token_jwt" \
     -H "Content-Type: application/json" \
     -d '{
         "cliente_id": "uuid_do_cliente",
         "vendedor_id": "uuid_do_vendedor",
         "valor_total": 1000.00,
         "itens": [
             {
                 "produto": "Nome do Produto",
                 "quantidade": 2,
                 "valor_unitario": 500.00
             }
         ]
     }'
```

### 6.3 Documentação Interativa

A API possui documentação interativa disponível em:

- Swagger UI: `/docs`
- ReDoc: `/redoc`
