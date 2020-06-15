import pygame
from pygame.locals import *
import sys
import random

######## Inicializa a biblioteca pygame
framerate = 60
pygame.init()
clock = pygame.time.Clock()

pygame.display.set_caption("Jornada do Aquiles")
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((600, 600))

######### Modelos de cartas
card_face_down = pygame.image.load("img/cards/facedown.png")

cards_color = {
    "Azul": [pygame.image.load("img/cards/blue_1.png"), pygame.image.load("img/cards/blue_2.png")],
    "Vermelho": [pygame.image.load("img/cards/red.png"), pygame.image.load("img/cards/red.png")],
    "Verde": [pygame.image.load("img/cards/green.png"), pygame.image.load("img/cards/green.png")],
    "Laranja": [pygame.image.load("img/cards/orange.png"), pygame.image.load("img/cards/orange.png")],
}


######## Classes
class Scenery:
    scenario = None
    border_x = None
    border_y = None

    def __init__(self, background, border_x, border_y):
        self.background = pygame.image.load(background)
        self.border_x = border_x
        self.border_y = border_y

    def get_SIZE(self):
        return self.background.get_rect().size

    def render(self):
        return self.background


class Character:
    sprite = pygame.image.load("img/sprites/O_1.png")
    x = 0
    y = 0

    def __init__(self):
        pass

    def walk_UP(self):
        self.y += 5

    def walk_DOWN(self):
        self.y -= 5

    def walk_LEFT(self):
        self.x -= 5

    def walk_RIGHT(self):
        self.x += 5

    def get_POSITION(self):
        return self.x, self.y

    def render(self):
        return self.sprite


class Camera:
    map_x = None
    map_y = None
    x = None
    y = None
    character_x = None
    character_y = None

    def __init__(self, scenery: Scenery):
        self.map_x = int(scenery.get_SIZE()[0] / 4) + 100
        self.map_y = int(scenery.get_SIZE()[1] / 4)

    def Update(self, position: Character):
        position = position.get_POSITION()
        self.character_x = position[0]
        self.character_y = position[1]
        x, y = self.character_x, self.character_y
        if self.character_x > self.map_x:
            x = self.map_x
        if self.character_x < self.map_x * -1:
            x = self.map_x * -1
        if self.character_y > self.map_y:
            y = self.map_y
        if self.character_y < self.map_y * -1:
            y = self.map_y * -1

        self.x = x
        self.y = y

    def get_POSITION_SCENARIO_PYGAMES(self):
        return (self.x * -1) - self.map_x, self.y - self.map_y

    def get_POSITION_CHARACTER_PYGAMES(self):
        return self.character_x + 260 - self.x, 215 - self.character_y + self.y


class Cards:
    deck = None
    cards_position = [
        (-450, 270), (-150, 270), (150, 270), (450, 270),
        (-450, -270), (-150, -270), (150, -270), (450, -270),
    ]
    card_size = (160, 200)
    card_face_up = []

    def __init__(self, cards_dictionary):
        self.add_to_deck(cards_dictionary)

    def add_to_deck(self, _cards):
        deck = []
        for card in _cards:
            c = [card, _cards[card][0]]
            deck.append(c)
            c = [card, _cards[card][1]]
            deck.append(c)

        self.shuffle(deck)

    def shuffle(self, _deck):
        raffle = random.sample(range(8), 8)
        deck = {}

        index = 0
        for s in raffle:
            deck[self.cards_position[index]] = _deck[s]
            index += 1

        self.deck = deck

    def flip_card(self, position):
        for card in self.cards_position:
            if (card[0] - (self.card_size[0] / 2) <= position[0] <= card[0] + (self.card_size[0] / 2) and
                    card[1] - (self.card_size[1] / 2) <= position[1] <= card[1] + (self.card_size[1] / 2)):
                self.card_face_up.append(position)
                self.check_cards()

    def check_cards(self):
        if len == 2:
            key_1 = self.card_face_up[0]
            key_2 = self.card_face_up[1]

            if self.deck[key_1][0] == self.deck[key_2][0]:
                del self.deck[key_1]
                del self.deck[key_2]
                self.card_face_up.clear()

            else:
                self.card_face_up.clear()


######## Funções

def start_event(char, map, cam, card):
    interval = 20
    input_last_time = 0
    pass_stage = False
    while pass_stage is False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        input_last_time += 1
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP] and char.y < map.border_y:
            char.walk_UP()
        if pressed[pygame.K_DOWN] and char.y > map.border_y * -1:
            char.walk_DOWN()
        if pressed[pygame.K_RIGHT] and char.x < map.border_x:
            char.walk_RIGHT()
        if pressed[pygame.K_LEFT] and char.x > map.border_x * -1:
            char.walk_LEFT()
        if pressed[pygame.K_SPACE]:
            if input_last_time > interval:
                card.flip_card(char.get_POSITION())

                input_last_time = 0

        cam.Update(char)

        screen.blit(map.render(), cam.get_POSITION_SCENARIO_PYGAMES())

        for card in card.cards:
            screen.blitz(card_face_down, card[0 + 320])

        screen.blit(char.render(), cam.get_POSITION_CHARACTER_PYGAMES())
        pygame.display.flip()
        clock.tick(framerate)


######## GAME

level = 1
while True:
    if level == 1:
        aquiles = Character()
        scenario = Scenery("img/scenes/mapa.png", 600, 430)
        camera = Camera(scenario)
        cards = Cards(cards_color)
        start_event(aquiles, scenario, camera, cards)

    if level == 2:
        aquiles = Character()
        scenario = Scenery("img/scenes/mapa.png", 600, 430)
        camera = Camera(scenario)
        start_event(aquiles, scenario, camera)
