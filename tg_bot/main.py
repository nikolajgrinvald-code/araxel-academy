import os
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import httpx
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton, WebAppInfo,
)
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.environ["BOT_TOKEN"]
API_URL = os.environ.get("API_URL", "https://araxelacademy.pro")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "")
ADMIN_IDS = {int(x) for x in os.environ.get("ADMIN_IDS", "").split(",") if x.strip().isdigit()}

app = FastAPI()
bot = Bot(BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()
client = httpx.AsyncClient(timeout=25)

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Каталог курсов")],
        [KeyboardButton(text="Мои задания")],
        [KeyboardButton(text="Регистрация")],
    ],
    resize_keyboard=True,
)


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


async def notify_students(text: str):
    # Здесь потом подключи рассылку по enrolled students из БД Django
    pass


@app.get("/")
def root():
    return {"status": "ok", "webhook": WEBHOOK_URL}


@app.post("/webhook/{token}")
async def telegram_webhook(request: Request, token: str):
    if token != BOT_TOKEN:
        return PlainTextResponse("forbidden", status_code=403)
    data = await request.json()
    update = types.Update.model_validate(data)
    await dp.feed_update(bot, update)
    return {"ok": True}


@dp.message(types.Message)
async def catch_all(message: types.Message):
    text = (message.text or "").strip()

    if text in {"/start", "Начать", "Запуск"}:
        notify_text = "Я бот ARAXEL Academy. Со мной можно открывать каталог, задания и войти на сайт."
        if message.from_user and is_admin(message.from_user.id):
            notify_text += "\n\nТы в админах. Пиши /admin."
        await message.answer(notify_text, reply_markup=main_kb)
        return

    if text in {"/courses", "Каталог курсов"}:
        await message.answer(f"Каталог курсов:\n{API_URL}/courses/", reply_markup=main_kb)
        return

    if text in {"/register", "Регистрация"}:
        tg_id = message.from_user.id if message.from_user else None
        url = f"{API_URL}/accounts/telegram-link/"
        if tg_id:
            url += f"?telegram_id={tg_id}"
        await message.answer(f"Регистрация / вход:\n{url}", reply_markup=main_kb)
        return

    if text in {"/myhomework", "Мои задания"}:
        tg_id = message.from_user.id if message.from_user else None
        if not tg_id:
            return await message.answer("Не удалось найти аккаунт Telegram.")
        r = await client.get(f"{API_URL}/api/telegram/auth/?telegram_id={tg_id}")
        if r.status_code == 200:
            data = r.json()
            deep = data.get("url")
            if deep:
                await message.answer(
                    "Открывай задания:",
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text="Открыть задания", web_app=WebAppInfo(url=deep))]
                    ]),
                )
                return
        await message.answer("Сначала зарегистрируйся через «Регистрация».", reply_markup=main_kb)
        return

    if text == "/admin":
        if message.from_user and is_admin(message.from_user.id):
            await message.answer(
                "Admin-доступ: https://araxelacademy.pro/admin/",
                reply_markup=main_kb,
            )
        else:
            await message.answer("Нет доступа.", reply_markup=main_kb)
        return

    await message.answer("Понял только меню. Выбирай действие:", reply_markup=main_kb)


@app.on_event("startup")
async def startup():
    webhook = (WEBHOOK_URL or "").rstrip("/") + f"/webhook/{BOT_TOKEN}"
    if webhook:
        try:
            await bot.set_webhook(webhook)
        except Exception as exc:  # noqa: BLE001
            print("set_webhook error:", exc)


@app.on_event("shutdown")
async def shutdown():
    await bot.delete_webhook(drop_pending_updates=True)
    await client.aclose()
    await bot.session.close()


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", "8080"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, log_level="info")
