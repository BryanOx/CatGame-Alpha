import pygame, random
from pygame import *

#---    CLASES    ---
class Puertas(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/tiles/puerta.png").convert()
        self.rect = self.image.get_rect()
        self.rect.x = 384
        self.rect.y = 0

class Bebedero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/tiles/bebedero.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x = 732
        self.rect.y = 64

class Comedero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/tiles/comida.png").convert()

        self.rect = self.image.get_rect()
        self.rect.x = 732
        self.rect.y = 192

class CamaGato(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/tiles/cama.png").convert()

        self.rect = self.image.get_rect()
        self.rect.x = 732
        self.rect.y = 384

class Arenero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = {"limpio":[pygame.image.load("assets/tiles/arenero.png").convert(),
                                 pygame.image.load("assets/tiles/arenero.png").convert()],

                       "sucio":[pygame.image.load("assets/tiles/areneroSucio0.png").convert(),
                                pygame.image.load("assets/tiles/areneroSucio1.png").convert(),
                                pygame.image.load("assets/tiles/areneroSucio2.png").convert()]}
        
        self.rect = pygame.Rect(64, 384, 64, 64)
        self.rect.x = 64
        self.rect.y = 384
        self.estado = "limpio"
        self.index = 0
        self.image = self.images.get(self.estado)[self.index]

    def actualizar(self):
        if self.index >= len(self.images.get(self.estado)):
            self.index = 0
        self.image = self.images.get(self.estado)[self.index]
        self.index += 1

class Raton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = [pygame.image.load("assets/personajes/npcs/raton-0.png").convert_alpha(),
                       pygame.image.load("assets/personajes/npcs/raton-0.png").convert_alpha(),
                       pygame.image.load("assets/personajes/npcs/raton-1.png").convert_alpha(),
                       pygame.image.load("assets/personajes/npcs/raton-1.png").convert_alpha(),
                       pygame.image.load("assets/personajes/npcs/raton-2.png").convert_alpha(),
                       pygame.image.load("assets/personajes/npcs/raton-2.png").convert_alpha(),
                       pygame.image.load("assets/personajes/npcs/raton-3.png").convert_alpha(),
                       pygame.image.load("assets/personajes/npcs/raton-3.png").convert_alpha(),
                       pygame.image.load("assets/personajes/npcs/raton-4.png").convert_alpha(),
                       pygame.image.load("assets/personajes/npcs/raton-4.png").convert_alpha(),
                       pygame.image.load("assets/personajes/npcs/raton-5.png").convert_alpha(),
                       pygame.image.load("assets/personajes/npcs/raton-5.png").convert_alpha()]
        
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

    def actualizar(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

    def recolocar(self):
        self.rect.x = random.randrange(64, 860 - 96)
        self.rect.y = random.randrange(64, 480 - 64)
        
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()        
        self.images = {"quietoAbajo":[pygame.image.load("assets/personajes/gato/gato-d0.png").convert_alpha(),
                                      pygame.image.load("assets/personajes/gato/gato-d0.png").convert_alpha()],

                       "quietoArriba":[pygame.image.load("assets/personajes/gato/gato-u0.png").convert_alpha(),
                                       pygame.image.load("assets/personajes/gato/gato-u0.png").convert_alpha()],

                       "quietoDerecha":[pygame.image.load("assets/personajes/gato/gato-r0.png").convert_alpha(),
                                        pygame.image.load("assets/personajes/gato/gato-r0.png").convert_alpha()],

                       "quietoIzquierda":[pygame.image.load("assets/personajes/gato/gato-l0.png").convert_alpha(),
                                          pygame.image.load("assets/personajes/gato/gato-l0.png").convert_alpha()],
                       
                       "caminaAbajo":[pygame.image.load("assets/personajes/gato/gato-d0.png").convert_alpha(),
                                      pygame.image.load("assets/personajes/gato/gato-d1.png").convert_alpha(),
                                      pygame.image.load("assets/personajes/gato/gato-d2.png").convert_alpha(),
                                      pygame.image.load("assets/personajes/gato/gato-d3.png").convert_alpha()],

                       "caminaArriba":[pygame.image.load("assets/personajes/gato/gato-u0.png").convert_alpha(),
                                       pygame.image.load("assets/personajes/gato/gato-u1.png").convert_alpha(),
                                       pygame.image.load("assets/personajes/gato/gato-u2.png").convert_alpha(),
                                       pygame.image.load("assets/personajes/gato/gato-u3.png").convert_alpha()],

                       "caminaDerecha":[pygame.image.load("assets/personajes/gato/gato-r0.png").convert_alpha(),
                                        pygame.image.load("assets/personajes/gato/gato-r1.png").convert_alpha(),
                                        pygame.image.load("assets/personajes/gato/gato-r2.png").convert_alpha(),
                                        pygame.image.load("assets/personajes/gato/gato-r3.png").convert_alpha()],

                       "caminaIzquierda":[pygame.image.load("assets/personajes/gato/gato-l0.png").convert_alpha(),
                                          pygame.image.load("assets/personajes/gato/gato-l1.png").convert_alpha(),
                                          pygame.image.load("assets/personajes/gato/gato-l2.png").convert_alpha(),
                                          pygame.image.load("assets/personajes/gato/gato-l3.png").convert_alpha()],
                       
                       "durmiendo":[pygame.image.load("assets/personajes/gato/gato-durmiendo0.png").convert_alpha(),
                                    pygame.image.load("assets/personajes/gato/gato-durmiendo1.png").convert_alpha(),
                                    pygame.image.load("assets/personajes/gato/gato-durmiendo2.png").convert_alpha(),
                                    pygame.image.load("assets/personajes/gato/gato-durmiendo3.png").convert_alpha()],

                       "cagando":[pygame.image.load("assets/personajes/gato/gato-cagando0.png").convert_alpha(),
                                  pygame.image.load("assets/personajes/gato/gato-cagando1.png").convert_alpha(),
                                  pygame.image.load("assets/personajes/gato/gato-cagando2.png").convert_alpha(),
                                  pygame.image.load("assets/personajes/gato/gato-cagando3.png").convert_alpha(),
                                  pygame.image.load("assets/personajes/gato/gato-cagando4.png").convert_alpha(),
                                  pygame.image.load("assets/personajes/gato/gato-cagando5.png").convert_alpha(),
                                  pygame.image.load("assets/personajes/gato/gato-cagando6.png").convert_alpha(),
                                  pygame.image.load("assets/personajes/gato/gato-cagando7.png").convert_alpha(),
                                  pygame.image.load("assets/personajes/gato/gato-cagando8.png").convert_alpha(),
                                  pygame.image.load("assets/personajes/gato/gato-cagando9.png").convert_alpha(),
                                  pygame.image.load("assets/personajes/gato/gato-cagando10.png").convert_alpha(),
                                  pygame.image.load("assets/personajes/gato/gato-cagando11.png").convert_alpha(),
                                  pygame.image.load("assets/personajes/gato/gato-cagando12.png").convert_alpha(),
                                  pygame.image.load("assets/personajes/gato/gato-cagando13.png").convert_alpha()]}
        
        self.nombre = "Sr Gato"
        self.estado = "quietoAbajo"
        self.index = 0
        self.vel = 6
        self.rect = pygame.Rect(0, 0, 64, 64)
        self.rect.x = 430
        self.rect.y = 240
        self.posX = self.rect.x
        self.posY = self.rect.y

        self.nivel = 1

        self.vida = 100
        self.hambre = 100
        self.sed = 100
        self.energia = 100
        self.intestinos = 0
        self.dinero = 0
        self.cansado = False
        self.limpiando = False

        self.cuentaPasos = 0

    def actualizar(self):
        if self.index >= len(self.images.get(self.estado)):
            self.index = 0
            if self.estado == "cagando":
                self.estado = "quietoArriba"
            if self.estado == "caminaAbajo" and self.limpiando:
                self.estado = "quietoAbajo"
                self.limpiando = False
        self.image = self.images.get(self.estado)[self.index]
        self.index += 1

    def movimiento(self):
        self.teclas = pygame.key.get_pressed()
        
        if self.teclas[pygame.K_d] and self.rect.x <= 860 - 128:
            self.rect.x += self.vel
            self.estado = "caminaDerecha"
            self.cuentaPasos += 1

        elif self.teclas[pygame.K_a] and self.rect.x > 64:
            self.rect.x -= self.vel
            self.estado = "caminaIzquierda"
            self.cuentaPasos += 1

        elif self.teclas[pygame.K_w] and self.rect.y > 64:
            self.rect.y -= self.vel
            self.estado = "caminaArriba"
            self.cuentaPasos += 1

        elif self.teclas[pygame.K_s] and self.rect.y < 480 - 90:
            self.rect.y += self.vel
            self.estado = "caminaAbajo"
            self.cuentaPasos += 1

        if self.teclas[pygame.K_LSHIFT]:
            self.vel = 15

        else:
            self.vel = 6