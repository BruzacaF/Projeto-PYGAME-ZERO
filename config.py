HEIGHT = 768  # Tamanho da altura da janela
WIDTH = 1024

TILE_SIZE = 64
TILES_Y = HEIGHT // TILE_SIZE
TILES_X = WIDTH // TILE_SIZE



TILES = {
    'G': 'tiles/grass',
    'DL': 'tiles/dirtleft',
    'DR': 'tiles/dirtright',
    'D': 'tiles/dirtmid',
    'S': 'tiles/stone',
    'BG': 'bg',
}

actor = {
    'weapon': 'weapons/raygun_big',
    'weapon_flipped': 'weapons/raygun_big_flipped',
    'weapon_ammo': 'weapons/laser_purple',
    'player': 'characters/alienyellow',
    'player_idle': ['characters/alienyellow', 'characters/alienyellow_stand'],
    'player_walk': ['characters/alienyellowwalk_1', 'characters/alienyellowwalk_2'],
    'player_jump': 'characters/alienyellow_jump',
    'player_idle_flipped': ['characters/alienyellow_flipped', 'characters/alienyellow_stand_flipped'],
    'player_walk_flipped': ['characters/alienyellow_walk1_flipped', 'characters/alienyellow_walk2_flipped'],
    'player_jump_flipped': 'characters/alienyellow_jump_flipped',
}


# Adiciona a arma como um ator separado




