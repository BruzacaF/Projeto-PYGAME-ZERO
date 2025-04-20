import pgzrun
import math
from pgzero.actor import Actor
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
        self.jump_speed = -10
        self.gravity = 0.5
        self.dy = 0  # Velocidade de movimento vertical

        # Variáveis para animação
        self.is_jumping = False
        self.is_moving = False
        self.facing_right = True  # Direção inicial do personagem
        self.idle_frame = 0
        self.walk_frame = 0
        self.last_frame_time = 0  # Marca o tempo da última troca de frame
        self.frame_delay = 10  # Intervalo de frames, controlado pelo Pygame Zero
        self.weapon_offset = 0  # Deslocamento da arma em relação ao personagem
        self.weapon_angle = 0  # Ângulo da arma
        


        # Controla o tempo entre as animações
        self.animation_time = 0  # Contador de tempo para animação
        self.animation_speed = 10  # Número de frames entre cada troca de animação

        self.lasers = []  # Lista de lasers disparados pelo jogador

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
                else:
                    # Se o personagem está pulando e virado para a esquerda
                    self.sprite.image = actor['player_jump_flipped']
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
            self.dy = self.jump_speed
            self.is_jumping = True

    def stop_moving(self):
        """Interrompe o movimento do personagem."""
        self.is_moving = False

    def update(self, mapa):
        """Atualiza a física e o comportamento do personagem."""
        # Atualiza a gravidade
        self.dy += self.gravity
        self.sprite.y += self.dy

        self.weapon.x = self.sprite.x + self.weapon_offset  # Atualiza a posição da arma em relação ao personagem
        self.weapon.y = self.sprite.y + self.weapon_offset  # Atualiza a posição da arma em relação ao personagem
        
        # Colisão com o chão (simples)
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
            laser['actor'].x += laser['dx']
            laser['actor'].y += laser['dy']
            # Verifica se o laser saiu da tela
        
        self.lasers = [laser for laser in self.lasers if 0 < laser['actor'].x < WIDTH and 0 < laser['actor'].y < HEIGHT]
        
        # Atualiza a direção da arma com base na posição do mouse
        self.update_weapon_direction(mouse_x=0, mouse_y=0)  # Inicializa com valores padrão, será atualizado no evento de movimento do mouse
       


    def update_weapon_direction(self, mouse_x, mouse_y):
        dx = mouse_x - self.sprite.pos[0]
        dy = mouse_y - self.sprite.pos[1]
        angle = math.degrees(math.atan2(dy, dx))
        self.weapon_angle = angle




    def shoot(self):
        print("Disparando laser!")
        # Cria um novo laser indo na direção do ângulo da arma
        angle_rad = math.radians(self.weapon.angle)
        laser_speed = 10
        dx = math.cos(angle_rad) * laser_speed
        dy = math.sin(angle_rad) * laser_speed

        laser = {
            'actor': Actor('weapons/weapon_ammo', (self.weapon.x, self.weapon.y)),
            'dx': dx,
            'dy': dy,
        }
        laser['actor'].angle = self.weapon.angle
        self.lasers.append(laser)
    
    def draw(self):
        """Desenha o personagem e a arma na tela."""
        self.sprite.draw()

        if self.weapon:
            self.weapon.angle = self.weapon.angle  # Atualiza o ângulo da arma
            self.weapon.draw()

        for laser in self.lasers:
            laser['actor'].draw()
    
    def update_weapon_position(self):
        offset_x = 20  # ajuste conforme necessário
        offset_y = -10
        self.weapon_sprite.pos = (self.x + offset_x, self.y + offset_y)



class Laser:
    def __init__(self, x, y, direction):
        self.sprite = Actor(actor['weapon_ammo'])
        self.sprite.pos = (x, y)
        self.direction = direction  # Direção do laser (1 para direita, -1 para esquerda)
        self.speed = 10

    def update(self):
        """Atualiza a posição do laser."""
        self.sprite.x += self.speed * self.direction

    def draw(self):
        """Desenha o laser na tela."""
        self.sprite.draw()
