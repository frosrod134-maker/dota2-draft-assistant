"""
Per-Hero Ability & Playstyle Signature Map for all 126 Dota 2 Heroes.
Used by the Hero Guides Tactical Engine to generate 100% unique,
non-repetitive, high-MMR gameplay explanations without copy-paste fallbacks.
"""

HERO_SIGNATURES: dict[int, dict] = {
    1: {
        "name": "Anti-Mage",
        "role": "carry",
        "style": "elusive",
        "sig": "выжигает ману ударами Mana Break, сплитпушит с блинком и стирает прокастеров ультимейтом Mana Void"
    },
    2: {
        "name": "Axe",
        "role": "offlane",
        "style": "frontline",
        "sig": "врывается с Blink Dagger, провоцирует через Berserker's Call и рубит топором Culling Blade"
    },
    3: {
        "name": "Bane",
        "role": "support",
        "style": "backline",
        "sig": "держит ключевую цель в контроле сквозь BKB через Fiend's Grip, выводит из драки Nightmare и ослабляет урон Enfeeble"
    },
    4: {
        "name": "Bloodseeker",
        "role": "carry",
        "style": "frontline",
        "sig": "намертво привязывает цель ультимейтом Rupture, разгоняется пассивкой Thirst и наносит чистый урон под Bloodrage"
    },
    5: {
        "name": "Crystal Maiden",
        "role": "support",
        "style": "backline",
        "sig": "замедляет область через Crystal Nova, фиксирует цель Frostbite и заливает ману аурой Arcane Aura"
    },
    6: {
        "name": "Drow Ranger",
        "role": "carry",
        "style": "backline",
        "sig": "расстреливает врагов ледяными стрелами Frost Arrows, дает сайленс волной Gust и пробивает броню ультой Marksmanship"
    },
    7: {
        "name": "Earthshaker",
        "role": "support",
        "style": "initiator",
        "sig": "выдает непрерывную цепочку станов Fissure / Enchant Totem и моментально стирает иллюзии и толпы комбо Echo Slam"
    },
    8: {
        "name": "Juggernaut",
        "role": "carry",
        "style": "frontline",
        "sig": "имеет встроенный иммунитет к магии в Blade Fury, лечит вардом Healing Ward и наносит колоссальный урон в Omnislash"
    },
    9: {
        "name": "Mirana",
        "role": "support",
        "style": "backline",
        "sig": "инициирует стрелой Sacred Arrow, разрывает дистанцию прыжком Leap и скрывает всю команду в невидимость Moonlight Shadow"
    },
    10: {
        "name": "Morphling",
        "role": "carry",
        "style": "elusive",
        "sig": "мгновенно меняет баланс силы и ловкости через Attribute Shift, наносит взрывной урон Adaptive Strike и копирует способности Morph"
    },
    11: {
        "name": "Shadow Fiend",
        "role": "mid",
        "style": "backline",
        "sig": "наносит взрывной урон койлами Shadowraze, снижает броню пассивкой Presence of the Dark Lord и ломает позиционку ультой Requiem of Souls"
    },
    12: {
        "name": "Phantom Lancer",
        "role": "carry",
        "style": "elusive",
        "sig": "плодит бесконечные копии через Juxtapose, выжигает ману диффузами и сбивает фокус способностью Doppelganger"
    },
    13: {
        "name": "Puck",
        "role": "mid",
        "style": "elusive",
        "sig": "избегает направленного урона через Phase Shift, блинкуется на Illusory Orb и привязывает врагов спиралью Dream Coil"
    },
    14: {
        "name": "Pudge",
        "role": "offlane",
        "style": "frontline",
        "sig": "вытягивает жертву из безопасной позиции крюком Meat Hook, замедляет аурой Rot и намертво держит ультимейтом Dismember"
    },
    15: {
        "name": "Razor",
        "role": "offlane",
        "style": "frontline",
        "sig": "высасывает физический урон через Static Link, крадет скорость движения и непрерывно бьет молниями Eye of the Storm"
    },
    16: {
        "name": "Sand King",
        "role": "offlane",
        "style": "initiator",
        "sig": "врывается с оглушением Burrowstrike, укрывается в песчаной буре Sand Storm и наносит колоссальный АоЕ-урон ультой Epicenter"
    },
    17: {
        "name": "Storm Spirit",
        "role": "mid",
        "style": "elusive",
        "sig": "летает через всё поле боя в Ball Lightning, стягивает жертву Vortex и наносит колоссальный берст Overload"
    },
    18: {
        "name": "Sven",
        "role": "carry",
        "style": "frontline",
        "sig": "врубает God's Strength, оглушает станом Storm Hammer и стирает вражеские ряды сплэшем Great Cleave"
    },
    19: {
        "name": "Tiny",
        "role": "mid",
        "style": "initiator",
        "sig": "мгновенно стирает цель прокастом Avalanche + Toss и наносит огромный урон с руки деревом Tree Grab"
    },
    20: {
        "name": "Vengeful Spirit",
        "role": "support",
        "style": "backline",
        "sig": "меняет позиционку ключевой цели ультимейтом Nether Swap, снижает броню Wave of Terror и дает ауру урона команде"
    },
    21: {
        "name": "Windranger",
        "role": "mid",
        "style": "elusive",
        "sig": "связывает врагов связкой Shackleshot, защищается от атак бегом Windrun и расстреливает цель под Focus Fire"
    },
    22: {
        "name": "Zeus",
        "role": "mid",
        "style": "backline",
        "sig": "закидывает врагов молниями Arc Lightning, сжигает процентное здоровье пассивкой и добивает ультимейтом Thundergod's Wrath / Nimbus"
    },
    23: {
        "name": "Kunkka",
        "role": "mid",
        "style": "frontline",
        "sig": "управляет позиционкой через X Marks the Spot, наносит урон сплэшем Tidebringer и накладывает бафф рома кораблем Ghostship"
    },
    25: {
        "name": "Lina",
        "role": "mid",
        "style": "backline",
        "sig": "наносит колоссальный магический прокаст Dragon Slave + Light Strike Array и стирает цель ультимейтом Laguna Blade"
    },
    26: {
        "name": "Lion",
        "role": "support",
        "style": "backline",
        "sig": "выдает надежный мгновенный хекс Hex, оглушает станом Earth Spike и взрывает цель ультимейтом Finger of Death"
    },
    27: {
        "name": "Shadow Shaman",
        "role": "support",
        "style": "backline",
        "sig": "держит цель в длительном контроле через Hex и Shackles, быстро ломая вышки змейками Mass Serpent Ward"
    },
    28: {
        "name": "Slardar",
        "role": "offlane",
        "style": "frontline",
        "sig": "врывается с блинка со станом Slithereen Crush, срезает броню ультимейтом Corrosive Haze и перманентно башит"
    },
    29: {
        "name": "Tidehunter",
        "role": "offlane",
        "style": "frontline",
        "sig": "впитывает тонны урона за счет пассивки Kraken Shell и переворачивает тимфайты глобальным ультимейтом Ravage"
    },
    30: {
        "name": "Witch Doctor",
        "role": "support",
        "style": "backline",
        "sig": "запускает прыгающий стан Paralyzing Cask, вешает смертельный маледикт Maledict и вносит урон Death Ward"
    },
    31: {
        "name": "Lich",
        "role": "support",
        "style": "backline",
        "sig": "накладывает защитную броню Frost Shield, притягивает врага Sinister Gaze и запускает отскакивающий Chain Frost"
    },
    32: {
        "name": "Riki",
        "role": "carry",
        "style": "elusive",
        "sig": "атакует со спины критическими ударами Backstab, блокирует обзор и скиллы тучкой Smoke Screen и прячется в Tricks of the Trade"
    },
    33: {
        "name": "Enigma",
        "role": "offlane",
        "style": "initiator",
        "sig": "стягивает всю вражескую команду в легендарный Black Hole и выжигает процентное здоровье поляной Midnight Pulse"
    },
    34: {
        "name": "Tinker",
        "role": "mid",
        "style": "backline",
        "sig": "спамит ослепляющим лазером Laser, зачищает зоны роботами March of the Machines, накладывает щит Defense Matrix со статус-резистом и перезаряжает способности через Rearm"
    },
    35: {
        "name": "Sniper",
        "role": "carry",
        "style": "backline",
        "sig": "расстреливает врагов с безопасной дистанции за счет дальности Take Aim, замедляет Shrapnel и добивает ультой Assassinate"
    },
    36: {
        "name": "Necrophos",
        "role": "mid",
        "style": "frontline",
        "sig": "лечит союзников и бьет врагов через Death Pulse, входит в астрал Ghost Shroud, выжигает здоровье аурой Heartstopper Aura и казнит ультимейтом Reaper's Scythe"
    },
    37: {
        "name": "Warlock",
        "role": "support",
        "style": "backline",
        "sig": "связывает врагов цепочкой урона Fatal Bonds, исцеляет союзников Shadow Word и обрушивает голема Chaotic Offering"
    },
    38: {
        "name": "Beastmaster",
        "role": "offlane",
        "style": "initiator",
        "sig": "дает надежный контроль сквозь BKB ультимейтом Primal Roar, дает вижн ястребом и пушит строения аурой Inner Beast"
    },
    39: {
        "name": "Queen of Pain",
        "role": "mid",
        "style": "elusive",
        "sig": "сокращает дистанцию блинком Blink, замедляет кинжалом Shadow Strike и сносит ряды чистым уроном Sonic Wave"
    },
    40: {
        "name": "Venomancer",
        "role": "support",
        "style": "backline",
        "sig": "замедляет всё поле боя ядовитыми змейками Plague Ward, заражает Poison Nova и лишает врагов мобильности"
    },
    41: {
        "name": "Faceless Void",
        "role": "carry",
        "style": "elusive",
        "sig": "ставит купол Chronosphere сквозь BKB, откатывает входящий урон через Time Walk и башит в Time Lock"
    },
    42: {
        "name": "Wraith King",
        "role": "carry",
        "style": "frontline",
        "sig": "воскресает в бою ультимейтом Reincarnation, наносит критические удары Mortal Strike и пушит скелетами"
    },
    43: {
        "name": "Death Prophet",
        "role": "mid",
        "style": "frontline",
        "sig": "впитывает урон высасыванием Spirit Siphon, дает сайленс Silence и сносит базы призраками Exorcism"
    },
    44: {
        "name": "Phantom Assassin",
        "role": "carry",
        "style": "elusive",
        "sig": "наносит ваншоты критическими ударами Coup de Grace, замедляет Stifling Dagger и избегает атак через Blur"
    },
    45: {
        "name": "Pugna",
        "role": "support",
        "style": "backline",
        "sig": "сжигает магов вардом Nether Ward, спамит Nether Blast по строениям и высасывает жизнь через Life Drain"
    },
    46: {
        "name": "Templar Assassin",
        "role": "carry",
        "style": "backline",
        "sig": "поглощает урон щитом Refraction, срезает броню Meld с дезолятором и замедляет карту ловушками Psionic Trap"
    },
    47: {
        "name": "Viper",
        "role": "mid",
        "style": "frontline",
        "sig": "накладывает истощение Nethertoxin, замедляет ядом Poison Attack и снижает сопротивления пассивкой Corrosive Skin"
    },
    48: {
        "name": "Luna",
        "role": "carry",
        "style": "backline",
        "sig": "нарезает все цели рикошетами Moon Glaives, разгоняет командный урон аурой и обрушивает Eclipse"
    },
    49: {
        "name": "Dragon Knight",
        "role": "mid",
        "style": "frontline",
        "sig": "оглушает надежным станом Dragon Tail, регенерирует броню и здоровье Dragon Blood и пушит в Elder Dragon Form"
    },
    50: {
        "name": "Dazzle",
        "role": "support",
        "style": "backline",
        "sig": "спасает от неминуемой смерти крестом Shallow Grave, снижает кулдауны ультой и лечит волной Shadow Wave"
    },
    51: {
        "name": "Clockwerk",
        "role": "support",
        "style": "initiator",
        "sig": "влетает через всю карту крюком Hookshot, закрывает цель в когах Power Cogs и прерывает касты Battery Assault"
    },
    52: {
        "name": "Leshrac",
        "role": "mid",
        "style": "frontline",
        "sig": "врывается в центр драки под Pulse Nova, сносит строения Diabolic Edict и оглушает станом Split Earth"
    },
    53: {
        "name": "Nature's Prophet",
        "role": "carry",
        "style": "backline",
        "sig": "телепортируется в любую точку карты через Teleportation, пушит трентами и наносит глобальный урон Wrath of Nature"
    },
    54: {
        "name": "Lifestealer",
        "role": "carry",
        "style": "frontline",
        "sig": "включает встроенный иммунитет к магии Rage, высасывает процентное HP через Feast и спасается в союзнике ультой Infest"
    },
    55: {
        "name": "Dark Seer",
        "role": "offlane",
        "style": "initiator",
        "sig": "стягивает врагов в вакуум Vacuum под стенку Wall of Replica и ускоряет союзников щитом Ion Shell"
    },
    56: {
        "name": "Clinkz",
        "role": "carry",
        "style": "elusive",
        "sig": "закидывает цель смолой Tar Bomb, поедает крипов через Death Pact, расстреливает под Strafe со скелетами-лучниками и нападает из инвиза Skeleton Walk"
    },
    57: {
        "name": "Omniknight",
        "role": "support",
        "style": "backline",
        "sig": "дает иммунитет к физическому урону ультимейтом Guardian Angel, лечит Purification, дает иммунитет к эффектам Repel и бьет чистым уроном Hammer of Purity"
    },
    58: {
        "name": "Enchantress",
        "role": "support",
        "style": "backline",
        "sig": "переманивает лесных крипов Enchant, защищается от атак замедлением Untouchable и пробивает ультимейтом Impetus"
    },
    59: {
        "name": "Huskar",
        "role": "mid",
        "style": "frontline",
        "sig": "наносит огромный урон копьями Burning Spear, прыгает в драку Life Break и бешено отхиливается на низком HP"
    },
    60: {
        "name": "Night Stalker",
        "role": "offlane",
        "style": "initiator",
        "sig": "доминирует на ночной карте под Dark Ascension, накладывает долгий сайленс Crippling Fear и ловит врагов Hunter in the Night"
    },
    61: {
        "name": "Broodmother",
        "role": "mid",
        "style": "elusive",
        "sig": "захватывает паутиной Spin Web линии, плодит орду паучат Spawn Spiderlings и вампирит под Insatiable Hunger"
    },
    62: {
        "name": "Bounty Hunter",
        "role": "support",
        "style": "elusive",
        "sig": "разведывает карту в инвизе Shadow Walk, вешает трек Track для бонусного золота и крадет деньги Jinada"
    },
    63: {
        "name": "Weaver",
        "role": "carry",
        "style": "elusive",
        "sig": "избегает фокуса максимальной скоростью Shukuchi, атакует дважды через Geminate Attack и откатывает время ультой Time Lapse"
    },
    64: {
        "name": "Jakiro",
        "role": "support",
        "style": "backline",
        "sig": "зонирует файты ледяной дорожкой Ice Path, сжигает ультимейтом Macropyre и замедляет атаки Liquid Fire"
    },
    65: {
        "name": "Batrider",
        "role": "mid",
        "style": "initiator",
        "sig": "заливает врагов напалмом Sticky Napalm, летает над деревьями Firefly и утаскивает ключевую цель в лассо Flaming Lasso"
    },
    66: {
        "name": "Chen",
        "role": "support",
        "style": "backline",
        "sig": "ведет армию подконтрольных крипов с аурами Holy Persuasion и глобально лечит команду ультимейтом Hand of God"
    },
    67: {
        "name": "Spectre",
        "role": "carry",
        "style": "frontline",
        "sig": "поглощает и отражает урон через Dispersion, наносит чистый урон одиночным целям Desolate и влетает ультой Haunt / Shadow Step"
    },
    68: {
        "name": "Ancient Apparition",
        "role": "support",
        "style": "backline",
        "sig": "запускает ледяной шар Ice Blast через всю карту, блокируя любое лечение и ваншотя цели с низким запасом здоровья"
    },
    69: {
        "name": "Doom",
        "role": "offlane",
        "style": "frontline",
        "sig": "выключает ключевого героя ультимейтом Doom сквозь BKB, ускоряется под Scorched Earth и фармит крипов Devour"
    },
    70: {
        "name": "Ursa",
        "role": "carry",
        "style": "frontline",
        "sig": "набивает экспоненциальный урон когтями Fury Swipes, мгновенно сносит Рошана и впитывает урон под ультимейтом Enrage"
    },
    71: {
        "name": "Spirit Breaker",
        "role": "support",
        "style": "initiator",
        "sig": "разгоняется через всю карту чарджем Charge of Darkness, сбивая позиционку башами Greater Bash сквозь BKB"
    },
    72: {
        "name": "Gyrocopter",
        "role": "carry",
        "style": "backline",
        "sig": "расстреливает всех врагов вокруг залпом Flak Cannon, замедляет ракетой Call Down и сносит соло-цели Rocket Barrage"
    },
    73: {
        "name": "Alchemist",
        "role": "carry",
        "style": "frontline",
        "sig": "фармит в разы быстрее карты пассивкой Greevil's Greed, регенерирует здоровье под Chemical Rage и дарит скипетры союзникам"
    },
    74: {
        "name": "Invoker",
        "role": "mid",
        "style": "backline",
        "sig": "комбинирует 10 заклинаний для глобального Sun Strike, контроля Tornado / EMP и разрушительного комбо Chaos Meteor"
    },
    75: {
        "name": "Silencer",
        "role": "support",
        "style": "backline",
        "sig": "сбивает любые прокасты и инициации глобальным безмолвием Global Silence и крадет интеллект при каждом убийстве"
    },
    76: {
        "name": "Outworld Destroyer",
        "role": "mid",
        "style": "backline",
        "sig": "прячет цели в астрал Astral Imprisonment, наносит чистый урон от маны Arcane Orb и взрывает драку ультой Sanity's Eclipse"
    },
    77: {
        "name": "Lycan",
        "role": "offlane",
        "style": "initiator",
        "sig": "разгоняет волков и команду ультимейтом Shapeshift до максимальной скорости, ломая строения за секунды под Howl"
    },
    78: {
        "name": "Brewmaster",
        "role": "offlane",
        "style": "frontline",
        "sig": "избегает атак пьяной стойкой Drunken Brawler и разделяется ультимейтом Primal Split на духов с полным набором контроля"
    },
    79: {
        "name": "Shadow Demon",
        "role": "support",
        "style": "backline",
        "sig": "сейвит союзников или ловит врагов в Disruption, заражает Shadow Poison и снимает баффы ультимейтом Demonic Purge"
    },
    80: {
        "name": "Lone Druid",
        "role": "carry",
        "style": "frontline",
        "sig": "сражается через бронированного медведя Spirit Bear с кор-слотами и увеличивает собственную плотность формой True Form"
    },
    81: {
        "name": "Chaos Knight",
        "role": "carry",
        "style": "frontline",
        "sig": "стягивает врага через Reality Rift, выдает непредсказуемый долгий стан Chaos Bolt и разрывает цель армией копий Phantasm"
    },
    82: {
        "name": "Meepo",
        "role": "mid",
        "style": "elusive",
        "sig": "связывает сетками Earthbind, вносит взрывной урон пуфами Poof и быстро пушит строения армией клонов"
    },
    83: {
        "name": "Treant Protector",
        "role": "support",
        "style": "backline",
        "sig": "лечит союзников и вышки броней Living Armor, замедляет семенами Leech Seed и связывает драку корнями Overgrowth"
    },
    84: {
        "name": "Ogre Magi",
        "role": "support",
        "style": "frontline",
        "sig": "впитывает урон за счет гигантской брони, разгоняет керри баффом Bloodlust и умножает заклинания мультикастом Multicast"
    },
    85: {
        "name": "Undying",
        "role": "support",
        "style": "frontline",
        "sig": "крадет силу Decay на линии, ставит бессмертную томбу Tombstone и усиливает урон команды в форме Flesh Golem"
    },
    86: {
        "name": "Rubick",
        "role": "support",
        "style": "backline",
        "sig": "подбрасывает врагов телекинезом Telekinesis, снижает урон Fade Bolt и ворует ключевые ультимейты способностью Spell Steal"
    },
    87: {
        "name": "Disruptor",
        "role": "support",
        "style": "backline",
        "sig": "возвращает врага назад во времени Glimpse, запирает в круге Kinetic Field и накладывает безмолвие с сайленсом Static Storm"
    },
    88: {
        "name": "Nyx Assassin",
        "role": "support",
        "style": "elusive",
        "sig": "охотится в невидимости Vendetta, оглушает станом Impale, возвращает урон панцирем Spiked Carapace и сжигает ману Mind Flare"
    },
    89: {
        "name": "Naga Siren",
        "role": "carry",
        "style": "elusive",
        "sig": "сетапит тимфайт через Song of the Siren, держит цель в сетке Ensnare и срезает броню армией копий под Rip Tide"
    },
    90: {
        "name": "Keeper of the Light",
        "role": "support",
        "style": "backline",
        "sig": "заливает ману через Chakra Magic, снижает перезарядки способностей, ослепляет врагов Blinding Light и зачищает волны крипов задувкой Illuminate"
    },
    91: {
        "name": "Io",
        "role": "support",
        "style": "backline",
        "sig": "связывается с союзным керри через Tether, многократно умножает отхил и переносит тиммейта ультимейтом Relocate"
    },
    92: {
        "name": "Visage",
        "role": "offlane",
        "style": "backline",
        "sig": "поглощает урон пассивкой Gravekeeper's Cloak, спамит зарядами Soul Assumption и уничтожает цели гаргульями Summon Familiars"
    },
    93: {
        "name": "Slark",
        "role": "carry",
        "style": "elusive",
        "sig": "ворует ловкость ударами Essence Shift, снимает контроль через Dark Pact, прыгает в Pounce и регенерирует в тумане Shadow Dance"
    },
    94: {
        "name": "Medusa",
        "role": "carry",
        "style": "frontline",
        "sig": "впитывает тонны входящего урона щитом Mana Shield, расстреливает всех врагов стрелами Split Shot и обращает в камень Stone Gaze"
    },
    95: {
        "name": "Troll Warlord",
        "role": "carry",
        "style": "frontline",
        "sig": "переключается между ближним и дальним боем, стакает скорость атаки Fervor, башит и отказывается умирать в Battle Trance"
    },
    96: {
        "name": "Centaur Warrunner",
        "role": "offlane",
        "style": "frontline",
        "sig": "врывается с блинка станом Hoof Stomp, наносит урон Double Edge, возвращает урон Retaliate и разгоняет команду ультой Stampede"
    },
    97: {
        "name": "Magnus",
        "role": "offlane",
        "style": "initiator",
        "sig": "стягивает всю вражескую команду в легендарный Reverse Polarity, увозит жертв рогом Skewer и баффает клив союзникам Empower"
    },
    98: {
        "name": "Timbersaw",
        "role": "offlane",
        "style": "frontline",
        "sig": "стакает броню и реген Reactive Armor, режет базовую силу Whirling Death и наносит чистый урон пилами Chakram"
    },
    99: {
        "name": "Bristleback",
        "role": "offlane",
        "style": "frontline",
        "sig": "поглощает урон пассивкой со спины Bristleback, стакает замедление соплями Viscous Nasal Goo и уничтожает шипами Quill Spray"
    },
    100: {
        "name": "Tusk",
        "role": "support",
        "style": "initiator",
        "sig": "вкатывает союзников в драку снежным комом Snowball, перекрывает путь осколками Ice Shards и отправляет в нокаут Walrus PUNCH!"
    },
    101: {
        "name": "Skywrath Mage",
        "role": "support",
        "style": "backline",
        "sig": "накладывает безмолвие и усиление магии Ancient Seal, спамит болтами Arcane Bolt и заливает гигантский урон ультой Mystic Flare"
    },
    102: {
        "name": "Abaddon",
        "role": "support",
        "style": "frontline",
        "sig": "снимает любой контроль щитом Aphotic Shield, спасает от смерти ультимейтом Borrowed Time и накладывает замедление Curse of Avernus"
    },
    103: {
        "name": "Elder Titan",
        "role": "support",
        "style": "initiator",
        "sig": "отправляет астрального духа Astral Spirit для кражи урона, усыпляет область Echo Stomp и срезает всю базовую броню аурой Natural Order"
    },
    104: {
        "name": "Legion Commander",
        "role": "offlane",
        "style": "frontline",
        "sig": "снимает дебаффы через Press the Attack, разгоняет урон Overwhelming Odds и намертво фиксирует цель в дуэли Duel"
    },
    105: {
        "name": "Techies",
        "role": "support",
        "style": "backline",
        "sig": "врывается с сайленсом Blast Off!, минирует карту красными минами Proximity Mines, кидает Sticky Bomb и защищается через Reactive Tazer"
    },
    106: {
        "name": "Ember Spirit",
        "role": "mid",
        "style": "elusive",
        "sig": "уклоняется от спеллов через Sleight of Fist, летает по копиям Fire Remnant и поглощает магию щитом Flame Guard"
    },
    107: {
        "name": "Earth Spirit",
        "role": "support",
        "style": "initiator",
        "sig": "манипулирует каменными копиями Stone Remnant, оглушает валуном Rolling Boulder, дает сайленс и заражает ультой Magnetize"
    },
    108: {
        "name": "Underlord",
        "role": "offlane",
        "style": "frontline",
        "sig": "зонирует файты дождем Firestorm, удерживает в оцепенении ямой Pit of Malice, крадет белый урон Atrophy Aura и перемещает команду через Fiend's Gate"
    },
    109: {
        "name": "Terrorblade",
        "role": "carry",
        "style": "elusive",
        "sig": "создает мощные копии Conjure Image, трансформируется в дальний бой Metamorphosis и переворачивает драку свапом здоровья Sunder"
    },
    110: {
        "name": "Phoenix",
        "role": "support",
        "style": "backline",
        "sig": "замедляет скорость атаки духов Fire Spirits, выжигает процентное здоровье лучом Sun Ray и возрождается в сверхновой Supernova"
    },
    111: {
        "name": "Oracle",
        "role": "support",
        "style": "backline",
        "sig": "держит союзника в полной неуязвимости к смертельному урону False Promise, развеивает спеллы Fortune's End и лечит комбо Purifying Flames"
    },
    112: {
        "name": "Winter Wyvern",
        "role": "support",
        "style": "backline",
        "sig": "спасает от физического урона ледяной глыбой Cold Embrace, замедляет Arctic Burn и заставляет врагов убивать союзника ультой Winter's Curse"
    },
    113: {
        "name": "Arc Warden",
        "role": "carry",
        "style": "elusive",
        "sig": "создает полноценную копию героя Tempest Double с копиями предметов, спамит духами Spark Wraith и защищается куполом Magnetic Field"
    },
    114: {
        "name": "Monkey King",
        "role": "carry",
        "style": "frontline",
        "sig": "прыгает по деревьям Tree Dance, оглушает посохом Boundless Strike, стакает пассивку Jingu Mastery и ставит круговую арену Wukong's Command"
    },
    119: {
        "name": "Dark Willow",
        "role": "support",
        "style": "elusive",
        "sig": "становится неуязвимой для таргета в Shadow Realm, связывает врагов страхом Terrorize и засыпает оглушениями Bramble Maze / Cursed Crown"
    },
    120: {
        "name": "Pangolier",
        "role": "offlane",
        "style": "elusive",
        "sig": "катается в драке неуязвимым шаром Rolling Thunder, пробивает ряды шпагой Swashbuckle и обезоруживает пассивкой Lucky Shot"
    },
    121: {
        "name": "Grimstroke",
        "role": "support",
        "style": "backline",
        "sig": "связывает двух врагов цепью Soulbind для дублирования направленных заклинаний, глушит призраком Phantom's Embrace и станит чернилами Ink Swell"
    },
    123: {
        "name": "Hoodwink",
        "role": "support",
        "style": "elusive",
        "sig": "привязывает к деревьям сеткой Bushwhack, рикошетит желудем Acorn Shot, прячется в лесу Scurry и снайпит ультимейтом Sharpshooter"
    },
    126: {
        "name": "Void Spirit",
        "role": "mid",
        "style": "elusive",
        "sig": "неуловимо скачет порталами Astral Step, взрывает область Dissimilate и впитывает урон щитом Resonant Pulse"
    },
    128: {
        "name": "Snapfire",
        "role": "support",
        "style": "backline",
        "sig": "замедляет выстрелом Scatterblast, дает союзнику щит и прыжок Firesnap Cookie и закидывает файты лавой Mortimer Kisses"
    },
    129: {
        "name": "Mars",
        "role": "offlane",
        "style": "initiator",
        "sig": "запирает врагов в гладиаторской арене Arena of Blood, пригвождает к стенам копьем Spear of Mars и блокирует тычки щитом Bulwark"
    },
    135: {
        "name": "Dawnbreaker",
        "role": "offlane",
        "style": "frontline",
        "sig": "прилетает через всю карту ультимейтом Solar Guardian с лечением и станом, крутится с молотом Starbreaker и замедляет Celestial Hammer"
    },
    136: {
        "name": "Marci",
        "role": "support",
        "style": "frontline",
        "sig": "перебрасывает врага через плечо Dispose, разгоняет союзника баффом Sidekick и выбивает колоссальный берст под ультимейтом Unleash"
    },
    137: {
        "name": "Primal Beast",
        "role": "offlane",
        "style": "frontline",
        "sig": "разгоняется через всю драку Onslaught, стакает сопротивление и урон Uproar и вбивает ключевую цель в землю ультой Pulverize"
    },
    138: {
        "name": "Muerta",
        "role": "carry",
        "style": "backline",
        "sig": "наносит колоссальный магический урон атаками под Pierce the Veil, рикошетит выстрелом Dead Shot и призывает призраков The Calling"
    },
    139: {
        "name": "Ringmaster",
        "role": "support",
        "style": "backline",
        "sig": "управляет позиционкой колесом Wheel of Wonder, сбивает фокус коробкой Escape Act и наносит процентный урон кнутом Tame the Beasts"
    },
    145: {
        "name": "Kez",
        "role": "carry",
        "style": "elusive",
        "sig": "переключается между катаной и сай, наносит серию молниеносных выпадов Falcon Rush, накладывает кровотечение и парирует атаки с разворотом"
    }
}
