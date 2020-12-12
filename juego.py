from clases import *
import pygame
from pygame.locals import *
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pytmx.util_pygame import load_pygame
from tkinter import Tk
from tkinter import messagebox

############################################################################################################

#---    VARIABLES     ---
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (52, 110, 158)
GRISOSC = (20, 20, 20)
MARRON = (158, 72, 41)
COLORKEY = (255, 0, 200)
DORADO = (230, 170, 0)

ancho = 860
alto = 480
tamaño = (ancho, alto)

Base = declarative_base()

############################################################################################################

class JugadorDB(Base):
    __tablename__="jugador"

    nombre = Column(String, primary_key=True)
    estado = Column(String)
    posX = Column(Integer)
    posY = Column(Integer)
    nivel = Column(Integer)
    vida = Column(Integer)
    hambre = Column(Integer)
    sed = Column(Integer)
    energia = Column(Integer)
    intestinos = Column(Integer)
    dinero = Column(Integer)
    lugar = Column(String)

class Juego(object):
    """
    CLASE 'JUEGO', ESTA CLASE ES EL JUEGO EN SI, SUS INSTRUCCIONES,
    COMO FUNCIONA EL JUEGO Y LAS COSAS EN ESTE
    """
    def __init__(self):
        """
        FUNCION CONSTRUCTORA DEL JUEGO, CREA LOS OBJETOS
        Y ESTADOS NECESARIOS PARA QUE EL JUEGO FUNCIONE
        """
        root = Tk()
        root.wm_withdraw() #to hide the main window
        self.lugar = "habitacion"

        self.cuarto = load_pygame("assets/mapas/Cuarto.tmx")
        self.world_offset = [0,0]

        self.seleccion = 1
        
        self.gameOver = False
        
        self.menuPausa = False
        
        self.menuAyuda = False

        self.menuLoc = False

        self.salirJuego = False
        
        self.score = 0
        self.fuente = pygame.font.Font(None, 24)
        self.fuenteGrande = pygame.font.Font(None, 40)
        
        self.lista_raton = pygame.sprite.Group()
        self.lista_sprites = pygame.sprite.Group()
        self.lista_utilidades = pygame.sprite.Group()
        self.lista_bebedero = pygame.sprite.Group()
        self.lista_puerta = pygame.sprite.Group()
        self.lista_comedero = pygame.sprite.Group()
        self.lista_cama = pygame.sprite.Group()
        self.lista_arenero = pygame.sprite.Group()
        self.listJugador = pygame.sprite.Group()

        self.meow = pygame.mixer.Sound("assets/sonidos/meow.ogg")
        self.ronroneo = pygame.mixer.Sound("assets/sonidos/ronroneo.ogg")
        self.squeak = pygame.mixer.Sound("assets/sonidos/squeak.ogg")
        self.abrirPuertas = pygame.mixer.Sound("assets/sonidos/puerta.ogg")
        self.beberAgua = pygame.mixer.Sound("assets/sonidos/beber_agua.ogg")
        self.comiendo = pygame.mixer.Sound("assets/sonidos/comiendo.ogg")
        self.durmiendo = pygame.mixer.Sound("assets/sonidos/durmiendo.ogg")
        self.cagando = pygame.mixer.Sound("assets/sonidos/pedos.ogg")
        
        self.bebedero = Bebedero()
        self.lista_bebedero.add(self.bebedero)
        self.lista_utilidades.add(self.bebedero)
        
        self.comedero = Comedero()
        self.lista_comedero.add(self.comedero)
        self.lista_utilidades.add(self.comedero)

        self.camaGato = CamaGato()
        self.lista_cama.add(self.camaGato)
        self.lista_utilidades.add(self.camaGato)

        self.arenero = Arenero()
        self.lista_arenero.add(self.arenero)
        self.lista_utilidades.add(self.arenero)

        self.puerta = Puertas()
        self.lista_puerta.add(self.puerta)
        self.lista_sprites.add(self.puerta)

        self.gato = Jugador()
        self.listJugador.add(self.gato)
        self.lista_sprites.add(self.gato)

        self.raton = Raton()

        #---- DB ----
        engine = create_engine("sqlite:///assets/Partida/SaveGame.db")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

