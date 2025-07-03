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