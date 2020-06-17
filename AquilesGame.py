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

font = pygame.font.SysFont('sans', 30)
BLACK = (0, 0, 0)
WHITE = (250, 250, 250)

######### Modelos de cartas
card_face_down = pygame.image.load("img/cards/test.jpeg")
cards_color = {
    "Azul": [pygame.image.load("img/cards/blue_1.png"), pygame.image.load("img/cards/blue_2.png")],
    "Vermelho": [pygame.image.load("img/cards/red.png"), pygame.image.load("img/cards/red.png")],
    "Verde": [pygame.image.load("img/cards/green.png"), pygame.image.load("img/cards/green.png")],
    "Laranja": [pygame.image.load("img/cards/orange.png"), pygame.image.load("img/cards/orange.png")],
}


######## Classes
class Level:
    lvl = None

    def __init__(self):
        self.lvl = 1

    def pass_level(self, passed: bool):
        if passed:
            self.lvl += 1


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
    sprite = "img/sprites/character/O_1.png"
    animation = 1
    x = 0
    y = 0
    hp = 3

    def __init__(self):
        pass

    def walk_UP(self):
        self.y += 5
        self.update_sprite("UP")

    def walk_DOWN(self):
        self.y -= 5
        self.update_sprite("DOWN")

    def walk_LEFT(self):
        self.x -= 5
        self.update_sprite("LEFT")

    def walk_RIGHT(self):
        self.x += 5
        self.update_sprite("RIGHT")

    def IDLE(self):
        self.animation = 1
        self.update_sprite("")

    def update_sprite(self, s):
        if self.animation > 5:
            self.animation = 1

        if s == "UP":
            self.sprite = "img/sprites/character/U_1.png"
        if s == "DOWN":
            self.sprite = "img/sprites/character/D_1.png"
        if s == "LEFT":
            self.sprite = "img/sprites/character/L_1.png"
        if s == "RIGHT":
            self.sprite = "img/sprites/character/R_1.png"

        self.sprite = self.sprite.replace(self.sprite[-5], str(int(self.animation)), 1)

    def render(self):
        return pygame.image.load(self.sprite)


class Boss:
    sprite = None
    x = None
    y = None
    skills = []
    count = 0
    interval = None

    def __init__(self, sprite, strength: int):
        self.sprite = sprite
        self.x = 0
        self.y = 200
        if strength == 1:
            self.interval = 160
        if strength == 2:
            self.interval = 120
        if strength == 3:
            self.interval = 60

    def update(self):
        if self.count > self.interval:
            self.teleport()
            self.count = 0
        else:
            self.count += 1

        self.update_skills()

    def teleport(self):
        self.x = random.choice(range(-700, 700))
        self.y = random.choice(range(-500, 500))
        self.attack()

    def attack(self):
        ball_1 = (self.x, self.y - 150)
        self.skills.append(ball_1)
        ball_2 = (self.x - 100, self.y - 100)
        self.skills.append(ball_2)
        ball_3 = (self.x - 150, self.y)
        self.skills.append(ball_3)
        ball_4 = (self.x - 100, self.y + 100)
        self.skills.append(ball_4)
        ball_5 = (self.x, self.y + 150)
        self.skills.append(ball_5)
        ball_6 = (self.x + 100, self.y + 100)
        self.skills.append(ball_6)
        ball_7 = (self.x + 150, self.y)
        self.skills.append(ball_7)
        ball_8 = (self.x + 100, self.y - 100)
        self.skills.append(ball_8)

    def update_skills(self):
        speed = (0, -4), (-4, -4), (-4, 0), (-4, 4), (0, 4), (4, 4), (4, 0), (4, -4)
        skill_update = []
        index = 0
        for skill in self.skills:
            skill_update.append((skill[0] + speed[index][0], skill[1] + speed[index][1]))
            index += 1
            if index > 7:
                index = 0
        self.skills = skill_update

        if len(skill_update) > 1000:
            del skill_update[0]

    def render(self):
        return pygame.image.load(self.sprite)


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
            else:
                self.cards_face_up.clear()


