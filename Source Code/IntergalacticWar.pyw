# Importing all modules
import os
import time
import pygame
import random
import pygame_menu

# Initialize the pygame & font
pygame.font.init()
pygame.init()

# Set window property
WIDTH, HEIGHT = 700, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Intergalactic War")
WINDOW_ICON = pygame.image.load(os.path.join("appdata", "texture", "game_icon", "app_icon.ico"))
pygame.display.set_icon(WINDOW_ICON)

# Importing enemies spaceship images
SKY_SPACE_SHIP = pygame.image.load(os.path.join("appdata", "texture", "enemy_ships", "ship_sky.bmp"))
RED_SPACE_SHIP = pygame.image.load(os.path.join("appdata", "texture", "enemy_ships", "ship_red.bmp"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("appdata", "texture", "enemy_ships", "ship_blue.bmp"))
GREY_SPACE_SHIP = pygame.image.load(os.path.join("appdata", "texture", "enemy_ships", "ship_grey.bmp"))
RED2_SPACE_SHIP = pygame.image.load(os.path.join("appdata", "texture", "enemy_ships", "ship_red2.bmp"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("appdata", "texture", "enemy_ships", "ship_green.bmp"))
PURPLE_SPACE_SHIP = pygame.image.load(os.path.join("appdata", "texture", "enemy_ships", "ship_purple.bmp"))
GREEN2_SPACE_SHIP = pygame.image.load(os.path.join("appdata", "texture", "enemy_ships", "ship_green2.bmp"))
VIOLET_SPACE_SHIP = pygame.image.load(os.path.join("appdata", "texture", "enemy_ships", "ship_violet.bmp"))
ORANGE_SPACE_SHIP = pygame.image.load(os.path.join("appdata", "texture", "enemy_ships", "ship_orange.bmp"))

# Importing players spaceship images
PLAYERS_SHIP_1 = pygame.image.load(os.path.join("appdata", "texture", "player_ships", "players_ship_1.bmp"))
PLAYERS_SHIP_2 = pygame.image.load(os.path.join("appdata", "texture", "player_ships", "players_ship_2.bmp"))
PLAYERS_SHIP_3 = pygame.image.load(os.path.join("appdata", "texture", "player_ships", "players_ship_3.bmp"))
PLAYERS_SHIP_4 = pygame.image.load(os.path.join("appdata", "texture", "player_ships", "players_ship_4.bmp"))
PLAYERS_SHIP_5 = pygame.image.load(os.path.join("appdata", "texture", "player_ships", "players_ship_5.bmp"))
PLAYERS_SHIP_6 = pygame.image.load(os.path.join("appdata", "texture", "player_ships", "players_ship_6.bmp"))
PLAYERS_SHIP_7 = pygame.image.load(os.path.join("appdata", "texture", "player_ships", "players_ship_7.bmp"))

# Importing all laser images
RED_LASER = pygame.image.load(os.path.join("appdata", "texture", "ship_lasers", "laser_red.bmp"))
BLUE_LASER = pygame.image.load(os.path.join("appdata", "texture", "ship_lasers", "laser_blue.bmp"))
GREEN_LASER = pygame.image.load(os.path.join("appdata", "texture", "ship_lasers", "laser_green.bmp"))
PURPLE_LASER = pygame.image.load(os.path.join("appdata", "texture", "ship_lasers", "laser_purple.bmp"))
YELLOW_LASER = pygame.image.load(os.path.join("appdata", "texture", "ship_lasers", "laser_yellow.bmp"))

# Importing map Images
UNDER_BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("appdata", "texture", "background", "background.png")), (WIDTH, HEIGHT))
MAP_DEFAULT = pygame.transform.scale(pygame.image.load(os.path.join("appdata", "texture", "background", "default.bmp")), (WIDTH, HEIGHT))
MAP_ZENDARIA = pygame.transform.scale(pygame.image.load(os.path.join("appdata", "texture", "background", "zendaria.bmp")), (WIDTH, HEIGHT))
MAP_NOWHERE = pygame.transform.scale(pygame.image.load(os.path.join("appdata", "texture", "background", "nowhere.bmp")), (WIDTH, HEIGHT))
MAP_MAGIC = pygame.transform.scale(pygame.image.load(os.path.join("appdata", "texture", "background", "magic.bmp")), (WIDTH, HEIGHT))
MAP_DARKEND = pygame.transform.scale(pygame.image.load(os.path.join("appdata", "texture", "background", "darkend.bmp")), (WIDTH, HEIGHT))
MAP_INTERGALACTIC = pygame.transform.scale(pygame.image.load(os.path.join("appdata", "texture", "background", "intergalactic.bmp")), (WIDTH, HEIGHT))
MAP_DEEP_DARK = pygame.transform.scale(pygame.image.load(os.path.join("appdata", "texture", "background", "deep_dark.bmp")), (WIDTH, HEIGHT))

