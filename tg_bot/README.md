# Бот ARAXEL Academy

Возможности:
1. Уведомления студентам: новые уроки и домашние задания.
2. Каталог курсов в Telegram.
3. Админ-уведомления: новые отправки ДЗ, оплаты.
4. Авторизация через Telegram: вход на сайт по ссылке.

## Быстрый деплой на Render

1. Создай бота у @BotFather, получи `BOT_TOKEN`.
2. Залей этот проект в репозиторий `nikolajgrinvald-code/araxel-academy-bot` или как отдельный Git-репозиторий.
3. В Render создай новый **Web Service** из этого репо.
4. Env Variables на Render:
   - `BOT_TOKEN`
   - `ADMIN_IDS=123456789,987654321`
   - `API_URL=https://araxelacademy.pro`
   - `WEBHOOK_URL=https://<твой-домен-бота>.onrender.com`
5. Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Нажми **Deploy**.

После деплоя открой через браузер:
`https://<домен-бота>.onrender.com/webhook/<BOT_TOKEN>/set`
Для сброса webhook:
`https://<домен-бота>.onrender.com/webhook/<BOT_TOKEN>`

## Локальный запуск
```bash
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
```

## Дальше
- Добавить рассылку студентам через Django REST API.
- Добавить webhooks из Django: при новом уроке отправлять сообщение боту.
