import pyglet
from random import randrange
from pyglet.window import key

from pathlib import Path

TILES_DIRECTORY = Path('snake-tiles')

snake_tiles = {}
for path in TILES_DIRECTORY.glob('*.png'):
    snake_tiles[path.stem] = pyglet.image.load(path)



#Window settings
ctverec = 64
sirka = 10
vyska = 10
hraci_pole_sirka = ((sirka + 1) * ctverec)
hraci_pole_vyska = ((vyska + 1) * ctverec)

window = pyglet.window.Window(width=hraci_pole_sirka, height=hraci_pole_vyska)

#Picture settings
list_pictures = []
picture_fruit = pyglet.image.load("apple.png")
list_pictures.append(picture_fruit)
list_pictures.append(snake_tiles["left-tongue"])
list_pictures.append(snake_tiles["tail-right"])
list_pictures.append(snake_tiles["left-right"])
list_pictures.append(snake_tiles["right-top"])
list_pictures.append(snake_tiles["left-top"])
list_pictures.append(snake_tiles["left-bottom"])
list_pictures.append(snake_tiles["right-bottom"])

for pic in list_pictures:
    pic.anchor_x = pic.width // 2
    pic.anchor_y = pic.height // 2

#Sounds
eat_sound = pyglet.media.load("whip.wav", streaming=False)
crash_sound = pyglet.media.load("smash.wav")

#Game lists
list_snake = []
list_snake_position = []
list_fruit = []
list_fruit_position = []

class Snake:
    def __init__(self, position_x, position_y, direction_x, direction_y, rotation, speed, round):
        """Nastaveni zakladnich atributu pro objekty tridy Snake - pozice, smer, rotace obrazku, rychlost"""
        self.position_x = position_x
        self.position_y = position_y
        self.direction = (direction_x, direction_y)
        self.game_ended = False
        self.rotation = rotation
        self.direction_change = False
        self.speed = speed
        self.round = round
        self.food = False

    def snake(self):
        """Nastaveni obrazku pro zakladniho hada - prvni tri ctverecky"""
        for self in list_snake:
            if self == list_snake[0]:
                picture = snake_tiles["tail-right"]
                self.picture = pyglet.sprite.Sprite(picture, (self.position_x * ctverec) + 32, (self.position_y * ctverec) + 32)
                self.picture.rotation = self.rotation
            elif self == list_snake[-1]:
                picture = snake_tiles["left-tongue"]
                self.picture = pyglet.sprite.Sprite(picture, (self.position_x * ctverec) + 32, (self.position_y * ctverec) + 32)
                self.picture.rotation = self.rotation
            else:
                picture = snake_tiles["left-right"]
                self.picture = pyglet.sprite.Sprite(picture, (self.position_x * ctverec) + 32, (self.position_y * ctverec) + 32)
                self.picture.rotation = self.rotation

class Fruit:
    def __init__(self, position_x, position_y):
        """Nastaveni zakladnich atributu pro objekty tridy Fruit - pozice a obrazky"""
        self.position_x = position_x
        self.position_y = position_y
        self.picture = pyglet.sprite.Sprite(picture_fruit, (self.position_x * ctverec) + 32, (self.position_y * ctverec) + 32)
        list_fruit.append(self)
        list_fruit_position.append((self.position_x, self.position_y))



def create_fruit():
    """Tato funkce vytvori ovoce na nahodnem miste v hracim poli"""
    position_x = randrange(sirka)
    position_y = randrange(vyska)
    while True:
        if (position_x, position_y) in list_snake_position:
            position_x = randrange(sirka)
            position_y = randrange(vyska)
        else:
            break

    while True:
        if (position_x, position_y) in list_fruit_position:
                position_x = randrange(sirka)
                position_y = randrange(vyska)
        else:
            break
    ovoce = Fruit(position_x, position_y)

#Default snake
had = Snake(0, 0, 1, 0, 0, 1, 0)
had.snake()
list_snake.append(had)
list_snake_position.append((had.position_x, had.position_y))
had1 = Snake(1, 0, 1, 0, 0, 1, 0)
had1.snake()
list_snake.append(had1)
list_snake_position.append((had1.position_x, had1.position_y))
had2 = Snake(2, 0, 1, 0, 0, 1, 0)
had2.snake()
list_snake.append(had2)
list_snake_position.append((had2.position_x, had2.position_y))
create_fruit()

def tik(t):
    """Tato funkce je na zacatku volana kazdou vterinu a jeji volani se zrychluje s kazdym snezenym ovocem, vytvari nove objekty tridy Snake a pohybuje hadem, overuje zda je had zivy."""
    snake = list_snake[-1]
    #vypocet nove pozice
    position_x = snake.position_x + snake.direction[0]
    position_y = snake.position_y + snake.direction[1]
    #overeni zda had nenarazil do sebe nebo do okraje hraciho pole
    if position_x < 0 or position_x > sirka:
        crash_sound.play()
        snake.game_ended = True
    elif position_y < 0 or position_y > vyska:
        crash_sound.play()
        snake.game_ended = True
    for i in list_snake_position:
        if position_x == (i[0]) and position_y == (i[1]):
            crash_sound.play()
            snake.game_ended = True
    #kontrola ovoce
    for fruit in list_fruit:
        if fruit.position_x == position_x and fruit.position_y == position_y:
            fruit_to_eat = fruit
            snake.food = True
            round = snake.round + 1
            if round == 5:
                create_fruit()
                round = 0
    #prodlouzeni hada pri jidle
    if snake.food == True:
        if snake.speed > 0.005:
            speed = snake.speed * 0.9
        eat_sound.play()
        list_fruit.remove(fruit_to_eat)
        snake_novy = Snake(position_x, position_y, snake.direction[0], snake.direction[1], snake.rotation, speed, round)
        list_snake.append(snake_novy)
        list_snake_position.append((position_x, position_y))
        create_fruit()
        pyglet.clock.unschedule(tik)
        pyglet.clock.schedule_interval(tik, speed)
    #had pokracuje bez jidla - neprodluzuje se
    else:
        del list_snake[0]
        del list_snake_position[0]
        snake_novy = Snake(position_x, position_y, snake.direction[0], snake.direction[1], snake.rotation, snake.speed, snake.round)
        list_snake.append(snake_novy)
        list_snake_position.append((position_x, position_y))

