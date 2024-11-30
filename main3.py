import pygame
import constantes
from personaje import Personaje
from weapon import Weapon
from textos import DamageText
from items import Item
from mundo import Mundo
import os
import csv

#funciones:
#escalar imagen
def escalar_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    nueva_imagen = pygame.transform.scale(image, (w*scale, h*scale))
    return nueva_imagen

#funcion para contar elementos
def contar_elementos(directorio):
    return len(os.listdir(directorio))

#funcion listar nombres elementos
def nombres_carpetas(directorio):
    return os.listdir(directorio)

pygame.init()
pygame.mixer.init()

ventana = pygame.display.set_mode((constantes.ANCHO_VENTANA,
                                   constantes.ALTO_VENTANA))
pygame.display.set_caption("Mi primer juego")

#variables
posicion_pantalla = [0, 0]
nivel = 1

#fuentes
font = pygame.font.Font("assets/fonts/mago3.ttf", 25)
font_game_over = pygame.font.Font("assets/fonts/mago3.ttf", 100)
font_reinicio = pygame.font.Font("assets/fonts/mago3.ttf", 30)
font_inicio = pygame.font.Font("assets/fonts/mago3.ttf", 30)
font_titulo = pygame.font.Font("assets/fonts/mago3.ttf", 75)


# Ejemplo de árbol de decisiones para diálogos
dialogos = {
    "inicio": {
        "pregunta": "¿Qué deseas hacer?",
        "opciones": {
            "explorar": "Explora el mundo a tu alrededor.",
            "hablar": {
                "pregunta": "¿Con quién deseas hablar?",
                "opciones": {
                    "NPC1": "El NPC1 te habla sobre la historia local.",
                    "NPC2": "El NPC2 te da una pista para tu misión."
                }
            }
        }
    }
}



game_over_text = font_game_over.render('Game Over',
                                       True, constantes.BLANCO)
texto_boton_reinicio = font_reinicio.render("Reiniciar",
                                            True, constantes.NEGRO)

# Botones de inicio
boton_jugar = pygame.Rect(constantes.ANCHO_VENTANA / 2 - 100,
                          constantes.ALTO_VENTANA / 2 - 50, 200, 50)
boton_salir = pygame.Rect(constantes.ANCHO_VENTANA / 2 - 100,
                          constantes.ALTO_VENTANA / 2 + 50, 200, 50)
texto_boton_jugar = font_inicio.render("Jugar", True,
                                constantes.NEGRO)
texto_boton_salir = font_inicio.render("Salir", True,
                                constantes.BLANCO)

# Pantalla de inicio
def pantalla_inicio():
    ventana.fill(constantes.MORADO)
    dibujar_texto("Mi primer juego", font_titulo, constantes.BLANCO,
                  constantes.ANCHO_VENTANA / 2 - 200,
                  constantes.ALTO_VENTANA / 2 - 200)
    pygame.draw.rect(ventana, constantes.AMARILLO, boton_jugar)
    pygame.draw.rect(ventana, constantes.ROJO, boton_salir)
    ventana.blit(texto_boton_jugar, (boton_jugar.x + 50, boton_jugar.y + 10))
    ventana.blit(texto_boton_salir, (boton_salir.x + 50, boton_salir.y + 10))
    pygame.display.update()

#Importar imagenes
#Energia
corazon_vacio = pygame.image.load("assets//images//items//heart_empty.png").convert_alpha()
corazon_vacio = escalar_img(corazon_vacio, constantes.SCALA_CORAZON)
corazon_mitad = pygame.image.load(f"assets//images//items//heart_half.png").convert_alpha()
corazon_mitad = escalar_img(corazon_mitad, constantes.SCALA_CORAZON)
corazon_lleno = pygame.image.load(f"assets//images//items//heart_full.png").convert_alpha()
corazon_lleno = escalar_img(corazon_lleno, constantes.SCALA_CORAZON)


#Personaje
animaciones = []
for i in range (7):
    img = pygame.image.load(f"assets//images//characters//player//Player_{i}.png").convert_alpha()
    img = escalar_img(img, constantes.SCALA_PERSONAJE)
    animaciones.append(img)

#enemigos
directorio_enemigos = "assets//images//characters//enemies"
tipo_enemigos =nombres_carpetas(directorio_enemigos)
animaciones_enemigos = []
for eni in tipo_enemigos:
    lista_temp = []
    ruta_temp = f"assets//images//characters//enemies//{eni}"
    num_animaciones = contar_elementos(ruta_temp)
    for i in range(num_animaciones):
        img_enemigo = pygame.image.load(f"{ruta_temp}//{eni}_{i + 1}.png").convert_alpha()
        img_enemigo = escalar_img(img_enemigo, constantes.SCALA_ENEMIGOS)
        lista_temp.append(img_enemigo)
    animaciones_enemigos.append(lista_temp)


