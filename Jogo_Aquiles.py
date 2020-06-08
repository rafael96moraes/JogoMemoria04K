import pygame, sys
from pygame.locals import *
from random import *

# ============ PARTE 1 ============
# Inicializa a biblioteca pygame
pygame.init()

clock = pygame.time.Clock()

# Cria a surface
size = (800, 600)
screen = pygame.display.set_mode(size)

# Define um titulo para a janela
pygame.display.set_caption("Jornada do Aquiles")

# Carrega o mapa do fundo
cenario = pygame.image.load("img/scenes/mapa.png")

# Aquiles
aquilesVelocidade = 5
aquiles = pygame.image.load("img/sprites/O_1.png")
aquilesPosicao = [0, 0] #posicao inicial, em centro do mapa

# TESTES
font = pygame.font.SysFont('sans', 30)
WHITE = (255, 255, 255)

# ============ PARTE 2 ============

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_UP]:
        aquilesPosicao[1] += aquilesVelocidade

    if pressed[pygame.K_DOWN]:
        aquilesPosicao[1] -= aquilesVelocidade

    if pressed[pygame.K_RIGHT]:
        aquilesPosicao[0] -= aquilesVelocidade

    if pressed[pygame.K_LEFT]:
        aquilesPosicao[0] += aquilesVelocidade

    camera = [aquilesPosicao[0], aquilesPosicao[1]]
    if camera[0] > 400:
        camera[0] = 400
    if camera[0] < -400:
        camera[0] = -400
    if camera[1] > 300:
        camera[1] = 300
    if camera[1] < -300:
        camera[1] = -300

    screen.blit(cenario, (camera[0] - 400, camera[1] - 300))
    screen.blit(aquiles, ((aquilesPosicao[0] * -1) + 350, (aquilesPosicao[1] * -1) + 215))

    aquilesLog_X = font.render('aquiles_X: ' + str(aquilesPosicao[0]), True, (WHITE))
    screen.blit(aquilesLog_X, (600, 50))

    aquilesLog_Y = font.render('aquiles_Y: ' + str(aquilesPosicao[1]), True, (WHITE))
    screen.blit(aquilesLog_Y, (600, 80))

    pygame.display.flip()
    clock.tick(60)
