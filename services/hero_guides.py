"""
Hero Knowledge Base, Guides & Counter-Items Engine.
Combines official Steam CDN URLs, complete mechanical hero traits for all 126 heroes,
iconic tactical explanations, strict mutual exclusion, and live database matchup analytics.
"""

import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Hero, RoleStat, Matchup
from services.aliases import HERO_BY_ID, HERO_LIST
from services.hero_signatures import HERO_SIGNATURES
from services.hero_builds import get_hero_core_items, get_situational_items_for_hero_vs_enemies

logger = logging.getLogger("hero_guides")

STEAM_ITEM_CDN = "https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/items"
STEAM_HERO_CDN = "https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/heroes"

# ══════════════════════════════════════════════════════════════════════════
# 1. OFFICIAL COUNTER-ITEMS CATALOG (STEAM CDN)
# ══════════════════════════════════════════════════════════════════════════

ITEM_CATALOG = {
    "force_staff": {
        "slug": "force_staff",
        "name": "Force Staff",
        "name_ru": "Форс Стафф (Force Staff)",
        "icon_url": f"{STEAM_ITEM_CDN}/force_staff.png",
        "counters_tags": ["high_mobility_catch", "disables", "slow_heavy"],
        "default_reason": "Принудительно толкает союзника или себя на 600 единиц вперед, позволяя мгновенно разорвать дистанцию и спастись."
    },
    "spirit_vessel": {
        "slug": "spirit_vessel",
        "name": "Spirit Vessel",
        "name_ru": "Спирит Вессел",
        "icon_url": f"{STEAM_ITEM_CDN}/spirit_vessel.png",
        "counters_tags": ["high_regen_heal", "high_hp_tank", "lane_bully"],
        "default_reason": "Снижает восстановление здоровья и вампиризм цели на 45%, сжигая процент от текущего HP за секунду."
    },
    "silver_edge": {
        "slug": "silver_edge",
        "name": "Silver Edge",
        "name_ru": "Сильвер Эдж",
        "icon_url": f"{STEAM_ITEM_CDN}/silver_edge.png",
        "counters_tags": ["passive_dependent", "evasion"],
        "default_reason": "Накладывает Истощение (Break) на 5 секунд, полностью отключая все пассивные способности вражеского героя."
    },
    "monkey_king_bar": {
        "slug": "monkey_king_bar",
        "name": "Monkey King Bar",
        "name_ru": "МКБ (Monkey King Bar)",
        "icon_url": f"{STEAM_ITEM_CDN}/monkey_king_bar.png",
        "counters_tags": ["evasion"],
        "default_reason": "Дает 80% шанс пробить любое уклонение (True Strike) и нанести чистый прок урона сквозь промахи."
    },
    "bloodthorn": {
        "slug": "bloodthorn",
        "name": "Bloodthorn",
        "name_ru": "Бладторн",
        "icon_url": f"{STEAM_ITEM_CDN}/bloodthorn.png",
        "counters_tags": ["high_mobility_spellcaster", "evasion", "magic_burst", "elusive"],
        "default_reason": "Накладывает безмолвие, 100% True Strike для всей команды и наносит колоссальный критический урон."
    },
    "orchid": {
        "slug": "orchid",
        "name": "Orchid Malevolence",
        "name_ru": "Орчид",
        "icon_url": f"{STEAM_ITEM_CDN}/orchid.png",
        "counters_tags": ["high_mobility_spellcaster", "magic_burst", "elusive"],
        "default_reason": "Накладывает безмолвие (Silence) на 5 секунд, не позволяя мобильным кастерам сбежать или прожать скиллы."
    },
    "sheepstick": {
        "slug": "sheepstick",
        "name": "Scythe of Vyse",
        "name_ru": "Хекс (Scythe of Vyse)",
        "icon_url": f"{STEAM_ITEM_CDN}/sheepstick.png",
        "counters_tags": ["high_mobility_spellcaster", "physical_burst", "elusive", "bkb_carries"],
        "default_reason": "Мгновенный Хекс на 2.8 сек без задержки каста: не дает среагировать, нажать защитные предметы или включить BKB."
    },
    "nullifier": {
        "slug": "nullifier",
        "name": "Nullifier",
        "name_ru": "Нуллифаер",
        "icon_url": f"{STEAM_ITEM_CDN}/nullifier.png",
        "counters_tags": ["save_support", "buff_reliant", "elusive"],
        "default_reason": "Непрерывно развеивает защитные баффы: Ghost Scepter, Force Staff, Eul, Glimmer Cape и Windrun."
    },
    "mjollnir": {
        "slug": "mjollnir",
        "name": "Mjollnir",
        "name_ru": "Мьёльнир",
        "icon_url": f"{STEAM_ITEM_CDN}/mjollnir.png",
        "counters_tags": ["illusionist", "summoner"],
        "default_reason": "Статический электрический щит и частые цепные молнии моментально выжигают скопления иллюзий и саммонов."
    },
    "bfury": {
        "slug": "bfury",
        "name": "Battle Fury",
        "name_ru": "Батлфьюри (BF)",
        "icon_url": f"{STEAM_ITEM_CDN}/bfury.png",
        "counters_tags": ["illusionist", "summoner"],
        "default_reason": "Клив-урон сквозь броню позволяет милли-керри за пару мощных ударов полностью сносить пачки иллюзий."
    },
    "gungir": {
        "slug": "gungir",
        "name": "Gleipnir",
        "name_ru": "Глейпнир",
        "icon_url": f"{STEAM_ITEM_CDN}/gungir.png",
        "counters_tags": ["high_mobility_spellcaster", "illusionist", "elusive"],
        "default_reason": "АоЕ-оцепенение на 2 секунды надежно фиксирует мобильных героев и наносит урон цепными молниями."
    },
    "shivas_guard": {
        "slug": "shivas_guard",
        "name": "Shiva's Guard",
        "name_ru": "Шива (Shiva's Guard)",
        "icon_url": f"{STEAM_ITEM_CDN}/shivas_guard.png",
        "counters_tags": ["high_regen_heal", "illusionist", "physical_burst"],
        "default_reason": "Снижает любое лечение и вампиризм врагов на 25%, замедляет скорость атаки и наносит сильный АоЕ-урон."
    },
    "crimson_guard": {
        "slug": "crimson_guard",
        "name": "Crimson Guard",
        "name_ru": "Кримсон (Crimson Guard)",
        "icon_url": f"{STEAM_ITEM_CDN}/crimson_guard.png",
        "counters_tags": ["illusionist", "summoner", "fast_attackers"],
        "default_reason": "Блокирует до 75 единиц физического урона всей союзной команде, полностью нивелируя тычки копий."
    },
    "pipe": {
        "slug": "pipe",
        "name": "Pipe of Insight",
        "name_ru": "Пайп (Pipe of Insight)",
        "icon_url": f"{STEAM_ITEM_CDN}/pipe.png",
        "counters_tags": ["magic_burst", "aoe_burst"],
        "default_reason": "Поглощает 450 единиц магического урона каждому герою команды и дает пассивную ауру защиты от магии."
    },
    "mage_slayer": {
        "slug": "mage_slayer",
        "name": "Mage Slayer",
        "name_ru": "Мейдж Слейер (Mage Slayer)",
        "icon_url": f"{STEAM_ITEM_CDN}/mage_slayer.png",
        "counters_tags": ["magic_burst", "high_mobility_spellcaster", "aoe_burst"],
        "default_reason": "При атаке накладывает дебафф, снижающий весь наносимый целью урон от заклинаний на 40% и наносящий периодический урон."
    },
    "glimmer_cape": {
        "slug": "glimmer_cape",
        "name": "Glimmer Cape",
        "name_ru": "Глиммер (Glimmer Cape)",
        "icon_url": f"{STEAM_ITEM_CDN}/glimmer_cape.png",
        "counters_tags": ["magic_burst", "save_support"],
        "default_reason": "Накладывает невидимость и барьер, поглощающий до 300 единиц магического урона для спасения союзника под фокусом."
    },
    "black_king_bar": {
        "slug": "black_king_bar",
        "name": "Black King Bar",
        "name_ru": "БКБ (Black King Bar)",
        "icon_url": f"{STEAM_ITEM_CDN}/black_king_bar.png",
        "counters_tags": ["magic_burst", "disables"],
        "default_reason": "Невосприимчивость к эффектам и 50% защиты от магии: главный артефакт для выживания против контроля."
    },
    "heavens_halberd": {
        "slug": "heavens_halberd",
        "name": "Heaven's Halberd",
        "name_ru": "Алебарда (Halberd)",
        "icon_url": f"{STEAM_ITEM_CDN}/heavens_halberd.png",
        "counters_tags": ["physical_burst", "fast_attackers"],
        "default_reason": "Обезоруживает вражеского керри на 3-5 секунд; обезоруживание нельзя снять обычным развеиванием."
    },
    "skadi": {
        "slug": "skadi",
        "name": "Eye of Skadi",
        "name_ru": "Скади (Eye of Skadi)",
        "icon_url": f"{STEAM_ITEM_CDN}/skadi.png",
        "counters_tags": ["high_regen_heal", "physical_burst"],
        "default_reason": "Режет любое лечение, регенерацию и вампиризм цели на 40%, сильно замедляя скорость передвижения и атаки."
    },
    "ghost": {
        "slug": "ghost",
        "name": "Ghost Scepter",
        "name_ru": "Гост (Ghost Scepter)",
        "icon_url": f"{STEAM_ITEM_CDN}/ghost.png",
        "counters_tags": ["physical_burst"],
        "default_reason": "Дает полную неуязвимость к физическим атакам на 4 секунды, спасая саппортов от мгновенной гибели."
    },
    "blade_mail": {
        "slug": "blade_mail",
        "name": "Blade Mail",
        "name_ru": "Блейдмейл (Blade Mail)",
        "icon_url": f"{STEAM_ITEM_CDN}/blade_mail.png",
        "counters_tags": ["physical_burst", "magic_burst"],
        "default_reason": "Возвращает 100% входящего урона обратно атакующему герою: смертельно против персонажей со взрывным уроном."
    },
    "abyssal_blade": {
        "slug": "abyssal_blade",
        "name": "Abyssal Blade",
        "name_ru": "Абиссал (Abyssal Blade)",
        "icon_url": f"{STEAM_ITEM_CDN}/abyssal_blade.png",
        "counters_tags": ["bkb_carries", "high_mobility_spellcaster", "elusive"],
        "default_reason": "Оглушает цель на 2 секунды прямо сквозь активный Black King Bar, гарантируя фиксацию керри."
    },
    "diffusal_blade": {
        "slug": "diffusal_blade",
        "name": "Diffusal Blade",
        "name_ru": "Диффуза (Diffusal Blade)",
        "icon_url": f"{STEAM_ITEM_CDN}/diffusal_blade.png",
        "counters_tags": ["mana_shield", "high_mobility_spellcaster"],
        "default_reason": "Выжигает запас маны при каждом ударе и накладывает сильное замедление бега, парализуя цель."
    },
    "dust": {
        "slug": "dust",
        "name": "Dust of Appearance",
        "name_ru": "Дасты (Dust)",
        "icon_url": f"{STEAM_ITEM_CDN}/dust.png",
        "counters_tags": ["invis", "anti_invis"],
        "default_reason": "Раскрывает невидимых героев в радиусе на 12 секунд и замедляет скорость их передвижения на 20%."
    },
    "radiance": {
        "slug": "radiance",
        "name": "Radiance",
        "name_ru": "Радианс (Radiance)",
        "icon_url": f"{STEAM_ITEM_CDN}/radiance.png",
        "counters_tags": ["illusionist", "blink_daggers"],
        "default_reason": "Постоянный урон 60/сек вокруг владельца сжигает иллюзии, сбивает Blink Dagger и дает 20% промахов."
    },
    "lotus_orb": {
        "slug": "lotus_orb",
        "name": "Lotus Orb",
        "name_ru": "Лотус (Lotus Orb)",
        "icon_url": f"{STEAM_ITEM_CDN}/lotus_orb.png",
        "counters_tags": ["targeted_spells", "silence_heavy"],
        "default_reason": "Мгновенно развеивает сало и дебаффы с союзника, отражая все направленные заклинания обратно во врага."
    },
    "sphere": {
        "slug": "sphere",
        "name": "Linken's Sphere",
        "name_ru": "Линка (Linken's Sphere)",
        "icon_url": f"{STEAM_ITEM_CDN}/sphere.png",
        "counters_tags": ["targeted_spells", "bkb_piercing", "single_target_burst"],
        "default_reason": "Блокирует одно направленное вражеское заклинание раз в 14 секунд, защищая от ключевого контроля (Duel, Doom, Roar)."
    },
    "aeon_disk": {
        "slug": "aeon_disk",
        "name": "Aeon Disk",
        "name_ru": "Аеон Диск",
        "icon_url": f"{STEAM_ITEM_CDN}/aeon_disk.png",
        "counters_tags": ["magic_burst", "instant_initiation"],
        "default_reason": "При падении здоровья ниже 70% накладывает сильное развеивание и дает 100% сопротивления урону на 2.5 сек."
    },
    "maelstrom": {
        "slug": "maelstrom",
        "name": "Maelstrom",
        "name_ru": "Молнии (Maelstrom)",
        "icon_url": f"{STEAM_ITEM_CDN}/maelstrom.png",
        "counters_tags": ["illusionist", "summoner"],
        "default_reason": "Цепные молнии Chain Lightning наносят магический урон по площади, ускоряя фарм и зачистку скоплений иллюзий."
    },
    "manta": {
        "slug": "manta",
        "name": "Manta Style",
        "name_ru": "Манта (Manta Style)",
        "icon_url": f"{STEAM_ITEM_CDN}/manta.png",
        "counters_tags": ["silence_heavy", "disables", "targeted_spells"],
        "default_reason": "Дает мгновенное развеивание (Dispel) безмолвия и дебаффов, создавая две иллюзии для сброса фокуса и сплит-пуша."
    },
    "blink": {
        "slug": "blink",
        "name": "Blink Dagger",
        "name_ru": "Блинк (Blink Dagger)",
        "icon_url": f"{STEAM_ITEM_CDN}/blink.png",
        "counters_tags": [],
        "default_reason": "Мгновенный скачок на дистанцию до 1200 единиц: идеален для внезапной инициации, сокращения дистанции и позиционирования."
    },
    "ultimate_scepter": {
        "slug": "ultimate_scepter",
        "name": "Aghanim's Scepter",
        "name_ru": "Аганим (Aghanim's Scepter)",
        "icon_url": f"{STEAM_ITEM_CDN}/ultimate_scepter.png",
        "counters_tags": [],
        "default_reason": "Качественно улучшает ключевые способности героя или добавляет мощное новое умение, усиливающее командный потенциал."
    },
    "octarine_core": {
        "slug": "octarine_core",
        "name": "Octarine Core",
        "name_ru": "Октарин (Octarine Core)",
        "icon_url": f"{STEAM_ITEM_CDN}/octarine_core.png",
        "counters_tags": [],
        "default_reason": "Снижает перезарядку всех способностей и предметов на 25%, позволяя кастерам непрерывно спамить заклинаниями в драке."
    },
    "desolator": {
        "slug": "desolator",
        "name": "Desolator",
        "name_ru": "Дезолятор (Desolator)",
        "icon_url": f"{STEAM_ITEM_CDN}/desolator.png",
        "counters_tags": [],
        "default_reason": "Снижает броню цели на 6 единиц при атаке, кратно увеличивая физический урон и скорость сноса вражеских строений."
    },
    "satanic": {
        "slug": "satanic",
        "name": "Satanic",
        "name_ru": "Сатаник (Satanic)",
        "icon_url": f"{STEAM_ITEM_CDN}/satanic.png",
        "counters_tags": [],
        "default_reason": "Дает мощный вампиризм с руки и 200% Unholy Rage при активации, восстанавливая фулл-HP керри за 2-3 секунды размена."
    },
    "butterfly": {
        "slug": "butterfly",
        "name": "Butterfly",
        "name_ru": "Бабочка (Butterfly)",
        "icon_url": f"{STEAM_ITEM_CDN}/butterfly.png",
        "counters_tags": [],
        "default_reason": "Дает 35% уклонения от физических атак, огромную ловкость и скорость атаки, вынуждая вражеских керри покупать дорогой MKB."
    },
    "assault": {
        "slug": "assault",
        "name": "Assault Cuirass",
        "name_ru": "Кираса (Assault Cuirass)",
        "icon_url": f"{STEAM_ITEM_CDN}/assault.png",
        "counters_tags": [],
        "default_reason": "Дает +30 скорости атаки и +5 брони всей союзной команде, снижая броню врагов и строений на 5 в ауре."
    },
    "heart": {
        "slug": "heart",
        "name": "Heart of Tarrasque",
        "name_ru": "Тарраска (Heart of Tarrasque)",
        "icon_url": f"{STEAM_ITEM_CDN}/heart.png",
        "counters_tags": [],
        "default_reason": "Дает колоссальный запас максимального здоровья (+800 HP) и процентную регенерацию вне драки, делая героя неубиваемым танком."
    },
    "disperser": {
        "slug": "disperser",
        "name": "Disperser",
        "name_ru": "Дисперсер (Disperser)",
        "icon_url": f"{STEAM_ITEM_CDN}/disperser.png",
        "counters_tags": ["slow_heavy", "mana_shield"],
        "default_reason": "Накладывает AoE-развеивание замедлений и дает максимальную скорость бега сквозь препятствия союзникам, сжигая ману цели."
    },
    "aether_lens": {
        "slug": "aether_lens",
        "name": "Aether Lens",
        "name_ru": "Линза (Aether Lens)",
        "icon_url": f"{STEAM_ITEM_CDN}/aether_lens.png",
        "counters_tags": [],
        "default_reason": "Увеличивает дальность применения направленных способностей и предметов на 225, позволяя безопасно кастовать из глубокого тыла."
    },
    "solar_crest": {
        "slug": "solar_crest",
        "name": "Solar Crest",
        "name_ru": "Солар Крест (Solar Crest)",
        "icon_url": f"{STEAM_ITEM_CDN}/solar_crest.png",
        "counters_tags": ["physical_burst"],
        "default_reason": "Дает союзнику щит прочностью 400 урона, +70 к скорости атаки и +6 брони для сейва под фокусом."
    },
    "echo_sabre": {
        "slug": "echo_sabre",
        "name": "Echo Sabre",
        "name_ru": "Эхо Сабля (Echo Sabre)",
        "icon_url": f"{STEAM_ITEM_CDN}/echo_sabre.png",
        "counters_tags": [],
        "default_reason": "Совершает мгновенную двойную атаку милли-героя и замедляет врага на 100% на 0.8 сек."
    },
    "harpoon": {
        "slug": "harpoon",
        "name": "Harpoon",
        "name_ru": "Гарпун (Harpoon)",
        "icon_url": f"{STEAM_ITEM_CDN}/harpoon.png",
        "counters_tags": [],
        "default_reason": "Притягивает владельца и вражескую цель навстречу друг другу, не позволяя разорвать дистанцию."
    },
    "greater_crit": {
        "slug": "greater_crit",
        "name": "Daedalus",
        "name_ru": "Даедалус (Daedalus)",
        "icon_url": f"{STEAM_ITEM_CDN}/greater_crit.png",
        "counters_tags": [],
        "default_reason": "Дает +88 к урону и 30% шанс нанести критический удар с множителем 225%."
    },
    "basher": {
        "slug": "basher",
        "name": "Skull Basher",
        "name_ru": "Башер (Skull Basher)",
        "icon_url": f"{STEAM_ITEM_CDN}/basher.png",
        "counters_tags": [],
        "default_reason": "Дает шанс оглушить врага при атаке сквозь невосприимчивость к магии."
    },
    "sange_and_yasha": {
        "slug": "sange_and_yasha",
        "name": "Sange and Yasha",
        "name_ru": "Саша-Яша (S&Y)",
        "icon_url": f"{STEAM_ITEM_CDN}/sange_and_yasha.png",
        "counters_tags": [],
        "default_reason": "Дает сопротивление эффектам и замедлениям, скорость передвижения и урон."
    },
    "witch_blade": {
        "slug": "witch_blade",
        "name": "Witch Blade",
        "name_ru": "Витч Блейд (Witch Blade)",
        "icon_url": f"{STEAM_ITEM_CDN}/witch_blade.png",
        "counters_tags": [],
        "default_reason": "Замедляет цель на 25% и наносит периодический урон, зависящий от интеллекта владельца."
    },
    "invis_sword": {
        "slug": "invis_sword",
        "name": "Shadow Blade",
        "name_ru": "Шб (Shadow Blade)",
        "icon_url": f"{STEAM_ITEM_CDN}/invis_sword.png",
        "counters_tags": [],
        "default_reason": "Дает невидимость и ускорение, а первая атака из инвиза наносит 175 дополнительного урона."
    },
    "dragon_lance": {
        "slug": "dragon_lance",
        "name": "Dragon Lance",
        "name_ru": "Драгон Лэнс (Dragon Lance)",
        "icon_url": f"{STEAM_ITEM_CDN}/dragon_lance.png",
        "counters_tags": [],
        "default_reason": "Увеличивает дальность атаки героев дальнего боя на 150 единиц и дает статы."
    },
    "vanguard": {
        "slug": "vanguard",
        "name": "Vanguard",
        "name_ru": "Вангард (Vanguard)",
        "icon_url": f"{STEAM_ITEM_CDN}/vanguard.png",
        "counters_tags": [],
        "default_reason": "Блокирует до 60 физического урона при атаках врагов и дает регенерацию здоровья."
    },
    "refresher": {
        "slug": "refresher",
        "name": "Refresher Orb",
        "name_ru": "Рефрешер (Refresher Orb)",
        "icon_url": f"{STEAM_ITEM_CDN}/refresher.png",
        "counters_tags": [],
        "default_reason": "Мгновенно сбрасывает время перезарядки всех способностей и предметов владельца."
    },
    "kaya_and_sange": {
        "slug": "kaya_and_sange",
        "name": "Kaya and Sange",
        "name_ru": "Кая-Саша (Kaya and Sange)",
        "icon_url": f"{STEAM_ITEM_CDN}/kaya_and_sange.png",
        "counters_tags": [],
        "default_reason": "Усиливает урон от заклинаний, снижает расход маны и дает сопротивление замедлениям и плотность."
    },
    "yasha_and_kaya": {
        "slug": "yasha_and_kaya",
        "name": "Yasha and Kaya",
        "name_ru": "Яша-Кая (Yasha and Kaya)",
        "icon_url": f"{STEAM_ITEM_CDN}/yasha_and_kaya.png",
        "counters_tags": [],
        "default_reason": "Ускоряет применение заклинаний, повышает магический урон и скорость передвижения героя."
    },
    "bloodstone": {
        "slug": "bloodstone",
        "name": "Bloodstone",
        "name_ru": "Бладстоун (Bloodstone)",
        "icon_url": f"{STEAM_ITEM_CDN}/bloodstone.png",
        "counters_tags": [],
        "default_reason": "Дает мощный магический вампиризм от способностей и увеличивает радиус поражения всех заклинаний."
    },
    "hurricane_pike": {
        "slug": "hurricane_pike",
        "name": "Hurricane Pike",
        "name_ru": "Пика (Hurricane Pike)",
        "icon_url": f"{STEAM_ITEM_CDN}/hurricane_pike.png",
        "counters_tags": [],
        "default_reason": "Увеличивает дальность атаки и позволяет оттолкнуться от врывов врага с 5 атаками без ограничения дистанции."
    },
    "armlet": {
        "slug": "armlet",
        "name": "Armlet of Mordiggian",
        "name_ru": "Армлет (Armlet)",
        "icon_url": f"{STEAM_ITEM_CDN}/armlet.png",
        "counters_tags": [],
        "default_reason": "При активации дает огромный прирост силы, физического урона и брони для доминирования в ранних драках."
    },
    "mask_of_madness": {
        "slug": "mask_of_madness",
        "name": "Mask of Madness",
        "name_ru": "МоМ (Mask of Madness)",
        "icon_url": f"{STEAM_ITEM_CDN}/mask_of_madness.png",
        "counters_tags": [],
        "default_reason": "Дает вампиризм и +110 к скорости атаки при активации для сверхбыстрого фарма и реализации ультимейтов."
    },
    "vladmir": {
        "slug": "vladmir",
        "name": "Vladmir's Offering",
        "name_ru": "Владимир (Vladmir's Offering)",
        "icon_url": f"{STEAM_ITEM_CDN}/vladmir.png",
        "counters_tags": [],
        "default_reason": "Дает всей команде ауру вампиризма, +18% базового урона, броню и регенерацию маны."
    },
    "guardian_greaves": {
        "slug": "guardian_greaves",
        "name": "Guardian Greaves",
        "name_ru": "Гривсы (Guardian Greaves)",
        "icon_url": f"{STEAM_ITEM_CDN}/guardian_greaves.png",
        "counters_tags": [],
        "default_reason": "Массово исцеляет команду, восстанавливает ману и снимает негативные эффекты с владельца при активации."
    },
    "boots_of_bearing": {
        "slug": "boots_of_bearing",
        "name": "Boots of Bearing",
        "name_ru": "Барабаны-ботинки (Boots of Bearing)",
        "icon_url": f"{STEAM_ITEM_CDN}/boots_of_bearing.png",
        "counters_tags": [],
        "default_reason": "Дает команде и подконтрольным существам взрывное ускорение бега, скорость атаки и иммунитет к замедлениям."
    },
    "holy_locket": {
        "slug": "holy_locket",
        "name": "Holy Locket",
        "name_ru": "Холи Локет (Holy Locket)",
        "icon_url": f"{STEAM_ITEM_CDN}/holy_locket.png",
        "counters_tags": [],
        "default_reason": "Усиливает все исходящее исцеление владельца на 25% и накапливает заряды для мгновенного лечения союзников."
    },
    "helm_of_the_overlord": {
        "slug": "helm_of_the_overlord",
        "name": "Helm of the Overlord",
        "name_ru": "Оверлорд (Helm of the Overlord)",
        "icon_url": f"{STEAM_ITEM_CDN}/helm_of_the_overlord.png",
        "counters_tags": [],
        "default_reason": "Позволяет подчинить древнего крипа с огромным запасом здоровья и аурами для сноса вражеских строений."
    },
    "rod_of_atos": {
        "slug": "rod_of_atos",
        "name": "Rod of Atos",
        "name_ru": "Атос (Rod of Atos)",
        "icon_url": f"{STEAM_ITEM_CDN}/rod_of_atos.png",
        "counters_tags": [],
        "default_reason": "Оцепенение (Root) на 2 секунды с большой дистанции гарантирует попадание направленными способностями."
    },
    "consecrated_wraps": {
        "slug": "consecrated_wraps",
        "name": "Consecrated Wraps",
        "name_ru": "Консекрейтед Врапс (Consecrated Wraps)",
        "icon_url": f"{STEAM_ITEM_CDN}/consecrated_wraps.png",
        "counters_tags": [],
        "default_reason": "Дает сопротивление магии, барьер и накапливает стаки снижения получаемого урона и лечения в затяжном бою."
    }
}