#Arma
imagen_pistola = pygame.image.load(f"assets//images//weapons//gun.png").convert_alpha()
imagen_pistola = escalar_img(imagen_pistola, constantes.SCALA_ARMA)

#Balas
imagen_balas = pygame.image.load(f"assets//images//weapons//bullet.png").convert_alpha()
imagen_balas = escalar_img(imagen_balas, constantes.SCALA_ARMA)

#cargar imagenes del mundo
tile_list  = []
for x in range(constantes.TILE_TYPES):
    tile_image = pygame.image.load(f"assets//images//tiles//tile ({x+1}).png")
    tile_image = pygame.transform.scale(tile_image, (constantes.TILE_SIZE, constantes.TILE_SIZE))
    tile_list.append(tile_image)

#cargar imagenes de los items
posion_roja = pygame.image.load("assets//images//items//potion.png")
posion_roja = escalar_img(posion_roja, 0.05)

coin_images = []
ruta_img = "assets//images//items//coin"
num_coin_images = contar_elementos(ruta_img)
for i in range(num_coin_images):
    img = pygame.image.load(f"assets//images//items//coin//coin_{i+1}.png")
    img = escalar_img(img, 1)
    coin_images.append(img)

item_imagenes = [coin_images, [posion_roja]]

def dibujar_texto(texto, fuente, color, x, y):
    img = fuente.render(texto, True, color)
    ventana.blit(img, (x,y))

def vida_jugador():
    c_mitad_dibujado = False
    for i in range(5):
        if jugador.energia >= ((i+1)*20):
            ventana.blit(corazon_lleno, (5+i*50, 5))
        elif jugador.energia % 20 > 0 and c_mitad_dibujado == False:
            ventana.blit(corazon_mitad, (5+i*50, 5))
            c_mitad_dibujado = True
        else:
            ventana.blit(corazon_vacio, (5 + i * 50, 5))

def resetear_mundo():
    grupo_damage_text.empty()
    grupo_balas.empty()
    grupo_items.empty()

    # crear lista de tile vacias
    data = []
    for fila in range(constantes.FILAS):
        filas = [2] * constantes.COLUMNAS
        data.append(filas)

    return data

world_data = []


for fila in range(constantes.FILAS):
    filas = [5] * constantes.COLUMNAS
    world_data.append(filas)

