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
    'weapon_ammo': 'weapons/weapon_ammo',
    'player': 'characters/alienyellow',
    'player_idle': ['characters/alienyellow', 'characters/alienyellow_stand'],
    'player_walk': ['characters/alienyellowwalk_1', 'characters/alienyellowwalk_2'],
    'player_jump': 'characters/alienyellow_jump',
    'player_idle_flipped': ['characters/alienyellow_flipped', 'characters/alienyellow_stand_flipped'],
    'player_walk_flipped': ['characters/alienyellow_walk1_flipped', 'characters/alienyellow_walk2_flipped'],
    'player_jump_flipped': 'characters/alienyellow_jump_flipped',
    'player_hurt': 'characters/alienyellow_hurt',
    'player_hurt_flipped': 'characters/alienyellow_hurt_flipped',

    ## Inimigos
    'enemy_idle': ['enemy/slime', 'enemy/slime_walk'],
    'enemy_idle_flipped': ['enemy/slime_flipped', 'enemy/slime_walk_flipped'],
    'enemy_walk': ['enemy/slime', 'enemy/slime_walk'],
    'enemy_walk_flipped': ['enemy/slime_flipped', 'enemy/slime_walk_flipped'],
    'enemy_hurt': 'enemy/slime_hurt',
    'enemy_dead': 'enemy/slime_dead',
    'enemy_dash': ['enemy/slime_squashed', 'enemy/slime', 'enemy/slime_walk'],
    'enemy_dash_flipped': ['enemy/slime_squashed_flipped', 'enemy/slime_flipped', 'enemy/slime_walk_flipped'],

}

MUSICS = {
    'menu': 'jingles1', 
    'select': 'select',
    'switch': 'switch',
}