############################################################################################################

    def proceso_eventos(self):
        """
        FUNCION PARA PROCESAR LOS EVENTOS DEL TECLADO/MOUSE/JOYSTICK
        Y CUMPLIR FUNCIONES DETERMINADAS PARA LAS TECLAS
        """
        if self.salirJuego:
            salir = messagebox.askquestion('Salir del juego.','¿Seguro que quieres salir del juego?\nAsegurate de haber guardado la partida antes para no perder progreso.')
            if salir == 'yes':
                return True
            else:
                self.salirJuego = False

        if self.menuLoc:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return True
                if event.type == KEYDOWN:
                    if event.key == (pygame.K_w or pygame.K_UP):
                        self.seleccion -= 1
                    if event.key == (pygame.K_s or pygame.K_DOWN):
                        self.seleccion += 1
                    if event.key == pygame.K_SPACE and self.seleccion == 2:
                        self.lugar = "despensa"
                        self.menuLoc = False
                    if event.key == pygame.K_SPACE and self.seleccion == 1:
                        self.lugar = "habitacion"
                        self.menuLoc = False
                    if event.key == pygame.K_ESCAPE:
                        self.menuLoc = False
        if self.menuAyuda:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return True
                if event.type == KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.menuAyuda = False
                if event.type == MOUSEBUTTONDOWN:
                    self.menuAyuda = False
                    
        if self.gameOver:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return True
                if event.type == KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return True
                if event.type == MOUSEBUTTONDOWN:
                    self.__init__()

        if self.menuPausa:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return True
                if event.type == KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.salirJuego = True
                    if event.key == pygame.K_h:
                        self.menuPausa = False
                        self.menuAyuda = True
                    if event.key == pygame.K_s:
                        self.guardar_partida()
                    if event.key == pygame.K_l:
                        self.cargar_partida()
                if event.type == MOUSEBUTTONDOWN:
                    self.menuPausa = False
        else:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return True
                
                if event.type == KEYUP:
                    if event.key == pygame.K_a and self.gato.estado != "quietoIzquierda":
                        self.gato.estado = "quietoIzquierda"
                    if event.key == pygame.K_d and self.gato.estado != "quietoDerecha":
                        self.gato.estado = "quietoDerecha"
                    if event.key == pygame.K_w and self.gato.estado != "quietoArriba":
                        self.gato.estado = "quietoArriba"
                    if event.key == pygame.K_s and self.gato.estado != "quietoAbajo":
                        self.gato.estado = "quietoAbajo"
                            
                if event.type == KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.menuPausa = True
                    if event.key == pygame.K_SPACE:
                        if pygame.sprite.spritecollide(self.gato, self.lista_bebedero, False) and pygame.sprite.spritecollide(self.gato, self.lista_utilidades, False):
                            self.beberAgua.play()
                            self.gato.sed += 50
                        elif pygame.sprite.spritecollide(self.gato, self.lista_comedero, False) and pygame.sprite.spritecollide(self.gato, self.lista_utilidades, False):
                            self.comiendo.play()
                            self.gato.hambre += 50
                        elif pygame.sprite.spritecollide(self.gato, self.lista_puerta, False):
                            self.abrirPuertas.play()
                            self.menuLoc = True
                        elif pygame.sprite.spritecollide(self.gato, self.lista_cama, False) and pygame.sprite.spritecollide(self.gato, self.lista_utilidades, False):
                            if self.gato.energia < 100:
                                self.durmiendo.play()
                                self.gato.estado = "durmiendo"
                                self.gato.rect.x = 732
                                self.gato.rect.y = 370
                        elif (pygame.sprite.spritecollide(self.gato, self.lista_arenero, False) and self.arenero.estado == "limpio") and pygame.sprite.spritecollide(self.gato, self.lista_utilidades, False):
                            self.gato.estado = "cagando"
                            self.gato.rect.x = 64
                            self.gato.rect.y = 360
                            self.cagando.play()
                        elif pygame.sprite.spritecollide(self.gato, self.lista_arenero, False) and self.arenero.estado == "sucio":
                            self.gato.rect.x = 64
                            self.gato.rect.y = 360
                            self.gato.estado = "caminaAbajo"
                            self.gato.limpiando = True
                            self.arenero.estado = "limpio"
                        else:
                            self.meow.play()
                            
        return False

############################################################################################################

    def spawnRaton(self):
        """
        FUNCION PARA SPAWNEAR UN RATON
        """
        self.lista_raton.add(self.raton)
        self.raton.recolocar()

