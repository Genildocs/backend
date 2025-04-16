# Documentação da API - Vidraçaria dos Anjos

## URL Base

```
https://sales-pro-ashen.vercel.app/api
```

## Endpoints

### Autenticação

- `POST /auth/register` - Registrar novo vendedor
- `POST /auth/login` - Login de vendedor

### Notificações

- `POST /notifications` - Criar notificação
- `GET /notifications` - Listar notificações
- `GET /notifications/unread` - Listar notificações não lidas
- `PUT /notifications/{id}` - Atualizar notificação
- `DELETE /notifications/{id}` - Deletar notificação

### Clientes

- `GET /clientes` - Listar clientes
- `POST /clientes` - Criar cliente
- `GET /clientes/{id}` - Obter cliente
- `PUT /clientes/{id}` - Atualizar cliente
- `DELETE /clientes/{id}` - Deletar cliente

### Vendedores

- `GET /vendedores` - Listar vendedores
- `POST /vendedores` - Criar vendedor
- `GET /vendedores/{id}` - Obter vendedor
- `PUT /vendedores/{id}` - Atualizar vendedor
- `DELETE /vendedores/{id}` - Deletar vendedor

### Vendas

- `GET /vendas` - Listar vendas
- `POST /vendas` - Criar venda
- `GET /vendas/{id}` - Obter venda
- `PUT /vendas/{id}` - Atualizar venda
- `DELETE /vendas/{id}` - Deletar venda

### Recuperação de Senha

- `POST /password-reset/request` - Solicitar redefinição de senha
- `POST /password-reset/reset` - Redefinir senha

## Exemplo de Uso

### Autenticação

```typescript
// Login
const login = async (email: string, senha: string) => {
  const response = await fetch(
    'https://sales-pro-ashen.vercel.app/api/auth/login',
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, senha }),
    }
  );
  return response.json();
};

// Registrar
const register = async (vendedorData: {
  nome: string;
  email: string;
  telefone: string;
  senha: string;
}) => {
  const response = await fetch(
    'https://sales-pro-ashen.vercel.app/api/auth/register',
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(vendedorData),
    }
  );
  return response.json();
};
```

### Notificações

```typescript
// Criar notificação
const createNotification = async (notification: {
  title: string;
  message: string;
  type: string;
}) => {
  const response = await fetch(
    'https://sales-pro-ashen.vercel.app/api/notifications',
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(notification),
    }
  );
  return response.json();
};

// Listar notificações
const getNotifications = async () => {
  const response = await fetch(
    'https://sales-pro-ashen.vercel.app/api/notifications',
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );
  return response.json();
};
```

## Headers Necessários

Para endpoints que requerem autenticação, inclua o token JWT no header:

```typescript
headers: {
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json'
}
```

## CORS

A API aceita requisições das seguintes origens:

- `http://localhost:5173` (desenvolvimento)
- `https://sales-pro-ashen.vercel.app` (produção)

## Status Codes

- 200: Sucesso
- 201: Criado com sucesso
- 400: Requisição inválida
- 401: Não autorizado
- 403: Acesso negado
- 404: Recurso não encontrado
- 422: Dados inválidos
- 500: Erro interno do servidor