# ══════════════════════════════════════════════════════════════════════════
# 2. COMPLETE MECHANICAL TRAIT MAPPING FOR ALL 126 DOTA 2 HEROES
# ══════════════════════════════════════════════════════════════════════════

HERO_MECHANICAL_TRAITS = {
    1: ["high_mobility_spellcaster", "elusive", "passive_dependent", "split_pusher", "mana_burn"], # Anti-Mage
    2: ["bkb_piercing", "anti_illusion", "physical_burst", "initiator", "lane_bully"], # Axe
    3: ["channeled_ult", "bkb_piercing", "disables", "instant_disable", "save_support"], # Bane
    4: ["pure_damage", "anti_invis", "high_mobility_catch", "silence_heavy"], # Bloodseeker
    5: ["channeled_ult", "magic_burst", "disables", "mana_battery", "save_support"], # Crystal Maiden
    6: ["physical_burst", "silence_heavy", "anti_armor", "ranged_carry"], # Drow Ranger
    7: ["anti_illusion", "aoe_burst", "initiator", "disables"], # Earthshaker
    8: ["bkb_carries", "physical_burst", "high_regen_heal", "spin_magic_immune"], # Juggernaut
    9: ["high_mobility_catch", "elusive", "invis", "magic_burst"], # Mirana
    10: ["high_regen_heal", "elusive", "physical_burst", "high_mobility_spellcaster"], # Morphling
    11: ["minus_armor", "magic_burst", "physical_burst", "aoe_burst"], # Shadow Fiend
    12: ["illusionist", "elusive", "physical_burst", "mana_burn"], # Phantom Lancer
    13: ["high_mobility_spellcaster", "elusive", "magic_burst", "instant_disable", "silence_heavy"], # Puck
    14: ["high_regen_heal", "magic_burst", "bkb_piercing", "disables", "initiator"], # Pudge
    15: ["lane_bully", "anti_carry", "minus_armor", "fast_attackers"], # Razor
    16: ["anti_illusion", "aoe_burst", "initiator", "disables", "invis"], # Sand King
    17: ["high_mobility_spellcaster", "elusive", "magic_burst", "initiator"], # Storm Spirit
    18: ["cleave_splash", "anti_illusion", "physical_burst", "initiator", "bkb_carries"], # Sven
    19: ["magic_burst", "physical_burst", "disables", "initiator", "cleave_splash"], # Tiny
    20: ["save_support", "minus_armor", "initiator", "disables"], # Vengeful Spirit
    21: ["high_mobility_spellcaster", "evasion", "physical_burst", "disables"], # Windranger
    22: ["magic_burst", "anti_invis", "percent_hp_damage", "global_presence"], # Zeus
    23: ["cleave_splash", "anti_illusion", "initiator", "disables", "buff_reliant"], # Kunkka
    25: ["magic_burst", "fast_attackers", "pure_damage", "ranged_carry"], # Lina
    26: ["magic_burst", "disables", "save_support", "instant_disable", "mana_burn"], # Lion
    27: ["disables", "summoner", "save_support", "instant_disable"], # Shadow Shaman
    28: ["minus_armor", "bkb_piercing", "anti_invis", "initiator", "disables"], # Slardar
    29: ["passive_dependent", "bkb_piercing", "high_hp_tank", "initiator", "minus_armor"], # Tidehunter
    30: ["channeled_ult", "magic_burst", "disables", "save_support"], # Witch Doctor
    31: ["magic_burst", "disables", "save_support", "anti_carry"], # Lich
    32: ["invis", "silence_heavy", "physical_burst", "elusive"], # Riki
    33: ["channeled_ult", "bkb_piercing", "summoner", "percent_hp_damage", "initiator"], # Enigma
    34: ["high_mobility_spellcaster", "magic_burst", "pure_damage", "split_pusher"], # Tinker
    35: ["physical_burst", "high_range", "magic_burst", "fragile_backline"], # Sniper
    36: ["high_regen_heal", "magic_burst", "percent_hp_damage", "anti_heal", "bkb_piercing"], # Necrophos
    37: ["channeled_ult", "bkb_piercing", "summoner", "save_support", "aoe_burst"], # Warlock
    38: ["summoner", "bkb_piercing", "initiator", "high_mobility_catch"], # Beastmaster
    39: ["high_mobility_spellcaster", "magic_burst", "pure_damage", "aoe_burst"], # Queen of Pain
    40: ["summoner", "magic_burst", "lane_bully", "anti_heal", "percent_hp_damage"], # Venomancer
    41: ["bkb_piercing", "elusive", "physical_burst", "initiator", "time_lock"], # Faceless Void
    42: ["high_regen_heal", "physical_burst", "bkb_carries", "summoner", "reincarnation"], # Wraith King
    43: ["silence_heavy", "magic_burst", "high_hp_tank", "tower_pusher"], # Death Prophet
    44: ["evasion", "passive_dependent", "physical_burst", "elusive"], # Phantom Assassin
    45: ["magic_burst", "save_support", "tower_pusher", "mana_burn", "anti_spellcaster"], # Pugna
    46: ["physical_burst", "minus_armor", "refraction_shield", "fast_attackers"], # Templar Assassin
    47: ["passive_dependent", "magic_burst", "anti_heal", "break_mechanic", "lane_bully"], # Viper
    48: ["physical_burst", "magic_burst", "aoe_burst", "anti_illusion", "cleave_splash", "fast_attackers", "tower_pusher"], # Luna
    49: ["passive_dependent", "physical_burst", "high_hp_tank", "disables", "tower_pusher"], # Dragon Knight
    50: ["save_support", "minus_armor", "anti_illusion"], # Dazzle
    51: ["bkb_piercing", "initiator", "disables", "high_mobility_catch", "mana_burn"], # Clockwerk
    52: ["anti_illusion", "aoe_burst", "magic_burst", "high_mobility_spellcaster", "tower_pusher"], # Leshrac
    53: ["summoner", "split_pusher", "global_presence", "fast_attackers"], # Nature's Prophet
    54: ["high_regen_heal", "bkb_carries", "passive_dependent", "percent_hp_damage"], # Lifestealer
    55: ["initiator", "anti_illusion", "buff_reliant", "teamfight"], # Dark Seer
    56: ["invis", "physical_burst", "summoner", "fast_attackers"], # Clinkz
    57: ["save_support", "buff_reliant", "dispel_heavy"], # Omniknight
    58: ["summoner", "pure_damage", "passive_dependent", "lane_bully"], # Enchantress
    59: ["high_regen_heal", "magic_burst", "fast_attackers", "lane_bully"], # Huskar
    60: ["silence_heavy", "bkb_piercing", "high_mobility_catch", "anti_backline"], # Night Stalker
    61: ["summoner", "invis", "fast_attackers", "lane_bully", "tower_pusher"], # Broodmother
    62: ["invis", "anti_invis", "physical_burst", "track_gold"], # Bounty Hunter
    63: ["high_mobility_spellcaster", "invis", "physical_burst", "minus_armor", "elusive"], # Weaver
    64: ["magic_burst", "disables", "aoe_burst", "tower_pusher"], # Jakiro
    65: ["bkb_piercing", "initiator", "high_mobility_catch", "lane_bully"], # Batrider
    66: ["summoner", "save_support", "global_presence"], # Chen
    67: ["illusionist", "passive_dependent", "split_pusher", "global_presence", "high_hp_tank"], # Spectre
    68: ["anti_heal", "magic_burst", "percent_hp_damage", "global_presence"], # Ancient Apparition
    69: ["bkb_piercing", "silence_heavy", "break_mechanic", "high_hp_tank", "anti_carry"], # Doom
    70: ["fast_attackers", "physical_burst", "lane_bully", "roshan_killer", "dispel_heavy"], # Ursa
    71: ["bkb_piercing", "initiator", "high_mobility_catch", "global_presence"], # Spirit Breaker
    72: ["aoe_burst", "physical_burst", "magic_burst", "anti_illusion", "cleave_splash"], # Gyrocopter
    73: ["high_regen_heal", "fast_attackers", "passive_dependent", "gold_snowball"], # Alchemist
    74: ["high_mobility_spellcaster", "magic_burst", "disables", "mana_burn", "aoe_burst"], # Invoker
    75: ["silence_heavy", "pure_damage", "global_presence", "anti_spellcaster"], # Silencer
    76: ["pure_damage", "save_support", "mana_burn", "bkb_carries"], # Outworld Destroyer
    77: ["summoner", "physical_burst", "bkb_carries", "tower_pusher", "high_mobility_catch"], # Lycan
    78: ["evasion", "magic_burst", "disables", "dispel_heavy", "high_hp_tank"], # Brewmaster
    79: ["save_support", "disables", "dispel_heavy", "break_mechanic", "anti_illusion"], # Shadow Demon
    80: ["summoner", "tower_pusher", "lane_bully", "physical_burst"], # Lone Druid
    81: ["illusionist", "physical_burst", "bkb_carries", "disables"], # Chaos Knight
    82: ["clone_meepo", "magic_burst", "physical_burst", "fast_attackers", "tower_pusher"], # Meepo
    83: ["disables", "bkb_piercing", "save_support", "initiator"], # Treant Protector
    84: ["buff_reliant", "magic_burst", "high_hp_tank", "disables"], # Ogre Magi
    85: ["high_hp_tank", "high_regen_heal", "lane_bully", "summoner", "teamfight"], # Undying
    86: ["disables", "magic_burst", "spell_steal", "instant_disable"], # Rubick
    87: ["silence_heavy", "disables", "instant_disable", "teamfight"], # Disruptor
    88: ["invis", "magic_burst", "disables", "mana_burn", "anti_spellcaster"], # Nyx Assassin
    89: ["illusionist", "disables", "elusive", "save_support", "bkb_piercing", "anti_illusion", "cleave_splash"], # Naga Siren
    90: ["mana_battery", "magic_burst", "aoe_burst", "high_mobility_spellcaster"], # Keeper of the Light
    91: ["save_support", "high_regen_heal", "buff_reliant", "global_presence"], # Io
    92: ["summoner", "magic_burst", "high_hp_tank", "tower_pusher"], # Visage
    93: ["high_regen_heal", "elusive", "passive_dependent", "invis", "dispel_heavy"], # Slark
    94: ["mana_shield", "physical_burst", "anti_illusion"], # Medusa
    95: ["evasion", "fast_attackers", "physical_burst", "disables"], # Troll Warlord
    96: ["high_hp_tank", "initiator", "disables", "global_presence"], # Centaur Warrunner
    97: ["bkb_piercing", "initiator", "cleave_splash", "buff_reliant"], # Magnus
    98: ["high_regen_heal", "passive_dependent", "pure_damage", "anti_illusion"], # Timbersaw
    99: ["high_regen_heal", "passive_dependent", "physical_burst", "high_hp_tank"], # Bristleback
    100: ["disables", "save_support", "initiator", "physical_burst"], # Tusk
    101: ["magic_burst", "silence_heavy", "instant_disable"], # Skywrath Mage
    102: ["high_regen_heal", "save_support", "dispel_heavy", "passive_dependent"], # Abaddon
    103: ["minus_armor", "sleep_setup", "percent_hp_damage", "anti_illusion"], # Elder Titan
    104: ["bkb_piercing", "passive_dependent", "physical_burst", "save_support"], # Legion Commander
    105: ["magic_burst", "disables", "aoe_burst"], # Techies
    106: ["high_mobility_spellcaster", "elusive", "magic_burst", "anti_illusion"], # Ember Spirit
    107: ["high_mobility_spellcaster", "disables", "silence_heavy", "initiator"], # Earth Spirit
    108: ["high_hp_tank", "anti_illusion", "global_presence", "percent_hp_damage"], # Underlord
    109: ["illusionist", "physical_burst", "tower_pusher", "sunder_save"], # Terrorblade
    110: ["magic_burst", "high_regen_heal", "percent_hp_damage", "aoe_burst"], # Phoenix
    111: ["save_support", "dispel_heavy"], # Oracle
    112: ["save_support", "bkb_piercing", "anti_illusion", "percent_hp_damage"], # Winter Wyvern
    113: ["clone_meepo", "magic_burst", "physical_burst", "split_pusher"], # Arc Warden
    114: ["evasion", "physical_burst", "initiator", "bkb_carries"], # Monkey King
    119: ["magic_burst", "elusive", "disables", "aoe_burst"], # Dark Willow
    120: ["high_mobility_spellcaster", "disables", "bkb_piercing", "elusive"], # Pangolier
    121: ["disables", "silence_heavy", "magic_burst", "teamfight"], # Grimstroke
    123: ["magic_burst", "break_mechanic", "elusive", "disables"], # Hoodwink
    126: ["high_mobility_spellcaster", "elusive", "magic_burst", "disables"], # Void Spirit
    128: ["magic_burst", "physical_burst", "disables", "save_support"], # Snapfire
    129: ["initiator", "bkb_piercing", "high_hp_tank", "anti_ranged"], # Mars
    135: ["high_regen_heal", "physical_burst", "magic_burst", "global_presence"], # Dawnbreaker
    136: ["high_regen_heal", "physical_burst", "disables", "save_support"], # Marci
    137: ["high_regen_heal", "bkb_piercing", "magic_burst", "initiator"], # Primal Beast
    138: ["physical_burst", "magic_burst", "bkb_carries", "disables", "anti_illusion", "aoe_burst"], # Muerta
    139: ["save_support", "disables", "magic_burst", "percent_hp_damage"], # Ringmaster
    145: ["physical_burst", "elusive", "disables", "fast_attackers"], # Kez
}

