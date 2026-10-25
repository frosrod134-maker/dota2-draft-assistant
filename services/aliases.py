"""
Comprehensive Dota 2 Heroes & CIS Slang Dictionary.
Includes official English names, Russian names, Steam CDN icons,
primary attributes, roles, and popular CIS abbreviations / nicknames.
"""

STEAM_CDN_BASE = "https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/heroes"

ALL_HEROES_DATA = [
    {
        "id": 1,
        "name": "npc_dota_hero_antimage",
        "localized_name": "Anti-Mage",
        "localized_name_ru": "Антимаг",
        "primary_attr": "agi",
        "attack_type": "Melee",
        "roles": "Carry,Escape,Nuker",
        "icon_key": "antimage",
        "aliases": ["ам", "магина", "иллюзионист", "блейд", "am", "magina", "antimage", "anti-mage"]
    },
    {
        "id": 2,
        "name": "npc_dota_hero_axe",
        "localized_name": "Axe",
        "localized_name_ru": "Акс",
        "primary_attr": "str",
        "attack_type": "Melee",
        "roles": "Initiator,Durable,Disabler,Carry",
        "icon_key": "axe",
        "aliases": ["акс", "топор", "могул", "крутилка", "axe", "mogul"]
    },
    {
        "id": 3,
        "name": "npc_dota_hero_bane",
        "localized_name": "Bane",
        "localized_name_ru": "Бейн",
        "primary_attr": "all",
        "attack_type": "Ranged",
        "roles": "Support,Disabler,Nuker",
        "icon_key": "bane",
        "aliases": ["бейн", "бане", "атропос", "сон", "bane", "atropos"]
    },
    {
        "id": 4,
        "name": "npc_dota_hero_bloodseeker",
        "localized_name": "Bloodseeker",
        "localized_name_ru": "Бладсикер",
        "primary_attr": "agi",
        "attack_type": "Melee",
        "roles": "Carry,Disabler,Initiator,Nuker",
        "icon_key": "bloodseeker",
        "aliases": ["сикер", "бс", "бладсикер", "гончая", "bloodseeker", "bs", "strygwyr"]
    },
    {
        "id": 5,
        "name": "npc_dota_hero_crystal_maiden",
        "localized_name": "Crystal Maiden",
        "localized_name_ru": "Кристал Мейден",
        "primary_attr": "int",
        "attack_type": "Ranged",
        "roles": "Support,Disabler,Nuker",
        "icon_key": "crystal_maiden",
        "aliases": ["цм", "цмка", "майдэн", "кристалка", "cm", "crystal maiden", "rylai"]
    },
    {
        "id": 6,
        "name": "npc_dota_hero_drow_ranger",
        "localized_name": "Drow Ranger",
        "localized_name_ru": "Дроу Рейнджер",
        "primary_attr": "agi",
        "attack_type": "Ranged",
        "roles": "Carry,Disabler,Pusher",
        "icon_key": "drow_ranger",
        "aliases": ["тракса", "дровка", "дрова", "тракс", "drow", "drow ranger", "traxex"]
    },
    {
        "id": 7,
        "name": "npc_dota_hero_earthshaker",
        "localized_name": "Earthshaker",
        "localized_name_ru": "Эрфшейкер",
        "primary_attr": "str",
        "attack_type": "Melee",
        "roles": "Support,Initiator,Disabler,Nuker",
        "icon_key": "earthshaker",
        "aliases": ["шейкер", "ес", "эхослэм", "землетряс", "тотем", "es", "earthshaker", "shaker"]
    },
    {
        "id": 8,
        "name": "npc_dota_hero_juggernaut",
        "localized_name": "Juggernaut",
        "localized_name_ru": "Джаггернаут",
        "primary_attr": "agi",
        "attack_type": "Melee",
        "roles": "Carry,Pusher,Escape",
        "icon_key": "juggernaut",
        "aliases": ["джагер", "юно", "крутилка", "джаггер", "jugg", "juggernaut", "yurnero"]
    },
    {
        "id": 9,
        "name": "npc_dota_hero_mirana",
        "localized_name": "Mirana",
        "localized_name_ru": "Мирана",
        "primary_attr": "all",
        "attack_type": "Ranged",
        "roles": "Carry,Support,Escape,Nuker,Disabler",
        "icon_key": "mirana",
        "aliases": ["мирана", "потма", "стрела", "кошка", "mirana", "potm"]
    },
    {
        "id": 10,
        "name": "npc_dota_hero_morphling",
        "localized_name": "Morphling",
        "localized_name_ru": "Морфлинг",
        "primary_attr": "agi",
        "attack_type": "Ranged",
        "roles": "Carry,Escape,Nuker",
        "icon_key": "morphling",
        "aliases": ["морф", "вода", "перекачка", "морфлинг", "morph", "morphling"]
    },
    {
        "id": 11,
        "name": "npc_dota_hero_nevermore",
        "localized_name": "Shadow Fiend",
        "localized_name_ru": "Шадоу Финд",
        "primary_attr": "agi",
        "attack_type": "Ranged",
        "roles": "Carry,Nuker",
        "icon_key": "nevermore",
        "aliases": ["сф", "невермор", "койлы", "гуль", "sf", "shadow fiend", "nevermore"]
    },
    {
        "id": 12,
        "name": "npc_dota_hero_phantom_lancer",
        "localized_name": "Phantom Lancer",
        "localized_name_ru": "Фантом Лансер",
        "primary_attr": "agi",
        "attack_type": "Melee",
        "roles": "Carry,Escape,Pusher",
        "icon_key": "phantom_lancer",
        "aliases": ["пл", "лансер", "фантомка лансер", "копейщик", "pl", "phantom lancer"]
    },
    {
        "id": 13,
        "name": "npc_dota_hero_puck",
        "localized_name": "Puck",
        "localized_name_ru": "Пак",
        "primary_attr": "int",
        "attack_type": "Ranged",
        "roles": "Initiator,Disabler,Escape,Nuker",
        "icon_key": "puck",
        "aliases": ["пак", "шарик", "иллюзорный", "дрейк", "puck"]
    },
    {
        "id": 14,
        "name": "npc_dota_hero_pudge",
        "localized_name": "Pudge",
        "localized_name_ru": "Падж",
        "primary_attr": "str",
        "attack_type": "Melee",
        "roles": "Disabler,Initiator,Durable,Nuker",
        "icon_key": "pudge",
        "aliases": ["пудж", "падж", "мясник", "руджер", "паджик", "хук", "pudge", "butcher"]
    },
    {
        "id": 15,
        "name": "npc_dota_hero_razor",
        "localized_name": "Razor",
        "localized_name_ru": "Разор",
        "primary_attr": "agi",
        "attack_type": "Ranged",
        "roles": "Carry,Durable,Nuker,Pusher",
        "icon_key": "razor",
        "aliases": ["разор", "молния", "статик", "razor"]
    },
    {
        "id": 16,
        "name": "npc_dota_hero_sand_king",
        "localized_name": "Sand King",
        "localized_name_ru": "Сэнд Кинг",
        "primary_attr": "all",
        "attack_type": "Melee",
        "roles": "Initiator,Disabler,Support,Nuker,Escape",
        "icon_key": "sand_king",
        "aliases": ["ск", "скорпион", "песок", "сенд кинг", "sk", "sand king", "crixalis"]
    },
    {
        "id": 17,
        "name": "npc_dota_hero_storm_spirit",
        "localized_name": "Storm Spirit",
        "localized_name_ru": "Шторм Спирит",
        "primary_attr": "int",
        "attack_type": "Ranged",
        "roles": "Carry,Escape,Nuker,Initiator,Disabler",
        "icon_key": "storm_spirit",
        "aliases": ["шторм", "панда", "электрик", "молния", "storm", "storm spirit", "raijin"]
    },
    {
        "id": 18,
        "name": "npc_dota_hero_sven",
        "localized_name": "Sven",
        "localized_name_ru": "Свен",
        "primary_attr": "str",
        "attack_type": "Melee",
        "roles": "Carry,Initiator,Disabler,Durable,Nuker",
        "icon_key": "sven",
        "aliases": ["свен", "рыцарь", "ульт свен", "sven", "rogue knight"]
    },
    {
        "id": 19,
        "name": "npc_dota_hero_tiny",
        "localized_name": "Tiny",
        "localized_name_ru": "Тини",
        "primary_attr": "str",
        "attack_type": "Melee",
        "roles": "Carry,Nuker,Initiator,Durable,Disabler",
        "icon_key": "tiny",
        "aliases": ["тини", "камень", "булыжник", "дерево", "прокаст", "tiny", "stone"]
    },
    {
        "id": 20,
        "name": "npc_dota_hero_vengefulspirit",
        "localized_name": "Vengeful Spirit",
        "localized_name_ru": "Венга",
        "primary_attr": "all",
        "attack_type": "Ranged",
        "roles": "Support,Initiator,Disabler,Nuker,Escape",
        "icon_key": "vengefulspirit",
        "aliases": ["венга", "свап", "вс", "venge", "vengeful spirit", "shendelzare"]
    },
    {
        "id": 21,
        "name": "npc_dota_hero_windrunner",
        "localized_name": "Windranger",
        "localized_name_ru": "Виндрейнджер",
        "primary_attr": "all",
        "attack_type": "Ranged",
        "roles": "Carry,Support,Disabler,Escape,Nuker",
        "icon_key": "windrunner",
        "aliases": ["вр", "врка", "рыжая", "ветрокрылая", "стрела", "wr", "windranger", "lyralei"]
    },
    {
        "id": 22,
        "name": "npc_dota_hero_zuus",
        "localized_name": "Zeus",
        "localized_name_ru": "Зевс",
        "primary_attr": "int",
        "attack_type": "Ranged",
        "roles": "Nuker,Carry",
        "icon_key": "zuus",
        "aliases": ["зевс", "дед", "молния", "марио", "зус", "zeus", "zuus"]
    },
    {
        "id": 23,
        "name": "npc_dota_hero_kunkka",
        "localized_name": "Kunkka",
        "localized_name_ru": "Кункка",
        "primary_attr": "str",
        "attack_type": "Melee",
        "roles": "Carry,Support,Disabler,Initiator,Durable,Nuker",
        "icon_key": "kunkka",
        "aliases": ["кунка", "корабль", "адмирал", "торрент", "kunkka", "admiral"]
    },
    {
        "id": 25,
        "name": "npc_dota_hero_lina",
        "localized_name": "Lina",
        "localized_name_ru": "Лина",
        "primary_attr": "int",
        "attack_type": "Ranged",
        "roles": "Support,Carry,Nuker,Disabler",
        "icon_key": "lina",
        "aliases": ["лина", "огонь", "лагуна", "рыжая", "lina", "slayer"]
    },
    {
        "id": 26,
        "name": "npc_dota_hero_lion",
        "localized_name": "Lion",
        "localized_name_ru": "Лион",
        "primary_attr": "int",
        "attack_type": "Ranged",
        "roles": "Support,Disabler,Nuker,Initiator",
        "icon_key": "lion",
        "aliases": ["лион", "палец", "стан", "хекс", "lion"]
    },
    {
        "id": 27,
        "name": "npc_dota_hero_shadow_shaman",
        "localized_name": "Shadow Shaman",
        "localized_name_ru": "Шадоу Шаман",
        "primary_attr": "int",
        "attack_type": "Ranged",
        "roles": "Support,Pusher,Disabler,Nuker,Initiator",
        "icon_key": "shadow_shaman",
        "aliases": ["растра", "шаман", "змейки", "сетка", "сс", "ss", "shadow shaman", "rhasta"]
    },
    {
        "id": 28,
        "name": "npc_dota_hero_slardar",
        "localized_name": "Slardar",
        "localized_name_ru": "Слардар",
        "primary_attr": "str",
        "attack_type": "Melee",
        "roles": "Carry,Durable,Initiator,Disabler,Escape",
        "icon_key": "slardar",
        "aliases": ["селедка", "слардар", "баш", "рыба", "slardar"]
    },
    {
        "id": 29,
        "name": "npc_dota_hero_tidehunter",
        "localized_name": "Tidehunter",
        "localized_name_ru": "Тайдхантер",
        "primary_attr": "str",
        "attack_type": "Melee",
        "roles": "Initiator,Durable,Disabler,Support,Nuker",
        "icon_key": "tidehunter",
        "aliases": ["тайд", "арбуз", "равага", "левиафан", "tide", "tidehunter", "leviathan"]
    },
    {
        "id": 30,
        "name": "npc_dota_hero_witch_doctor",
        "localized_name": "Witch Doctor",
        "localized_name_ru": "Вич Доктор",
        "primary_attr": "int",
        "attack_type": "Ranged",
        "roles": "Support,Nuker,Disabler",
        "icon_key": "witch_doctor",
        "aliases": ["вд", "доктор", "каски", "маледикт", "wd", "witch doctor"]
    },
    {
        "id": 31,
        "name": "npc_dota_hero_lich",
        "localized_name": "Lich",
        "localized_name_ru": "Лич",
        "primary_attr": "int",
        "attack_type": "Ranged",
        "roles": "Support,Nuker",
        "icon_key": "lich",
        "aliases": ["лич", "чайник", "мертвец", "lich"]
    },
    {
        "id": 32,
        "name": "npc_dota_hero_riki",
        "localized_name": "Riki",
        "localized_name_ru": "Рики",
        "primary_attr": "agi",
        "attack_type": "Melee",
        "roles": "Carry,Escape,Disabler",
        "icon_key": "riki",
        "aliases": ["рики", "крыса", "инвиз", "тучка", "рикимару", "riki", "rikimaru"]
    },
    {
        "id": 33,
        "name": "npc_dota_hero_enigma",
        "localized_name": "Enigma",
        "localized_name_ru": "Энигма",
        "primary_attr": "all",
        "attack_type": "Ranged",
        "roles": "Disabler,Initiator,Pusher",
        "icon_key": "enigma",
        "aliases": ["энигма", "блекхол", "дыра", "эдики", "enigma", "black hole"]
    },
    {
        "id": 34,
        "name": "npc_dota_hero_tinker",
        "localized_name": "Tinker",
        "localized_name_ru": "Тинкер",
        "primary_attr": "int",
        "attack_type": "Ranged",
        "roles": "Carry,Nuker,Pusher",
        "icon_key": "tinker",
        "aliases": ["тинкер", "бош", "ракеты", "робот", "tinker", "boush"]
    },
    {
        "id": 35,
        "name": "npc_dota_hero_sniper",
        "localized_name": "Sniper",
        "localized_name_ru": "Снайпер",
        "primary_attr": "agi",
        "attack_type": "Ranged",
        "roles": "Carry,Nuker",
        "icon_key": "sniper",
        "aliases": ["снайпер", "дед", "карлик", "тракса2", "sniper", "kardel"]
    },
    {
        "id": 36,
        "name": "npc_dota_hero_necrolyte",
        "localized_name": "Necrophos",
        "localized_name_ru": "Некрофос",
        "primary_attr": "int",
        "attack_type": "Ranged",
        "roles": "Carry,Nuker,Durable,Disabler",
        "icon_key": "necrolyte",
        "aliases": ["некр", "дед", "коса", "некрофос", "дедушка", "necro", "necrophos"]
    },
    {
        "id": 37,
        "name": "npc_dota_hero_warlock",
        "localized_name": "Warlock",
        "localized_name_ru": "Варлок",
        "primary_attr": "int",
        "attack_type": "Ranged",
        "roles": "Support,Initiator,Disabler",
        "icon_key": "warlock",
        "aliases": ["варлок", "голем", "связка", "дед", "warlock"]
    },
    {
        "id": 38,
        "name": "npc_dota_hero_beastmaster",
        "localized_name": "Beastmaster",
        "localized_name_ru": "Бистмастер",
        "primary_attr": "all",
        "attack_type": "Melee",
        "roles": "Initiator,Disabler,Durable,Pusher",
        "icon_key": "beastmaster",
        "aliases": ["бист", "бистмастер", "кабан", "птица", "рев", "bm", "beastmaster"]
    },
    {
        "id": 39,
        "name": "npc_dota_hero_queenofpain",
        "localized_name": "Queen of Pain",
        "localized_name_ru": "Квопа",
        "primary_attr": "int",
        "attack_type": "Ranged",
        "roles": "Carry,Nuker,Escape",
        "icon_key": "queenofpain",
        "aliases": ["квопа", "королева", "крик", "блинк", "qop", "queen of pain", "akasha"]
    },
    {
        "id": 40,
        "name": "npc_dota_hero_venomancer",
        "localized_name": "Venomancer",
        "localized_name_ru": "Веномансер",
        "primary_attr": "all",
        "attack_type": "Ranged",
        "roles": "Support,Nuker,Initiator,Pusher,Disabler",
        "icon_key": "venomancer",
        "aliases": ["веник", "змея", "сопля", "яд", "veno", "venomancer"]
    },
    {
        "id": 41,
        "name": "npc_dota_hero_faceless_void",
        "localized_name": "Faceless Void",
        "localized_name_ru": "Фейслес Войд",
        "primary_attr": "agi",
        "attack_type": "Melee",
        "roles": "Carry,Initiator,Disabler,Escape,Durable",
        "icon_key": "faceless_void",
        "aliases": ["войд", "купол", "хроносфера", "бздун", "void", "faceless void", "darkterror"]
    },
    {
        "id": 42,
        "name": "npc_dota_hero_skeleton_king",
        "localized_name": "Wraith King",
        "localized_name_ru": "Врейс Кинг",
        "primary_attr": "str",
        "attack_type": "Melee",
        "roles": "Carry,Support,Durable,Disabler,Initiator",
        "icon_key": "skeleton_king",
        "aliases": ["вк", "папич", "леорик", "король", "скелет", "wk", "wraith king", "leoric"]
    },
    {
        "id": 43,
        "name": "npc_dota_hero_death_prophet",
        "localized_name": "Death Prophet",
        "localized_name_ru": "Дез Профет",
        "primary_attr": "int",
        "attack_type": "Ranged",
        "roles": "Carry,Pusher,Nuker,Disabler",
        "icon_key": "death_prophet",
        "aliases": ["банша", "дп", "духи", "dp", "death prophet", "krobelus"]
    },
    {
        "id": 44,
        "name": "npc_dota_hero_phantom_assassin",
        "localized_name": "Phantom Assassin",
        "localized_name_ru": "Фантом Ассасин",
        "primary_attr": "agi",
        "attack_type": "Melee",
        "roles": "Carry,Escape",
        "icon_key": "phantom_assassin",
        "aliases": ["па", "мортра", "криты", "кинжал", "фантомка", "pa", "phantom assassin", "mortred"]
    },
    {
        "id": 45,
        "name": "npc_dota_hero_pugna",
        "localized_name": "Pugna",
        "localized_name_ru": "Пугна",
        "primary_attr": "int",
        "attack_type": "Ranged",
        "roles": "Nuker,Pusher,Support",
        "icon_key": "pugna",
        "aliases": ["пугна", "соска", "вардило", "варды", "зеленый", "pugna"]
    },
    {
        "id": 46,
        "name": "npc_dota_hero_templar_assassin",
        "localized_name": "Templar Assassin",
        "localized_name_ru": "Темплар Ассасин",
        "primary_attr": "agi",
        "attack_type": "Ranged",
        "roles": "Carry,Escape",
        "icon_key": "templar_assassin",
        "aliases": ["та", "ланая", "темпларка", "рефракшн", "ta", "templar assassin", "lanaya"]
    },
    {
        "id": 47,
        "name": "npc_dota_hero_viper",
        "localized_name": "Viper",
        "localized_name_ru": "Вайпер",
        "primary_attr": "agi",
        "attack_type": "Ranged",
        "roles": "Carry,Durable,Initiator,Disabler",
        "icon_key": "viper",
        "aliases": ["вайпер", "плювалка", "змея", "viper", "netherdrake"]
    },
    {
        "id": 48,
        "name": "npc_dota_hero_luna",
        "localized_name": "Luna",
        "localized_name_ru": "Луна",
        "primary_attr": "agi",
        "attack_type": "Ranged",
        "roles": "Carry,Nuker,Pusher",
        "icon_key": "luna",
        "aliases": ["луна", "пантера", "эклипс", "лучик", "luna", "moon"]
    },
    {
        "id": 49,
        "name": "npc_dota_hero_dragon_knight",
        "localized_name": "Dragon Knight",
        "localized_name_ru": "Драгон Найт",
        "primary_attr": "str",
        "attack_type": "Melee",
        "roles": "Carry,Pusher,Durable,Disabler,Initiator,Nuker",
        "icon_key": "dragon_knight",
        "aliases": ["дк", "дракон", "рыцарь", "давион", "dk", "dragon knight", "davion"]
    },
    {
        "id": 50,
        "name": "npc_dota_hero_dazzle",
        "localized_name": "Dazzle",
        "localized_name_ru": "Даззл",
        "primary_attr": "all",
        "attack_type": "Ranged",
        "roles": "Support,Nuker,Disabler",
        "icon_key": "dazzle",
        "aliases": ["дазл", "даззл", "крест", "грэйв", "dazzle", "shadow priest"]
    },
    {
        "id": 51,
        "name": "npc_dota_hero_rattletrap",
        "localized_name": "Clockwerk",
        "localized_name_ru": "Клокверк",
        "primary_attr": "all",
        "attack_type": "Melee",
        "roles": "Initiator,Disabler,Durable,Nuker",
        "icon_key": "rattletrap",
        "aliases": ["клок", "клокверк", "консервная банка", "коги", "clock", "clockwerk"]
    },
    {
        "id": 52,
        "name": "npc_dota_hero_leshrac",
        "localized_name": "Leshrac",
        "localized_name_ru": "Лешрак",
        "primary_attr": "int",
        "attack_type": "Ranged",
        "roles": "Carry,Support,Nuker,Pusher,Disabler",
        "icon_key": "leshrac",
        "aliases": ["леший", "конь", "лешрак", "дискотека", "lesh", "leshrac", "tormented soul"]
    },
    {
        "id": 53,
        "name": "npc_dota_hero_furion",
        "localized_name": "Nature's Prophet",
        "localized_name_ru": "Фурион",
        "primary_attr": "int",
        "attack_type": "Ranged",
        "roles": "Carry,Pusher,Escape,Nuker",
        "icon_key": "furion",
        "aliases": ["фурион", "фура", "профет", "пни", "np", "natures prophet", "furion"]
    },
    {
        "id": 54,
        "name": "npc_dota_hero_life_stealer",
        "localized_name": "Lifestealer",
        "localized_name_ru": "Лайфстилер",
        "primary_attr": "str",
        "attack_type": "Melee",
        "roles": "Carry,Durable,Escape,Disabler",
        "icon_key": "life_stealer",
        "aliases": ["гуля", "наикс", "найкс", "гуль", "собака", "ls", "lifestealer", "naix"]
    },
    {
        "id": 55,
        "name": "npc_dota_hero_dark_seer",
        "localized_name": "Dark Seer",
        "localized_name_ru": "Дарк Сир",
        "primary_attr": "all",
        "attack_type": "Melee",
        "roles": "Initiator,Escape,Disabler",
        "icon_key": "dark_seer",
        "aliases": ["дс", "сир", "стена", "стяжка", "щиток", "ds", "dark seer", "ishkafel"]
    },
    {
        "id": 56,
        "name": "npc_dota_hero_clinkz",
        "localized_name": "Clinkz",
        "localized_name_ru": "Клинкз",
        "primary_attr": "agi",
        "attack_type": "Ranged",
        "roles": "Carry,Escape,Pusher",
        "icon_key": "clinkz",
        "aliases": ["клинкз", "боник", "скелет", "инвизер", "clinkz", "bone"]
    },
    {
        "id": 57,
        "name": "npc_dota_hero_omniknight",
        "localized_name": "Omniknight",
        "localized_name_ru": "Омникнайт",
        "primary_attr": "str",
        "attack_type": "Melee",
        "roles": "Support,Durable,Nuker",
        "icon_key": "omniknight",
        "aliases": ["омник", "хилер", "репел", "паладин", "omni", "omniknight"]
    },
    {
        "id": 58,
        "name": "npc_dota_hero_enchantress",
        "localized_name": "Enchantress",
        "localized_name_ru": "Энчантресс",
        "primary_attr": "all",
        "attack_type": "Ranged",
        "roles": "Support,Pusher,Durable,Nuker",
        "icon_key": "enchantress",
        "aliases": ["энча", "коза", "олененок", "айлуш", "encha", "enchantress", "bambi"]
    },
    {
        "id": 59,
        "name": "npc_dota_hero_huskar",
        "localized_name": "Huskar",
        "localized_name_ru": "Хускар",
        "primary_attr": "str",
        "attack_type": "Ranged",
        "roles": "Carry,Durable,Initiator",
        "icon_key": "huskar",
        "aliases": ["хуск", "хускар", "копья", "прыжок", "huskar"]
    },
    {
        "id": 60,
        "name": "npc_dota_hero_night_stalker",
        "localized_name": "Night Stalker",
        "localized_name_ru": "Найт Сталкер",
        "primary_attr": "str",
        "attack_type": "Melee",
        "roles": "Carry,Initiator,Durable,Disabler,Nuker",
        "icon_key": "night_stalker",
        "aliases": ["нс", "баланар", "вампир", "ночь", "ns", "night stalker", "balanar"]
    },
    {
        "id": 61,
        "name": "npc_dota_hero_broodmother",
        "localized_name": "Broodmother",
        "localized_name_ru": "Брудмазер",
        "primary_attr": "all",
        "attack_type": "Melee",
        "roles": "Carry,Pusher,Escape,Nuker",
        "icon_key": "broodmother",
        "aliases": ["бруда", "паучиха", "пауки", "паутина", "brood", "broodmother"]
    },
    {
        "id": 62,
        "name": "npc_dota_hero_bounty_hunter",
        "localized_name": "Bounty Hunter",
        "localized_name_ru": "Баунти Хантер",
        "primary_attr": "agi",
        "attack_type": "Melee",
        "roles": "Escape,Nuker",
        "icon_key": "bounty_hunter",
        "aliases": ["бх", "гондар", "трек", "монетка", "bh", "bounty hunter", "gondar"]
    },
    {
        "id": 63,
        "name": "npc_dota_hero_weaver",
        "localized_name": "Weaver",
        "localized_name_ru": "Вивер",
        "primary_attr": "agi",
        "attack_type": "Ranged",
        "roles": "Carry,Escape",
        "icon_key": "weaver",
        "aliases": ["вивер", "жук", "шукучи", "таймлепс", "weaver", "skitskurr"]
    },
    {
        "id": 64,
        "name": "npc_dota_hero_jakiro",
        "localized_name": "Jakiro",
        "localized_name_ru": "Джакиро",
        "primary_attr": "int",
        "attack_type": "Ranged",
        "roles": "Support,Nuker,Pusher,Disabler",
        "icon_key": "jakiro",
        "aliases": ["джакиро", "дракон", "двухголовый", "лед и пламя", "thd", "jakiro"]
    },
    {
        "id": 65,
        "name": "npc_dota_hero_batrider",
        "localized_name": "Batrider",
        "localized_name_ru": "Бэтрайдер",
        "primary_attr": "all",
        "attack_type": "Ranged",
        "roles": "Initiator,Disabler,Escape",
        "icon_key": "batrider",
        "aliases": ["бет", "летучая мышь", "лассо", "масло", "bat", "batrider"]
    },
    {
        "id": 66,
        "name": "npc_dota_hero_chen",
        "localized_name": "Chen",
        "localized_name_ru": "Чен",
        "primary_attr": "all",
        "attack_type": "Ranged",
        "roles": "Support,Pusher",
        "icon_key": "chen",
        "aliases": ["чен", "зоопарк", "крипы", "священник", "chen"]
    },
    {
        "id": 67,
        "name": "npc_dota_hero_spectre",
        "localized_name": "Spectre",
        "localized_name_ru": "Спектра",
        "primary_attr": "agi",
        "attack_type": "Melee",
        "roles": "Carry,Durable,Escape",
        "icon_key": "spectre",
        "aliases": ["спектра", "меркуриал", "дисперсия", "иллюзии", "spec", "spectre", "mercurial"]
    },
    {
        "id": 68,
        "name": "npc_dota_hero_ancient_apparition",
        "localized_name": "Ancient Apparition",
        "localized_name_ru": "Аппарат",
        "primary_attr": "int",
        "attack_type": "Ranged",
        "roles": "Support,Disabler,Nuker",
        "icon_key": "ancient_apparition",
        "aliases": ["аппарат", "аа", "мороженое", "ледышка", "aa", "ancient apparition", "kaldr"]
    },
    {
        "id": 69,
        "name": "npc_dota_hero_doom_bringer",
        "localized_name": "Doom",
        "localized_name_ru": "Дум",
        "primary_attr": "str",
        "attack_type": "Melee",
        "roles": "Carry,Disabler,Initiator,Durable,Nuker",
        "icon_key": "doom_bringer",
        "aliases": ["дум", "люцифер", "печать", "пожиратель", "doom", "lucifer"]
    },
    {
        "id": 70,
        "name": "npc_dota_hero_ursa",
        "localized_name": "Ursa",
        "localized_name_ru": "Урса",
        "primary_attr": "agi",
        "attack_type": "Melee",
        "roles": "Carry,Durable,Disabler",
        "icon_key": "ursa",
        "aliases": ["урса", "медведь", "мишка", "рошан", "когти", "ursa", "fuzzi-wuzzi"]
    },
    {
        "id": 71,
        "name": "npc_dota_hero_spirit_breaker",
        "localized_name": "Spirit Breaker",
        "localized_name_ru": "Спирит Брейкер",
        "primary_attr": "str",
        "attack_type": "Melee",
        "roles": "Initiator,Durable,Disabler,Escape",
        "icon_key": "spirit_breaker",
        "aliases": ["бара", "корова", "разбег", "баратрум", "сб", "bara", "spirit breaker", "sb", "barathrum"]
    },
    {
        "id": 72,
        "name": "npc_dota_hero_gyrocopter",
        "localized_name": "Gyrocopter",
        "localized_name_ru": "Гирокоптер",
        "primary_attr": "agi",
        "attack_type": "Ranged",
        "roles": "Carry,Nuker,Disabler",
        "icon_key": "gyrocopter",
        "aliases": ["гиро", "вертолет", "самолет", "дед", "gyro", "gyrocopter", "aurel"]
    },
    {
        "id": 73,
        "name": "npc_dota_hero_alchemist",
        "localized_name": "Alchemist",
        "localized_name_ru": "Алхимик",
        "primary_attr": "str",
        "attack_type": "Melee",
        "roles": "Carry,Support,Durable,Disabler,Nuker",
        "icon_key": "alchemist",
        "aliases": ["алхим", "алхимик", "гоблин", "золото", "монетка", "alch", "alchemist", "razzil"]
    },
    {
        "id": 74,
        "name": "npc_dota_hero_invoker",
        "localized_name": "Invoker",
        "localized_name_ru": "Инвокер",
        "primary_attr": "all",
        "attack_type": "Ranged",
        "roles": "Carry,Nuker,Disabler,Escape,Pusher",
        "icon_key": "invoker",
        "aliases": ["инвокер", "вокер", "пианист", "карл", "сферы", "санстрайк", "invoker", "karl", "kael"]
    },
    {
        "id": 75,
        "name": "npc_dota_hero_silencer",
        "localized_name": "Silencer",
        "localized_name_ru": "Сайленсер",
        "primary_attr": "int",
        "attack_type": "Ranged",
        "roles": "Carry,Support,Disabler,Initiator,Nuker",
        "icon_key": "silencer",
        "aliases": ["сало", "сайленсер", "глобал", "кража интеллекта", "silencer", "nortrom"]
    },
    {
        "id": 76,
        "name": "npc_dota_hero_obsidian_destroyer",
        "localized_name": "Outworld Destroyer",
        "localized_name_ru": "Аутворлд Дестроер",
        "primary_attr": "int",
        "attack_type": "Ranged",
        "roles": "Carry,Nuker,Disabler",
        "icon_key": "obsidian_destroyer",
        "aliases": ["од", "дестр", "птица", "астрал", "od", "outworld destroyer", "obsidian"]
    },
    {
        "id": 77,
        "name": "npc_dota_hero_lycan",
        "localized_name": "Lycan",
        "localized_name_ru": "Ликан",
        "primary_attr": "all",
        "attack_type": "Melee",
        "roles": "Carry,Pusher,Durable,Escape",
        "icon_key": "lycan",
        "aliases": ["ликан", "волк", "собака", "зубы", "люкан", "lycan", "banehallow"]
    },
    {
        "id": 78,
        "name": "npc_dota_hero_brewmaster",
        "localized_name": "Brewmaster",
        "localized_name_ru": "Брюмастер",
        "primary_attr": "all",
        "attack_type": "Melee",
        "roles": "Carry,Initiator,Durable,Disabler,Nuker,Escape",
        "icon_key": "brewmaster",
        "aliases": ["панда", "брю", "пивовар", "брюмастер", "хмелевар", "brew", "brewmaster", "mangix"]
    },
    {
        "id": 79,
        "name": "npc_dota_hero_shadow_demon",
        "localized_name": "Shadow Demon",
        "localized_name_ru": "Шадоу Демон",
        "primary_attr": "int",
        "attack_type": "Ranged",
        "roles": "Support,Disabler,Initiator,Nuker",
        "icon_key": "shadow_demon",
        "aliases": ["сд", "демон", "иллюзии", "яд", "sd", "shadow demon", "eredar"]
    },
    {
        "id": 80,
        "name": "npc_dota_hero_lone_druid",
        "localized_name": "Lone Druid",
        "localized_name_ru": "Лон Друид",
        "primary_attr": "all",
        "attack_type": "Ranged",
        "roles": "Carry,Pusher,Durable",
        "icon_key": "lone_druid",
        "aliases": ["друид", "мишка", "силла", "лд", "ld", "lone druid", "sylla"]
    },
    {
        "id": 81,
        "name": "npc_dota_hero_chaos_knight",
        "localized_name": "Chaos Knight",
        "localized_name_ru": "Хаос Найт",
        "primary_attr": "str",
        "attack_type": "Melee",
        "roles": "Carry,Disabler,Durable,Pusher,Initiator",
        "icon_key": "chaos_knight",
        "aliases": ["цк", "хаос", "конь", "рандом", "иллюзии", "ck", "chaos knight", "nessaj"]
    },
    {
        "id": 82,
        "name": "npc_dota_hero_meepo",
        "localized_name": "Meepo",
        "localized_name_ru": "Мипо",
        "primary_attr": "agi",
        "attack_type": "Melee",
        "roles": "Carry,Escape,Nuker,Disabler,Initiator,Pusher",
        "icon_key": "meepo",
        "aliases": ["мипо", "геомансер", "лопата", "клоны", "meepo", "geomancer"]
    },
    {
        "id": 83,
        "name": "npc_dota_hero_treant",
        "localized_name": "Treant Protector",
        "localized_name_ru": "Трент Протектор",
        "primary_attr": "str",
        "attack_type": "Melee",
        "roles": "Support,Initiator,Durable,Disabler,Escape",
        "icon_key": "treant",
        "aliases": ["дерево", "трент", "пень", "рут", "treant", "tree", "rooftrellen"]
    },
    {
        "id": 84,
        "name": "npc_dota_hero_ogre_magi",
        "localized_name": "Ogre Magi",
        "localized_name_ru": "Огр Маг",
        "primary_attr": "str",
        "attack_type": "Melee",
        "roles": "Support,Nuker,Disabler,Durable,Initiator",
        "icon_key": "ogre_magi",
        "aliases": ["огр", "огр маг", "мультикаст", "дубина", "два дебила", "ogre", "ogre magi"]
    },
    {
        "id": 85,
        "name": "npc_dota_hero_undying",
        "localized_name": "Undying",
        "localized_name_ru": "Андаинг",
        "primary_attr": "str",
        "attack_type": "Melee",
        "roles": "Support,Durable,Disabler,Nuker",
        "icon_key": "undying",
        "aliases": ["зомби", "бомж", "томба", "андаинг", "дирга", "undying", "dirge"]
    },
    {
        "id": 86,
        "name": "npc_dota_hero_rubick",
        "localized_name": "Rubick",
        "localized_name_ru": "Рубик",
        "primary_attr": "int",
        "attack_type": "Ranged",
        "roles": "Support,Disabler,Nuker",
        "icon_key": "rubick",
        "aliases": ["рубик", "вор", "маг", "телекинез", "rubick", "grand magus"]
    },
    {
        "id": 87,
        "name": "npc_dota_hero_disruptor",
        "localized_name": "Disruptor",
        "localized_name_ru": "Дисраптор",
        "primary_attr": "int",
        "attack_type": "Ranged",
        "roles": "Support,Disabler,Nuker,Initiator",
        "icon_key": "disruptor",
        "aliases": ["тралл", "дисраптор", "купол", "забор", "дизраптор", "disruptor", "thrall"]
    },
    {
        "id": 88,
        "name": "npc_dota_hero_nyx_assassin",
        "localized_name": "Nyx Assassin",
        "localized_name_ru": "Никс Ассасин",
        "primary_attr": "all",
        "attack_type": "Melee",
        "roles": "Disabler,Nuker,Initiator,Escape",
        "icon_key": "nyx_assassin",
        "aliases": ["никс", "жук", "шипы", "карапасы", "анубарак", "nyx", "anubarak"]
    },
    {
        "id": 89,
        "name": "npc_dota_hero_naga_siren",
        "localized_name": "Naga Siren",
        "localized_name_ru": "Нага Сирена",
        "primary_attr": "agi",
        "attack_type": "Melee",
        "roles": "Carry,Support,Pusher,Disabler,Initiator,Escape",
        "icon_key": "naga_siren",
        "aliases": ["нага", "сирена", "сон", "иллюзии", "сетка", "naga", "slithice"]
    },
    {
        "id": 90,
        "name": "npc_dota_hero_keeper_of_the_light",
        "localized_name": "Keeper of the Light",
        "localized_name_ru": "Котл",
        "primary_attr": "int",
        "attack_type": "Ranged",
        "roles": "Support,Nuker,Disabler",
        "icon_key": "keeper_of_the_light",
        "aliases": ["котл", "дед на коне", "эзалор", "луч", "мана", "kotl", "keeper", "ezalor"]
    },
    {
        "id": 91,
        "name": "npc_dota_hero_wisp",
        "localized_name": "Io",
        "localized_name_ru": "Ио",
        "primary_attr": "all",
        "attack_type": "Ranged",
        "roles": "Support,Escape,Nuker",
        "icon_key": "wisp",
        "aliases": ["висп", "шарик", "ио", "релокейт", "тизер", "io", "wisp"]
    },
    {
        "id": 92,
        "name": "npc_dota_hero_visage",
        "localized_name": "Visage",
        "localized_name_ru": "Визаж",
        "primary_attr": "all",
        "attack_type": "Ranged",
        "roles": "Support,Nuker,Durable,Disabler,Pusher",
        "icon_key": "visage",
        "aliases": ["визаж", "птицы", "горгульи", "некролик", "visage", "necrolic"]
    },
    {
        "id": 93,
        "name": "npc_dota_hero_slark",
        "localized_name": "Slark",
        "localized_name_ru": "Сларк",
        "primary_attr": "agi",
        "attack_type": "Melee",
        "roles": "Carry,Escape,Disabler,Nuker",
        "icon_key": "slark",
        "aliases": ["сларк", "рыба", "прыгун", "паунс", "тучка", "slark"]
    },
    {
        "id": 94,
        "name": "npc_dota_hero_medusa",
        "localized_name": "Medusa",
        "localized_name_ru": "Медуза",
        "primary_attr": "agi",
        "attack_type": "Ranged",
        "roles": "Carry,Disabler,Durable",
        "icon_key": "medusa",
        "aliases": ["дуза", "медуза", "змея", "щит", "взор", "duda", "medusa", "gorgon"]
    },
    {
        "id": 95,
        "name": "npc_dota_hero_troll_warlord",
        "localized_name": "Troll Warlord",
        "localized_name_ru": "Тролль Варлорд",
        "primary_attr": "agi",
        "attack_type": "Ranged",
        "roles": "Carry,Pusher,Disabler,Durable",
        "icon_key": "troll_warlord",
        "aliases": ["тролль", "варлорд", "топоры", "джахракал", "troll", "troll warlord", "jahrakal"]
    },
    {
        "id": 96,
        "name": "npc_dota_hero_centaur",
        "localized_name": "Centaur Warrunner",
        "localized_name_ru": "Кентавр",
        "primary_attr": "str",
        "attack_type": "Melee",
        "roles": "Durable,Initiator,Disabler,Nuker",
        "icon_key": "centaur",
        "aliases": ["кентавр", "кент", "конь", "стамп", "телега", "centaur", "bradwarden"]
    },
    {
        "id": 97,
        "name": "npc_dota_hero_magnataur",
        "localized_name": "Magnus",
        "localized_name_ru": "Магнус",
        "primary_attr": "all",
        "attack_type": "Melee",
        "roles": "Initiator,Disabler,Nuker,Escape",
        "icon_key": "magnataur",
        "aliases": ["магнус", "рп", "скьювер", "мамонт", "носорог", "rp", "magnus", "magnataur"]
    },
    {
        "id": 98,
        "name": "npc_dota_hero_shredder",
        "localized_name": "Timbersaw",
        "localized_name_ru": "Тимберсоу",
        "primary_attr": "all",
        "attack_type": "Melee",
        "roles": "Nuker,Durable,Escape",
        "icon_key": "shredder",
        "aliases": ["тимбер", "пила", "дереворуб", "ризан", "timber", "timbersaw", "rizzrack"]
    },
    {
        "id": 99,
        "name": "npc_dota_hero_bristleback",
        "localized_name": "Bristleback",
        "localized_name_ru": "Бристлбек",
        "primary_attr": "str",
        "attack_type": "Melee",
        "roles": "Carry,Durable,Initiator,Nuker",
        "icon_key": "bristleback",
        "aliases": ["брист", "свинья", "еж", "спина", "колючки", "сопли", "bb", "bristle", "bristleback"]
    },
    {
        "id": 100,
        "name": "npc_dota_hero_tusk",
        "localized_name": "Tusk",
        "localized_name_ru": "Таск",
        "primary_attr": "str",
        "attack_type": "Melee",
        "roles": "Initiator,Disabler,Nuker",
        "icon_key": "tusk",
        "aliases": ["таск", "морж", "снежок", "удар", "tusk", "ymir"]
    },
    {
        "id": 101,
        "name": "npc_dota_hero_skywrath_mage",
        "localized_name": "Skywrath Mage",
        "localized_name_ru": "Скайрас Маг",
        "primary_attr": "int",
        "attack_type": "Ranged",
        "roles": "Support,Nuker,Disabler",
        "icon_key": "skywrath_mage",
        "aliases": ["петух", "скай", "птица", "ульт", "sky", "skywrath", "dragonus"]
    },
    {
        "id": 102,
        "name": "npc_dota_hero_abaddon",
        "localized_name": "Abaddon",
        "localized_name_ru": "Абаддон",
        "primary_attr": "all",
        "attack_type": "Melee",
        "roles": "Support,Carry,Durable",
        "icon_key": "abaddon",
        "aliases": ["аба", "абаддон", "щит", "всадник", "abaddon", "aba"]
    },
    {
        "id": 103,
        "name": "npc_dota_hero_elder_titan",
        "localized_name": "Elder Titan",
        "localized_name_ru": "Элдер Титан",
        "primary_attr": "str",
        "attack_type": "Melee",
        "roles": "Initiator,Disabler,Nuker,Durable",
        "icon_key": "elder_titan",
        "aliases": ["ет", "титан", "чемодан", "дух", "топот", "et", "elder titan"]
    },
    {
        "id": 104,
        "name": "npc_dota_hero_legion_commander",
        "localized_name": "Legion Commander",
        "localized_name_ru": "Легион Коммандер",
        "primary_attr": "str",
        "attack_type": "Melee",
        "roles": "Carry,Disabler,Initiator,Durable,Nuker",
        "icon_key": "legion_commander",
        "aliases": ["легионка", "лк", "дуэль", "треска", "баба с мечом", "lc", "legion", "tresdin"]
    },
    {
        "id": 105,
        "name": "npc_dota_hero_techies",
        "localized_name": "Techies",
        "localized_name_ru": "Течис",
        "primary_attr": "all",
        "attack_type": "Ranged",
        "roles": "Nuker,Disabler",
        "icon_key": "techies",
        "aliases": ["минер", "течис", "бомбы", "суицид", "мины", "techies", "miner"]
    },
    {
        "id": 106,
        "name": "npc_dota_hero_ember_spirit",
        "localized_name": "Ember Spirit",
        "localized_name_ru": "Эмбер Спирит",
        "primary_attr": "agi",
        "attack_type": "Melee",
        "roles": "Carry,Escape,Nuker,Disabler,Initiator",
        "icon_key": "ember_spirit",
        "aliases": ["эмбер", "огонь", "реминанты", "фисты", "ember", "ember spirit", "xin"]
    },
    {
        "id": 107,
        "name": "npc_dota_hero_earth_spirit",
        "localized_name": "Earth Spirit",
        "localized_name_ru": "Эрф Спирит",
        "primary_attr": "str",
        "attack_type": "Melee",
        "roles": "Nuker,Escape,Disabler,Initiator,Durable",
        "icon_key": "earth_spirit",
        "aliases": ["земеля", "земля", "камни", "спирит", "earth", "earth spirit", "kaolin"]
    },
    {
        "id": 108,
        "name": "npc_dota_hero_underlord",
        "localized_name": "Underlord",
        "localized_name_ru": "Андерлорд",
        "primary_attr": "str",
        "attack_type": "Melee",
        "roles": "Support,Durable,Nuker,Disabler,Escape",
        "icon_key": "underlord",
        "aliases": ["питлорд", "андерлорд", "телепорт", "яма", "underlord", "pit lord", "pitlord", "abyssal"]
    },
    {
        "id": 109,
        "name": "npc_dota_hero_terrorblade",
        "localized_name": "Terrorblade",
        "localized_name_ru": "Террорблейд",
        "primary_attr": "agi",
        "attack_type": "Melee",
        "roles": "Carry,Pusher,Nuker",
        "icon_key": "terrorblade",
        "aliases": ["тб", "террор", "свап хп", "метаморфоза", "tb", "terrorblade"]
    },
    {
        "id": 110,
        "name": "npc_dota_hero_phoenix",
        "localized_name": "Phoenix",
        "localized_name_ru": "Феникс",
        "primary_attr": "all",
        "attack_type": "Ranged",
        "roles": "Support,Nuker,Initiator,Escape,Disabler",
        "icon_key": "phoenix",
        "aliases": ["феникс", "птица", "яйцо", "солнце", "луч", "phoenix"]
    },
    {
        "id": 111,
        "name": "npc_dota_hero_oracle",
        "localized_name": "Oracle",
        "localized_name_ru": "Оракул",
        "primary_attr": "int",
        "attack_type": "Ranged",
        "roles": "Support,Nuker,Disabler,Escape",
        "icon_key": "oracle",
        "aliases": ["оракул", "ульт оракула", "хил", "невидимка", "oracle", "nerif"]
    },
    {
        "id": 112,
        "name": "npc_dota_hero_winter_wyvern",
        "localized_name": "Winter Wyvern",
        "localized_name_ru": "Винтер Виверна",
        "primary_attr": "all",
        "attack_type": "Ranged",
        "roles": "Support,Disabler,Nuker",
        "icon_key": "winter_wyvern",
        "aliases": ["виверна", "вв", "курса", "хил", "драконша", "ww", "winter wyvern", "auroth"]
    },
    {
        "id": 113,
        "name": "npc_dota_hero_arc_warden",
        "localized_name": "Arc Warden",
        "localized_name_ru": "Арк Варден",
        "primary_attr": "agi",
        "attack_type": "Ranged",
        "roles": "Carry,Escape,Nuker",
        "icon_key": "arc_warden",
        "aliases": ["арк", "варден", "копия", "купол", "дублер", "arc", "arc warden", "zet"]
    },
    {
        "id": 114,
        "name": "npc_dota_hero_monkey_king",
        "localized_name": "Monkey King",
        "localized_name_ru": "Манки Кинг",
        "primary_attr": "agi",
        "attack_type": "Melee",
        "roles": "Carry,Escape,Disabler,Initiator",
        "icon_key": "monkey_king",
        "aliases": ["мк", "обезьяна", "палка", "деревья", "mk", "monkey king", "wukong"]
    },
    {
        "id": 119,
        "name": "npc_dota_hero_dark_willow",
        "localized_name": "Dark Willow",
        "localized_name_ru": "Дарк Виллоу",
        "primary_attr": "all",
        "attack_type": "Ranged",
        "roles": "Support,Nuker,Disabler,Escape",
        "icon_key": "dark_willow",
        "aliases": ["фея", "виллоу", "дв", "страх", "dw", "dark willow", "mireska"]
    },
    {
        "id": 120,
        "name": "npc_dota_hero_pangolier",
        "localized_name": "Pangolier",
        "localized_name_ru": "Пангольер",
        "primary_attr": "all",
        "attack_type": "Melee",
        "roles": "Carry,Nuker,Disabler,Durable,Escape,Initiator",
        "icon_key": "pangolier",
        "aliases": ["панго", "броненосец", "шар", "шпага", "pango", "pangolier", "dont"]
    },
    {
        "id": 121,
        "name": "npc_dota_hero_grimstroke",
        "localized_name": "Grimstroke",
        "localized_name_ru": "Гримстрок",
        "primary_attr": "int",
        "attack_type": "Ranged",
        "roles": "Support,Nuker,Disabler,Escape",
        "icon_key": "grimstroke",
        "aliases": ["грим", "кисть", "связка", "художник", "grim", "grimstroke"]
    },
    {
        "id": 123,
        "name": "npc_dota_hero_hoodwink",
        "localized_name": "Hoodwink",
        "localized_name_ru": "Худвинк",
        "primary_attr": "agi",
        "attack_type": "Ranged",
        "roles": "Support,Nuker,Escape,Disabler",
        "icon_key": "hoodwink",
        "aliases": ["белка", "худвинк", "арбалет", "орех", "hoodwink", "squirrel"]
    },
    {
        "id": 126,
        "name": "npc_dota_hero_void_spirit",
        "localized_name": "Void Spirit",
        "localized_name_ru": "Войд Спирит",
        "primary_attr": "all",
        "attack_type": "Melee",
        "roles": "Carry,Escape,Nuker,Disabler",
        "icon_key": "void_spirit",
        "aliases": ["спирит", "войд спирит", "фиолетовый", "астрал", "inai", "void spirit"]
    },
    {
        "id": 128,
        "name": "npc_dota_hero_snapfire",
        "localized_name": "Snapfire",
        "localized_name_ru": "Снэпфайр",
        "primary_attr": "all",
        "attack_type": "Ranged",
        "roles": "Support,Nuker,Disabler,Escape",
        "icon_key": "snapfire",
        "aliases": ["бабка", "ящерица", "снапфайр", "печенька", "пулемет", "snapfire", "mortimer"]
    },
    {
        "id": 129,
        "name": "npc_dota_hero_mars",
        "localized_name": "Mars",
        "localized_name_ru": "Марс",
        "primary_attr": "str",
        "attack_type": "Melee",
        "roles": "Initiator,Durable,Disabler,Nuker",
        "icon_key": "mars",
        "aliases": ["марс", "арена", "копье", "щит", "римлянин", "mars"]
    },
    {
        "id": 135,
        "name": "npc_dota_hero_dawnbreaker",
        "localized_name": "Dawnbreaker",
        "localized_name_ru": "Даунбрейкер",
        "primary_attr": "str",
        "attack_type": "Melee",
        "roles": "Carry,Durable",
        "icon_key": "dawnbreaker",
        "aliases": ["валдай", "даунбрейкер", "молот", "звезда", "db", "dawnbreaker", "valora"]
    },
    {
        "id": 136,
        "name": "npc_dota_hero_marci",
        "localized_name": "Marci",
        "localized_name_ru": "Марси",
        "primary_attr": "all",
        "attack_type": "Melee",
        "roles": "Support,Carry,Initiator,Disabler,Escape",
        "icon_key": "marci",
        "aliases": ["марси", "немая", "аниме", "кулаки", "бросок", "marci"]
    },
    {
        "id": 137,
        "name": "npc_dota_hero_primal_beast",
        "localized_name": "Primal Beast",
        "localized_name_ru": "Праймал Бист",
        "primary_attr": "str",
        "attack_type": "Melee",
        "roles": "Initiator,Durable,Disabler,Nuker",
        "icon_key": "primal_beast",
        "aliases": ["пб", "бист", "динозавр", "захват", "разбег", "pb", "primal", "primal beast"]
    },
    {
        "id": 138,
        "name": "npc_dota_hero_muerta",
        "localized_name": "Muerta",
        "localized_name_ru": "Муэрта",
        "primary_attr": "int",
        "attack_type": "Ranged",
        "roles": "Carry,Nuker,Disabler",
        "icon_key": "muerta",
        "aliases": ["муэрта", "пистолеты", "призрак", "мексиканка", "muerta"]
    },
    {
        "id": 139,
        "name": "npc_dota_hero_ringmaster",
        "localized_name": "Ringmaster",
        "localized_name_ru": "Рингмастер",
        "primary_attr": "int",
        "attack_type": "Ranged",
        "roles": "Support,Nuker,Disabler",
        "icon_key": "ringmaster",
        "aliases": ["рингмастер", "циркач", "колесо", "клоун", "ringmaster"]
    },
    {
        "id": 145,
        "name": "npc_dota_hero_kez",
        "localized_name": "Kez",
        "localized_name_ru": "Кез",
        "primary_attr": "agi",
        "attack_type": "Melee",
        "roles": "Carry,Escape,Nuker",
        "icon_key": "kez",
        "aliases": ["кез", "птица самурай", "катана", "kez"]
    }
]

# Build lookup tables
HERO_LIST = []
HERO_BY_ID = {}
HERO_BY_NAME = {}

for h in ALL_HEROES_DATA:
    icon_url = f"{STEAM_CDN_BASE}/{h['icon_key']}.png"
    hero_obj = {
        "id": h["id"],
        "name": h["name"],
        "localized_name": h["localized_name"],
        "localized_name_ru": h["localized_name_ru"],
        "primary_attr": h["primary_attr"],
        "attack_type": h["attack_type"],
        "roles": h["roles"],
        "icon_url": icon_url,
        "aliases": h["aliases"]
    }
    HERO_LIST.append(hero_obj)
    HERO_BY_ID[h["id"]] = hero_obj
    HERO_BY_NAME[h["name"]] = hero_obj

def search_heroes(query: str):
    """
    Search heroes by substring in English name, Russian name, or CIS slang aliases.
    """
    if not query:
        return HERO_LIST
    
    q = query.lower().strip()
    results = []
    for h in HERO_LIST:
        # Check direct names
        if q in h["localized_name"].lower() or q in h["localized_name_ru"].lower():
            results.append(h)
            continue
        # Check aliases
        if any(q in alias.lower() for alias in h["aliases"]):
            results.append(h)
    return results
