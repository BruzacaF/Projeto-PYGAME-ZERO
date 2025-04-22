# engine/map.py
import pgzrun

from pgzero.builtins import Actor
from config import TILE_SIZE, TILES_X, TILES_Y, WIDTH, HEIGHT,TILES

def generate_map():
    mapa = []
    for y in range(TILES_Y):
        linha = []
        for x in range(TILES_X):
            if y == (TILES_Y) - 1:  # A última linha será o chão
                linha.append('D')
            else:
                linha.append('BG')  
        mapa.append(linha)
    return mapa

from config import TILE_SIZE, WIDTH, HEIGHT, TILES
from pgzero.actor import Actor

def draw_map(mapa):
    # Desenha o fundo
    fundo = Actor(TILES['BG'])
    fundo.topleft = (0, 0)
    fundo.draw()

    # Desenha o mapa com os tiles
    for y, linha in enumerate(mapa):
        for x, tile in enumerate(linha):
            if tile:
                tile_name = TILES.get(tile)
                if tile_name:
                    tile_actor = Actor(tile_name)
                    tile_actor.topleft = (x * TILE_SIZE, y * TILE_SIZE)
                    tile_actor.draw()