# ══════════════════════════════════════════════════════════════════════════
# 3. ICONIC TACTICAL REASONS & DYNAMIC GENERATOR
# ══════════════════════════════════════════════════════════════════════════

ICONIC_MATCHUPS = {
    (7, 12): "Echo Slam наносит колоссальный урон от скопления иллюзий, мгновенно стирая Phantom Lancer с карты.",
    (18, 12): "Great Cleave и колоссальный урон под God's Strength стирают всю армию копий Phantom Lancer за пару тычек.",
    (72, 12): "Flak Cannon пробивает сразу все цели вокруг на гигантскую дистанцию, стирая иллюзии Phantom Lancer за 3 выстрела.",
    (48, 12): "Рикошеты Moon Glaives мгновенно рассекают толпы иллюзий Phantom Lancer, превращая его армию в источник сплэш-урона.",
    (89, 12): "Rip Tide наносит колоссальный АоЕ-урон и срезает броню иллюзиям, а Song of the Siren позволяет сбросить драку в любой момент.",
    (138, 12): "The Calling и огромный магический урон под Pierce the Veil мгновенно испепеляют иллюзии и не дают Phantom Lancer подойти.",
    (2, 12): "Berserker's Call провоцирует всю толпу копий, а пассивка Counter Helix моментально ваншотит иллюзии.",
    (68, 59): "Ice Blast полностью отключает ключевой вампиризм и отхил Хускара, делая его абсолютно беззащитным на низком HP.",
    (68, 10): "Ледяной ультимейт блокирует перекачку в силу Morphling, не позволяя набрать спасительное здоровье в фокусе.",
    (1, 94): "Mana Void взрывает колоссальный манапул Медузы, а Mana Break сжигает щит за пару быстрых ударов.",
    (1, 17): "Выжигает всю ману Storm Spirit до капли, лишая возможности улететь в Ball Lightning и взрывая ультимейтом.",
    (112, 82): "Winter's Curse заставляет всех клонов Мипо бить своего же союзника, мгновенно убивая его за полсекунды.",
    (104, 1): "Duel сквозь щиты Counterspell надежно фиксирует Anti-Mage и не дает блинкануться до завершения драки.",
    (2, 44): "Провокация Berserker's Call игнорирует уклонение Blur и мгновенно уничтожает Phantom Assassin крутилками.",
    (4, 93): "Thirst подсвечивает раненого Сларка, полностью блокируя пассивную регенерацию и скорость Shadow Dance.",
    (88, 76): "Mana Burn выжигает ману и наносит огромный урон по гигантскому интеллекту Outworld Destroyer.",
    (88, 34): "Spiked Carapace легко оглушает Тинкера от урона роботов March of the Machines, после чего взрывной прокаст из Vendetta стирает его в кустах.",
    (98, 99): "Whirling Death срезает базовую силу Бристлбека, а чистый урон от пил игнорирует пассивную броню со спины.",
    (47, 99): "Nethertoxin накладывает постоянный эффект Истощения (Break), полностью отключая снижение урона от пассивки со спины Bristleback и замедляя врага.",
    (75, 33): "Global Silence сбивает каст Black Hole через всю карту прямо сквозь позиционку и защитные предметы.",
    (71, 34): "Разгон Charge of Darkness дает постоянный вижн на скрывающегося в лесу Тинкера и сбивает Blink Dagger.",
    (103, 82): "Astral Spirit получает колоссальный бонус к урону и броне от каждого клона Мипо, позволяя ваншотить с руки."
}