# Importing in game sounds
pygame.mixer.init()
laser_sound = pygame.mixer.Sound(os.path.join("appdata", "music", "laser_sound.mp3"))
death_sound = pygame.mixer.Sound(os.path.join("appdata", "music", "death_sound.mp3"))

# Importing menu background music
menu_sound = pygame.mixer.music.load(os.path.join("appdata", "music", "menu_music.mp3"))

# Set music sound
pygame.mixer.music.set_volume(1.5)
laser_sound.set_volume(0.2)
death_sound.set_volume(0.5)

# Setting up global variable
R, G, B = 255, 255, 255
PLAYER_SELECTED = PLAYERS_SHIP_1
LASER_SELECTED = YELLOW_LASER
DEFAULT_SHIP = 0
MAP_BACKGROUND = MAP_DEFAULT
DEFAULT_MAP = 0
BACKGROUND_SOUND = None
PLAY_SOUND = 0

# Initializing ships laser class
class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)

# Initializing ship class
class Ship:
    COOLDOWN = 12
    
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1
    
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x+42, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
            # play sound after checking settings
            if PLAY_SOUND == 0:
                laser_sound.play()

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

# Initializing players ship class
class Player(Ship):
    def __init__(self, x, y, health=200): # add players health
        super().__init__(x, y, health)
        self.ship_img = PLAYER_SELECTED
        self.laser_img = LASER_SELECTED
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

# Initializing enemys ship class
class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
        "purple": (PURPLE_SPACE_SHIP, PURPLE_LASER),
        "sky": (SKY_SPACE_SHIP, BLUE_LASER),
        "green2": (GREEN2_SPACE_SHIP, GREEN_LASER),
        "orange": (ORANGE_SPACE_SHIP, RED_LASER),
        "violet": (VIOLET_SPACE_SHIP, PURPLE_LASER),
        "grey": (GREY_SPACE_SHIP, RED_LASER),
        "red2": (RED2_SPACE_SHIP, RED_LASER)
    }
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x+36, self.y, self.laser_img) # Set laser position for enemy ships
            self.lasers.append(laser)
            self.cool_down_counter = 1
            
            # play sound after checking settings
            if PLAY_SOUND == 0:
                laser_sound.play()

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

# Main game loop
def main():
    run = True
    FPS = 60
    level = 0
    lives = 10 # Set Player Lives
    enemy_vel = 1
    main_font = pygame.font.SysFont("comicsans", 30)
    lost_font = pygame.font.SysFont("comicsans", 35)

    enemies = []
    wave_length = 5

    player_vel = 5
    laser_vel = 5
    player = Player(300, 450)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0
    
    def redraw_window():
        WIN.blit(MAP_BACKGROUND, (0,0))
        # Create text label with font
        lives_label = main_font.render(f"Lives: {lives}", 1, (R, G, B))
        level_label = main_font.render(f"Level: {level}", 1, (R, G, B))
        # Draw labeled text on display
        WIN.blit(lives_label, (10,5))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 5))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("You couldn't survive any longer :(", 1, (255,0,0))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 280))
            pygame.mixer.music.stop() # stop music
            explosion = death_sound.get_num_channels()
            if explosion == 1:
                pass
            else:
                if PLAY_SOUND == 0:
                    death_sound.play(1)

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 2:
                death_sound.stop()
                time.sleep(3)
                if PLAY_SOUND == 0:
                    pygame.mixer.music.play(fade_ms=1000)
                run = False
            else:
                continue

        if len (enemies) == 0:
            level +=1
            wave_length += 3
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green", "purple", "sky", "green2", "orange", "violet", "grey", "red2"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        # Take keyboard buttons input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0: # Move left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: # Move Right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0: # Move up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT: # Move down
            player.y += player_vel
        if keys[pygame.K_LEFT] and player.x - player_vel > 0: # Move left
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH: # Move right
            player.x += player_vel
        if keys[pygame.K_UP] and player.y - player_vel > 0: # Move up
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() + 15 < HEIGHT: # Move down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot() # Let player shoot laser if not on cooldown
        if keys[pygame.K_m]:
            main_menu()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)

