# ⚔️ Dota 2 Draft Assistant (Telegram Mini App + FastAPI + aiogram 3)

Интеллектуальный математический ассистент для драфта и контр-пиков в Dota 2 с поддержкой Telegram WebApp, актуальной метой D2PT (Dota 2 Pro Tracker) и словарем СНГ-сленга героев.

---

## 📁 Структура проекта

```
├── requirements.txt            # Зависимости (FastAPI, aiogram 3, SQLAlchemy, curl_cffi, aiosqlite)
├── main.py                     # Запуск FastAPI + aiogram Bot параллельно в одном цикле
├── config.py                   # Переменные окружения (.env) и настройки
├── .env.example                # Шаблон конфигурации
├── database/
│   ├── db.py                   # Асинхронная сессия SQLAlchemy + aiosqlite
│   ├── models.py               # Модели: Hero, RoleStat (D2PT), Matchup (Dotabuff/OpenDota)
│   └── dota_draft.db           # Локальная база SQLite
├── services/
│   ├── draft_engine.py         # Математический движок ранжирования контр-пиков и синергий
│   ├── aliases.py              # Официальные имена (EN/RU), Steam CDN иконки и СНГ-сленг
│   └── scraper/
│       ├── seed_data.py        # Мгновенная инициализация базы + синхронизация OpenDota
│       ├── d2pt_scraper.py     # Скрапер Dota 2 Pro Tracker с обходом TLS через curl_cffi
│       └── dotabuff_scraper.py # Скрапер матчапов Dotabuff / OpenDota
├── bot/
│   └── handlers.py             # aiogram 3 хэндлеры, инлайн-клавиатура с WebApp кнопкой
└── static/
    ├── index.html              # Интерфейс Telegram Mini App (Tailwind CSS, Dark Mode)
    └── app.js                  # Клиентская логика, моментальный поиск и расчет драфта
```

---

## 🚀 Быстрый запуск

### 1. Активация виртуального окружения

Виртуальное окружение `.venv` уже создано и все зависимости установлены:
```powershell
.\.venv\Scripts\activate
```

### 2. Настройка бота (Опционально)
Скопируйте `.env.example` в `.env`:
```powershell
Copy-Item .env.example .env
```
Укажите токен вашего бота от `@BotFather` в `BOT_TOKEN`:
```env
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
WEBAPP_URL=http://localhost:8000
```
*(Если токен не указан, сервер FastAPI и веб-интерфейс работают автономно в браузере)*

### 3. Запуск приложения
```powershell
python main.py
```
Сервер запустится по адресу: **`http://localhost:8000`**

---

## 🎯 Возможности

1. **Telegram Mini App & Web**:
   - Адаптивный темный интерфейс в стиле Dota 2.
   - Полноценная интеграция с Telegram WebApp SDK (`Telegram.WebApp.ready()`, `expand()`).
2. **Словарь СНГ-сленга**:
   - Поиск понимает: *СФ, Гуля, Бара, Тракса, Мортра, Бабка, Потма, Магина, Корова, Леший, Пак, ДК, ЦМка, Котл, Бруда* и многие другие.
3. **Математическая модель скоринга**:
   - $Score = S_{meta} + S_{counter} + S_{synergy}$
   - Учитывает винрейт и тир героя на выбранной позиции (Поз 1–5), преимущества над вражеским пиком и синергии со способностями союзников.
4. **Автономность**:
   - При первом запуске база автоматически наполняется готовым срезом меты и контр-пиков, поэтому приложение работает мгновенно даже без интернета.