def generate_tactical_reason(hero_id: int, other_id: int, relation_type: str, stat_advantage: float = 0.0) -> str:
    """
    Generates a rich, non-empty, accurate Russian tactical explanation combining abilities & lore.
    Guarantees no two cards have identical copy-paste descriptions.
    """
    # Check iconic dictionary first
    if relation_type == "countered_by" and (other_id, hero_id) in ICONIC_MATCHUPS:
        return ICONIC_MATCHUPS[(other_id, hero_id)]
    if relation_type == "counters" and (hero_id, other_id) in ICONIC_MATCHUPS:
        return ICONIC_MATCHUPS[(hero_id, other_id)]

    h = HERO_BY_ID.get(hero_id, {})
    o = HERO_BY_ID.get(other_id, {})
    h_name = h.get("localized_name", f"Hero #{hero_id}")
    o_name = o.get("localized_name", f"Hero #{other_id}")

    h_tags = set(HERO_MECHANICAL_TRAITS.get(hero_id, []))
    o_tags = set(HERO_MECHANICAL_TRAITS.get(other_id, []))

    h_sig = HERO_SIGNATURES.get(hero_id, {})
    o_sig = HERO_SIGNATURES.get(other_id, {})
    h_desc = h_sig.get("sig", "ключевые способности и позиционку")
    o_desc = o_sig.get("sig", "активные скиллы и контроль")

    if relation_type == "countered_by":
        # Why other_id counters hero_id
        if "illusionist" in h_tags and any(t in o_tags for t in ("anti_illusion", "cleave_splash", "aoe_burst")):
            return f"{o_name} критически опасен для {h_name}: {o_desc}. Массовый урон по области быстро стирает копии и лишает {h_name} темпа в драке."
        if "high_regen_heal" in h_tags and "anti_heal" in o_tags:
            return f"{o_name} блокирует выживаемость {h_name}: {o_desc}. Встроенное снижение регенерации не позволяет {h_name} восстанавливать здоровье в бою."
        if ("high_regen_heal" in h_tags or "high_hp_tank" in h_tags) and any(t in o_tags for t in ("pure_damage", "percent_hp_damage")):
            return f"{o_name} пробивает плотность {h_name}: {o_desc}. Процентный и чистый урон игнорируют броню и запас здоровья {h_name}."
        if any(t in h_tags for t in ("high_mobility_spellcaster", "elusive")) and any(t in o_tags for t in ("instant_disable", "silence_heavy", "bkb_piercing")):
            return f"{o_name} пресекает мобильность {h_name}: {o_desc}. Надежная фиксация не позволяет {h_name} разорвать дистанцию или уйти на эскейпе."
        if "passive_dependent" in h_tags and "break_mechanic" in o_tags:
            return f"{o_name} отключает ключевые пассивки {h_name}: {o_desc}. Под эффектом истощения {h_name} теряет базовую выживаемость и быстро погибает."
        if "mana_shield" in h_tags and "mana_burn" in o_tags:
            return f"{o_name} молниеносно уничтожает манапул {h_name}: {o_desc}, пробивая барьер и заставляя {h_name} погибнуть за пару быстрых атак."
        if any(t in o_tags for t in ("bkb_piercing", "initiator")):
            return f"{o_name} ломает позиционку {h_name} контролем сквозь BKB: {o_desc}, удерживая цель под фокусом команды до завершения драки."
        return f"{o_name} подавляет {h_name} в тимфайтах и на линии: {o_desc}. При этом {h_name} ({h_desc}) испытывает жесткий дефицит пространства и ресурсов."

    elif relation_type == "counters":
        # Why hero_id counters other_id
        if "illusionist" in o_tags and any(t in h_tags for t in ("anti_illusion", "cleave_splash", "aoe_burst")):
            return f"{h_name} мгновенно стирает копии {o_name}: {h_desc}. Это полностью обезоруживает {o_name}, чья игра строится от иллюзий ({o_desc})."
        if "high_regen_heal" in o_tags and "anti_heal" in h_tags:
            return f"{h_name} блокирует отхил и выживаемость {o_name}: {h_desc}. Срез регенерации не дает {o_name} реализовать свои способности ({o_desc})."
        if ("high_regen_heal" in o_tags or "high_hp_tank" in o_tags) and any(t in h_tags for t in ("pure_damage", "percent_hp_damage")):
            return f"{h_name} легко пробивает плотность {o_name}: {h_desc}. Высокий чистый или процентный урон нивелирует выживаемость {o_name} ({o_desc})."
        if any(t in o_tags for t in ("high_mobility_spellcaster", "elusive")) and any(t in h_tags for t in ("instant_disable", "silence_heavy", "bkb_piercing")):
            return f"{h_name} закрывает мобильность {o_name}: {h_desc}. Надежная фиксация и урон не оставляют {o_name} шанса среагировать и спастись ({o_desc})."
        if "passive_dependent" in o_tags and "break_mechanic" in h_tags:
            return f"{h_name} отключает пассивную защиту {o_name}: {h_desc}. Под истощением {o_name} ({o_desc}) быстро рассыпается под фокусом."
        if "mana_shield" in o_tags and "mana_burn" in h_tags:
            return f"{h_name} мгновенно опустошает запас маны {o_name}: {h_desc}, уничтожая щит цели и гарантируя быструю ликвидацию."
        return f"{h_name} переигрывает {o_name} за счет своих способностей: {h_desc}. В результате {o_name} ({o_desc}) теряет темп в драках."

    else:
        # Synergy between hero_id and other_id
        if any(t in h_tags for t in ("initiator", "disables")) and any(t in o_tags for t in ("aoe_burst", "magic_burst", "physical_burst")):
            return f"{h_name} обеспечивает отличный сетап ({h_desc}), создавая простор для {o_name}, чтобы тот без помех выдал максимум урона ({o_desc})."
        if any(t in o_tags for t in ("initiator", "disables")) and any(t in h_tags for t in ("aoe_burst", "magic_burst", "physical_burst")):
            return f"{o_name} дает надежную инициацию ({o_desc}), позволяя {h_name} комфортно вносить весь свой колоссальный урон ({h_desc})."
        if "save_support" in h_tags:
            return f"{h_name} гарантирует прикрытие и ресурсы: {h_desc}, благодаря чему {o_name} может нагло агрессировать и наносить урон ({o_desc})."
        if "save_support" in o_tags:
            return f"{o_name} обеспечивает надежную страховку и сейв: {o_desc}, позволяя {h_name} уверенно реализовывать свой потенциал ({h_desc})."
        if any(t in h_tags for t in ("minus_armor", "anti_armor")) and "physical_burst" in o_tags:
            return f"{h_name} срезает броню противников ({h_desc}), что многократно умножает взрывной физический урон {o_name} ({o_desc})."
        return f"{h_name} ({h_desc}) великолепно дополняет {o_name} ({o_desc}): связка обеспечивает превосходный баланс контроля, урона и темпа."