def main_menu():
    
    def keymaps():
        title_font = pygame.font.SysFont("comicsans", 32)
        run = True
        while run:
            WIN.blit(MAP_DARKEND, (0,0))
            title_label_line1 = title_font.render("Key maps:", 1, (255,255,255))
            title_label_line2 = title_font.render("a : Left  |  d : Right", 1, (255,255,255))
            title_label_line3 = title_font.render("w : Up    |  s : Down", 1, (255,255,255))
            title_label_line4 = title_font.render("Arrows : Movement", 1, (255,255,255))
            title_label_line5 = title_font.render("SPACE : Shoot", 1, (255,255,255))
            title_label_line6 = title_font.render("m : Menu", 1, (255,255,255))
            title_label_line7 = title_font.render("Any key to go back...", 1, (255,255,255))

            # blit text on display
            WIN.blit(title_label_line1, (WIDTH/2 - title_label_line1.get_width()/2, 110))
            WIN.blit(title_label_line2, (WIDTH/2 - title_label_line2.get_width()/2, 190))
            WIN.blit(title_label_line3, (WIDTH/2 - title_label_line3.get_width()/2, 240))
            WIN.blit(title_label_line4, (WIDTH/2 - title_label_line4.get_width()/2, 290))
            WIN.blit(title_label_line5, (WIDTH/2 - title_label_line5.get_width()/2, 340))
            WIN.blit(title_label_line6, (WIDTH/2 - title_label_line6.get_width()/2, 390))
            WIN.blit(title_label_line7, (WIDTH/2 - title_label_line7.get_width()/2, 440))

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    main_menu()
        pygame.quit()
    
    def about():
        title_font = pygame.font.SysFont("comicsans", 25)
        run = True
        while run:
            WIN.blit(MAP_DARKEND, (0,0))
            title_label_line1 = title_font.render("Intergalactic War is a space shooter game", 1, (255,255,255))
            title_label_line2 = title_font.render("made using Python (pygame, pygame-menu) by", 1, (255,255,255))
            title_label_line3 = title_font.render("Abdullah Al Noman (MagenusSkyler) in 2022.", 1, (255,255,255))
            title_label_line4 = title_font.render("GitHub : https://github.com/MagenusSkyler", 1, (255,255,255))
            title_label_line5 = title_font.render("Any key to go back...", 1, (255,255,255))

            WIN.blit(title_label_line1, (WIDTH/2 - title_label_line1.get_width()/2, 180))
            WIN.blit(title_label_line2, (WIDTH/2 - title_label_line2.get_width()/2, 220))
            WIN.blit(title_label_line3, (WIDTH/2 - title_label_line3.get_width()/2, 260))
            WIN.blit(title_label_line4, (WIDTH/2 - title_label_line4.get_width()/2, 300))
            WIN.blit(title_label_line5, (WIDTH/2 - title_label_line5.get_width()/2, 430))

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    main_menu()
        pygame.quit()

    def start_the_game():
        pygame.mixer.music.fadeout(64)
        main()

    # Play menu sound when menu is open
    if PLAY_SOUND == 0:
        menu_music = pygame.mixer.music.get_busy()
        if menu_music == True:
            pass
        else:
            pygame.mixer.music.play(-1, fade_ms=1000)
    else:
        pass

    # Background (under the menu)
    def menu_background():
        WIN.blit(UNDER_BACKGROUND, (0,0))
    
    # Background (on the menu)
    menu_bg = pygame_menu.baseimage.BaseImage(
            image_path="appdata\\texture\\background\\menu_bg.bmp",
            drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY,
        )
    
    # Set up theme for pygame_menu
    theme_body = pygame_menu.themes.THEME_DARK.copy()
    theme_body.title_background_color=(42, 104, 112)
    theme_body.background_color = menu_bg

    menu = pygame_menu.menu.Menu("Intergalactic War", WIDTH -10, HEIGHT -10, theme=theme_body)

    def map_selector(value, selected_index):
        global MAP_BACKGROUND
        global DEFAULT_MAP
        global BACKGROUND_SOUND
        if selected_index == 0:
            MAP_BACKGROUND = MAP_DEFAULT
            DEFAULT_MAP = 0
        elif selected_index == 1:
            MAP_BACKGROUND = MAP_ZENDARIA
            DEFAULT_MAP = 1
        elif selected_index == 2:
            MAP_BACKGROUND = MAP_NOWHERE
            DEFAULT_MAP = 2
        elif selected_index == 3:
            MAP_BACKGROUND = MAP_MAGIC
            DEFAULT_MAP = 3
        elif selected_index == 4:
            MAP_BACKGROUND = MAP_DARKEND
            DEFAULT_MAP = 4
        elif selected_index == 5:
            MAP_BACKGROUND = MAP_INTERGALACTIC
            DEFAULT_MAP = 5
        elif selected_index == 6:
            MAP_BACKGROUND = MAP_DEEP_DARK
            DEFAULT_MAP = 6
        else:
            pass

    def ship_selector(value, selected_index):
        global PLAYER_SELECTED
        global LASER_SELECTED
        global DEFAULT_SHIP
        if selected_index == 1:
            PLAYER_SELECTED = PLAYERS_SHIP_1
            LASER_SELECTED = YELLOW_LASER
            DEFAULT_SHIP = 0
        elif selected_index == 2:
            PLAYER_SELECTED = PLAYERS_SHIP_2
            LASER_SELECTED = YELLOW_LASER
            DEFAULT_SHIP = 1
        elif selected_index == 3:
            PLAYER_SELECTED = PLAYERS_SHIP_3
            LASER_SELECTED = RED_LASER
            DEFAULT_SHIP = 2
        elif selected_index == 4:
            PLAYER_SELECTED = PLAYERS_SHIP_4
            LASER_SELECTED = YELLOW_LASER
            DEFAULT_SHIP = 3
        elif selected_index == 5:
            PLAYER_SELECTED = PLAYERS_SHIP_5
            LASER_SELECTED = RED_LASER
            DEFAULT_SHIP = 4
        elif selected_index == 6:
            PLAYER_SELECTED = PLAYERS_SHIP_6
            LASER_SELECTED = RED_LASER
            DEFAULT_SHIP = 5
        elif selected_index == 7:
            PLAYER_SELECTED = PLAYERS_SHIP_7
            LASER_SELECTED = YELLOW_LASER
            DEFAULT_SHIP = 6
        else:
            pass

    def sound_set(value, selected_index):
        global PLAY_SOUND
        if selected_index == 1:
            PLAY_SOUND = 0
            pygame.mixer.music.play(-1, fade_ms=1000)
        else:
            PLAY_SOUND = 1
            pygame.mixer.music.fadeout(2000)

    menu.add.selector(
        "Map:\t",
        [('Default', 0), ('Zendaria', 1), ('Nowhere', 2), ('Magic', 3),
        ('Darkend', 4), ('Intergalactic', 5), ('Deep-dark', 6)],
        onchange=(map_selector), onreturn=(map_selector), default=DEFAULT_MAP
        )

    menu.add.selector(
        "Ship:\t",
        [('Battleship', 1), ('Cruiseship', 2), ('Pelican', 3), ('Gradius', 4),
        ('Hot-Bat', 5), ('Moldy', 6), ('Heavy-Ship', 7)],
        onchange=(ship_selector), onreturn=(ship_selector), default=DEFAULT_SHIP
        )

    menu.add.selector(
        "Sound:\t",
        [('ON', 1), ('OFF', 2)],
        onchange=(sound_set), onreturn=(sound_set),
        default=PLAY_SOUND
        )
    
    menu.add.button(" Keymaps ", keymaps)
    menu.add.button("  About  ", about)
    menu.add.button("   Play   ", start_the_game)
    menu.add.button("   Quit   ", pygame_menu.events.EXIT)

    menu.mainloop(WIN, bgfun=menu_background)
main_menu()
