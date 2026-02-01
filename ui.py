import pygame
from typing import List, Optional

class Menu:
    def __init__(self, opciones: List[str]):
        pygame.init()
        self.pantalla = pygame.display.set_mode((600, 400))
        self.fuente = pygame.font.SysFont('Arial', 28)
        self.opciones = opciones
        self.seleccion = 0
    
    def loop(self) -> Optional[str]:
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.seleccion = (self.seleccion - 1) % len(self.opciones)
                    if event.key == pygame.K_DOWN:
                        self.seleccion = (self.seleccion + 1) % len(self.opciones)
                    if event.key == pygame.K_RETURN:
                        return self.opciones[self.seleccion]
            self.pantalla.fill((30, 30, 30))
            for idx, texto in enumerate(self.opciones):
                color = (255, 255, 255) if idx == self.seleccion else (180, 180, 180)
                superficie = self.fuente.render(texto, True, color)
                self.pantalla.blit(superficie, (60, 60 + idx * 50))
            pygame.display.flip()
            clock.tick(60)