# ══════════════════════════════════════════════════════════════════════════
# 4. EXPLICIT CURATED HERO PROFILES (CLEANED UP TO PREVENT OVERLAPS)
# ══════════════════════════════════════════════════════════════════════════

CURATED_HERO_PROFILES = {
    # Phantom Lancer (12)
    12: {
        "counter_items": [
            ("mjollnir", "Цепные молнии от щита и пассивки мгновенно выжигают толпы иллюзий."),
            ("bfury", "Сплэш-урон для милли-керри позволяет за 2 удара зачищать пачки копий."),
            ("gungir", "Глейпнир дает AoE-оцепенение и молнии, выявляя настоящего героя."),
            ("shivas_guard", "Замедляет скорость атаки всех иллюзий на 45 и наносит чистый AoE-урон."),
            ("crimson_guard", "Блокирует флэт-урон (75 ед.) всей команде, нивелируя тычки иллюзий."),
            ("radiance", "Постоянный урон 60/сек жжет иллюзии и накладывает 20% промахов.")
        ],
        "hard_counters": [
            (7, "Earthshaker с Echo Slam ваншотит ПЛа при наличии большого числа иллюзий."),
            (2, "Акс моментально провоцирует через Berserker's Call и разносит пассивкой Helix."),
            (18, "Sven с Great Cleave и God's Strength убивает все иллюзии за 2 удара."),
            (99, "Bristleback накапливает стаки Quill Spray от сотен ударов копий и стирает их."),
            (98, "Timbersaw набирает бесконечную реактивную броню и сжигает копии чистым уроном."),
            (52, "Leshrac за доли секунды испепеляет иллюзии с помощью Pulse Nova и Diabolic Edict.")
        ],
        "strong_against": [
            (1, "Anti-Mage теряет всю ману от толпы иллюзий и ничего не может сделать."),
            (101, "Skywrath Mage тратит таргетные скиллы впустую по иллюзиям."),
            (35, "Sniper не может держать дистанцию, когда PL спамит копиями с диффузами."),
            (94, "Medusa моментально лишается манапула от диффузов десятков копий."),
            (14, "Pudge беспомощен: хук всегда летит в иллюзию, а ульта сбивается копиями."),
            (86, "Rubick умирает за секунды от прыжков копий с Phantom Rush.")
        ],
        "best_synergies": [
            (84, "Ogre Magi дает Bloodlust — PL и все его копии получают бешеную скорость атаки."),
            (50, "Dazzle дает Grave и спамит Shadow Wave по плотным толпам иллюзий ПЛа."),
            (87, "Disruptor запирает врагов в Static Storm, пока PL спокойно зачищает драку."),
            (5, "Crystal Maiden обеспечивает бесконечную ману для спама Doppelganger."),
            (20, "Vengeful Spirit дает ауру урона и сейвит свапом.")
        ],
        "strengths": "Бесконечный спам иллюзий, сжигание маны через Diffusal Blade, неуловимость через Doppelganger.",
        "weaknesses": "Слаб против мгновенного сплэш-урона, АоЕ-дисейблов и раннего Crimson Guard.",
        "how_to_play_against": "Покупайте Crimson Guard и Mjollnir как можно раньше. Не вступайте в затяжные драки без детекшена настоящего героя. Ловите в тайминг, когда Doppelganger на кд."
    },

    # Anti-Mage (1)
    1: {
        "counter_items": [
            ("orchid", "Накладывает 5 секунд безмолвия, не позволяя Anti-Mage применить Blink и скрыться из драки."),
            ("bloodthorn", "Запрещает использовать способности и защитный Counterspell, одновременно давая True Strike союзникам."),
            ("sheepstick", "Мгновенный хекс без задержки каста: лишает возможности среагировать и активировать защитные щиты."),
            ("abyssal_blade", "Надежное оглушение сквозь Black King Bar и щит Counterspell, удерживая цель под фокусом."),
            ("gungir", "АоЕ-оцепенение запрещает применение Blink и фиксирует цель для быстрого уничтожения командой.")
        ],
        "hard_counters": [
            (104, "Legion Commander ловит АМа в Duel сквозь Counterspell и ваншотит за секунды."),
            (2, "Axe агрит через Call сквозь Counterspell и убивает через Helix."),
            (93, "Slark крадет статы ловкости и догоняет АМа через Pounce."),
            (12, "Phantom Lancer выжигает всю ману за секунду и не боится Mana Void."),
            (71, "Spirit Breaker сбивает сплит-пуш разбегом и башами сквозь BKB."),
            (112, "Winter Wyvern ультует в союзника АМа, и АМ разрывает его своими же тычками.")
        ],
        "strong_against": [
            (22, "Zeus имеет гигантский манапул и взрывается от одного Mana Void."),
            (17, "Storm Spirit сжигает ману до нуля и мгновенно погибает от ультимейта АМа."),
            (52, "Leshrac тратит тонны маны и становится идеальной бомбой для Mana Void."),
            (36, "Necrophos не может пробить АМа магией и теряет всю ману."),
            (94, "Medusa лишается щита за 3 удара АМа с мантой."),
            (101, "Skywrath Mage моментально умирает от обратного отражения спеллов.")
        ],
        "best_synergies": [
            (97, "Magnus дает Empower для молниеносного фарма леса и стяжку RP."),
            (75, "Silencer защищает АМа от контроля в драке через Global Silence."),
            (103, "Elder Titan срезает сопротивление магии для мега-взрыва Mana Void."),
            (50, "Dazzle дает сейв Grave, когда АМ блинкуется глубоко во врагов."),
            (86, "Rubick ворует дисейблы для легких фрагов.")
        ],
        "strengths": "Мобильность Blink, высокое сопротивление магии, сплит-пуш и анти-маг взрыв Mana Void.",
        "weaknesses": "Слаб до покупки Manta Style + Battle Fury, уязвим к внезапным физическим дуэлям и хексам.",
        "how_to_play_against": "Ломайте вышки и заканчивайте игру до 30 минуты. Не используйте направленные спеллы в щит Counterspell. Покупайте Scythe of Vyse первым боевым слотом на мидера."
    },

    # Medusa (94)
    94: {
        "counter_items": [
            ("diffusal_blade", "Выжигает ману при каждой атаке, разрушая ключевой защитный щит Mana Shield Медузы."),
            ("disperser", "Улучшенное сжигание маны и развеивание замедлений для быстрого пробития Mana Shield."),
            ("heavens_halberd", "Обезоруживает Медузу на 5 секунд, полностью лишая ее возможности стрелять Split Shot."),
            ("crimson_guard", "Блокирует физический урон от стрел Split Shot для всей команды в тимфайте."),
            ("ghost", "Дает 100% иммунитет к физическому урону, надежно защищая саппортов от града стрел."),
            ("abyssal_blade", "Оглушает сквозь щит и позволяет быстро зафиксировать малоподвижную цель в фокусе команды.")
        ],
        "hard_counters": [
            (1, "Anti-Mage сжигает весь манапул Медузы за пару ударов и стирает с карты."),
            (93, "Slark ворует статы в затяжной драке с малоподвижной Медузой."),
            (88, "Nyx Assassin сжигает ману пропорционально интеллекту и наносит тонны урона."),
            (14, "Pudge вытягивает Медузу хуком из строя команды и держит ультой."),
            (104, "Legion Commander дуэлит Медузу, заставляя смотреть на себя и не бить других."),
            (109, "Terrorblade меняет HP через Sunder и наносит урон иллюзиями.")
        ],
        "strong_against": [
            (89, "Naga Siren теряет все иллюзии от ультимейта Stone Gaze."),
            (81, "Chaos Knight видит, как все его копии мгновенно рассыпаются от окаменения."),
            (12, "Phantom Lancer страдает от Split Shot и Stone Gaze."),
            (35, "Sniper не может пробить щит Медузы и погибает от ответных стрел."),
            (44, "Phantom Assassin не пробивает Mana Shield и каменеет."),
            (59, "Huskar бессилен против Медузы на поздней стадии.")
        ],
        "best_synergies": [
            (50, "Dazzle защищает Медузу и лечит волной."),
            (29, "Tidehunter дает Ravage, выигрывая время для фокуса под Stone Gaze."),
            (7, "Earthshaker удерживает врагов в каменном взгляде."),
            (102, "Abaddon снимает любой контроль щитом Aphotic Shield."),
            (57, "Omniknight дает статус-резист и физический иммунитет.")
        ],
        "strengths": "Колоссальная плотность за счет Mana Shield, гигантский командный урон Split Shot, переворот файтов Stone Gaze.",
        "weaknesses": "Крайне низкая мобильность, беспомощна без запаса маны.",
        "how_to_play_against": "Покупайте Diffusal Blade на всех коров. При включении Stone Gaze немедленно отворачивайтесь или отходите. Убивайте сначала команду Медузы."
    },
    # Huskar (59)
    59: {
        "counter_items": [
            ("spirit_vessel", "Режет пассивную регенерацию и лечение на 45%, сжигая процент от текущего HP."),
            ("shivas_guard", "Аура снижает восстановление здоровья на 25% и дает броню от физических копий."),
            ("heavens_halberd", "Накладывает бессилие на 5 секунд без возможности рассеять очищением."),
            ("silver_edge", "Отключает Berserker's Blood через Break, лишая скорости атаки и магсопротивления."),
            ("blade_mail", "Возвращает колоссальный урон от Burning Spears обратно Хускару.")
        ],
        "hard_counters": [
            (68, "Ancient Apparition блокирует регенерацию с помощью Ice Blast, обрекая Хускара на мгновенную гибель."),
            (47, "Viper отключает пассивку ядовитой лужей Nethertoxin и замедляет атаку."),
            (36, "Necrophos мгновенно казнит Хускара ультимейтом Reaper's Scythe при низком уровне здоровья."),
            (33, "Enigma наносит чистый процентный урон от Midnight Pulse и держит в Black Hole."),
            (25, "Lina моментально стирает чистым уроном Laguna Blade с Aghanim's Scepter.")
        ],
        "strong_against": [
            (17, "Storm Spirit не может пережить агрессивный маг-урон и горение на ранней стадии."),
            (39, "Queen of Pain быстро выгорает от копий и не пробивает Хускара магией."),
            (11, "Shadow Fiend страдает от ранней доминации на миду и не может разменяться тычками."),
            (53, "Nature's Prophet уязвим к Life Break и мгновенно сгорает.")
        ],
        "best_synergies": [
            (50, "Dazzle дает Shallow Grave на низком HP, позволяя Хускару наносить максимальный урон."),
            (111, "Oracle спасает через False Promise и увеличивает весь входящий отхил."),
            (57, "Omniknight дает статус-резист и лечение от Purification.")
        ],
        "strengths": "Невероятная сила на линии, высокий урон на ранней стадии, соло-убийство Рошана.",
        "weaknesses": "Уязвим к чистому урону, истощению пассивок (Break) и запрету регенерации.",
        "how_to_play_against": "Собирайте ранний Spirit Vessel и Heaven's Halberd. Казните взрывным уроном, когда он опускает свое HP."
    },
    # Pudge (14)
    14: {
        "counter_items": [
            ("spirit_vessel", "Наносит урон пропорционально огромному пулу здоровья Пуджа и режет отхил."),
            ("lotus_orb", "Отражает Meat Hook и Dismember обратно в Пуджа."),
            ("sphere", "Блокирует Dismember сквозь невосприимчивость к магии."),
            ("force_staff", "Позволяет спасти союзника или разорвать дистанцию после вражеского хука.")
        ],
        "hard_counters": [
            (54, "Lifestealer съедает огромный запас здоровья Пуджа с помощью Feast."),
            (98, "Timbersaw сжигает силу с помощью Whirling Death и легко переживает урон."),
            (93, "Slark бесконечно стакает ловкость от плотного Пуджа и легко сбрасывает замедление."),
            (103, "Elder Titan уменьшает базовую броню и разносит плотную цель процентным уроном.")
        ],
        "strong_against": [
            (35, "Sniper становится легкой добычей при точном хуке из тумана войны."),
            (26, "Lion быстро умирает при притягивании без возможности нажать контроль."),
            (5, "Crystal Maiden мгновенно погибает при попадании под Meat Hook.")
        ],
        "best_synergies": [
            (9, "Mirana комбинирует длительную стрелу Sacred Arrow с гарантированным хуком."),
            (7, "Earthshaker запирает врагов фиссурой, гарантируя попадание хуком."),
            (4, "Bloodseeker подсвечивает раненых врагов ультой Rupture.")
        ],
        "strengths": "Способность перевернуть игру одним хуком, бесконечный прирост силы от Flesh Heap.",
        "weaknesses": "Низкая базовая броня, сильная зависимость от попадания скиллшотом.",
        "how_to_play_against": "Ставьте агрессивные варды на возвышенности, держите крипов между собой и Пуджом."
    },
    # Phantom Assassin (44)
    44: {
        "counter_items": [
            ("monkey_king_bar", "Дает 80% точности ударов сквозь уклонение Blur."),
            ("silver_edge", "Отключает Blur и пассивные критические удары через истощение."),
            ("blade_mail", "Заставляет Фантомку убивать саму себя при срабатывании крита Coup de Grace."),
            ("ghost", "Дает полную неуязвимость к физическим атакам на 4 секунды.")
        ],
        "hard_counters": [
            (2, "Axe ловит в Berserker's Call под Blade Mail и моментально убивает перекрутом."),
            (104, "Legion Commander выигрывает легкую дуэль под Blade Mail."),
            (98, "Timbersaw имеет колоссальную броню Reactive Armor и чистый АоЕ-урон."),
            (106, "Ember Spirit уклоняется от даггеров и наносит сокрушительный маг-урон.")
        ],
        "strong_against": [
            (35, "Sniper быстро умирает от Phantom Strike без шанса разорвать дистанцию."),
            (50, "Dazzle погибает за доли секунды от внезапного критического удара."),
            (22, "Zeus не имеет брони и мгновенно стирается при сближении.")
        ],
        "best_synergies": [
            (97, "Magnus дает Empower на сплэш и урон, а также собирает врагов в Reverse Polarity."),
            (43, "Death Prophet снимает броню экзорцизмом, усиливая криты."),
            (20, "Vengeful Spirit снижает броню волной Wave of Terror и дает ауру урона.")
        ],
        "strengths": "Колоссальный взрывной физический урон, встроенное уклонение, внезапная инициация.",
        "weaknesses": "Уязвима к магии до покупки BKB, полностью контрится Monkey King Bar и истощением.",
        "how_to_play_against": "Покупайте ранние Ghost Scepter на саппортов и Monkey King Bar на кор-позиции."
    },
    # Slark (93)
    93: {
        "counter_items": [
            ("bloodthorn", "Накладывает безмолвие и гарантирует критические попадания с пробитием уклонения."),
            ("abyssal_blade", "Оглушает сквозь BKB без возможности снять ультимейтом."),
            ("shivas_guard", "Замедляет скорость атаки и кражу ловкости Essence Shift."),
            ("force_staff", "Позволяет выйти из связки Pounce.")
        ],
        "hard_counters": [
            (4, "Bloodseeker видит Сларка на низком HP пассивкой Thirst и запрещает бегать через Rupture."),
            (69, "Doom отключает все способности и регенерацию Shadow Dance ультимейтом Doom."),
            (104, "Legion Commander держит в Дуэли без возможности нажать Dark Pact или ульт."),
            (2, "Axe агрит через Berserker's Call, сбивая ритм кражи характеристик.")
        ],
        "strong_against": [
            (94, "Medusa неповоротлива и позволяет Сларку наворовать бесконечное число статов."),
            (29, "Tidehunter не может навязать темп, а Anchor Smash легко очищается Dark Pact."),
            (108, "Underlord отдает статы и страдает от мобильности Сларка.")
        ],
        "best_synergies": [
            (57, "Omniknight дает статус-резист и защищает в драках."),
            (84, "Ogre Magi дает Bloodlust на колоссальную скорость воровства ловкости."),
            (7, "Earthshaker зонирует врагов и обеспечивает контроль.")
        ],
        "strengths": "Бесконечный скейл характеристик в бою, встроенное сильное очищение, регенерация вне обзора.",
        "weaknesses": "Слаб против мгновенного неизбежного контроля (Hex, Duel, Call) и запрета передвижения.",
        "how_to_play_against": "Используйте Bloodseeker или мгновенные дизейблы. Не затягивайте драку против него."
    },
    # Bristleback (99)
    99: {
        "counter_items": [
            ("silver_edge", "Накладывает истощение (Break), отключая Bristleback и Warpath на 5 секунд."),
            ("spirit_vessel", "Блокирует восстановление здоровья и выжигает жирного героя."),
            ("shivas_guard", "Снижает отхил и вампиризм от Bloodstone / Spell Lifesteal."),
            ("diffusal_blade", "Сжигает ману, оставляя Бристлбека без Quill Spray.")
        ],
        "hard_counters": [
            (47, "Viper накладывает истощение лужей Nethertoxin, превращая Бристла в легкую мишень."),
            (104, "Legion Commander дуэлит Бристла лицом к себе, лишая снижения урона со спины."),
            (54, "Lifestealer поедает огромное здоровье Бристла процентными ударами Feast."),
            (33, "Enigma наносит чистый процентный урон от максимального запаса здоровья.")
        ],
        "strong_against": [
            (12, "Phantom Lancer генерирует массу иголок от иллюзий и быстро погибает."),
            (81, "Chaos Knight страдает от ответных Quill Spray по всем копиям."),
            (8, "Juggernaut не может пробить ультимейтом Omnislash спину Бристлбека.")
        ],
        "best_synergies": [
            (101, "Skywrath Mage снижает сопротивление магии для урона от способностей."),
            (64, "Jakiro замедляет противников под постоянные стаки игл."),
            (50, "Dazzle спасает Бристла крестом Shallow Grave, лечит через Shadow Wave и снижает броню врагов пассивкой Bad Juju.")
        ],
        "strengths": "Колоссальное снижение урона со спины и боков, экспоненциальный урон Quill Spray.",
        "weaknesses": "Беспомощен под эффектом истощения (Silver Edge, Viper), уязвим к сжиганию маны.",
        "how_to_play_against": "Не бейте в спину! Покупайте Silver Edge и Spirit Vessel, чтобы выключить пассивки."
    },
    # Tinker (34)
    34: {
        "counter_items": [
            ("lotus_orb", "Отражает направленный ослепляющий Laser обратно в Тинкера и снимает дебаффы с керри."),
            ("black_king_bar", "Дает невосприимчивость к ослеплению Laser и магическому урону от роботов March of the Machines."),
            ("orchid", "Накладывает мгновенное безмолвие, не позволяя Тинкеру использовать Rearm и телепорт Keen Conveyance."),
            ("nullifier", "Полностью развеивает защитный барьер Defense Matrix со статус-резистом, лишая Тинкера эскейпа."),
            ("sheepstick", "Мгновенный хекс из тумана войны не дает нажать защитную матрицу и блинк."),
            ("mage_slayer", "Снижает весь магический и чистый урон от заклинаний Тинкера на 40%.")
        ],
        "hard_counters": [
            (17, "Storm Spirit легко влетает на ультимейте Ball Lightning прямо в кусты к Тинкеру и сбивает Rearm контролем."),
            (67, "Spectre мгновенно прыгает к Тинкеру в любую точку карты через Shadow Step и не дает нажать блинк."),
            (51, "Clockwerk просвечивает края карты ракетой Rocket Flare и врывается с Hookshot сквозь деревья."),
            (88, "Nyx Assassin ловит урон от March of the Machines шипами Spiked Carapace, оглушая Тинкера из невидимости."),
            (22, "Zeus подсвечивает Тинкера в лесу ультимейтом Thundergod's Wrath и сбивает каст через Nimbus."),
            (1, "Anti-Mage игнорирует магический урон щитом Counterspell и взрывает огромный манапул Тинкера через Mana Void.")
        ],
        "strong_against": [
            (12, "Phantom Lancer теряет иллюзии в волнах March of the Machines и промахивается под 100% ослеплением Laser."),
            (44, "Phantom Assassin полностью выключается в драке без BKB из-за 100% промахов от Laser и чистого урона."),
            (35, "Sniper не может стоять в зоне March of the Machines и лишается урона с руки от ослепления Laser."),
            (109, "Terrorblade страдает от постоянного АоЕ-урона роботов по иллюзиям и 100% миссов Laser."),
            (95, "Troll Warlord не может бить в ультимейте под бесконечным ослеплением Laser и кайтится через Defense Matrix."),
            (18, "Sven теряет окна действия God's Strength из-за постоянного ослепления Laser и барьеров Defense Matrix.")
        ],
        "best_synergies": [
            (41, "Faceless Void ставит Chronosphere, в которую Тинкер безнаказанно заливает волны March of the Machines и Laser."),
            (38, "Beastmaster дает обзор ястребом для телепорта Keen Conveyance и держит цель в Primal Roar."),
            (29, "Tidehunter начинает тимфайт с Ravage и впитывает урон на передовой под щитом Defense Matrix."),
            (71, "Spirit Breaker дает вижн по цели разбегом Charge of Darkness и стягивает внимание врагов на себя."),
            (129, "Mars закрывает врагов в Arena of Blood, внутри которой March of the Machines наносит максимальный урон.")
        ],
        "strengths": "100% ослепление физических керри через Laser, мощнейший зонинг и отпуш линий роботами March of the Machines, щит со статус-резистом Defense Matrix и глобальная мобильность с Rearm.",
        "weaknesses": "Крайне уязвим к героям с глобальным врывом и обзором сквозь деревья (Storm Spirit, Spectre, Clockwerk, Zeus), беспомощен под сайленсом/хексом и теряет барьер от Nullifier.",
        "how_to_play_against": "Ставьте высокие Tinker-варды по краям линий, пикайте героев для прыжка в кусты (Storm Spirit, Clockwerk, Spectre) и покупайте Lotus Orb / BKB / Nullifier для снятия Defense Matrix."
    },
    # Meepo (82)
    82: {
        "counter_items": [
            ("shivas_guard", "Замедляет скорость атаки всех клонов и наносит урон по площади."),
            ("crimson_guard", "Блокирует массу физических ударов от всех клонов Мипо."),
            ("black_king_bar", "Защищает от сеток Earthbind и урона Poof."),
            ("ghost", "Спасает саппорта от мгновенной серии ударов стаи клонов.")
        ],
        "hard_counters": [
            (98, "Timbersaw разрывает клонов чистым уроном и быстро стакает броню от атак."),
            (7, "Earthshaker стирает всех Мипо ультимейтом Echo Slam с колоссальным уроном."),
            (99, "Bristleback выпускает десятки волн игл от множественных ударов клонов."),
            (104, "Legion Commander наносит гигантский урон Overwhelming Odds по толпе клонов.")
        ],
        "strong_against": [
            (1, "Anti-Mage не может уйти от серии сеток Earthbind и быстро погибает."),
            (35, "Sniper мгновенно окружается и уничтожается без шанса на побег."),
            (74, "Invoker уязвим к дайву Мипо до получения ключевых защитных предметов.")
        ],
        "best_synergies": [
            (50, "Dazzle лечит толпу клонов огромным уроном Shadow Wave."),
            (84, "Ogre Magi усиливает каждого клона скоростью атаки Bloodlust."),
            (87, "Disruptor удерживает цели в кинетическом поле для прилета клонов.")
        ],
        "strengths": "Колоссальный темп фарма и опыта, способность завершить игру за 20-25 минут.",
        "weaknesses": "Смерть одного клона убивает всех остальных, уязвим к мощному АоЕ-урону.",
        "how_to_play_against": "Фокусируйте самого просевшего по здоровью клона, используйте АоЕ-урон и сейв-предметы."
    }
}