############################################################################################################

    def guardar_partida(self):
        if (self.session.query(JugadorDB).get(self.gato.nombre)==None):
            jugador = JugadorDB(
                nombre = self.gato.nombre,
                estado = self.gato.estado,
                posX = self.gato.posX,
                posY = self.gato.posY,
                nivel = self.gato.nivel,
                vida = self.gato.vida,
                hambre = self.gato.hambre,
                sed = self.gato.sed,
                energia = self.gato.energia,
                intestinos = self.gato.intestinos,
                dinero = self.gato.dinero,
                lugar = self.lugar
            )
            self.session.add(jugador)
            self.session.commit()
        else:
            SaveG = self.session.query(JugadorDB).get(self.gato.nombre)
            SaveG.estado = self.gato.estado
            SaveG.posX = self.gato.rect.x
            SaveG.posY = self.gato.rect.y
            SaveG.nivel = self.gato.nivel
            SaveG.vida = self.gato.vida
            SaveG.hambre = self.gato.hambre
            SaveG.sed = self.gato.sed
            SaveG.energia = self.gato.energia
            SaveG.intestinos = self.gato.intestinos
            SaveG.dinero = self.gato.dinero
            SaveG.lugar = self.lugar
            self.session.commit()
        messagebox.showinfo('Guardar partida.','La partida ha sido guardada con exito.')

############################################################################################################

    def cargar_partida(self):
        SaveG = self.session.query(JugadorDB).get(self.gato.nombre)
        self.gato.estado = SaveG.estado
        self.gato.rect.x = SaveG.posX
        self.gato.rect.y = SaveG.posY
        self.gato.nivel = SaveG.nivel
        self.gato.vida = SaveG.vida
        self.gato.hambre = SaveG.hambre
        self.gato.sed = SaveG.sed
        self.gato.energia = SaveG.energia
        self.gato.intestinos = SaveG.intestinos
        self.gato.dinero = SaveG.dinero
        self.lugar = SaveG.lugar
        self.session.commit()
        self.menuPausa = False
        messagebox.showinfo('Cargar partida.','La partida ha sido cargada con exito.')

############################################################################################################

    def correr_logica(self):
        """
        FUNCION DONDE CORRE TODA LA PARTE LOGICA
        DEL JUEGO EN SI MISMO
        """
        if self.menuLoc:
            #-----------------------
            #   selecion de menu
            if self.seleccion > 2:
                self.seleccion = 1
            if self.seleccion < 1:
                self.seleccion = 2

            #----------------------
                
        if self.gameOver:
            pass
        
        if self.menuPausa:
            pass
        
        else:
            self.gato.actualizar()
            self.gato.movimiento()

            #-------------------------------------------
            #       despensa para atrapar ratones
            if self.lugar == "despensa":
                if len(self.lista_utilidades) > 0:
                    for i in self.lista_utilidades:
                        self.lista_utilidades.remove(i)
                
                if len(self.lista_raton) < 1:
                    self.spawnRaton()
                self.raton.actualizar()
                
                self.raton_golpe_lista = pygame.sprite.spritecollide(self.gato, self.lista_raton, True)

                if len(self.raton_golpe_lista) == 1:
                    self.ronroneo.play()
                    self.score += 1
                    self.raton_golpe_lista.pop
                    self.squeak.play()
                    self.raton.recolocar()
                    self.lista_raton.add(self.raton)
                    self.gato.hambre += 5
            #-------------------------------------------
            
            #-------------------------------------------
            #       habitacion
            if self.lugar == "habitacion":
                try:
                    self.lista_utilidades.add(self.bebedero)
                    self.lista_utilidades.add(self.comedero)
                    self.lista_utilidades.add(self.camaGato)
                    self.lista_utilidades.add(self.arenero)
                    if len(self.lista_raton) > 0:
                        self.lista_raton.pop

                except:
                    pass
            
            #-------------------------------------------
                
            self.arenero.actualizar()
                
            if self.gato.cuentaPasos > 80:
                self.gato.cuentaPasos = 0
                self.gato.hambre -= 5
                self.gato.sed -= 5
                self.gato.energia -= 10

            if self.gato.hambre > 100:
                self.gato.hambre = 100

            if self.gato.sed > 100:
                self.gato.sed = 100

            if self.gato.vida > 100:
                self.gato.vida = 100

            if self.gato.energia == 100 and self.gato.estado == "durmiendo":
                self.gato.estado = "quietoIzquierda"

            if self.score == 10:
                self.gato.dinero += 1
                self.score = 0

            if self.gato.hambre <= 0 and self.gato.sed <= 0:
                self.gato.vida -= 1

            if self.gato.vida == 0:
                self.gameOver = True

            if self.gato.hambre < 0:
                self.gato.hambre = 0

            if self.gato.sed < 0:
                self.gato.sed = 0

            if self.gato.energia <= 20:
                self.gato.cansado = True

            else:
                self.gato.cansado = False

            if self.gato.cansado:
                self.gato.vel = 3

            if self.gato.estado == "durmiendo":
                self.gato.energia += 1

            if self.gato.index == 14 and self.gato.estado == "cagando":
                self.arenero.estado = "sucio"

