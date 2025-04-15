# Documentação da API - Vidraçaria dos Anjos

## 1. Visão Geral

A API da Vidraçaria dos Anjos será responsável por gerenciar vendas, orçamentos e dados de clientes. Será desenvolvida utilizando padrões RESTful e retornará dados no formato JSON.

## 2. Base URL

```
https://api.vidracariadosanjos.com.br/v1
```

## 3. Endpoints

### 3.1. Vendas e Orçamentos

#### POST /sales
Cria uma nova venda ou orçamento.

**Request:**
```json
{
  "tipo": "BUDGET|ORDER",
  "cliente": {
    "nome": "string",
    "cpf": "string",
    "telefone": "string",
    "endereco": "string",
    "numero": "string",
    "bairro": "string",
    "cidade": "string",
    "cep": "string"
  },
  "itens": [
    {
      "quantidade": "number",
      "material": "string",
      "medidas": "string",
      "cor": "string",
      "espessura": "string",
      "unitario": "number",
      "subtotal": "number"
    }
  ],
  "vendedor_id": "string",
  "total": "number",
  "data_criacao": "datetime"
}
```

**Response (201 Created):**
```json
{
  "id": "string",
  "numero_documento": "string",
  "tipo": "BUDGET|ORDER",
  "status": "PENDING",
  "cliente": {
    "id": "string",
    "nome": "string",
    "cpf": "string",
    "telefone": "string",
    "endereco": "string",
    "numero": "string",
    "bairro": "string",
    "cidade": "string",
    "cep": "string"
  },
  "itens": [
    {
      "id": "string",
      "quantidade": "number",
      "material": "string",
      "medidas": "string",
      "cor": "string",
      "espessura": "string",
      "unitario": "number",
      "subtotal": "number"
    }
  ],
  "vendedor": {
    "id": "string",
    "nome": "string"
  },
  "total": "number",
  "data_criacao": "datetime",
  "data_atualizacao": "datetime"
}
```

#### GET /sales
Lista todas as vendas e orçamentos com paginação.

**Query Parameters:**
- `page`: número da página (default: 1)
- `limit`: itens por página (default: 10)
- `tipo`: filtro por tipo (BUDGET|ORDER)
- `status`: filtro por status
- `data_inicio`: filtro por data inicial
- `data_fim`: filtro por data final

**Response (200 OK):**
```json
{
  "items": [
    {
      "id": "string",
      "numero_documento": "string",
      "tipo": "BUDGET|ORDER",
      "status": "string",
      "cliente": {
        "nome": "string"
      },
      "total": "number",
      "data_criacao": "datetime"
    }
  ],
  "total": "number",
  "page": "number",
  "limit": "number",
  "pages": "number"
}
```

#### GET /sales/:id
Retorna os detalhes de uma venda ou orçamento específico.

**Response (200 OK):**
```json
{
  "id": "string",
  "numero_documento": "string",
  "tipo": "BUDGET|ORDER",
  "status": "string",
  "cliente": {
    "id": "string",
    "nome": "string",
    "cpf": "string",
    "telefone": "string",
    "endereco": "string",
    "numero": "string",
    "bairro": "string",
    "cidade": "string",
    "cep": "string"
  },
  "itens": [
    {
      "id": "string",
      "quantidade": "number",
      "material": "string",
      "medidas": "string",
      "cor": "string",
      "espessura": "string",
      "unitario": "number",
      "subtotal": "number"
    }
  ],
  "vendedor": {
    "id": "string",
    "nome": "string"
  },
  "total": "number",
  "data_criacao": "datetime",
  "data_atualizacao": "datetime"
}
```

#### PATCH /sales/:id/status
Atualiza o status de uma venda ou orçamento.

**Request:**
```json
{
  "status": "APPROVED|REJECTED|CANCELLED"
}
```

**Response (200 OK):**
```json
{
  "id": "string",
  "status": "string",
  "data_atualizacao": "datetime"
}
```

### 3.2. Clientes

#### GET /customers
Lista todos os clientes com paginação.

**Query Parameters:**
- `page`: número da página (default: 1)
- `limit`: itens por página (default: 10)
- `search`: busca por nome, cpf ou telefone

**Response (200 OK):**
```json
{
  "items": [
    {
      "id": "string",
      "nome": "string",
      "cpf": "string",
      "telefone": "string"
    }
  ],
  "total": "number",
  "page": "number",
  "limit": "number",
  "pages": "number"
}
```

#### GET /customers/:id
Retorna os detalhes de um cliente específico.

**Response (200 OK):**
```json
{
  "id": "string",
  "nome": "string",
  "cpf": "string",
  "telefone": "string",
  "endereco": "string",
  "numero": "string",
  "bairro": "string",
  "cidade": "string",
  "cep": "string",
  "vendas": [
    {
      "id": "string",
      "numero_documento": "string",
      "tipo": "BUDGET|ORDER",
      "status": "string",
      "total": "number",
      "data_criacao": "datetime"
    }
  ]
}
```

