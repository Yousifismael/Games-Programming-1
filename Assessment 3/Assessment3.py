import pygame, sys, math
from random import randrange
import random

pygame.font.get_fonts()
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.display.set_caption("Cooking game")

screenx = 1520
screeny = 780
screen = pygame.display.set_mode((screenx, screeny))
clock = pygame.time.Clock()

# assets
# Main Dishes
burger_image = pygame.image.load("burger.png").convert_alpha()
croissant_image = pygame.image.load("Croissant1.png").convert_alpha()
eggs_bacon_image = pygame.image.load("Eggs&Bacon.png").convert_alpha()

# Ingredients
bacon_image = pygame.image.load("bacon1.png").convert_alpha()
bread_image = pygame.image.load("bread1.png").convert_alpha()
cheese_image = pygame.image.load("cheese1.png").convert_alpha()
eggs_image = pygame.image.load("eggs.png").convert_alpha()
meat_image = pygame.image.load("meat1.png").convert_alpha()
dough_image = pygame.image.load("dough.png").convert_alpha()

# Player
chef_image = pygame.image.load("chef1.png").convert_alpha()

background_image = pygame.image.load("garden.jpeg")
Victory_image = pygame.image.load("Victory.png").convert_alpha()
font = pygame.font.Font(None, 48)


# define Cloud
class MainDish:
    def __init__(self, image, ingredients):
        self.xpos = 1400
        self.ypos = 650
        self.image = image
        self.ingredients = ingredients
        self.rect = self.image.get_rect()
        self.rect.x = randrange(screenx - self.rect.width)
        self.rect.y = randrange(screeny - self.rect.height)


class Ingredient:
    def __init__(self, image, name):
        self.image = image
        self.name = name
        self.rect = self.image.get_rect()
        self.rect.x = randrange(screenx - self.rect.width)
        self.rect.y = randrange(screeny - self.rect.height)


# player character
class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = 5
        self.sizex = 60
        self.sizey = 32
        self.sprite = pygame.transform.scale(chef_image, (self.sizex, self.sizey))
        self.rect = pygame.Rect(self.x, screeny - self.sizey, self.sizex, self.sizey)

    def Move(self, move_right):
        if move_right:
            self.x += self.speed
            if self.x + self.sizex > screenx:
                self.x = screenx - self.sizex
        else:
            self.x -= self.speed
            if self.x < 0:
                self.x = 0
        self.rect.x = self.x

    def MoveY(self, move_up):
        if move_up:
            self.y -= self.speed
            if self.y < 0:
                self.y = 0
        else:
            self.y += self.speed
            if self.y + self.sizey > screeny:
                self.y = screeny - self.sizey

        self.rect.y = self.y

    def Draw(self):
        self.sprite.set_colorkey((255, 255, 255))
        screen.blit(self.sprite, (self.x, self.y))


# spawning main dishes
burger = MainDish(burger_image, ["bread", "meat", "cheese"])
croissant = MainDish(croissant_image, ["dough", "cheese"])
eggs_bacon = MainDish(eggs_bacon_image, ["eggs", "bacon"])

# spawning ingredients
ingredients = [
    Ingredient(bacon_image, "bacon"),
    Ingredient(bread_image, "bread"),
    Ingredient(cheese_image, "cheese"),
    Ingredient(eggs_image, "eggs"),
    Ingredient(meat_image, "meat"),
    Ingredient(dough_image, "dough")
]


# add player and background image
player = Player()
background_image = pygame.transform.scale(background_image, (screenx, screeny))
timerr = 0
seconds = 0
minutes = 0
score = 0
MaxFrame = 60
timer = 50
Dish = [burger, croissant, eggs_bacon]
wrongIngredients = []
MainCookingDish = random.choice(Dish)
ingredients_collected = []
# w, h = background_image.get_size()

