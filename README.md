# Local HTTPS web stack

Локальный стенд из четырёх сервисов:

- **Nginx** — reverse proxy и TLS termination на `https://localhost:443`;
- **Python/Flask backend** — HTTP на `:8080` внутри Docker-сети;
- **PostgreSQL 15** — база данных;
- **Redis 7** — кэш/хранилище сессий.

Nginx передаёт `Host`, `X-Real-IP`, `X-Forwarded-For`, `X-Forwarded-Proto` и `X-Forwarded-Host`, ограничивает запросы до **10 req/s на IP** и размер тела запроса до **10 MB**.

Перед запуском при необходимости измените локальные пароли в `.env`.

## Запуск — 5 команд

```bash
chmod +x gen-certs.sh && ./gen-certs.sh
docker compose up -d --build
docker compose ps
curl -k https://localhost/
docker compose logs -f nginx backend
```

Остановить стенд: `docker compose down`. Удалить также данные PostgreSQL/Redis: `docker compose down -v`.

> Сертификат self-signed, поэтому для локальной проверки `curl` используется с `-k`. Файлы `.env` и приватный ключ сертификата добавлены в `.gitignore`.