class Event:
    map = None
    cam_x = 0
    cam_y = 0
    character = None
    boss = None
    deck = None
    time_delay = 0
    time_interval_hit = 0
    character_hit = False

    def __init__(self, scenery: Scenery, character: Character, deck: Deck, enemy: Boss):
        self.map = scenery
        self.character = character
        self.deck = deck
        self.boss = enemy

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
        self.check_collision()

    def check_collision(self):
        if self.time_interval_hit <= 60:
            self.time_interval_hit += 1
        else:
            collison = 45
            for skill in self.boss.skills:
                if (self.character.x - collison <= skill[0] <= self.character.x + collison and
                        self.character.y - collison <= skill[1] <= self.character.y + collison):
                    self.character.hp -= 1
                    self.time_interval_hit = 0

    def get_POSITION_SCENARIO_PYGAMES(self):
        self.Update()
        return (self.cam_x * -1) - self.map.x, self.cam_y - self.map.y

    def get_POSITION_CHARACTER_PYGAMES(self):
        return self.character.x + 260 - self.cam_x, 215 - self.character.y + self.cam_y

    def get_POSITION_BOSS_PYGAMES(self):
        return self.boss.x + 180 - self.cam_x, 170 - self.boss.y + self.cam_y

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

    def get_POSITIONS_SKILLS_PYGAMES(self):
        list_skills = []
        for skill in self.boss.skills:
            list_skills.append((skill[0] + 325 - self.cam_x, (skill[1] * -1) + 300 + self.cam_y))
        return list_skills


######## Funções

def start_event(game_event: Event):
    interval = 30
    input_last_time = 0
    loop = True
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        input_last_time += 1
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RIGHT] and game_event.character.x < game_event.map.border_x:
            game_event.character.walk_RIGHT()
        if pressed[pygame.K_LEFT] and game_event.character.x > game_event.map.border_x * -1:
            game_event.character.walk_LEFT()
        if pressed[pygame.K_UP] and game_event.character.y < game_event.map.border_y:
            game_event.character.walk_UP()
        if pressed[pygame.K_DOWN] and game_event.character.y > game_event.map.border_y * -1:
            game_event.character.walk_DOWN()
        if not pressed[pygame.K_UP] and not pressed[pygame.K_DOWN] and not pressed[pygame.K_RIGHT] and not pressed[
            pygame.K_LEFT]:
            game_event.character.IDLE()
        else:
            game_event.character.animation += 0.15
        if pressed[pygame.K_SPACE]:
            if input_last_time > interval:
                game_event.deck.flip_card(game_event.character.x, game_event.character.y)
                input_last_time = 0

        game_event.boss.update()

        screen.blit(game_event.map.render(), game_event.get_POSITION_SCENARIO_PYGAMES())

        for card in game_event.get_POSITIONS_CARDS_FACEDOWN_PYGAMES():
            screen.blit(card_face_down, card)

        for position, value in game_event.get_POSITIONS_CARDS_FACEUP_PYGAMES().items():
            screen.blit(value[1], position)

        screen.blit(game_event.character.render(), game_event.get_POSITION_CHARACTER_PYGAMES())
        screen.blit(game_event.boss.render(), game_event.get_POSITION_BOSS_PYGAMES())

        for ball in game_event.get_POSITIONS_SKILLS_PYGAMES():
            pygame.draw.circle(screen, (255, 0, 0), [ball[0], ball[1]], 20)

        pygame.draw.rect(screen, BLACK, [0, 0, 110, 50])

        aquiles_hp = font.render('VIDA: ' + str(game_event.character.hp), True, WHITE)
        screen.blit(aquiles_hp, (10, 5))
        pygame.display.flip()
        clock.tick(framerate)

        if len(game_event.deck.cards) == 0:
            pygame.time.wait(500)
            return True

        if game_event.character.hp <= 0:
            pygame.time.wait(500)
            return False


######## GAME
level = Level()
while True:

    if level.lvl == 1:
        aquiles = Character()
        enemy = Boss("img/sprites/bosses/boss_test.png", 1)
        scenario = Scenery("img/scenes/mapa.png", 600, 430)
        cards = Deck(cards_color)
        game = Event(scenario, aquiles, cards, enemy)
        if_passed = start_event(game)
        level.pass_level(if_passed)

    if level.lvl == 2:
        aquiles = Character()
        enemy = Boss("img/sprites/bosses/boss_test.png", 2)
        scenario = Scenery("img/scenes/mapa.png", 600, 430)
        cards = Deck(cards_color)
        game = Event(scenario, aquiles, cards, enemy)
        if_passed = start_event(game)
        level.pass_level(if_passed)

    if level.lvl == 3:
        aquiles = Character()
        enemy = Boss("img/sprites/bosses/boss_test.png", 3)
        scenario = Scenery("img/scenes/mapa.png", 600, 430)
        cards = Deck(cards_color)
        game = Event(scenario, aquiles, cards, enemy)
        if_passed = start_event(game)
        level.pass_level(if_passed)

pygame.quit()
sys.exit()
