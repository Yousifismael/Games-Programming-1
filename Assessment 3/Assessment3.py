import pygame
import sys
import math
import random
from random import randrange

pygame.font.get_fonts()
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.display.set_caption("Cooking game")

screenx = 1520
screeny = 780
screen = pygame.display.set_mode((screenx, screeny))
clock = pygame.time.Clock()

# Load images
burger_image = pygame.image.load("burger.png").convert_alpha()
croissant_image = pygame.image.load("Croissant.png").convert_alpha()
eggs_bacon_image = pygame.image.load("Eggs&Bacon.png").convert_alpha()
bacon_image = pygame.image.load("bacon.png").convert_alpha()
bread_image = pygame.image.load("bread.png").convert_alpha()
cheese_image = pygame.image.load("cheese.png").convert_alpha()
eggs_image = pygame.image.load("eggs.png").convert_alpha()
meat_image = pygame.image.load("meat.png").convert_alpha()
dough_image = pygame.image.load("dough.png").convert_alpha()
chef_image = pygame.image.load("chef.jpeg").convert_alpha()
background_image = pygame.image.load("garden.jpeg")
Victory_image = pygame.image.load("Victory.png").convert_alpha()
font = pygame.font.Font(None, 48)

# Define colors
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)

# Define button properties
button_width = 200
button_height = 50
button_x = (screenx - button_width) // 2
button_y = (screeny - button_height) // 2

# Function to draw text on button
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

# Function to check if a point is within a rectangle
def is_mouse_over(x, y, rect):
    if rect.left < x < rect.right and rect.top < y < rect.bottom:
        return True
    return False

# Main menu loop
def main_menu():
    global start_button
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if is_mouse_over(mouse_x, mouse_y, start_button):
                    return

        screen.blit(background_image, (0, 0))
        start_button = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(screen, GRAY, start_button)
        draw_text("Start", font, WHITE, screen, button_x + button_width // 2, button_y + button_height // 2)
        pygame.display.flip()
        clock.tick(30)

# Define Cloud
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

# Player character
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

# Spawning main dishes
burger = MainDish(burger_image, ["bread", "meat", "cheese"])
croissant = MainDish(croissant_image, ["dough", "cheese"])
eggs_bacon = MainDish(eggs_bacon_image, ["eggs", "bacon"])

# Spawning ingredients
ingredients = [
    Ingredient(bacon_image, "bacon"),
    Ingredient(bread_image, "bread"),
    Ingredient(cheese_image, "cheese"),
    Ingredient(eggs_image, "eggs"),
    Ingredient(meat_image, "meat"),
    Ingredient(dough_image, "dough")
]

# Add player and background image
player = Player()
background_image = pygame.transform.scale(background_image, (screenx, screeny))

# Function to reset the game
def reset_game():
    global MainCookingDish, ingredients, ingredients_collected, score, timer
    MainCookingDish = random.choice([burger, croissant, eggs_bacon])
    ingredients = [
        Ingredient(bacon_image, "bacon"),
        Ingredient(bread_image, "bread"),
        Ingredient(cheese_image, "cheese"),
        Ingredient(eggs_image, "eggs"),
        Ingredient(meat_image, "meat"),
        Ingredient(dough_image, "dough")
    ]
    ingredients_collected = []
    score = 0
    timer = 50

# Game loop
def game_loop():
    global score, timer
    while True:
        clock.tick(60)
        timer -= (1 / 60)
        if timer <= 0:
            reset_game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Player movement
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
        elif MainCookingDish == croissant:
            screen.blit(croissant.image, (croissant.xpos, croissant.ypos))
        elif MainCookingDish == eggs_bacon:
            screen.blit(eggs_bacon.image, (eggs_bacon.xpos, eggs_bacon.ypos))

        for ingredient in ingredients:
            if player.rect.colliderect(ingredient.rect):
                for dish in [MainCookingDish]:
                    if ingredient.name in dish.ingredients:
                        score += 10
                        ingredients.remove(ingredient)
                        ingredients_collected.append(ingredient.name)
                        break
                    else:
                        score -= 10
                        ingredients.remove(ingredient)
                        break

        # Win condition
        if score == 200:
            screen.blit(Victory_image, (-100, -100))
            pygame.display.flip()
            pygame.time.wait(4000)
            pygame.quit()
            sys.exit()

        # Draw ingredients
        for ingredient in ingredients:
            screen.blit(ingredient.image, ingredient.rect)

        # Draw scoreboard
        scoreboard_text = "Score: " + str(score)
        goalscore_text = "Goal: 200"
        goalscore_surface = font.render(goalscore_text, True, WHITE)
        scoreboard_surface = font.render(scoreboard_text, True, WHITE)
        screen.blit(scoreboard_surface, (10, 680))
        screen.blit(goalscore_surface, (10, 720))

        # Check if the player has collected all ingredients for the current dish
        if set(ingredients_collected) == set(MainCookingDish.ingredients):
            reset_game()

        # Draw background and player
        screen.blit(font.render("Chef Alex", True, WHITE), (0, 0))
        screen.blit(font.render("Timer: " + str(math.floor(timer)), True, WHITE), ((screenx - 160), 10))
        player.Draw()

        pygame.display.flip()

# Main menu
main_menu()
# Start the game
game_loop()
