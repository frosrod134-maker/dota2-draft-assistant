"""
Hero Role Viability and Classification Map for Dota 2 (Patch 7.41f).
Defines which positions [1, 2, 3, 4, 5] each hero actually plays in high-MMR pubs.
Prevents illegitimate cross-role recommendations (e.g. Pos 5 Crystal Maiden as Pos 1 Carry).
"""

# 1: Carry (Pos 1), 2: Mid (Pos 2), 3: Offlane (Pos 3), 4: Soft Support (Pos 4), 5: Hard Support (Pos 5)
HERO_VIABLE_ROLES: dict[int, list[int]] = {
    1: [1],             # Anti-Mage
    2: [3],             # Axe
    3: [5],             # Bane
    4: [1, 3],          # Bloodseeker
    5: [5],             # Crystal Maiden
    6: [1],             # Drow Ranger
    7: [4, 3],          # Earthshaker
    8: [1],             # Juggernaut
    9: [4, 2],          # Mirana
    10: [1, 2],         # Morphling
    11: [2, 1],         # Shadow Fiend
    12: [1],            # Phantom Lancer
    13: [2],            # Puck
    14: [1, 3, 4],      # Pudge
    15: [1, 3, 2],      # Razor
    16: [3, 4],         # Sand King
    17: [2],            # Storm Spirit
    18: [1, 3],         # Sven
    19: [1, 2, 4],      # Tiny
    20: [4, 5, 1],      # Vengeful Spirit
    21: [2, 3, 4],      # Windranger
    22: [2, 4],         # Zeus
    23: [2, 3],         # Kunkka
    25: [1, 2, 4],      # Lina
    26: [4, 5],         # Lion
    27: [5, 4],         # Shadow Shaman
    28: [3],            # Slardar
    29: [3],            # Tidehunter
    30: [5],            # Witch Doctor
    31: [5],            # Lich
    32: [1, 4],         # Riki
    33: [3, 4],         # Enigma
    34: [4, 2],         # Tinker
    35: [1, 2, 4],      # Sniper
    36: [2, 3],         # Necrophos
    37: [5],            # Warlock
    38: [3],            # Beastmaster
    39: [2],            # Queen of Pain
    40: [3, 4, 5],      # Venomancer
    41: [1],            # Faceless Void
    42: [1, 3],         # Wraith King
    43: [2, 3],         # Death Prophet
    44: [1],            # Phantom Assassin
    45: [4, 5, 2],      # Pugna
    46: [1, 2],         # Templar Assassin
    47: [2, 3],         # Viper
    48: [1],            # Luna
    49: [2, 3, 1],      # Dragon Knight
    50: [5, 4, 2],      # Dazzle
    51: [4, 5, 3],      # Clockwerk
    52: [2, 1, 3],      # Leshrac
    53: [4, 5, 3, 1],   # Nature's Prophet
    54: [1],            # Lifestealer
    55: [3],            # Dark Seer
    56: [1, 2, 4],      # Clinkz
    57: [3, 5],         # Omniknight
    58: [5, 4],         # Enchantress
    59: [2, 1],         # Huskar
    60: [3],            # Night Stalker
    61: [2, 3],         # Broodmother
    62: [4, 3],         # Bounty Hunter
    63: [1, 4],         # Weaver
    64: [5],            # Jakiro
    65: [2, 3, 4],      # Batrider
    66: [5],            # Chen
    67: [1],            # Spectre
    68: [5, 4],         # Ancient Apparition
    69: [3],            # Doom
    70: [1],            # Ursa
    71: [4, 3],         # Spirit Breaker
    72: [1, 4],         # Gyrocopter
    73: [1, 2],         # Alchemist
    74: [2],            # Invoker
    75: [4, 5],         # Silencer
    76: [2],            # Outworld Destroyer
    77: [1, 3],         # Lycan
    78: [3],            # Brewmaster
    79: [5, 4],         # Shadow Demon
    80: [1, 2],         # Lone Druid
    81: [1, 3],         # Chaos Knight
    82: [2, 1],         # Meepo
    83: [5],            # Treant Protector
    84: [5, 3, 4],      # Ogre Magi
    85: [5],            # Undying
    86: [4],            # Rubick
    87: [5],            # Disruptor
    88: [4, 2],         # Nyx Assassin
    89: [1, 4],         # Naga Siren
    90: [4, 5, 2],      # Keeper of the Light
    91: [5, 4],         # Io
    92: [2, 3],         # Visage
    93: [1],            # Slark
    94: [1],            # Medusa
    95: [1],            # Troll Warlord
    96: [3],            # Centaur Warrunner
    97: [3, 2, 1],      # Magnus
    98: [2, 3],         # Timbersaw
    99: [1, 3],         # Bristleback
    100: [4, 3],        # Tusk
    101: [4, 5],        # Skywrath Mage
    102: [5, 3, 1],     # Abaddon
    103: [4, 5, 3],     # Elder Titan
    104: [3],           # Legion Commander
    105: [4, 2],        # Techies
    106: [2, 1],        # Ember Spirit
    107: [4, 2],        # Earth Spirit
    108: [3],           # Underlord
    109: [1],           # Terrorblade
    110: [4, 5, 3],     # Phoenix
    111: [5],           # Oracle
    112: [5, 4],        # Winter Wyvern
    113: [2, 1],        # Arc Warden
    114: [1, 2, 4],     # Monkey King
    119: [4, 5],        # Dark Willow
    120: [2, 3],        # Pangolier
    121: [4, 5],        # Grimstroke
    123: [4, 5],        # Hoodwink
    126: [2],           # Void Spirit
    128: [4, 5, 2],     # Snapfire
    129: [3],           # Mars
    135: [3, 4, 1],     # Dawnbreaker
    136: [4, 1, 3],     # Marci
    137: [2, 3],        # Primal Beast
    138: [1, 2, 4],     # Muerta
    139: [4, 5],        # Ringmaster
    145: [1, 2],        # Kez
}

