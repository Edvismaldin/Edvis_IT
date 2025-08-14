# Agenda FEG - Sistema de Agendamento de Eventos

Stack: PHP 8 + SQLite (PDO) + HTML/CSS/JS.

## Como rodar

1. Configure a senha de admin (opcional):
   - Linux/macOS: `export ADMIN_PASSWORD="minhasenha"`
   - Windows (PowerShell): `$env:ADMIN_PASSWORD="minhasenha"`

2. Suba o servidor embutido do PHP na raiz do projeto:

```bash
php -S 0.0.0.0:8080 -t .
```

3. Acesse:
   - Público: http://localhost:8080/public/index.html
   - Admin: http://localhost:8080/public/admin.html

## Endpoints
- `GET /api/events.php` lista eventos
- `POST /api/events.php` cria evento (admin)
- `PUT /api/events.php` atualiza evento (admin)
- `DELETE /api/events.php?id=ID` remove evento (admin)
- `POST /api/registrations.php` cria inscrição
- `GET /api/registrations.php?event_id=ID` lista inscrições (admin)
- `GET /api/auth.php` estado da sessão
- `POST /api/auth.php` login admin `{ password }`
- `POST /api/auth.php?action=logout` logout

## Notas
- Banco em `data/database.sqlite` é criado automaticamente.
- Datas/hora devem ser enviadas como `YYYY-MM-DD HH:mm:ss`.