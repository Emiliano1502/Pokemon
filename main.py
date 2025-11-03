import pygame
import random
import json
import sys

pygame.init()

# --- Configuración de pantalla ---
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pokémon Lineal")

#Pokemon
# Cargar las imágenes de Pokémon salvajes
wild_images = [
    pygame.image.load("assets/pokemon/pikachu.png"),
    pygame.image.load("assets/pokemon/bulbasaur.png"),
    pygame.image.load("assets/pokemon/indeedee.png"),
   pygame.image.load("assets/pokemon/azumarill.png")
]

# Escalar solo una vez
wild_images = [pygame.transform.scale(img, (200, 200)) for img in wild_images]



# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)

FONT = pygame.font.Font(None, 36)

clock = pygame.time.Clock()

# --- Función para mostrar texto ---
def mostrar_texto(texto, y, color=(0, 0, 0)):
    font = pygame.font.Font(None, 36)
    render = font.render(texto, True, color)
    rect = render.get_rect(center=(WIDTH // 2, y))
    screen.blit(render, rect)

# --- Estado del juego ---
vidas = 3
pokemons_capturados = []

# --- CARGA DE PREGUNTAS ---
with open("data/preguntas.json", "r", encoding="utf-8") as f:
    preguntas = json.load(f)

# --- FUNCIONES AUXILIARES ---

def mostrar_texto(texto, y, color=BLACK):
    render = FONT.render(texto, True, color)
    screen.blit(render, (50, y))

def batalla():
    wild_img = random.choice(wild_images)  # Pokémon aleatorio
    """Pantalla de batalla con pregunta"""
    global vidas  # <-- corrección: vidas es una variable global en el módulo
    pregunta = random.choice(preguntas)
    seleccion = 0
    en_batalla = True
    resultado = None

    while en_batalla:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(pregunta["opciones"])
                elif event.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(pregunta["opciones"])
                elif event.key == pygame.K_RETURN:
                    respuesta = pregunta["opciones"][seleccion]
                    if respuesta == pregunta["respuesta"]:
                        resultado = "¡Correcto! Capturaste al Pokémon."
                        pokemons_capturados.append("Pokémon salvaje")
                    else:
                        resultado = "Respuesta incorrecta. ¡Tu Pokémon recibió daño!"
                        vidas -= 1
                    en_batalla = False

        screen.fill(WHITE)
        mostrar_texto("¡Un Pokémon salvaje apareció!", 40, RED)
        screen.blit(wild_img, (WIDTH // 2 - 32, HEIGHT // 2 - 100))

        # render pregunta y opciones
        mostrar_texto(pregunta["pregunta"], 150)
        y = 200
        for i, op in enumerate(pregunta["opciones"]):
            color = BLUE if i == seleccion else BLACK
            mostrar_texto(f"{i+1}. {op}", y, color)
            y += 40

        pygame.display.flip()
        pygame.time.Clock().tick(30)

    # Pantalla de resultado
    screen.fill(WHITE)
    color_res = RED if "incorrecta" in resultado else BLUE
    mostrar_texto(resultado, 200, color_res)
    mostrar_texto(f"Vidas restantes: {vidas}", 260)
    mostrar_texto("Presiona ENTER para continuar...", 320)
    pygame.display.flip()

    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                esperando = False


# --- Cargar tile de fondo ---
tile = pygame.image.load("assets/tiles/Grass.jpg").convert()
tile = pygame.transform.scale(tile, (32, 32))


# =====================================================
# SELECCIÓN DE ENTRENADOR (chico o chica)
# =====================================================
trainer_boy = pygame.image.load("assets/player/trainer_boy.png")
trainer_girl = pygame.image.load("assets/player/trainer_girl.png")

trainer_boy = pygame.transform.scale(trainer_boy, (128, 128))
trainer_girl = pygame.transform.scale(trainer_girl, (128, 128))

def seleccionar_entrenador():
    seleccion = 0  # 0 = chico, 1 = chica
    en_seleccion = True

    while en_seleccion:
        screen.fill((255, 255, 255))
        mostrar_texto("Elige tu entrenador:", 50)

        # Dibujar los entrenadores
        screen.blit(trainer_boy, (WIDTH//4 - 64, HEIGHT//2 - 64))
        screen.blit(trainer_girl, (3*WIDTH//4 - 64, HEIGHT//2 - 64))

        # Marco sobre el seleccionado
        if seleccion == 0:
            pygame.draw.rect(screen, (255, 0, 0), (WIDTH//4 - 70, HEIGHT//2 - 70, 140, 140), 4)
        else:
            pygame.draw.rect(screen, (255, 0, 0), (3*WIDTH//4 - 70, HEIGHT//2 - 70, 140, 140), 4)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    seleccion = 0
                elif event.key == pygame.K_RIGHT:
                    seleccion = 1
                elif event.key == pygame.K_RETURN:
                    en_seleccion = False

    if seleccion == 0:
        return "chico"
    else:
        return "chica"


# --- Cargar sprites del jugador ---
# Seleccionar entrenador
entrenador = seleccionar_entrenador()

# Cargar sprites del jugador según el entrenador elegido
if entrenador == "chico":
    player_sprites = {
        "down": [pygame.image.load("assets/player/down1_b.png"), pygame.image.load("assets/player/down2_b.png")],
        "up": [pygame.image.load("assets/player/up1_b.png"), pygame.image.load("assets/player/up2_b.png")],
        "left": [pygame.image.load("assets/player/left1_b.png"), pygame.image.load("assets/player/left2_b.png")],
        "right": [pygame.image.load("assets/player/right1_b.png"), pygame.image.load("assets/player/right2_b.png")]
    }
else:
    player_sprites = {
        "down": [pygame.image.load("assets/player/down1_g.png"), pygame.image.load("assets/player/down2_g.png")],
        "up": [pygame.image.load("assets/player/up1_g.png"), pygame.image.load("assets/player/up2_g.png")],
        "left": [pygame.image.load("assets/player/left1_g.png"), pygame.image.load("assets/player/left2_g.png")],
        "right": [pygame.image.load("assets/player/right1_g.png"), pygame.image.load("assets/player/right2_g.png")]
    }

    
for direction in player_sprites:
    player_sprites[direction] = [pygame.transform.scale(img, (48, 48)) for img in player_sprites[direction]]

player_direction = "down"
player_index = 0
frame_count = 0

# --- Rectángulo del jugador ---
player_rect = player_sprites[player_direction][0].get_rect(center=(WIDTH // 2, HEIGHT // 2))

# --- Bucle principal ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

 # Aparición aleatoria de Pokémon salvaje
    if random.randint(0, 200) == 1:
        batalla()

    # Verificar si el jugador perdió
    if vidas <= 0:
        screen.fill(WHITE)
        mostrar_texto("Te has quedado sin vidas...", 250, RED)
        mostrar_texto("Fin del juego", 300)
        pygame.display.flip()
        pygame.time.wait(3000)
        break

    # === Fondo con mosaico de pasto ===
    tile_w, tile_h = tile.get_width(), tile.get_height()
    for x in range(0, WIDTH, tile_w):
        for y in range(0, HEIGHT, tile_h):
            screen.blit(tile, (x, y))

    # === Movimiento y animación ===
    keys = pygame.key.get_pressed()
    moving = False

    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player_rect.y -= 4
        player_direction = "up"
        moving = True
    elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player_rect.y += 4
        player_direction = "down"
        moving = True
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_rect.x -= 4
        player_direction = "left"
        moving = True
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_rect.x += 4
        player_direction = "right"
        moving = True

    # Animación de pasos
    if moving:
        frame_count += 1
        if frame_count % 10 == 0:
            player_index = (player_index + 1) % len(player_sprites[player_direction])
    else:
        player_index = 0

    # Dibujar jugador
    current_sprite = player_sprites[player_direction][player_index]
    screen.blit(current_sprite, player_rect)

    # --- Interfaz ---
    mostrar_texto(f"Vidas: {vidas}", 10)
    mostrar_texto(f"Pokémon capturados: {len(pokemons_capturados)}", 40)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
