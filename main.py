import pgzrun
from config import WIDTH, HEIGHT, TILE_SIZE, MUSICS
from engine.core import generate_map, draw_map
from engine.player import Player
from engine.enemy import Enemy
from pgzero import music
import random

# ======= ESTADO GLOBAL =======
show_menu = True
is_muted = False
game_started = False
game_over = False

# Música de menu
music.set_volume(0.25)
music.play('ost')	




# ======= REFERÊNCIAS DO JOGO =======
player = None
enemies = []
mapa = []

# ======= MENU =======
def draw_menu():
    screen.clear()
    screen.draw.text("SHOOT THE SLIME", center=(WIDTH//2, HEIGHT//4), fontsize=64, color="white")

    play_btn = Rect((WIDTH//2 - 100, HEIGHT//2 - 40), (200, 50))
    mute_btn = Rect((WIDTH//2 - 100, HEIGHT//2 + 30), (200, 50))

    screen.draw.filled_rect(play_btn, "green")
    screen.draw.text("PLAY", center=play_btn.center, fontsize=32, color="black")

    screen.draw.filled_rect(mute_btn, "gray")
    mute_text = "MUTE" if not is_muted else "UNMUTE"
    screen.draw.text(mute_text, center=mute_btn.center, fontsize=32, color="black")

    return play_btn, mute_btn

# ======= INICIALIZA O JOGO =======
def start_game():
    global game_started, show_menu, player, enemies, mapa, game_over

    game_started = True
    show_menu = False
    game_over = False

    spanw_quantity = random.randint(1, 3)  # Quantidade de inimigos que aparecem na tela
    print(f"Quantidade de inimigos: {spanw_quantity}")

    mapa = generate_map()
    player = Player(WIDTH // 2, HEIGHT - TILE_SIZE)
    enemies = [Enemy(player)]
    

# ======= LOOP DE ATUALIZAÇÃO =======
def update():

    global game_over

    if game_over:
        return

    
    if not game_started:
        return
    if keyboard.left:
        player.move_left()
    if keyboard.right:
        player.move_right()
    if keyboard.up:
        player.jump()
    if is_moving := not (keyboard.left or keyboard.right or keyboard.space):
        player.stop_moving()
    if keyboard.space and not player.is_shooting:
        player.shoot()
        player.is_shooting = True
    elif not keyboard.space:
        player.is_shooting = False

    player.update(mapa)

    if enemies and enemies[-1].death == True:
        for _ in range(2):
            enemies.append(Enemy(player))

    player.set_enemies_in_map(enemies)

    # Atualiza inimigos
    enemies_to_remove = []
    new_enemies = []

    for enemy in enemies:
        enemy.update(mapa, player)

        if getattr(enemy, 'dead', False):
            enemies_to_remove.append(enemy)
            new_enemies.extend([Enemy(player), Enemy(player)])

    for e in enemies_to_remove:
        enemies.remove(e)
    enemies.extend(new_enemies)

    if player.died:
        game_over = True
        enemies.clear()
        
        

# ======= DESENHA NA TELA =======
def draw():
    if game_over:
        draw_game_over()
    if show_menu:
        draw_menu()
    else:
        screen.clear()
        draw_map(mapa)
        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)

# ======= CLIQUE DO MOUSE =======
def on_mouse_down(pos):
    global is_muted

    if show_menu:
        play_btn, mute_btn = draw_menu()

        if play_btn.collidepoint(pos):
    
            start_game()

        elif mute_btn.collidepoint(pos):
            is_muted = not is_muted
            volume = 0 if is_muted else 0.5
            music.set_volume(volume)
            print("Som mutado!" if is_muted else "Som ativado!")

    else:
        player.shoot()




# ======= Game Over =======

def draw_game_over():
    screen.clear()
    screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//4), fontsize=64, color="red")
   
    
    

        


# ======= MOVIMENTO DO MOUSE PARA A ARMA =======
def on_mouse_move(pos):
    if game_started:
        player.update_weapon_direction(*pos)

# ======= EXECUTA O JOGO =======
pgzrun.go()