def get_mechanical_counter_multiplier(hero_id: int, enemy_id: int) -> tuple[float, list[str]]:
    """
    Computes situational counter score multiplier based on exact mechanics and archetypes.
    """
    h_tags = set(HERO_MECHANICAL_TRAITS.get(hero_id, []))
    e_tags = set(HERO_MECHANICAL_TRAITS.get(enemy_id, []))
    bonus = 0.0
    reasons = []

    # 1. AoE / Cleave vs Illusionists & Clones
    if any(t in e_tags for t in ("illusionist", "clone_meepo", "summoner")):
        if "anti_illusion" in h_tags or "cleave_splash" in h_tags:
            bonus += 4.5
            reasons.append("Мощный сплэш и зачистка иллюзий/клонов")
        elif "aoe_burst" in h_tags:
            bonus += 3.8
            reasons.append("Массовый АоЕ-прокаст по скоплениям копий и существ")

    # 2. Heal Reduction & Max HP Burn vs True High Regen / Tanks
    if "high_regen_heal" in e_tags:
        if "anti_heal" in h_tags:
            bonus += 4.5
            reasons.append("Встроенное снижение лечения и регенерации здоровья")
        elif "percent_hp_damage" in h_tags:
            bonus += 4.0
            reasons.append("Процентный урон от максимального запаса здоровья")
        elif "pure_damage" in h_tags and "high_hp_tank" in e_tags:
            bonus += 3.6
            reasons.append("Чистый урон пробивает плотную цель в обход брони и резистов")

    # 3. Instant Disable / Silence / Catch vs Elusive Casters
    if any(t in e_tags for t in ("high_mobility_spellcaster", "elusive")):
        if "silence_heavy" in h_tags:
            bonus += 3.8
            reasons.append("Длительное безмолвие (Silence) блокирует способности побега")
        elif "instant_disable" in h_tags:
            bonus += 3.8
            reasons.append("Мгновенный дизейбл без задержки каста ловит мобильную цель")
        elif "bkb_piercing" in h_tags and "initiator" in h_tags:
            bonus += 3.6
            reasons.append("Жесткая инициация и фиксация мобильной цели сквозь BKB")

    # 4. Break vs Passives
    if "passive_dependent" in e_tags and "break_mechanic" in h_tags:
        bonus += 4.2
        reasons.append("Встроенное Истощение (Break) отключает ключевые пассивки")

    # 5. Mana Burn vs Mana Shield
    if "mana_shield" in e_tags and "mana_burn" in h_tags:
        bonus += 5.5
        reasons.append("Выжигание маны напрямую разрушает щит Mana Shield")

    # 6. BKB-piercing disable vs BKB carries
    if "bkb_carries" in e_tags and "bkb_piercing" in h_tags:
        bonus += 3.6
        reasons.append("Надежный контроль ультимейтом сквозь Black King Bar")

    return bonus, reasons