pyglet.clock.schedule_interval(tik, had.speed)

def smer(key, mod):
    """Tato funkce meni smer hada podle stisknute klavesy"""
    snake = list_snake[-1]
    if key == pyglet.window.key.UP:
        snake.direction = (0, 1)
        snake.rotation = - 90
        snake.direction_change = True
    elif key == pyglet.window.key.DOWN:
        snake.direction = (0, -1)
        snake.rotation = 90
        snake.direction_change = True
    elif key == pyglet.window.key.LEFT:
        snake.direction = (-1, 0)
        snake.rotation = 180
        snake.direction_change = True
    elif key == pyglet.window.key.RIGHT:
        snake.direction = (1, 0)
        snake.rotation = 0
        snake.direction_change = True


def vykresli():
    """Funkce pro vykresleni obrazku a napisu"""
    window.clear()
    for snake in list_snake:
        had_older_index = list_snake.index(snake) - 1
        had_older = list_snake[had_older_index]
        if snake == list_snake[0]:
            snake.picture = pyglet.sprite.Sprite(snake_tiles["tail-right"], (snake.position_x * ctverec) + 32, (snake.position_y * ctverec) + 32)
            snake.picture.rotation = snake.rotation
        elif snake == list_snake[-1]:
            snake.picture = pyglet.sprite.Sprite(snake_tiles["left-tongue"], (snake.position_x * ctverec) + 32, (snake.position_y * ctverec) + 32)
            snake.picture.rotation = had_older.rotation
        elif snake.direction_change == True:
            had_index = list_snake.index(snake) + 1
            had = list_snake[had_index]
            had_old = snake
            if had_older.position_x < had_old.position_x and had_old.position_y < had.position_y:
                snake.picture = pyglet.sprite.Sprite(snake_tiles["left-top"], (snake.position_x * ctverec + 32), (snake.position_y * ctverec) + 32)
            elif had_older.position_y < had_old.position_y and had_old.position_x > had.position_x:
                snake.picture = pyglet.sprite.Sprite(snake_tiles["left-bottom"], (snake.position_x * ctverec) + 32, (snake.position_y * ctverec) + 32)
            elif had_older.position_x > had_old.position_x and had_old.position_y > had.position_y:
                snake.picture = pyglet.sprite.Sprite(snake_tiles["right-bottom"], (snake.position_x * ctverec) + 32, (snake.position_y * ctverec) + 32)
            elif had_older.position_y > had_old.position_y and had_old.position_x < had.position_x:
                snake.picture = pyglet.sprite.Sprite(snake_tiles["right-top"], (snake.position_x * ctverec) + 32, (snake.position_y * ctverec) + 32)
            elif had_older.position_x > had_old.position_x and had_old.position_y < had.position_y:
                snake.picture = pyglet.sprite.Sprite(snake_tiles["right-top"], (snake.position_x * ctverec) + 32, (snake.position_y * ctverec) + 32)
            elif had_older.position_y < had_old.position_y and had_old.position_x < had.position_x:
                snake.picture = pyglet.sprite.Sprite(snake_tiles["right-bottom"], (snake.position_x * ctverec) + 32, (snake.position_y * ctverec) + 32)
            elif had_older.position_x < had_old.position_x and had_old.position_y > had.position_y:
                snake.picture = pyglet.sprite.Sprite(snake_tiles["left-bottom"], (snake.position_x * ctverec) + 32, (snake.position_y * ctverec) + 32)
            elif had_older.position_y > had_old.position_y and had_old.position_x > had.position_x:
                snake.picture = pyglet.sprite.Sprite(snake_tiles["left-top"], (snake.position_x * ctverec) + 32, (snake.position_y * ctverec) + 32)
        else:
            snake.picture = pyglet.sprite.Sprite(snake_tiles["left-right"], (snake.position_x * ctverec) + 32, (snake.position_y * ctverec) + 32)
            snake.picture.rotation = snake.rotation
        snake.picture.draw()
    for fruit in list_fruit:
        fruit.picture.draw()
    if any([hasattr(snake, 'game_ended') and snake.game_ended for snake in list_snake]):
        gameover = pyglet.text.Label(
            "Game Over!", font_name='Times New Roman', font_size=36,
            x=window.width//2, y=window.height//2, anchor_x='center', anchor_y='center')
        gameover.draw()
        pyglet.clock.unschedule(tik)


window.push_handlers(
    on_draw=vykresli,
    on_key_press=smer,
)

pyglet.app.run()
