import pygame, sys
from juego import *

def main():
    pygame.init()
    
    pantalla = pygame.display.set_mode(tamaño)
    pygame.FULLSCREEN
    pygame.display.set_caption("My Own Virtual Cat")
    ico = pygame.image.load("assets/ico/catIco.ico")
    pygame.display.set_icon(ico)

    done = False
    
    clock = pygame.time.Clock()

    game = Juego()

    while not done:
        done = game.proceso_eventos()
        game.correr_logica()
        game.frame_pantalla(pantalla)
        clock.tick(10)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
