import logging
import time
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo
)
from config import settings
from services.aliases import search_heroes, HERO_BY_ID

logger = logging.getLogger("bot_handlers")
router = Router()

def get_main_keyboard() -> InlineKeyboardMarkup:
    """Creates the primary WebApp launch keyboard."""
    rows = []
    if settings.WEBAPP_URL and settings.WEBAPP_URL.startswith("https://"):
        sep = "&" if "?" in settings.WEBAPP_URL else "?"
        bust_url = f"{settings.WEBAPP_URL}{sep}v={int(time.time())}"
        rows.append([
            InlineKeyboardButton(
                text="⚔️ Открыть Draft Assistant (Mini App)",
                web_app=WebAppInfo(url=bust_url)
            )
        ])
    elif (
        settings.WEBAPP_URL
        and settings.WEBAPP_URL.startswith("http://")
        and "localhost" not in settings.WEBAPP_URL
        and "127.0.0.1" not in settings.WEBAPP_URL
    ):
        rows.append([
            InlineKeyboardButton(
                text="🌐 Открыть Draft Assistant",
                url=settings.WEBAPP_URL
            )
        ])
    else:
        rows.append([
            InlineKeyboardButton(
                text="💻 Ссылка на Web-интерфейс",
                callback_data="webapp_info"
            )
        ])

    rows.append([
        InlineKeyboardButton(
            text="📊 Топ меты (D2PT)",
            callback_data="meta_summary"
        ),
        InlineKeyboardButton(
            text="❓ Как пользоваться",
            callback_data="help_info"
        )
    ])
    return InlineKeyboardMarkup(inline_keyboard=rows)

@router.message(CommandStart())
async def cmd_start(message: Message):
    url_hint = ""
    if not settings.WEBAPP_URL.startswith("https://"):
        url_hint = f"\n\n💻 <b>Локальный веб-интерфейс:</b> <code>{settings.WEBAPP_URL}</code>"

    text = (
        "👋 <b>Добро пожаловать в Dota 2 Draft Assistant!</b>\n\n"
        "Умный помощник для пиков и контр-пиков в реальном времени:\n"
        "• ⚡ <b>D2PT Мета</b>: актуальные винрейты и тиры по ролям (Pos 1-5).\n"
        "• 🎯 <b>Контр-пики</b>: математический расчет преимущества над врагами.\n"
        "• 🤝 <b>Синергии</b>: идеальные связки и комбинации способностей.\n"
        "• 🔍 <b>Поиск на сленге</b>: понимает СФ, Гуля, Бара, Тракса, Бабка и др."
        f"{url_hint}\n\n"
        "Нажмите кнопку ниже, чтобы начать:"
    )
    await message.answer(text, reply_markup=get_main_keyboard(), parse_mode="HTML")

@router.callback_query(F.data == "webapp_info")
async def cb_webapp_info(callback):
    await callback.answer()
    text = (
        "💻 <b>Веб-интерфейс Draft Assistant:</b>\n\n"
        f"🔗 <code>{settings.WEBAPP_URL}</code>\n\n"
        "Откройте эту ссылку в браузере на вашем компьютере!\n\n"
        "<i>Примечание: для открытия Mini App прямо внутри мобильного Telegram "
        "требуется публичный HTTPS-адрес.</i>"
    )
    await callback.message.answer(text, parse_mode="HTML")

@router.message(Command("draft"))
async def cmd_draft(message: Message):
    text = "Нажмите кнопку, чтобы открыть интерактивное окно драфта:"
    await message.answer(text, reply_markup=get_main_keyboard())

@router.message(Command("help"))
async def cmd_help(message: Message):
    text = (
        "📖 <b>Инструкция по использованию:</b>\n\n"
        "1. Нажмите <b>«Открыть Draft Assistant»</b>.\n"
        "2. Выберите пики врагов (до 5 героев) и союзников (до 4 героев).\n"
        "3. Выберите вашу роль (Керри, Мид, Оффлейн, Саппорт 4/5).\n"
        "4. Алгоритм рассчитает топ лучших героев с подробным объяснением плюсов и минусов!\n\n"
        "💡 <i>Вы также можете написать в этот чат любое имя героя или сленг (например: «пудж», «гуля», «сф»), чтобы быстро найти его!</i>"
    )
    await message.answer(text, parse_mode="HTML")

