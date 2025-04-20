import pgzrun
from config import WIDTH, HEIGHT, TILE_SIZE
from engine.core import generate_map, draw_map
from engine.player import Player

# Gera o mapa com os tiles definidos
mapa = generate_map()

# Cria o jogador
player = Player(WIDTH // 2, HEIGHT - TILE_SIZE)

def update():
    # Controle de movimento
    if keyboard.left:
        player.move_left()
    if keyboard.right:
        player.move_right()
    if keyboard.space:
        player.jump()
    if is_moving := not (keyboard.left or keyboard.right or keyboard.space):
        player.stop_moving()

    # Atualiza a física e estado do jogador
    player.update(mapa)

def draw():
    screen.clear()  # Limpa a tela
    draw_map(mapa, player)  # Desenha o mapa e o jogador
    player.draw()  # Desenha o jogador, arma e laser

def on_mouse_move(pos):
    mouse_x, mouse_y = pos
    print (f"Mouse position: {mouse_x}, {mouse_y}")
    player.update_weapon_direction(mouse_x, mouse_y)  # Atualiza a direção da arma com base na posição do mouse

def on_mouse_down(pos, button):
    if button == mouse.LEFT:
        player.shoot()

pgzrun.go()
