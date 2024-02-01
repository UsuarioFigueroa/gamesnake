import pygame
import sys
import random
import time

pygame.init()

# Configuración de la pantalla
ANCHO, ALTO = 600, 400
TAMANO_CELDA = 20
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de la Serpiente")

# Colores
COLOR_FONDO = (30, 30, 30)
COLOR_TITULO = (255, 255, 255)
COLOR_SERPIENTE = (0, 255, 0)
COLOR_COMIDA = (255, 0, 0)

# Direcciones
ARRIBA = (0, -1)
ABAJO = (0, 1)
IZQUIERDA = (-1, 0)
DERECHA = (1, 0)

# Clase para la serpiente
class Serpiente:
    def __init__(self):
        self.cuerpo = [(100, 100), (90, 100), (80, 100)]
        self.direccion = DERECHA
        self.crecimiento_pendiente = 0

    def mover(self):
        cabeza = self.cuerpo[0]
        nueva_cabeza = (cabeza[0] + self.direccion[0] * TAMANO_CELDA, cabeza[1] + self.direccion[1] * TAMANO_CELDA)
        self.cuerpo.insert(0, nueva_cabeza)

        if self.crecimiento_pendiente == 0:
            self.cuerpo.pop()
        else:
            self.crecimiento_pendiente -= 1

    def crecer(self):
        self.crecimiento_pendiente += 1

    def verificar_colision(self):
        cabeza = self.cuerpo[0]
        if cabeza[0] < 0 or cabeza[0] >= ANCHO or cabeza[1] < 0 or cabeza[1] >= ALTO:
            return True
        if cabeza in self.cuerpo[1:]:
            return True
        return False

    def actualizar(self):
        self.mover()
        if self.verificar_colision():
            return True

# Clase para la comida
class Comida:
    def __init__(self):
        self.posicion = (0, 0)
        self.puntos = 100  # Puntos por cada comida
        self.generar_comida()

    def generar_comida(self):
        self.posicion = (random.randint(0, (ANCHO - TAMANO_CELDA) // TAMANO_CELDA) * TAMANO_CELDA,
                         random.randint(0, (ALTO - TAMANO_CELDA) // TAMANO_CELDA) * TAMANO_CELDA)

    def dibujar(self):
        pygame.draw.rect(pantalla, COLOR_COMIDA, (self.posicion[0], self.posicion[1], TAMANO_CELDA, TAMANO_CELDA))

# Función para mostrar el mensaje
def mostrar_mensaje(mensaje, tamano_fuente=36, duracion=2):
    fuente = pygame.font.Font(None, tamano_fuente)
    texto = fuente.render(mensaje, True, COLOR_TITULO)
    rectangulo_texto = texto.get_rect(center=(ANCHO // 2, ALTO // 2 - tamano_fuente // 2))
    pantalla.blit(texto, rectangulo_texto)
    pygame.display.flip()
    time.sleep(duracion)

# Función para mostrar las instrucciones
def mostrar_instrucciones():
    instrucciones = [
        "Instrucciones:",
        "- Usa las teclas de flecha para mover la serpiente.",
        "- Come la comida roja para crecer y obtener puntos.",
        "- Evita chocar contra las paredes y contra vos mismo.",
        "- Presiona 'ESC' para regresar al menú en cualquier momento.",
        "",
        "¡Buena suerte!",
    ]

    pantalla.fill(COLOR_FONDO)
    fuente = pygame.font.Font(None, 25)

    for i, linea in enumerate(instrucciones):
        texto_linea = fuente.render(linea, True, COLOR_TITULO)
        pantalla.blit(texto_linea, (20, 20 + i * 30))

    pygame.display.flip()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return

# Función para mostrar el menú
def mostrar_menu():
    opciones = ["Jugar", "Instrucciones", "Salir"]
    opcion_seleccionada = 0

    while True:
        pantalla.fill(COLOR_FONDO)
        fuente = pygame.font.Font(None, 36)

        for i, opcion in enumerate(opciones):
            color = COLOR_TITULO if i == opcion_seleccionada else (150, 150, 150)
            texto_opcion = fuente.render(opcion, True, color)
            pantalla.blit(texto_opcion, (ANCHO // 2 - texto_opcion.get_width() // 2, ALTO // 2 - 30 + i * 40))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    opcion_seleccionada = (opcion_seleccionada + 1) % len(opciones)
                elif evento.key == pygame.K_UP:
                    opcion_seleccionada = (opcion_seleccionada - 1) % len(opciones)
                elif evento.key == pygame.K_RETURN:
                    return opcion_seleccionada + 1  # Devuelve la opción seleccionada

# Función principal del juego
def main():
    mostrar_mensaje("SNAKE GAME", 72, 1)  # Título más grande con efecto
    time.sleep(0.5)  # Pequeña pausa antes de mostrar el menú

    while True:
        opcion = mostrar_menu()

        if opcion == 1:  # Jugar
            break
        elif opcion == 2:  # Instrucciones
            mostrar_instrucciones()
        elif opcion == 3:  # Salir
            pygame.quit()
            sys.exit()

    serpiente = Serpiente()
    comida = Comida()
    puntuacion = 0  # Puntuación inicial

    reloj = pygame.time.Clock()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return  # Regresar al menú

                if evento.key == pygame.K_UP and serpiente.direccion != ABAJO:
                    serpiente.direccion = ARRIBA
                elif evento.key == pygame.K_DOWN and serpiente.direccion != ARRIBA:
                    serpiente.direccion = ABAJO
                elif evento.key == pygame.K_LEFT and serpiente.direccion != DERECHA:
                    serpiente.direccion = IZQUIERDA
                elif evento.key == pygame.K_RIGHT and serpiente.direccion != IZQUIERDA:
                    serpiente.direccion = DERECHA

        juego_terminado = serpiente.actualizar()

        if juego_terminado:
            # Hacer una pausa antes de mostrar la puntuación
            time.sleep(1.5)

            pantalla.fill(COLOR_FONDO)  # Limpiar la pantalla antes de mostrar el mensaje de puntuación
            mostrar_mensaje("GAME OVER", 62, 1)
            mostrar_mensaje("", 24, 0.5)  # Espacio en blanco para separar los mensajes

            # Hacer una pausa adicional antes de mostrar la puntuación
            time.sleep(0.5)

            pantalla.fill(COLOR_FONDO)  # Limpiar la pantalla antes de mostrar el mensaje de puntuación
            texto_puntuacion = f"PUNTUACIÓN: {puntuacion}"
            mostrar_mensaje(texto_puntuacion, 36, 1.5)  # Se ha aumentado el tiempo de visualización de la puntuación
            pygame.quit()
            sys.exit()

        if serpiente.cuerpo[0] == comida.posicion:
            serpiente.crecer()
            comida.generar_comida()
            puntuacion += comida.puntos  # Añadir puntos por cada comida

        # Dibujar en la pantalla
        pantalla.fill(COLOR_FONDO)
        for segmento in serpiente.cuerpo:
            pygame.draw.rect(pantalla, COLOR_SERPIENTE, (segmento[0], segmento[1], TAMANO_CELDA, TAMANO_CELDA))
        comida.dibujar()

        pygame.display.flip()

        reloj.tick(10)  # Puedes ajustar la velocidad del juego aquí

# Iniciar el juego
main()
