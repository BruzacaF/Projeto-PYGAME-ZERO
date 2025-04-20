import pgzrun
import math
from pgzero.actor import Actor
from pgzero.rect import Rect
from config import TILE_SIZE, TILES_X, TILES_Y, WIDTH, HEIGHT, TILES, actor
import random


class Enemy:
    def __init__(self, player):
        """Inicializa o inimigo com saúde, poder de ataque e posição inicial."""
        # Variáveis de instância
        self.sprite = Actor(actor['enemy_idle'][0], midbottom=(WIDTH//random.randint(1, 10), (player.sprite.height // 2)))  # Posição inicial do inimigo
        self.sprite.angle = 0
        self.sprite.scale = 1.0
        self.gravity = 0.1
        self.dy = 0  # Velocidade de movimento vertical

        self.hitbox = Rect((0, 0),(self.sprite.width + 20, self.sprite.height + 20))  # Hitbox do inimigo (ajustar conforme necessário)

        #variaveis de jogo
        self.name = "Slime"
        self.target = player  # Referência ao jogador
        self.health = 20  # Vida do inimigo
        self.attack_power = 200
        self.quantity = 1  # Quantidade de inimigos
        self.spanw_quantity = 1  # Quantidade de inimigos que aparecem na tela

        # Variáveis para animação
        self.is_moving = False
        self.is_jumping = False
        self.facing_right = True
        self.speed = 1
        self.jump_speed = 10
        self.dy = 0
        self.gravity = 0.5
        self.walk_frame = 0
        self.idle_frame = 0
        self.last_frame_time = 0
        self.frame_delay = 0.1  # Tempo entre os frames da animação
        self.death = False
        self.death_time = 0  # Tempo total da animação de morte
        


        # Controla o tempo entre as animações
        self.animation_time = 0  # Tempo total da animação
        self.animation_speed = 15

         # Definição de animações
        self.walk_frames_right = [actor['enemy_walk_flipped'][0], actor['enemy_walk_flipped'][1]]
        self.walk_frames_left = [actor['enemy_walk'][0], actor['enemy_walk'][1]]
        self.dash_frames_right = [actor['enemy_dash'][0], actor['enemy_dash'][1], actor['enemy_dash'][2]]
        self.dash_frames_left = [actor['enemy_dash_flipped'][0], actor['enemy_dash_flipped'][1], actor['enemy_dash_flipped'][2]]
    
    def animate(self):
        """Atualiza a animação do inimigo com base no seu estado de movimento ou pulo."""
        self.animation_time += 1

        # Verifica se já passou o tempo necessário para trocar o frame
        if self.animation_time >= self.animation_speed:
            self.animation_time = 0
            if self.is_jumping:
                if self.facing_right:
                    self.sprite.image = actor['enemy_walk_flipped'][0]
                else:
                    self.sprite.image = actor['enemy_walk'][0]
            elif self.is_moving:
                if self.facing_right:
                    self.sprite.image = self.walk_frames_right[self.walk_frame]
                    self.walk_frame = (self.walk_frame + 1) % len(self.walk_frames_right)

                else:
                    self.sprite.image = self.walk_frames_left[self.walk_frame]
                    self.walk_frame = (self.walk_frame + 1) % len(self.walk_frames_left)
            else:
                if self.facing_right:
                    self.sprite.image = actor['enemy_idle_flipped'][0]
                else:
                    self.sprite.image = actor['enemy_idle'][0]
                self.walk_frame = 0
                self.idle_frame = 0
                self.walk_frame = 0

    def move_left(self):
        """Move o inimigo para a esquerda."""
        if self.facing_right:
            self.facing_right = False
        self.sprite.x -= self.speed
        self.is_moving = True

    def move_right(self):
        """Move o inimigo para a direita."""
        if not self.facing_right:
            self.facing_right = True
        self.sprite.x += self.speed
        self.is_moving = True

    def reset_position(self):
        """Reseta a posição do inimigo para 10 px à direita ou esquerda da borda da tela."""
        if self.facing_right:
            self.sprite.x = 10  # Coloca o inimigo fora da tela à esquerda
        else:
            self.sprite.x = WIDTH - 10  # Coloca o inimigo fora da tela à direita

    def die(self):
        self.death = True
        print(f"{self.name} has died!")

        

    def stop_moving(self):
        """Para o movimento do inimigo."""
        self.is_moving = False
        self.sprite.image = actor['enemy_idle'][0] if self.facing_right else actor['enemy_idle_flipped'][0]
        self.walk_frame = 0
        self.idle_frame = 0
        self.walk_frame = 0
        self.animation_time = 0
        self.speed = 0  # Para o movimento do inimigo

    def update(self, mapa, player):
        """Atualiza a posição e animação do inimigo."""
        self.dy += self.gravity
        self.sprite.y += self.dy

        # Centraliza o hitbox no sprite
        self.hitbox.center = (self.sprite.x, self.sprite.y)
        self.hitbox.width = self.sprite.width * 0.8

        self.animate()

        # Colisão com o chão 
        if self.sprite.y >= 768 - (TILE_SIZE * 1.5):  # No chão
            self.sprite.y = 768 - (TILE_SIZE * 1.1)   # Ajusta a posição do personagem
            self.dy = 0
            self.is_jumping = False
            
        # Atualiza a posição do inimigo em relação ao jogador
        if self.sprite.x < player.sprite.x:
             self.move_right()
        elif self.sprite.x > player.sprite.x:
            self.move_left()

        if abs(self.sprite.x - player.sprite.x) < 400 and abs(self.sprite.y - player.sprite.y) < 100:
            # Se o inimigo estiver próximo do jogador, ataca
            self.attack(player)

        if self.death:
            self.health = 0  # Zera a vida do inimigo
            self.quantity += 1  # Aumenta a quantidade de inimigos mortos
            self.spanw_quantity += 1  # Aumenta a quantidade de inimigos que aparecem na tela
            self.stop_moving()  # Para o movimento do inimigo
            self.sprite.image = actor['enemy_dead']
            self.death_time += 1
            if self.death_time >= 60:  # 2 segundos (assumindo 60 FPS)
                self.death = False
                self.death_time = 0
                self.sprite.scale = 1.0  # Restaura o tamanho original
                self.reset_position()  # Reseta a posição do inimigo
                self.revive()  # Restaura a vida do inimigo
        else :
            self.speed = 1  # Restaura a velocidade original se não estiver morto
            

    def revive(self):
        self.health += 15 * random.randint(1, 4)  # Restaura a vida do inimigo
        self.death = False  # Restaura o estado de morte    

    def attack(self, player):
        if not self.is_jumping:  # Verifica se o inimigo já realizou um salto
            self.jump()  # Pula em direção ao jogador
            if self.hitbox.colliderect(player.hitbox):
                self.reset_position()  # Reseta a posição do inimigo
                player.health -= self.attack_power  # Dano ao jogador
                player.die()  # Ataca o jogador
    
    def jump(self):
        """Faz o inimigo realizar um salto parabólico na direção que estiver andando."""
        if not self.is_jumping:  # Verifica se o inimigo já está no ar
            self.is_jumping = True
            self.dy = -self.jump_speed  # Define a velocidade inicial do salto
            
            if self.facing_right:
                self.sprite.x += self.speed * 1.5  # Move para frente durante o salto
            else:
                self.sprite.x -= self.speed * 1.5  # Move para trás durante o salto

    def draw_text(self, screen): 
        """Desenha o texto de vida acima do inimigo."""
        screen.draw.text(f"Vida: {self.health}", (self.hitbox.x, self.hitbox.y - 20), color=(255, 0, 0))

    def draw(self, screen):
        """Desenha o inimigo na tela."""
        self.sprite.draw()
        self.draw_text(screen)  # Desenha o texto de vida acima do inimigo
        # Aqui você pode desenhar a barra de vida ou outros elementos relacionados ao inimigo




        


    


    
