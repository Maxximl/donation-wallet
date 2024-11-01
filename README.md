# donation-wallet

~~ Описание ~~

## Инструкция по запуску

Для работы понадобится:

- `Docker` и `docker compose`
- `Python 3.11`

Затем нужно создать `.env` файл с этими переменными (шаблон можно командой `make env`)

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_PORT=5432
POSTGRES_DB=postgres
APP_HOST=0.0.0.0
APP_PORT=8000
PATH_PREFIX=/api
```

Api работает на 8000 порту, чтобы запустить проект:
```
docker compose up --build
```

Документация - http://localhost:8000/docs 