def reset_game():
    global MainCookingDish, ingredients, ingredients_collected
    MainCookingDish = random.choice(Dish)
    ingredients = [
        Ingredient(bacon_image, "bacon"),
        Ingredient(bread_image, "bread"),
        Ingredient(cheese_image, "cheese"),
        Ingredient(eggs_image, "eggs"),
        Ingredient(meat_image, "meat"),
        Ingredient(dough_image, "dough")
    ]
    ingredients_collected = []

burger_ingredients = "Meat, Cheese, Bread"
Croissant_ingredients = "Dough, Cheese"
Eggs_Bacon_ingredients = "Eggs, Bacon"


# Game Loop
while True:
    clock.tick(MaxFrame)
    #timer += (1 / MaxFrame)
    timer -= (1 / MaxFrame)
    if timer <= 0:
        reset_game()
        score = 0
        timer = 50
    seconds = timer % 60
    minutes = (seconds / 60) % 60

    # print(round(Timer))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()


    screen.blit(background_image, (0, 0))




    # player movement
    pressed_key = pygame.key.get_pressed()

    if pressed_key[pygame.K_RIGHT]:
        player.Move(True)

    elif pressed_key[pygame.K_LEFT]:
        player.Move(False)

    if pressed_key[pygame.K_UP]:
        player.MoveY(True)

    elif pressed_key[pygame.K_DOWN]:
        player.MoveY(False)



    # Drawing the recipe that the player has to cook
    if MainCookingDish == burger:
        screen.blit(burger.image, (burger.xpos, burger.ypos))
        Burger_surface = font.render(burger_ingredients, True, (255, 255, 255))
        screen.blit(Burger_surface, (1050, 720))

    elif MainCookingDish == croissant:
        screen.blit(croissant.image, (croissant.xpos, croissant.ypos))
        Croissant_surface = font.render(Croissant_ingredients, True, (255, 255, 255))
        screen.blit(Croissant_surface, (1150, 720))
    elif MainCookingDish == eggs_bacon:
        screen.blit(eggs_bacon.image, (eggs_bacon.xpos, eggs_bacon.ypos))
        Eggs_Bacon_surface = font.render(Eggs_Bacon_ingredients, True, (255, 255, 255))
        screen.blit(Eggs_Bacon_surface, (1200, 720))




    for ingredient in ingredients:
        if player.rect.colliderect(ingredient.rect):
            # Check if the collected ingredient is required for any main dish
            for dish in [MainCookingDish]:

                if ingredient.name in dish.ingredients:
                    # Increasing score for collecting the right ingredient
                    score += 10
                    print("Collected", ingredient.name)
                    # Remove the collected ingredient from the screen
                    ingredients.remove(ingredient)
                    ingredients_collected.append(ingredient.name)
                    break
                else:
                    score -= 10

                    wrongIngredients.append(ingredient.name)
                    ingredients.remove(ingredient)
                    print("new list: ", wrongIngredients)
                    break



 # win condition
    if score == 200:
        screen.blit(Victory_image, (-100, -100))
        pygame.display.flip()
        pygame.time.wait(4000)
        sys.exit()


    # Draw ingredients
    for ingredient in ingredients:
        screen.blit(ingredient.image, ingredient.rect)


        # Draw scoreboard


        scoreboard_text = "Score: " + str(score)
        goalscore_text = "Goal: 200"
        goalscore_surface = font.render(goalscore_text, True, (255, 255, 255))
        scoreboard_surface = font.render(scoreboard_text, True, (255, 255, 255))
        screen.blit(scoreboard_surface, (10, 680))
        screen.blit(goalscore_surface, (10, 720))

        # Check if the player has collected all ingredients for the current dish
        if set(ingredients_collected) == set(MainCookingDish.ingredients):
            reset_game()



    # background
    screen.blit(font.render("Chef Alex", True, (255, 255, 255)), (0, 0))
    screen.blit(font.render("Timer: " + str(math.floor(minutes) + (math.floor(seconds))), True, (255, 255, 255)),
                ((screenx - 160), 10))
    # screen.blit(font.render())

    # player
    player.Draw()

    pygame.display.flip()
    pygame.display.update()