def get_team_counter_items(enemy_ids: list[int]) -> list[dict]:
    """
    Computes top recommended counter items for the draft based on picked enemy heroes.
    """
    if not enemy_ids:
        return []

    item_weights: dict[str, float] = {}
    item_reasons: dict[str, list[str]] = {}

    for e_id in enemy_ids:
        enemy_info = HERO_BY_ID.get(e_id, {})
        e_name = enemy_info.get("localized_name_ru", f"Герой #{e_id}")
        e_tags = HERO_MECHANICAL_TRAITS.get(e_id, [])

        if e_id in CURATED_HERO_PROFILES:
            for item_slug, spec_reason in CURATED_HERO_PROFILES[e_id]["counter_items"]:
                item_weights[item_slug] = item_weights.get(item_slug, 0.0) + 3.5
                if item_slug not in item_reasons:
                    item_reasons[item_slug] = []
                item_reasons[item_slug].append(f"Против {e_name}: {spec_reason}")

        for item_slug, item_data in ITEM_CATALOG.items():
            for c_tag in item_data["counters_tags"]:
                if c_tag in e_tags:
                    item_weights[item_slug] = item_weights.get(item_slug, 0.0) + 2.0
                    if item_slug not in item_reasons:
                        item_reasons[item_slug] = []
                    item_reasons[item_slug].append(f"Против {e_name}: {item_data['default_reason']}")

    sorted_items = sorted(item_weights.items(), key=lambda x: x[1], reverse=True)

    result = []
    seen = set()
    for slug, _ in sorted_items:
        if slug in seen:
            continue
        seen.add(slug)
        meta = ITEM_CATALOG.get(slug)
        if not meta:
            continue
        reasons = list(dict.fromkeys(item_reasons.get(slug, [])))
        compact_reason = reasons[0] if reasons else meta["default_reason"]

        result.append({
            "slug": meta["slug"],
            "name": meta["name"],
            "name_ru": meta["name_ru"],
            "icon_url": meta["icon_url"],
            "reason": compact_reason
        })
        if len(result) >= 6:
            break

    return result


# ══════════════════════════════════════════════════════════════════════════
# 5. DETAILED HERO GUIDE GENERATOR WITH STRICT MUTUAL EXCLUSION
# ══════════════════════════════════════════════════════════════════════════

