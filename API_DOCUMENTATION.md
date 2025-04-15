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
DATABASE_URL=postgresql+asyncpg://user:password@localhost/vidracaria

# Configurações de Segurança
SECRET_KEY=sua_chave_secreta_aqui_mude_em_producao
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
```http
POST /auth/login
```

**Request:**
```json
{
    "email": "vendedor@email.com",
    "senha": "senha123"
}
```

**Response:**
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "token_type": "bearer",
    "vendedor": {
        "id": "uuid",
        "nome": "Nome do Vendedor",
        "email": "vendedor@email.com"
    }
}
```

## 4. Endpoints

### 4.1 Clientes

#### Criar Cliente
```http
POST /clientes
```
**Request:**
```json
{
    "nome": "João Silva",
    "cpf": "123.456.789-00",
    "telefone": "(11) 98765-4321",
    "endereco": "Rua Example",
    "numero": "123",
    "bairro": "Centro",
    "cidade": "São Paulo",
    "cep": "01234-567"
}
```

#### Listar Clientes
```http
GET /clientes?skip=0&limit=100&search=João
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
```http
POST /vendedores
```
**Request:**
```json
{
    "nome": "Maria Oliveira",
    "email": "maria@email.com",
    "telefone": "(11) 98765-4321",
    "senha": "senha123"
}
```

#### Listar Vendedores
```http
GET /vendedores?skip=0&limit=100
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
```http
POST /vendas
```
**Request:**
```json
{
    "tipo": "BUDGET",
    "cliente_id": "uuid",
    "vendedor_id": "uuid",
    "total": 1500.00,
    "itens": [
        {
            "quantidade": 2,
            "material": "Vidro Temperado",
            "medidas": "1.00x1.50",
            "cor": "Incolor",
            "espessura": "8mm",
            "unitario": 500.00,
            "subtotal": 1000.00
        }
    ]
}
```

#### Listar Vendas
```http
GET /vendas?skip=0&limit=100&tipo=BUDGET&status=PENDING
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
     -d '{"email": "vendedor@email.com", "senha": "senha123"}'
```

**Criar Cliente:**
```bash
curl -X POST "http://localhost:8000/clientes" \
     -H "Authorization: Bearer {seu_token}" \
     -H "Content-Type: application/json" \
     -d '{
         "nome": "João Silva",
         "cpf": "123.456.789-00",
         "telefone": "(11) 98765-4321",
         "endereco": "Rua Example",
         "numero": "123",
         "bairro": "Centro",
         "cidade": "São Paulo",
         "cep": "01234-567"
     }'
```

**Criar Orçamento:**
```bash
curl -X POST "http://localhost:8000/vendas" \
     -H "Authorization: Bearer {seu_token}" \
     -H "Content-Type: application/json" \
     -d '{
         "tipo": "BUDGET",
         "cliente_id": "uuid",
         "vendedor_id": "uuid",
         "total": 1500.00,
         "itens": [
             {
                 "quantidade": 2,
                 "material": "Vidro Temperado",
                 "medidas": "1.00x1.50",
                 "cor": "Incolor",
                 "espessura": "8mm",
                 "unitario": 500.00,
                 "subtotal": 1000.00
             }
         ]
     }'
```

### 6.3 Documentação Interativa
A API possui documentação interativa disponível em:
- Swagger UI: `/docs`
- ReDoc: `/redoc` 