############################################################################################################

    def frame_pantalla(self, pantalla):
        """
        FUNCION PARA ACTUALIZAR Y DIBUJAR LA PANTALLA
        SEGUN EL DIFERENTE ESTADO DEL JUEGO Y OBJETOS
        """
        cuarto = pygame.image.load("assets/tiles/cuarto.png").convert()
        pantalla.blit(cuarto, (0, 0))
        
        if self.lugar == "habitacion":
            self.lista_utilidades.draw(pantalla)
            self.lista_bebedero.draw(pantalla)
            self.lista_comedero.draw(pantalla)
            self.lista_cama.draw(pantalla)
            self.lista_arenero.draw(pantalla)
            
        self.lista_sprites.draw(pantalla)

        if self.lugar == "despensa":
            self.lista_raton.draw(pantalla)
            
            self.scoreIco = pygame.image.load("assets/ico/score.png").convert_alpha()
            pantalla.blit(self.scoreIco, (810, 40))

            m_score = self.fuente.render(str(self.score), True, BLANCO)
            m_score_rect = m_score.get_rect(center = (840, 50))
            pantalla.blit(m_score, m_score_rect)

        self.monedaIco = pygame.image.load("assets/ico/moneda.png").convert_alpha()
        pantalla.blit(self.monedaIco, (810, 10))

        m_dinero = self.fuente.render(str(self.gato.dinero), True, BLANCO)
        m_dinero_rect = m_dinero.get_rect(center = (840, 20))
        pantalla.blit(m_dinero, m_dinero_rect)

        contenedorVida = pygame.draw.rect(pantalla, GRISOSC, (13, 13, 106, 10))
        barraVida = pygame.draw.rect(pantalla, ROJO, (16, 16, self.gato.vida, 4))

        contenedorHambre = pygame.draw.rect(pantalla, GRISOSC, (13, 33, 106, 10))
        barraHambre = pygame.draw.rect(pantalla, MARRON, (16, 36, self.gato.hambre, 4))

        contenedorSed = pygame.draw.rect(pantalla, GRISOSC, (13, 53, 106, 10))
        barraSed = pygame.draw.rect(pantalla, AZUL, (16, 56, self.gato.sed, 4))

        contenedorEnergia = pygame.draw.rect(pantalla, GRISOSC, (13, 73, 106, 10))
        barraEnergia = pygame.draw.rect(pantalla, DORADO, (16, 76, self.gato.energia, 4))

        #-----------------------------------------------------------

        if self.menuLoc:
            pantalla.fill(NEGRO)
            
            l1 = self.fuenteGrande.render("habitacion", True, BLANCO)
            l1_rect = l1.get_rect(center = (int(ancho // 2), int(alto // 2.7)))
            pantalla.blit(l1, l1_rect)

            l2 = self.fuenteGrande.render("despensa", True, BLANCO)
            l2_rect = l2.get_rect(center = (int(ancho // 2), int(alto // 1.3)))
            pantalla.blit(l2, l2_rect)
            if self.seleccion == 1:
                sel = pygame.draw.rect(pantalla, DORADO, (l1_rect.x - 30, l1_rect.y - 15, 200, 50), 3)
                self.lugar = "habitacion"
                
            elif self.seleccion == 2:
                sel = pygame.draw.rect(pantalla, DORADO, (l2_rect.x - 30, l2_rect.y - 12, 200, 50), 3)
                
        if self.gameOver:
            gameOver = pygame.image.load("assets/imagenes/gameOver.png").convert()
            pantalla.blit(gameOver, (0, 0))
        
        if self.menuPausa:
            menu_pausa = pygame.image.load("assets/imagenes/pausa.png").convert_alpha()
            pantalla.blit(menu_pausa, (0, 0))
            
        if self.menuAyuda:
            menu_ayuda = pygame.image.load("assets/imagenes/menuAyuda.png").convert()
            pantalla.blit(menu_ayuda, (0, 0))

        pygame.display.flip()