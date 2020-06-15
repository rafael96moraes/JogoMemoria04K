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
card_face_down = pygame.image.load("img/cards/test.jpeg")

cards_color = {
    "Azul": [pygame.image.load("img/cards/blue_1.png"), pygame.image.load("img/cards/blue_2.png")],
    "Vermelho": [pygame.image.load("img/cards/red.png"), pygame.image.load("img/cards/red.png")],
    "Verde": [pygame.image.load("img/cards/green.png"), pygame.image.load("img/cards/green.png")],
    "Laranja": [pygame.image.load("img/cards/orange.png"), pygame.image.load("img/cards/orange.png")],
}


######## Classes
class Scenery:
    scenario = None
    x = None
    y = None
    border_x = None
    border_y = None

    def __init__(self, background, border_x, border_y):
        self.background = pygame.image.load(background)
        self.border_x = border_x
        self.border_y = border_y
        self.x = int(self.background.get_rect().size[0] / 4) + 100
        self.y = int(self.background.get_rect().size[1] / 4)

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

    def render(self):
        return self.sprite


class Deck:
    cards = None
    _cards_position = [
        (-450, 270), (-150, 270), (150, 270), (450, 270),
        (-450, -270), (-150, -270), (150, -270), (450, -270),
    ]
    card_size = (160, 200)
    cards_face_up = {}
    cards_cache = {}

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
            deck[self._cards_position[index]] = _deck[s]
            index += 1

        self.cards = deck

    def flip_card(self, position_x, position_y):
        for card in self._cards_position:
            if (card[0] - (self.card_size[0] / 2) <= position_x <= card[0] + (self.card_size[0] / 2) and
                    card[1] - (self.card_size[1] / 2) <= position_y <= card[1] + (self.card_size[1] / 2)):

                try:
                    self.cards_face_up[card] = self.cards[card]
                    self.cards_cache[card] = self.cards[card]
                except KeyError:
                    pass

                self.check_cards()

    def check_cards(self):
        if len(self.cards_face_up) == 2:
            _cards = []
            for card_position, card_value in self.cards_face_up.items():
                _cards.append([card_position, card_value])

            if _cards[0][1][0] == _cards[1][1][0] and _cards[0][0] != _cards[1][0]:
                del self.cards[_cards[0][0]]
                del self.cards[_cards[1][0]]
                self.cards_face_up.clear()
                print(len(self.cards))
            else: self.cards_face_up.clear()


class Event:
    map = None
    cam_x = 0
    cam_y = 0
    character = None
    deck = None
    time_delay = 0

    def __init__(self, scenery: Scenery, character: Character, deck: Deck):
        self.map = scenery
        self.character = character
        self.deck = deck

    def Update(self):
        x, y = self.character.x, self.character.y
        if self.character.x > self.map.x:
            x = self.map.x
        if self.character.x < self.map.x * -1:
            x = self.map.x * -1
        if self.character.y > self.map.y:
            y = self.map.y
        if self.character.y < self.map.y * -1:
            y = self.map.y * -1

        self.cam_x = x
        self.cam_y = y

    def get_POSITION_SCENARIO_PYGAMES(self):
        self.Update()
        return (self.cam_x * -1) - self.map.x, self.cam_y - self.map.y

    def get_POSITION_CHARACTER_PYGAMES(self):
        return self.character.x + 260 - self.cam_x, 215 - self.character.y + self.cam_y

    def get_POSITIONS_CARDS_FACEDOWN_PYGAMES(self):
        list_cards = []
        for card in self.deck.cards:
            card_pygames = card[0] + 235 - self.cam_x, (card[1] * -1) + 190 + self.cam_y
            list_cards.append(card_pygames)

        return list_cards

    def get_POSITIONS_CARDS_FACEUP_PYGAMES(self):
        list_cards = {}
        for card_position, card_values in self.deck.cards_face_up.items():
            card_pygames = card_position[0] + 235 - self.cam_x, (card_position[1] * -1) + 190 + self.cam_y

            list_cards[card_pygames] = card_values

        if len(self.deck.cards_cache) == 2:
            self.time_delay += 1
            if self.time_delay < 60:
                for card_position, card_values in self.deck.cards_cache.items():
                    card_pygames = card_position[0] + 235 - self.cam_x, (card_position[1] * -1) + 190 + self.cam_y

                    list_cards[card_pygames] = card_values
            else:
                self.time_delay = 0
                self.deck.cards_cache.clear()

        return list_cards


######## Funções

def start_event(game_event: Event):
    interval = 30
    input_last_time = 0
    pass_stage = False
    while pass_stage is False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        input_last_time += 1
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP] and game_event.character.y < game_event.map.border_y:
            game_event.character.walk_UP()
        if pressed[pygame.K_DOWN] and game_event.character.y > game_event.map.border_y * -1:
            game_event.character.walk_DOWN()
        if pressed[pygame.K_RIGHT] and game_event.character.x < game_event.map.border_x:
            game_event.character.walk_RIGHT()
        if pressed[pygame.K_LEFT] and game_event.character.x > game_event.map.border_x * -1:
            game_event.character.walk_LEFT()
        if pressed[pygame.K_SPACE]:
            if input_last_time > interval:
                game_event.deck.flip_card(game_event.character.x, game_event.character.y)
                input_last_time = 0

        screen.blit(game_event.map.render(), game_event.get_POSITION_SCENARIO_PYGAMES())

        for card in game_event.get_POSITIONS_CARDS_FACEDOWN_PYGAMES():
            screen.blit(card_face_down, card)

        for position, value in game_event.get_POSITIONS_CARDS_FACEUP_PYGAMES().items():
            screen.blit(value[1], position)

        screen.blit(game_event.character.render(), game_event.get_POSITION_CHARACTER_PYGAMES())
        pygame.display.flip()
        clock.tick(framerate)


######## GAME

level = 1
while True:
    if level == 1:
        aquiles = Character()
        scenario = Scenery("img/scenes/mapa.png", 600, 430)
        cards = Deck(cards_color)
        game = Event(scenario, aquiles, cards)
        start_event(game)

    if level == 2:
        pass

    if level == 3:
        pass

    pygame.quit()
    sys.exit()