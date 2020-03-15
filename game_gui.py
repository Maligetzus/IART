import pygame
from pygame.locals import *



def init_game_window():
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Neutron")

    # Create The Backgound
    background = pygame.Surface(screen.get_size()) #Creates a Surface with Size = Screen
    background = background.convert()
    background.fill((204, 229, 255))

    #Load Pieces and Board
    red_piece_image = pygame.image.load('resources/red_piece.png')
    blue_piece_image  = pygame.image.load('resources/blue_piece.png')
    game_board_image_5_by_5 = pygame.image.load('resources/board.png')

    # Put Text On The Background, Centered
    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("Neutron", 1, (10, 10, 10))
        textpos = text.get_rect(centery=background.get_height() / 2, centerx=background.get_width() / 2)
        background.blit(text, textpos)

    # Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Prepare Game Objects
    clock = pygame.time.Clock()

    # Main Loop
    going = True
    while going:
        clock.tick(60)

        # Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
            elif event.type == MOUSEBUTTONDOWN:
                print("Mouse button Pressed at: ", pygame.mouse.get_pos())
            elif event.type == KEYDOWN and event.key == K_SPACE:
                print("ESPACOOOOOOOOOOOOOO")
            #elif event.type == MOUSEMOTION:
                #print("Mouse Movement")


        # Draw Everything
        screen.blit(background, (0, 0))
        screen.blit(game_board_image_5_by_5, (25, 25))
        screen.blit(red_piece_image, (50, 50))
        pygame.display.flip()

    pygame.quit()