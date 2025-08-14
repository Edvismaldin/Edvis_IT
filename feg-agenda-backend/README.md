# FEG Agenda API

API de agendamento de eventos da FEG (salas, eventos, usuários) construída com FastAPI + SQLite.

## Rodando localmente

1. Crie e ative um virtualenv (opcional)
2. Instale dependências:

```bash
pip install -r requirements.txt
```

3. Rode o servidor:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

O banco SQLite ficará em `data/app.db`. O usuário admin é semeado no startup com:
- Email: `admin@feg.br`
- Senha: `admin123`

## Endpoints principais
- POST `/auth/login` (OAuth2): retorna `access_token`
- GET `/users/me`
- POST `/users/` (apenas admin)
- POST `/rooms/` (apenas admin)
- GET `/rooms/`
- POST `/events/`
- GET `/events/`

## Variáveis de ambiente
- `SQLITE_DB_PATH` (opcional)
- `JWT_SECRET_KEY` (recomendado em produção)
- `ADMIN_EMAIL` e `ADMIN_PASSWORD`