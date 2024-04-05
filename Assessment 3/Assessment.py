import pygame,sys
clock = pygame.time.Clock()
pygame.display.set_caption(("Game"))
screenx = 1108
screeny = 650
screen = pygame.display.set_mode((screenx, screeny))

while True:
    clock.tick(60)
    screen.fill((0, 150, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    print("Hello")
    pygame.display.flip()
    pygame.display.update()