@router.message(Command("report"))
@router.message(Command("doc"))
@router.message(Command("file"))
async def cmd_send_report(message: Message):
    import os
    from aiogram.types import FSInputFile
    file_path = "FOR_GEMINI_REVIEW.txt"
    if os.path.exists(file_path):
        doc = FSInputFile(file_path, filename="FOR_GEMINI_REVIEW.txt")
        await message.answer_document(doc, caption="📄 Полный отчет FOR_GEMINI_REVIEW.txt (Dota 2 Draft Assistant & Encyclopedia)")
    else:
        await message.answer("⚠️ Файл FOR_GEMINI_REVIEW.txt еще не сформирован. Запустите build_report.py.")

@router.message(Command("update_meta"))
async def cmd_update_meta(message: Message):
    status_msg = await message.answer("🔄 <b>Запущено обновление меты (D2PT & Dotabuff)...</b>\nПожалуйста, подождите...", parse_mode="HTML")
    try:
        from database.db import AsyncSessionLocal
        from services.scraper.d2pt_scraper import d2pt_scraper
        from services.scraper.dotabuff_scraper import dotabuff_scraper
        async with AsyncSessionLocal() as session:
            await d2pt_scraper.sync_d2pt(session)
            await dotabuff_scraper.sync_top_heroes(session, limit=10)
        await status_msg.edit_text("✅ <b>База меты и контр-пиков успешно обновлена!</b>", parse_mode="HTML")
    except Exception as e:
        logger.error(f"Error updating meta: {e}")
        await status_msg.edit_text(f"⚠️ Ошибка при обновлении: {e}")

@router.callback_query(F.data == "help_info")
async def cb_help(callback):
    await callback.answer()
    await cmd_help(callback.message)

@router.callback_query(F.data == "meta_summary")
async def cb_meta(callback):
    await callback.answer()
    text = (
        "🏆 <b>Топ героев меты по позициям (D2PT High MMR):</b>\n\n"
        "• <b>Поз 1 (Керри)</b>: Morphling (53.2%), Ursa (53.0%), Lifestealer (52.9%)\n"
        "• <b>Поз 2 (Мид)</b>: Lina (53.4%), Puck (53.1%), Templar Assassin (53.0%)\n"
        "• <b>Поз 3 (Тройка)</b>: Dark Seer (53.6%), Primal Beast (53.3%), Slardar (53.2%)\n"
        "• <b>Поз 4 (Семи-сап)</b>: Nyx Assassin (52.8%), Clockwerk (52.7%), Earthshaker (52.6%)\n"
        "• <b>Поз 5 (Фулл-сап)</b>: Chen (54.1%), Witch Doctor (53.4%), Warlock (53.1%)\n\n"
        "Запустите Mini App для персонального расчета под текущий драфт!"
    )
    await callback.message.answer(text, parse_mode="HTML", reply_markup=get_main_keyboard())

@router.message(F.text)
async def handle_hero_text_search(message: Message):
    query = message.text.strip()
    if query.startswith("/"):
        return

    matches = search_heroes(query)
    if not matches:
        await message.answer(
            f"❌ Герой по запросу «<b>{query}</b>» не найден.\n"
            "Попробуйте официальное имя или сленг (СФ, Гуля, Бара, Тракса, Пудж...)",
            parse_mode="HTML"
        )
        return

    hero = matches[0]
    roles_display = ", ".join(hero["roles"].split(","))
    aliases_display = ", ".join(hero["aliases"][:4])
    
    caption = (
        f"🦸‍♂️ <b>{hero['localized_name_ru']}</b> ({hero['localized_name']})\n\n"
        f"• <b>Основной атрибут</b>: {hero['primary_attr'].upper()}\n"
        f"• <b>Тип атаки</b>: {hero['attack_type']}\n"
        f"• <b>Роли</b>: {roles_display}\n"
        f"• <b>Сленг / алиасы</b>: {aliases_display}\n\n"
        f"Используйте WebApp для анализа драфта с этим героем!"
    )
    
    await message.answer_photo(
        photo=hero["icon_url"],
        caption=caption,
        parse_mode="HTML",
        reply_markup=get_main_keyboard()
    )
