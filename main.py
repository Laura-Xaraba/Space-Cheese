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