# cargar el archivo con el nivel
with open("niveles/nivel_1.csv", newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, fila in enumerate(reader):
        for y, columna in enumerate(fila):
            world_data[x][y] = int(columna)
world = Mundo()
world.process_data(world_data, tile_list, item_imagenes, animaciones_enemigos)

def dibujar_grid():
    for x in range(30):
        pygame.draw.line(ventana, constantes.BLANCO, (x*constantes.TILE_SIZE, 0), (x*constantes.TILE_SIZE, constantes.ALTO_VENTANA))
        pygame.draw.line(ventana, constantes.BLANCO, (0, x * constantes.TILE_SIZE), (constantes.ANCHO_VENTANA, x* constantes.TILE_SIZE))


#crear un jugador de la clase personaje
jugador = Personaje(50,50, animaciones, 20, 1)


#crear lista de enemigos
lista_enemigos = []
for ene in world.lista_enemigo:
    lista_enemigos.append(ene)



#crear un arma de la clase weapon
pistola = Weapon(imagen_pistola, imagen_balas)

#crear un grupo de sprites
grupo_damage_text = pygame.sprite.Group()
grupo_balas = pygame.sprite.Group()
grupo_items = pygame.sprite.Group()
# añadir items dede la data del nivel
for item in world.lista_item:
    grupo_items.add(item)




#definir las variables de movimiento del jugador
mover_arriba = False
mover_abajo = False
mover_izquierda = False
mover_derecha = False

#controlar el frame rate
reloj = pygame.time.Clock()


# Botón de reinicio
boton_reinicio = pygame.Rect(constantes.ANCHO_VENTANA / 2 - 100,
                             constantes.ALTO_VENTANA / 2 + 100, 200, 50)

pygame.mixer.music.load("assets/sounds/cancion.mp3")
pygame.mixer.music.play(-1)

sonido_disparo = pygame.mixer.Sound("assets/sounds/disparo.mp3")

mostrar_inicio = True
run = True
while run == True:
    if mostrar_inicio:
        pantalla_inicio()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.collidepoint(event.pos):
                    mostrar_inicio = False
                if boton_salir.collidepoint(event.pos):
                    run = False

    else:
        #que vaya a 60 FPS
        reloj.tick(constantes.FPS)
        ventana.fill(constantes.MORADO)


        if jugador.vivo == True:
            #Calcular el movimiento del jugador
            delta_x = 0
            delta_y = 0

            if mover_derecha == True:
                delta_x = constantes.VELOCIDAD
            if mover_izquierda == True:
                delta_x = -constantes.VELOCIDAD
            if mover_arriba == True:
                delta_y = -constantes.VELOCIDAD
            if mover_abajo == True:
                delta_y = constantes.VELOCIDAD

            #mover al jugador
            posicion_pantalla, nivel_completado = jugador.movimiento(delta_x,delta_y, world.obstaculos_tiles,
                                                   world.exit_tile)

            #actualizar mapa
            world.update(posicion_pantalla)

            # actualiza estado del jugador
            jugador.update()
            # actualiza estado del enemigo
            for ene in lista_enemigos:
                ene.update()


            # actualiza el estado del arma
            bala = pistola.update(jugador)
            if bala:
                grupo_balas.add(bala)
                sonido_disparo.play()
            for bala in grupo_balas:
                damage, pos_damage = bala.update(lista_enemigos, world.obstaculos_tiles)
                if damage:
                    damage_text = DamageText(pos_damage.centerx, pos_damage.centery, str(damage), font, constantes.ROJO)
                    grupo_damage_text.add(damage_text)


            #actualizar daño
            grupo_damage_text.update(posicion_pantalla)

            #actualizar items
            grupo_items.update(posicion_pantalla, jugador)

        #dibujar mundo
        world.draw(ventana)

        # dibujar al jugador
        jugador.dibujar(ventana)

        # dibujar al enemigos
        for ene in lista_enemigos:
            if ene.energia == 0:
                lista_enemigos.remove(ene)
            if ene.energia > 0:
                ene.enemigos(jugador, world.obstaculos_tiles, posicion_pantalla,
                             world.exit_tile)
                ene.dibujar(ventana)

        # dibujar el arma
        pistola.dibujar(ventana)

        # dibujar balas
        for bala in grupo_balas:
            bala.dibujar(ventana)

        #dibujar los corazones
        vida_jugador()

        #dibujar textos
        grupo_damage_text.draw(ventana)
        dibujar_texto(f"Score: {jugador.score}", font, (255,255,0), 700, 5)
        #nivel
        dibujar_texto(f"Nivel: " + str(nivel), font, constantes.BLANCO, constantes.ANCHO_VENTANA / 2, 5)

        #dibujar items
        grupo_items.draw(ventana)

        #chequear si el nivel está completo
        if nivel_completado == True:
            if nivel < constantes.NIVEL_MAXIMO:
                nivel +=1
                world_data = resetear_mundo()
                # cargar el archivo con el nivel
                with open(f"niveles/nivel_{nivel}.csv", newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, fila in enumerate(reader):
                        for y, columna in enumerate(fila):
                            world_data[x][y] = int(columna)
                world = Mundo()
                world.process_data(world_data, tile_list, item_imagenes, animaciones_enemigos)
                jugador.actualizar_coordenadas(constantes.COORDENADAS[str(nivel)])

                # crear lista de enemigos
                lista_enemigos = []
                for ene in world.lista_enemigo:
                    lista_enemigos.append(ene)

                # añadir items dede la data del nivel
                for item in world.lista_item:
                    grupo_items.add(item)

        if jugador.vivo == False:
            ventana.fill(constantes.ROJO_OSCURO)
            text_rect = game_over_text.get_rect(center=(constantes.ANCHO_VENTANA / 2,
                                                       constantes.ALTO_VENTANA / 2))
            ventana.blit(game_over_text, text_rect)
            pygame.draw.rect(ventana, constantes.AMARILLO, boton_reinicio)
            ventana.blit(texto_boton_reinicio,
                         (boton_reinicio.x + 50, boton_reinicio.y + 10))

        for event in pygame.event.get():
            #Para cerrar el juego
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    mover_izquierda = True
                if event.key == pygame.K_d:
                    mover_derecha = True
                if event.key == pygame.K_w:
                    mover_arriba = True
                if event.key == pygame.K_s:
                    mover_abajo = True
                if event.key == pygame.K_e:
                    if world.cambiar_puerta(jugador, tile_list):
                        print("Puerta cambiada")

            # Para cuando se suelta la tecla
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                     mover_izquierda = False
                if event.key == pygame.K_d:
                    mover_derecha = False
                if event.key == pygame.K_w:
                    mover_arriba = False
                if event.key == pygame.K_s:
                    mover_abajo = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_reinicio.collidepoint(event.pos) and not jugador.vivo:
                    jugador.vivo = True
                    jugador.energia = 100
                    jugador.score = 0
                    nivel = 1
                    world_data = resetear_mundo()
                    with open(f"niveles/nivel_{nivel}.csv", newline="") as file:
                        reader = csv.reader(file, delimiter=",")
                        for x, fila in enumerate(reader):
                            for y, columna in enumerate(fila):
                                world_data[x][y] = int(columna)
                    world = Mundo()
                    world.process_data(world_data, tile_list, item_imagenes, animaciones_enemigos)
                    jugador.actualizar_coordenadas(constantes.COORDENADAS[str(nivel)])
                    for item in world.lista_item:
                        grupo_items.add(item)
                    lista_enemigos = []
                    for ene in world.lista_enemigo:
                        lista_enemigos.append(ene)


        pygame.display.update()

pygame.quit()




