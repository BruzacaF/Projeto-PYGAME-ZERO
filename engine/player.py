import pgzrun
import math
from pgzero.actor import Actor
from pgzero.rect import Rect
from config import TILE_SIZE, TILES_X, TILES_Y, WIDTH, HEIGHT, TILES, actor

class Player:
    def __init__(self, x, y):
        self.sprite = Actor(actor['player_idle'][0])  # Começa com o primeiro sprite de idle
        self.sprite.pos = (x, y)
        self.weapon = Actor(actor['weapon'])  # Adiciona a arma como um ator separado
        self.weapon.pos = (x, y)
        self.weapon_radius = 30  # Raio do ponto ao redor do personagem onde a arma gira
        self.weapon_offset = 0  # Deslocamento da arma para melhor posicionamento visual
        self.speed = 5
        self.jump_speed = -15
        self.gravity = 0.5
        self.dy = 0  # Velocidade de movimento vertical
        self.hitbox = Rect((0, 0),(self.sprite.width, self.sprite.height))  # Hitbox do jogador (ajustar conforme necessário)


        
        # Variáveis para animação
        self.is_jumping = False
        self.is_moving = False
        self.facing_right = True  # Direção inicial do personagem
        self.idle_frame = 0
        self.walk_frame = 0
        self.last_frame_time = 0  # Marca o tempo da última troca de frame
        self.frame_delay = 0.1  # Intervalo de frames, controlado pelo Pygame Zero
        self.weapon_offset = 0  # Deslocamento da arma em relação ao personagem
        self.weapon_angle = 0  # Ângulo da arma
        self.sprite.visible = True  # Visibilidade do sprite

        #variaveis de jogo
        self.name = "Player"  # Nome do jogador
        self.score = 0  # Pontuação do jogador
        self.health = 100
        self.lives = 3  # Vidas do jogador    
        self.died = False
        self.enemies_in_map = []  # Lista de inimigos no mapa
        self.lasers = []  # Lista de lasers disparados pelo jogador


        # Controla o tempo entre as animações
        self.animation_time = 0  # Contador de tempo para animação
        self.animation_speed = 10  # Número de frames entre cada troca de animação

        

        # Definição de animações
        self.walk_frames_right = actor['player_walk']
        self.walk_frames_left = actor['player_walk_flipped']  # Inverte os frames para andar para a esquerda

    def animate(self):
        """Atualiza a animação do personagem com base no seu estado de movimento ou pulo."""
        self.animation_time += 1

        # Verifica se já passou o tempo necessário para trocar o frame
        if self.animation_time >= self.animation_speed:
            self.animation_time = 0  # Reseta o contador de tempo
            if self.is_jumping:
                if self.facing_right:
                    # Se o personagem está pulando e virado para a direita
                    self.sprite.image = actor['player_jump']
                    self.weapon.image = actor['weapon']  # Arma normal
                    if self.weapon.image == actor['weapon']:
                        self.weapon.angle = 0
                        self.weapon.pos = (120, 0)
                else:
                    # Se o personagem está pulando e virado para a esquerda
                    self.sprite.image = actor['player_jump_flipped']
                    self.weapon.image = actor['weapon_flipped']
                    if self.weapon.image == actor['weapon_flipped']:
                        self.weapon.angle = 180
                        self.weapon.pos = (-120, 0)

                # Atualiza o frame da animação de pulo
            elif not self.is_jumping and not self.is_moving:
                # Se o personagem está parado
                if self.facing_right:
                    self.sprite.image = actor['player_idle'][self.idle_frame]
                else:
                    self.sprite.image = actor['player_idle_flipped'][self.idle_frame]
            elif self.is_moving:
                # Se o personagem está se movendo
                if self.facing_right:
                    self.sprite.image = self.walk_frames_right[self.walk_frame]
                    self.weapon.image = actor['weapon']  # Arma normal
                    if self.weapon.image == actor['weapon']:
                        self.weapon.angle = 0
                        self.weapon.pos = (120, 0)
                else:
                    self.sprite.image = self.walk_frames_left[self.walk_frame]
                    self.weapon.image = actor['weapon_flipped']  # Arma virada para a esquerda
                    if self.weapon.image == actor['weapon_flipped']:
                        self.weapon.angle = 180  # Vira a arma para a esquerda
                        self.weapon.pos = (-120, 0)  # Ajusta a posição da arma para a esquerda
                # Atualiza o frame da animação de andar
                self.walk_frame = (self.walk_frame + 1) % len(self.walk_frames_right)

            elif self.is_hurt:
                # Se o personagem está ferido
                if self.facing_right:
                    self.sprite.image = actor['player_hurt']
                else:
                    self.sprite.image = actor['player_hurt_flipped']
                
                # Faz o personagem piscar enquanto está invulnerável
                if self.animation_time % 2 == 0:
                    self.sprite.visible = not self.sprite.visible
                else:
                    self.sprite.visible = True

                # Define o tempo de invulnerabilidade
                self.invulnerability_timer = getattr(self, 'invulnerability_timer', 0) + 1
                if self.invulnerability_timer > 30:  # Duração da invulnerabilidade (30 frames)
                    self.is_hurt = False
                    self.sprite.visible = True
                    self.invulnerability_timer = 0

                self.walk_frame = 0
                self.idle_frame = 0


            else:
                # Se não está se movendo ou pulando, animação de idle
                self.sprite.image = actor['player_idle'][0]
                self.idle_frame = 0
                self.walk_frame = 0

    def move_left(self):
        """Move o personagem para a esquerda."""
        if self.facing_right:
            self.facing_right = False  # Está virado para a esquerda
        self.sprite.x -= self.speed
        self.is_moving = True

    def move_right(self):
        """Move o personagem para a direita."""
        if not self.facing_right:
            self.facing_right = True  # Está virado para a direita
        self.sprite.x += self.speed
        self.is_moving = True

    def jump(self):
        """Faz o personagem pular, se não estiver pulando já."""
        if not self.is_jumping:
            self.dy = self.jump_speed * 1.2
            self.is_jumping = True

    def stop_moving(self):
        """Interrompe o movimento do personagem."""
        self.is_moving = False

    def update(self, mapa):
        """Atualiza a física e o comportamento do personagem."""
        # Atualiza a gravidade
        self.dy += self.gravity
        self.sprite.y += self.dy

        # Atualiza a posição do hitbox
        self.hitbox.x = self.sprite.x - self.hitbox.width // 2  # Centraliza o hitbox em relação ao sprite no eixo X
        self.hitbox.y = self.sprite.y - self.hitbox.height // 2  # Centraliza o hitbox em relação ao sprite no eixo Y
        

        self.weapon.x = self.sprite.x + self.weapon_offset  # Atualiza a posição da arma em relação ao personagem
        self.weapon.y = self.sprite.y + self.weapon_offset  # Atualiza a posição da arma em relação ao personagem
        
        # Colisão com o chão
        if self.sprite.y >= 768 - (TILE_SIZE * 1.5):  # No chão
            self.sprite.y = 768 - (TILE_SIZE * 1.5)  # Ajusta a posição do personagem
            self.dy = 0
            self.is_jumping = False

        # Atualiza a animação com base no estado do personagem
        self.animate()

        # Atualiza a posição da arma para acompanhar o personagem
        
        self.weapon.pos = (self.sprite.x + 55, self.sprite.y + 15)  # Ajusta a posição da arma em relação ao personagem
        if not self.facing_right:
            self.weapon.x = self.sprite.x - 55

        # Atualiza os lasers
        for laser in self.lasers:
            laser.update()
            laser.draw()  # Desenha o laser na tela
            # Verifica se o laser saiu da tela
            if not laser.update():
                self.lasers.remove(laser)
                print("Laser removido!")

            if self.lasers.__len__() > 0:
                for laser in self.lasers[:]:
                    laser.update()
                    for enemy in self.enemies_in_map:
                        if laser.hitbox.colliderect(enemy.hitbox):
                            enemy.health -= laser.damage
                            laser.hitted = True
                            print(f"{self.name} atingiu {enemy.name} com o laser! Vida restante: {enemy.health}")
                            if enemy.health <= 0:
                                enemy.die()
                                print(f"{enemy.name} foi derrotado!")
                            break
                    if laser.hitted:
                        self.lasers.remove(laser)
                        laser.hitted = False  # Reseta o estado do laser após a colisão
        
        # Atualiza a direção da arma com base na posição do mouse
        self.update_weapon_direction(mouse_x=0, mouse_y=0)  # Inicializa com valores padrão, será atualizado no evento de movimento do mouse
       
    def update_weapon_direction(self, mouse_x, mouse_y):
        dx = mouse_x - self.sprite.pos[0]
        dy = mouse_y - self.sprite.pos[1]
        angle = math.degrees(math.atan2(dy, dx))
        self.weapon_angle = angle

    def shoot(self):
        # Cria um novo laser indo na direção do ângulo da arma
        angle_rad = math.radians(self.weapon.angle)
        laser_speed = 10
        dx = math.cos(angle_rad) * laser_speed
        dy = math.sin(angle_rad) * laser_speed

        laser = Laser(self.weapon.x, self.weapon.y, (dx, dy))  # Cria o laser na posição da arma
        self.lasers.append(laser)
      
    def draw(self,screen):
        """Desenha o personagem e a arma na tela."""
        self.sprite.draw()
        self.draw_text(screen)  # Desenha o texto de vida acima do personagem

        if self.weapon:
            self.weapon.angle = self.weapon.angle  # Atualiza o ângulo da arma
            self.weapon.draw()

        for laser in self.lasers:
            laser.draw()
            
    def update_weapon_position(self):
        offset_x = 20  # ajuste conforme necessário
        offset_y = -10
        self.weapon_sprite.pos = (self.x + offset_x, self.y + offset_y)
    
    def die(self):

        if self.health <= 0:
            self.lives -= 1
            self.health = 100  # Reseta a vida do jogador
            self.position = (WIDTH // 2, HEIGHT // 2)  # Reseta a posição do jogador
            self.sprite.pos = self.position  # Reseta a posição do sprite
            print(f"{self.name} morreu! Vidas restantes: {self.lives}")
            if self.lives < 1:
                self.died = True
               

        
        
            

    def draw_text(self, screen): 
        """Desenha o texto de vida acima do inimigo."""
        screen.draw.text(f"Vida: {self.health}", (self.hitbox.x, self.hitbox.y - 20), color=(255, 0, 0))
    
    def set_enemies_in_map(self, enemies):
        """Define a lista de inimigos no mapa."""
        self.enemies_in_map.extend(enemies)  # Adiciona os inimigos ao mapa

class Laser:
    def __init__(self, x, y, direction):
        self.sprite = Actor(actor['weapon_ammo'])
        self.sprite.pos = (x, y)
        self.direction = direction  # Direção do laser (1 para direita, -1 para esquerda)
        self.speed = 0.5
        self.hitbox = Rect((0, 0),(self.sprite.width, self.sprite.height))
        self.hitted = False  # Verifica se o laser atingiu algo

        # Variáveis de jogo
        self.damage = 10 

    def update(self):
        """Atualiza a posição do laser."""
        # Atualiza a posição do hitbox do laser
        self.hitbox.center = (self.sprite.x, self.sprite.y)
        self.hitbox.width = self.sprite.width * 1.2
        self.hitbox.height = self.sprite.height * 1.2

        # Atualiza a posição do laser
        self.sprite.x += self.direction[0] * self.speed
        self.sprite.y += self.direction[1] * self.speed
        # Atualiza a hitbox do laser
        self.hitbox.x = self.sprite.x - self.hitbox.width // 2
        self.hitbox.y = self.sprite.y - self.hitbox.height // 2
        self.hitbox.width = self.sprite.width * 0.8
        self.hitbox.height = self.sprite.height * 0.8

        # Verifica se o laser saiu da tela
        if self.sprite.x < 0 or self.sprite.x > WIDTH or self.sprite.y < 0 or self.sprite.y > HEIGHT:
            return False
        return True

        if self.hitted:
            print("Laser atingiu o inimigo!")

            
            return False

    def draw(self):
        """Desenha o laser na tela."""
        self.sprite.draw()

    def draw_hitbox(self, screen):
        screen.draw.rect(self.hitbox, (255, 0, 0))


