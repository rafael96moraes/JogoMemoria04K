import sys, pygame
from pygame.locals import *

# ----- PARTE 1 ------

# Iniciar a biblioteca pygame
pygame.init()

# Janela
size = (1400, 1000)
screen = pygame.display.set_mode(size)
from random import *

# titulo do jogo
pygame.display.set_caption("Jogo de Memória")

# fundo da janela
imagem = pygame.image.load("animation/cenario1.jpg").convert()

# Variável para contagem de tempo, utilizado para controlar a velocidade de quadros (de atualizações da tela)
clock = pygame.time.Clock()

# Temporizador q atualiza cada 1s
CLOCKTICK = pygame.USEREVENT + 1
pygame.time.set_timer(CLOCKTICK, 1000)

# ===============PERSONAGEM================
#imagem do personagem
personagem = pygame.image.load("animation/O_1.png")
personagem_passos = 0
personagem_ocioso = pygame.image.load("animation/O_1.png")
personagem_direita = [pygame.image.load("animation/R_1.png"), pygame.image.load("animation/R_2.png"), pygame.image.load("animation/R_3.png"), pygame.image.load("animation/R_4.png"), pygame.image.load("animation/R_5.png")]
personagem_esquerda = [pygame.image.load("animation/L_1.png"), pygame.image.load("animation/L_2.png"), pygame.image.load("animation/L_3.png"), pygame.image.load("animation/L_4.png"), pygame.image.load("animation/L_5.png")]
personagem_subindo = [pygame.image.load("animation/U_1.png"), pygame.image.load("animation/U_2.png"), pygame.image.load("animation/U_3.png"), pygame.image.load("animation/U_4.png"), pygame.image.load("animation/U_5.png")]
personagem_descendo = [pygame.image.load("animation/D_1.png"), pygame.image.load("animation/D_2.png"), pygame.image.load("animation/D_3.png"), pygame.image.load("animation/D_4.png"), pygame.image.load("animation/D_5.png")]

# Posicao do personagem
posicaoPersonagem = [700, 500]

# Velocidade do personagem
velocidadePersonagem = [7, 7]

# ===============VILÕES================
vilao_1 = pygame.image.load("animation/O_1.png")

vilao_2 = pygame.image.load("animation/monstro2.png")
vilao_3 = pygame.image.load("animation/monstro3.png")
X_vilao = 0
Y_vilao = 20
#Iniciar o ataque
atacar = True;

# Temporizador do ataque
temporizador = 0

# Level da fase. O inicial é 1
level = 1

# ================PEDRAS=================
pedra = pygame.image.load("animation/O_1.png")

# ----- PARTE 3 ------

while True:

    for event in pygame.event.get():
        # Verifica se foi um evento de saida (pygame.QUIT)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # capturando evendo de relogio a cada 1 segundo e atualizando a variável contadora
        if event.type == CLOCKTICK:
            temporizador += 1

    #Ataque do vilão
    if atacar == True:
        X_vilao = randint(40, 960)
        Y_vilao = 20
        posicaoPedra = [Y_vilao-3, X_vilao]
        atacar = False

    posicaoPedra[1] = -1


    #Se ñ tiver uma tecla pressionada, personagem fica com animação ocioso
    #if pygame.key.get_focused != True:
        #personagem = personagem_ocioso


    # Verifica qual tecla (seta) foi pressionada e captura evento
    pressed = pygame.key.get_pressed()

    # Controla a animação andando. Maior numero, mais rapido a troca de animação
    personagem_passos += 0.3

    if pressed[pygame.K_UP]:
        posicaoPersonagem[1] -= velocidadePersonagem[1]
        personagem = personagem_subindo[(int(personagem_passos) % 5)]

    if pressed[pygame.K_DOWN]:
        posicaoPersonagem[1] += velocidadePersonagem[1]
        personagem = personagem_subindo[(int(personagem_passos) % 5)]

    if pressed[pygame.K_LEFT]:
        posicaoPersonagem[0] -= velocidadePersonagem[0]
        personagem = personagem_esquerda[(int(personagem_passos) % 5)]

    if pressed[pygame.K_RIGHT]:
        posicaoPersonagem[0] += velocidadePersonagem[0]
        personagem = personagem_direita[(int(personagem_passos) % 5)]



    # Blita a imagem de fundo na tela
    screen.blit(imagem, (0, 0))
    screen.blit(personagem, (posicaoPersonagem[0], posicaoPersonagem[1]))
    screen.blit(vilao_1, (X_vilao, Y_vilao))
    screen.blit(pedra, (posicaoPedra[0], posicaoPedra[1]))

    # Atualiza a tela visivel ao usuario
    pygame.display.flip()

    # Limita para 60fps
    clock.tick(60)