### 3.3. Vendedores

#### GET /sellers
Lista todos os vendedores ativos.

**Response (200 OK):**
```json
{
  "items": [
    {
      "id": "string",
      "nome": "string",
      "email": "string",
      "telefone": "string"
    }
  ]
}
```

## 4. Códigos de Status

- `200 OK`: Requisição bem-sucedida
- `201 Created`: Recurso criado com sucesso
- `400 Bad Request`: Erro de validação
- `401 Unauthorized`: Não autorizado
- `403 Forbidden`: Acesso negado
- `404 Not Found`: Recurso não encontrado
- `500 Internal Server Error`: Erro interno do servidor

## 5. Autenticação

A API utiliza autenticação JWT (JSON Web Token).

### POST /auth/login
Realiza o login e retorna o token de acesso.

**Request:**
```json
{
  "email": "string",
  "senha": "string"
}
```

**Response (200 OK):**
```json
{
  "access_token": "string",
  "token_type": "Bearer",
  "expires_in": "number"
}
```

## 6. Modelos de Dados

### 6.1. Venda/Orçamento
```typescript
interface Sale {
  id: string;
  numero_documento: string;
  tipo: 'BUDGET' | 'ORDER';
  status: 'PENDING' | 'APPROVED' | 'REJECTED' | 'CANCELLED';
  cliente_id: string;
  vendedor_id: string;
  total: number;
  data_criacao: Date;
  data_atualizacao: Date;
}
```

### 6.2. Item
```typescript
interface Item {
  id: string;
  venda_id: string;
  quantidade: number;
  material: string;
  medidas: string;
  cor: string;
  espessura: string;
  unitario: number;
  subtotal: number;
}
```

### 6.3. Cliente
```typescript
interface Cliente {
  id: string;
  nome: string;
  cpf: string;
  telefone: string;
  endereco: string;
  numero: string;
  bairro: string;
  cidade: string;
  cep: string;
}
```

## 7. Banco de Dados

### 7.1. Tabelas Principais

```sql
CREATE TABLE clientes (
  id UUID PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
  cpf VARCHAR(14) UNIQUE NOT NULL,
  telefone VARCHAR(15) NOT NULL,
  endereco VARCHAR(100) NOT NULL,
  numero VARCHAR(10) NOT NULL,
  bairro VARCHAR(50) NOT NULL,
  cidade VARCHAR(50) NOT NULL,
  cep VARCHAR(9) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE vendedores (
  id UUID PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  telefone VARCHAR(15) NOT NULL,
  senha VARCHAR(255) NOT NULL,
  ativo BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE vendas (
  id UUID PRIMARY KEY,
  numero_documento VARCHAR(20) UNIQUE NOT NULL,
  tipo VARCHAR(10) NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
  cliente_id UUID REFERENCES clientes(id),
  vendedor_id UUID REFERENCES vendedores(id),
  total DECIMAL(10,2) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE itens (
  id UUID PRIMARY KEY,
  venda_id UUID REFERENCES vendas(id),
  quantidade INTEGER NOT NULL,
  material VARCHAR(100) NOT NULL,
  medidas VARCHAR(50) NOT NULL,
  cor VARCHAR(50) NOT NULL,
  espessura VARCHAR(50) NOT NULL,
  unitario DECIMAL(10,2) NOT NULL,
  subtotal DECIMAL(10,2) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 8. Recomendações de Implementação

1. **Segurança**:
   - Implementar rate limiting
   - Validar todos os inputs
   - Usar HTTPS
   - Implementar logs de auditoria

2. **Performance**:
   - Implementar cache
   - Otimizar queries
   - Usar índices apropriados
   - Implementar compressão gzip

3. **Manutenibilidade**:
   - Documentar com Swagger/OpenAPI
   - Implementar testes automatizados
   - Usar migrations para o banco de dados
   - Seguir padrões de código

4. **Monitoramento**:
   - Implementar health checks
   - Configurar logs estruturados
   - Monitorar métricas de performance
   - Configurar alertas

## 9. Próximos Passos

1. **Fase 1 - Estrutura Básica**:
   - Configurar ambiente de desenvolvimento
   - Criar estrutura do projeto
   - Implementar autenticação
   - Criar CRUDs básicos

2. **Fase 2 - Funcionalidades Principais**:
   - Implementar fluxo de vendas/orçamentos
   - Desenvolver gestão de clientes
   - Criar relatórios básicos
   - Implementar validações

3. **Fase 3 - Melhorias**:
   - Adicionar cache
   - Implementar logs
   - Configurar monitoramento
   - Realizar testes de carga

4. **Fase 4 - Integrações**:
   - Integrar com sistema de e-mail
   - Implementar notificações
   - Desenvolver webhooks
   - Criar documentação completa 