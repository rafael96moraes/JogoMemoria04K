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

#define as fronteiras, que ñ deixará o personagem ultrapassar
fronteira_X = 600
fronteira_Y = 430

# Aquiles
aquilesAndar = 5
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
    #Movimentacao do aquiles
    if pressed[pygame.K_UP]:
        aquilesPosicao[1] += aquilesAndar
    if pressed[pygame.K_DOWN]:
        aquilesPosicao[1] -= aquilesAndar
    if pressed[pygame.K_RIGHT]:
        aquilesPosicao[0] += aquilesAndar
    if pressed[pygame.K_LEFT]:
        aquilesPosicao[0] -= aquilesAndar

    #Verifica se ultrapassou limites da fronteiras.Caso sim, corrige
    if aquilesPosicao[0] > fronteira_X:
        aquilesPosicao[0] = fronteira_X
    if aquilesPosicao[0] < fronteira_X * -1:
        aquilesPosicao[0] = fronteira_X * -1
    if aquilesPosicao[1] > fronteira_Y:
        aquilesPosicao[1] = fronteira_Y
    if aquilesPosicao[1] < fronteira_Y * -1:
        aquilesPosicao[1] = fronteira_Y * -1


    camera = [aquilesPosicao[0], aquilesPosicao[1]]
    #Não permitir que camera atravesse o mapa. A camera só fica presa no cenário
    if camera[0] > 400:
        camera[0] = 400
    if camera[0] < -400:
        camera[0] = -400
    if camera[1] > 300:
        camera[1] = 300
    if camera[1] < -300:
        camera[1] = -300

    screen.blit(cenario, ((camera[0] * -1) - 400, camera[1] - 300))
    screen.blit(aquiles, ((aquilesPosicao[0] + 350) - camera[0], ((aquilesPosicao[1] * -1) + 215) + camera[1]))

    #Apenas para "debug"
    aquilesLog_X = font.render('aquiles_X: ' + str(aquilesPosicao[0]), True, (WHITE))
    screen.blit(aquilesLog_X, (600, 50))
    aquilesLog_Y = font.render('aquiles_Y: ' + str(aquilesPosicao[1]), True, (WHITE))
    screen.blit(aquilesLog_Y, (600, 80))

    pygame.display.flip()
    clock.tick(60)