# Primary signature position for team composition analysis
HERO_PRIMARY_ROLE: dict[int, int] = {
    1: 1, 2: 3, 3: 5, 4: 1, 5: 5, 6: 1, 7: 4, 8: 1, 9: 4, 10: 1,
    11: 2, 12: 1, 13: 2, 14: 1, 15: 3, 16: 3, 17: 2, 18: 1, 19: 1, 20: 5,
    21: 2, 22: 2, 23: 2, 25: 1, 26: 4, 27: 5, 28: 3, 29: 3, 30: 5,
    31: 5, 32: 1, 33: 3, 34: 4, 35: 1, 36: 2, 37: 5, 38: 3, 39: 2, 40: 4,
    41: 1, 42: 1, 43: 2, 44: 1, 45: 4, 46: 1, 47: 2, 48: 1, 49: 2, 50: 5,
    51: 4, 52: 2, 53: 4, 54: 1, 55: 3, 56: 1, 57: 3, 58: 5, 59: 2, 60: 3,
    61: 3, 62: 4, 63: 1, 64: 5, 65: 2, 66: 5, 67: 1, 68: 5, 69: 3, 70: 1,
    71: 4, 72: 1, 73: 1, 74: 2, 75: 5, 76: 2, 77: 3, 78: 3, 79: 5, 80: 2,
    81: 1, 82: 2, 83: 5, 84: 5, 85: 5, 86: 4, 87: 5, 88: 4, 89: 1, 90: 4,
    91: 5, 92: 3, 93: 1, 94: 1, 95: 1, 96: 3, 97: 3, 98: 3, 99: 3, 100: 4,
    101: 4, 102: 5, 103: 5, 104: 3, 105: 4, 106: 2, 107: 4, 108: 3, 109: 1, 110: 4,
    111: 5, 112: 5, 113: 2, 114: 1, 119: 4, 120: 2, 121: 5, 123: 4, 126: 2, 128: 4, 129: 3, 135: 3,
    136: 4, 137: 3, 138: 1, 139: 4, 145: 1
}

HARD_CARRIES: set[int] = {1, 6, 8, 10, 12, 41, 44, 48, 54, 67, 70, 89, 93, 94, 95, 109, 145}