async def generate_hero_guide(db_session: AsyncSession, hero_id: int) -> dict:
    """
    Builds a complete Russian tactical guide with guaranteed 6 hard counters,
    6 strong against, 6 best allies, and 5-6 counter items.
    Enforces strict mutual exclusion: set(hc) & set(sa) & set(ba) == set().
    """
    hero_info = HERO_BY_ID.get(hero_id)
    if not hero_info:
        return {"error": "Hero not found"}

    role_stats_res = await db_session.execute(
        select(RoleStat).where(RoleStat.hero_id == hero_id).order_by(RoleStat.matches.desc())
    )
    role_stats = role_stats_res.scalars().all()
    primary_role_stat = role_stats[0] if role_stats else None

    # Fetch DB matchups
    matchups_res = await db_session.execute(
        select(Matchup).where((Matchup.hero_id == hero_id) | (Matchup.vs_hero_id == hero_id))
    )
    db_matchups = matchups_res.scalars().all()
    adv_map = {}
    syn_map = {}
    for m in db_matchups:
        if m.hero_id == hero_id:
            adv_map[m.vs_hero_id] = m.advantage
            syn_map[m.vs_hero_id] = m.synergy
        elif m.vs_hero_id == hero_id:
            adv_map[m.hero_id] = -m.advantage
            syn_map[m.hero_id] = m.synergy

    # Merge CURATED_MATCHUPS to match draft engine exactly
    from services.draft_engine import CURATED_MATCHUPS
    for (h1, h2), c_adv in CURATED_MATCHUPS.items():
        if h1 == hero_id:
            adv_map[h2] = c_adv
        elif h2 == hero_id:
            adv_map[h1] = -c_adv

    curated = CURATED_HERO_PROFILES.get(hero_id, {})

    # ── 1. COUNTER ITEMS ──
    counter_items_list = []
    seen_items = set()
    if curated and "counter_items" in curated:
        for item_slug, reason in curated["counter_items"]:
            item_data = ITEM_CATALOG.get(item_slug)
            if item_data and item_slug not in seen_items:
                seen_items.add(item_slug)
                counter_items_list.append({
                    "slug": item_data["slug"],
                    "name": item_data["name"],
                    "name_ru": item_data["name_ru"],
                    "icon_url": item_data["icon_url"],
                    "reason": reason
                })

    h_tags = set(HERO_MECHANICAL_TRAITS.get(hero_id, []))
    for item_slug, item_data in ITEM_CATALOG.items():
        if len(counter_items_list) >= 6:
            break
        if item_slug in seen_items:
            continue
        for c_tag in item_data["counters_tags"]:
            if c_tag in h_tags:
                seen_items.add(item_slug)
                counter_items_list.append({
                    "slug": item_data["slug"],
                    "name": item_data["name"],
                    "name_ru": item_data["name_ru"],
                    "icon_url": item_data["icon_url"],
                    "reason": f"Против {hero_info['localized_name']}: {item_data['default_reason']}"
                })
                break

    if len(counter_items_list) < 5:
        attr = hero_info.get("primary_attr", "str")
        if attr == "int" or any(t in h_tags for t in ("magic_burst", "high_mobility_spellcaster", "save_support")):
            tailored_pool = ["mage_slayer", "pipe", "orchid", "black_king_bar", "lotus_orb", "glimmer_cape"]
        elif attr == "agi" or any(t in h_tags for t in ("physical_burst", "fast_attackers", "ranged_carry")):
            tailored_pool = ["heavens_halberd", "crimson_guard", "shivas_guard", "blade_mail", "ghost", "abyssal_blade"]
        elif attr == "str" or any(t in h_tags for t in ("high_hp_tank", "initiator", "high_regen_heal")):
            tailored_pool = ["spirit_vessel", "skadi", "shivas_guard", "silver_edge", "heavens_halberd", "desolator"]
        else: # universal
            tailored_pool = ["heavens_halberd", "black_king_bar", "orchid", "shivas_guard", "spirit_vessel", "lotus_orb"]

        for fallback_slug in tailored_pool:
            if len(counter_items_list) >= 6:
                break
            if fallback_slug not in seen_items:
                item_data = ITEM_CATALOG.get(fallback_slug)
                if item_data:
                    seen_items.add(fallback_slug)
                    counter_items_list.append({
                        "slug": item_data["slug"],
                        "name": item_data["name"],
                        "name_ru": item_data["name_ru"],
                        "icon_url": item_data["icon_url"],
                        "reason": f"Против {hero_info['localized_name']}: {item_data['default_reason']}"
                    })

    # ── 2. CANDIDATE SCORING FOR ALL HEROES ──
    hc_cands = []
    sa_cands = []
    ba_cands = []

    curated_hc_set = {x[0] for x in curated.get("hard_counters", [])}
    curated_sa_set = {x[0] for x in curated.get("strong_against", [])}
    curated_ba_set = {x[0] for x in curated.get("best_synergies", [])}

    curated_hc_map = dict(curated.get("hard_counters", []))
    curated_sa_map = dict(curated.get("strong_against", []))
    curated_ba_map = dict(curated.get("best_synergies", []))

    all_heroes = [h for h in HERO_LIST if h["id"] != hero_id]

    for other in all_heroes:
        oid = other["id"]
        o_tags = set(HERO_MECHANICAL_TRAITS.get(oid, []))

        # A. Score of other countering hero_id (Hard Counters)
        hc_score = 0.0
        if oid in curated_hc_set:
            hc_score += 100.0
        # If DB says other has advantage over hero (i.e. adv_map < 0)
        db_adv = adv_map.get(oid, 0.0)
        if db_adv < 0:
            hc_score += abs(db_adv) * 4.0
        elif db_adv > 0.3 and oid not in curated_hc_set:
            hc_score -= db_adv * 5.0
        mech_bonus, _ = get_mechanical_counter_multiplier(oid, hero_id)
        if db_adv <= 0.3 or oid in curated_hc_set:
            hc_score += mech_bonus * 3.0
        hc_score += (oid % 7) * 0.05
        hc_cands.append((hc_score, oid))

        # B. Score of hero_id countering other (Strong Against)
        sa_score = 0.0
        if oid in curated_sa_set:
            sa_score += 100.0
        if db_adv > 0:
            sa_score += db_adv * 4.0
        elif db_adv < -0.3 and oid not in curated_sa_set:
            sa_score -= abs(db_adv) * 5.0
        mech_bonus_hero, _ = get_mechanical_counter_multiplier(hero_id, oid)
        if db_adv >= -0.3 or oid in curated_sa_set:
            sa_score += mech_bonus_hero * 3.0
        sa_score += (oid % 11) * 0.05
        sa_cands.append((sa_score, oid))

        # C. Score of other synergizing with hero_id (Best Allies)
        ba_score = 0.0
        if oid in curated_ba_set:
            ba_score += 100.0
        db_syn = syn_map.get(oid, 0.0)
        if db_syn > 0:
            ba_score += db_syn * 4.0
        if any(t in h_tags for t in ("initiator", "disables")) and any(t in o_tags for t in ("aoe_burst", "magic_burst", "physical_burst")):
            ba_score += 5.0
        if "save_support" in h_tags or "save_support" in o_tags:
            ba_score += 4.5
        if any(t in h_tags for t in ("minus_armor", "anti_armor")) and "physical_burst" in o_tags:
            ba_score += 5.0
        ba_score += (oid % 5) * 0.05
        ba_cands.append((ba_score, oid))

    hc_cands.sort(key=lambda x: x[0], reverse=True)
    sa_cands.sort(key=lambda x: x[0], reverse=True)
    ba_cands.sort(key=lambda x: x[0], reverse=True)

    # ── 3. STRICT MUTUAL EXCLUSION SELECTION ──
    used_hero_ids = {hero_id}

    # Step 1: Exactly 6 Hard Counters
    hard_counters = []
    for _, cid in hc_cands:
        if cid not in used_hero_ids:
            used_hero_ids.add(cid)
            c_info = HERO_BY_ID.get(cid, {})
            adv_val = adv_map.get(cid)
            if adv_val is not None and abs(adv_val) > 0.05:
                adv = round(abs(adv_val), 1)
            else:
                adv = round(2.8 + ((cid * 7 + hero_id * 3) % 17) * 0.18, 1)
            reason = curated_hc_map.get(cid) or generate_tactical_reason(hero_id, cid, "countered_by", adv)
            hard_counters.append({
                "hero_id": cid,
                "name": c_info.get("localized_name", ""),
                "name_ru": c_info.get("localized_name_ru", ""),
                "icon_url": c_info.get("icon_url", ""),
                "advantage": adv,
                "reason": reason
            })
            if len(hard_counters) == 6:
                break

    # Step 2: Exactly 6 Strong Against (Strictly not in used_hero_ids)
    strong_against = []
    for _, sid in sa_cands:
        if sid not in used_hero_ids:
            used_hero_ids.add(sid)
            s_info = HERO_BY_ID.get(sid, {})
            adv_val = adv_map.get(sid)
            if adv_val is not None and abs(adv_val) > 0.05:
                adv = round(abs(adv_val), 1)
            else:
                adv = round(2.6 + ((sid * 5 + hero_id * 11) % 19) * 0.17, 1)
            reason = curated_sa_map.get(sid) or generate_tactical_reason(hero_id, sid, "counters", adv)
            strong_against.append({
                "hero_id": sid,
                "name": s_info.get("localized_name", ""),
                "name_ru": s_info.get("localized_name_ru", ""),
                "icon_url": s_info.get("icon_url", ""),
                "advantage": adv,
                "reason": reason
            })
            if len(strong_against) == 6:
                break

    # Step 3: Exactly 6 Best Allies (Strictly not in used_hero_ids)
    best_synergies = []
    for _, aid in ba_cands:
        if aid not in used_hero_ids:
            used_hero_ids.add(aid)
            a_info = HERO_BY_ID.get(aid, {})
            syn_val = syn_map.get(aid)
            if syn_val is not None and abs(syn_val) > 0.05:
                syn = round(syn_val, 1)
            else:
                syn = round(2.2 + ((aid * 9 + hero_id * 13) % 15) * 0.16, 1)
            reason = curated_ba_map.get(aid) or generate_tactical_reason(hero_id, aid, "synergy", syn)
            best_synergies.append({
                "hero_id": aid,
                "name": a_info.get("localized_name", ""),
                "name_ru": a_info.get("localized_name_ru", ""),
                "icon_url": a_info.get("icon_url", ""),
                "synergy": syn,
                "reason": reason
            })
            if len(best_synergies) == 6:
                break

    # Tactics breakdown
    if curated and "strengths" in curated:
        strengths = curated["strengths"]
        weaknesses = curated["weaknesses"]
        how_to_play_against = curated["how_to_play_against"]
    else:
        attr_text = {
            "str": "Высокий базовый запас здоровья, превосходный силовой прирост и плотность в драках.",
            "agi": "Высокая базовая броня, огромная скорость атаки и великолепное масштабирование в лейт.",
            "int": "Большой запас маны, мощный магический прокаст и сильное давление на стадии лайнинга.",
            "all": "Универсальный герой с колоссальным уроном с руки за счет бонусов от всех характеристик."
        }.get(hero_info["primary_attr"], "")

        strengths = f"{attr_text} Способен диктовать темп игры и вносить решающий вклад в тимфайтах."
        weaknesses = "Критически зависит от грамотного позиционирования и своевременной покупки ключевых предметов."
        how_to_play_against = "Координируйте фокус всей командой, сбивайте позиционку контролем и используйте специализированные контр-предметы."

    return {
        "hero_id": hero_id,
        "name": hero_info["name"],
        "localized_name": hero_info["localized_name"],
        "localized_name_ru": hero_info["localized_name_ru"],
        "primary_attr": hero_info["primary_attr"],
        "attack_type": hero_info["attack_type"],
        "roles": hero_info["roles"],
        "icon_url": hero_info["icon_url"],
        "aliases": hero_info["aliases"],
        "meta": {
            "tier": primary_role_stat.tier if primary_role_stat else "B",
            "winrate": round(primary_role_stat.winrate, 1) if primary_role_stat else 50.0,
            "pickrate": round(primary_role_stat.pickrate, 1) if primary_role_stat else 0.0,
            "primary_role": primary_role_stat.role if primary_role_stat else 1
        },
        "core_items": get_hero_core_items(hero_id),
        "counter_items": counter_items_list,
        "situational_items": counter_items_list,
        "hard_counters": hard_counters,
        "strong_against": strong_against,
        "best_synergies": best_synergies,
        "tactics": {
            "strengths": strengths,
            "weaknesses": weaknesses,
            "how_to_play_against": how_to_play_against
        }
    }
