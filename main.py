import pygame
import random
import os
import sys

# ----- Constantes e configurações iniciais -----
LARGURA_TELA = 800
ALTURA_TELA = 600
TITULO_JOGO = "Space Cheese"
COR_PRETO = (0, 0, 0)

pygame.init()
pygame.mixer.init()

# ----- Configuração dos paths -----
if getattr(sys, 'frozen', False):
    diretorio_principal = sys._MEIPASS
else:
    diretorio_principal = os.path.dirname(__file__)
diretorio_img = os.path.join(diretorio_principal, 'assets', 'img')
diretorio_snd = os.path.join(diretorio_principal, 'assets', 'sfx')

# ----- Estabelecimento de classes -----
# JOGADOR 
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

# ASTERÓIDE 
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

# COLETÁVEL
class Coletavel(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(diretorio_img, 'cheese.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(LARGURA_TELA - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(2, 5)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > ALTURA_TELA + 10:
            self.rect.x = random.randrange(LARGURA_TELA - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 5)

# ----- Desenho do nome do jogo -----
def desenhar_texto(surface, text, size, x, y):
    try:
        fonte = pygame.font.Font("font/DePixelBreit.ttf", size)
    except FileNotFoundError:
        fonte = pygame.font.SysFont("arial", size)
    text_surface = fonte.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# ----- Loop principal -----
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption(TITULO_JOGO)
clock = pygame.time.Clock()

# ----- Carregamento dos sons -----
som_coleta = pygame.mixer.Sound(os.path.join(diretorio_snd, 'item_pickup.wav'))
som_impacto = pygame.mixer.Sound(os.path.join(diretorio_snd, 'impact.wav'))

# ----- Agrupamento de sprites -----
todos_os_sprites = pygame.sprite.Group()
inimigos = pygame.sprite.Group()
coletaveis = pygame.sprite.Group()

jogador = Jogador()
todos_os_sprites.add(jogador)

for i in range(8):
    inimigo = Inimigo()
    todos_os_sprites.add(inimigo)
    inimigos.add(inimigo)

for i in range(4):
    estrela = Coletavel()
    todos_os_sprites.add(estrela)
    coletaveis.add(estrela)

# ----- Estrelas -----
estrelas_fundo = []
for i in range(150):
    x = random.randrange(0, LARGURA_TELA)
    y = random.randrange(0, ALTURA_TELA)
    velocidade = random.randint(1, 3)  
    estrelas_fundo.append([x, y, velocidade])

# ----- Variáveis -----
pontuacao = 0
vidas = 3

# ----- Loop do jogo -----
rodando = True
while rodando:
    clock.tick(60)

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    # Lógica e Atualizações
    todos_os_sprites.update()

    # Estrelas caindo (background)
    for estrela in estrelas_fundo:
        estrela[1] += estrela[2]
        if estrela[1] > ALTURA_TELA:
            estrela[1] = random.randrange(-20, -5)
            estrela[0] = random.randrange(0, LARGURA_TELA)

    # Colisão do jogador com coletáveis
    colisoes_coletaveis = pygame.sprite.spritecollide(jogador, coletaveis, True)
    for colisao in colisoes_coletaveis:
        pontuacao += 10
        som_coleta.play()
        # Adiciona uma nova estrela para manter o número
        estrela = Coletavel()
        todos_os_sprites.add(estrela)
        coletaveis.add(estrela)

    # Colisão do jogador com inimigos
    colisoes_inimigos = pygame.sprite.spritecollide(jogador, inimigos, True)
    if colisoes_inimigos:
        vidas -= 1
        som_impacto.play()

        # Adiciona um novo inimigo
        inimigo = Inimigo()
        todos_os_sprites.add(inimigo)
        inimigos.add(inimigo)
        if vidas == 0:
            rodando = False # Fim de jogo

    # Desenho (Renderização)
    tela.fill(COR_PRETO)
    
    # Desenho estrelas 
    for estrela in estrelas_fundo:
        pygame.draw.circle(tela, (255, 255, 255), (estrela[0], estrela[1]), 1)
    
    todos_os_sprites.draw(tela)

    # Desenhando o placar e as vidas
    desenhar_texto(tela, f"Pontos: {pontuacao}", 18, LARGURA_TELA / 2, 10)
    desenhar_texto(tela, f"Vidas: {vidas}", 18, 50, 10)

    pygame.display.flip()

pygame.quit()