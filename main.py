import pygame
import random
import os

# ----- Constantes e configurações iniciais -----
LARGURA_TELA = 800
ALTURA_TELA = 600
TITULO_JOGO = "Coletor Cósmico"
COR_PRETO = (0, 0, 0)

pygame.init()
pygame.mixer.init()

# Configuração dos paths
diretorio_principal = os.path.dirname(__file__)
diretorio_img = os.path.join(diretorio_principal, 'assets', 'img', 'sfx')

# Estabelecimento de classes

# ----- JOGADOR -----
class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Carregamento da imagem, Ajuste do tamanho e posição inicial
        self.image = pygame.image.load(os.path.join(diretorio_img, 'player__space_ship.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 40))
        self.rect = self.image.get_rect()
        self.rect.centerx = LARGURA_TELA / 2
        self.rect.bottom = ALTURA_TELA - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx

        # Jogador permanece dentro da tela
        if self.rect.right > LARGURA_TELA:
            self.rect.right = LARGURA_TELA
        if self.rect.left < 0:
            self.rect.left = 0

# ----- ASTERÓIDE -----
class Inimigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(diretorio_img, 'asteroid.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(LARGURA_TELA - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 4)

    def update(self):
        self.rect.y += self.speedy

        # Reposicionamento do inimigo no topo da tela quando este sai da mesma
        if self.rect.top > ALTURA_TELA + 10:
            self.rect.x = random.randrange(LARGURA_TELA - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 4)