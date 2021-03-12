'''Retro space invaders game built using pygame'''
import pygame as pg, random, sys, time
from math import sqrt


# CONSTANTS
GAME_TEXT = (0, 255, 0) # green
FPS = 30


class Spaceship:
    def __init__(self, game_window):
        self.game_window = game_window
        self.player_img = pg.image.load('Space-Invaders-assets/player.png')
        self.xcor = 370
        self.ycor = 480
        self.lateral_movement = 0


    def draw_player(self):
        '''Simple method to draw player spaceship'''
        self.game_window.blit(self.player_img, (self.xcor, self.ycor))
        

    def player_boundaries(self):
        '''Simple method to keep player spaceship within the boundaries of the screen'''
        if self.xcor <= 0:
            self.xcor = 0
        elif self.xcor > 736:
            self.xcor = 736 


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Enemies:
    def __init__(self, game_window):
        self.game_window = game_window
        self.enemies_img = []
        self.xcor = []
        self.ycor = []
        self.Xchange = []
        self.Ychange = []
        self.num_enemies = 6


    def create_enemies(self):
        '''Simple method to append enemy image, x and y coordinates and changes to x and y coordinates to the lists of Enemies class'
        properties.'''
        for enemy in range(self.num_enemies):
            self.enemies_img.append(pg.image.load('Space-Invaders-assets/enemy-spaceship.png'))
            self.xcor.append(random.randint(0, 735))
            self.ycor.append(random.randint(50, 100))
            self.Xchange.append(9)
            self.Ychange.append(40)


    def draw_enemies(self, x, y, i):
        '''Simple method to draw enemies, i value will be defined in the Game class' play() method'''
        self.game_window.blit(self.enemies_img[i], (self.xcor[i], self.ycor[i]))
        

    def movement_and_boundaries(self):
        '''Simple method to initialise default enemy movements and boundaries'''
        for i in range(self.num_enemies):
            self.xcor[i] += self.Xchange[i] # Enables auto-movement for the enemies
            if self.xcor[i] <= 0:
                self.Xchange[i] = 9 # Right
                self.ycor[i] += self.Ychange[i]
            elif self.xcor[i] >= 736:
                self.Xchange[i] = -9 # Left
                self.ycor[i] += self.Ychange[i]

        
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Bullet:
    def __init__(self, game_window):
        self.game_window = game_window
        self.bullet_img = pg.image.load('Space-Invaders-assets/bullet.png')
        self.xcor = 0
        self.ycor = 480 
        self.Ychange = 30
        self.bullet_state = False
        self.bullet_sound = pg.mixer.Sound('Space-Invaders-assets/laser.wav')


    def fire_bullet(self, x, y):
        '''Simple method to draw bullet. self.bullet_state == True when the bullet is on screen, xcor and ycor have been increased
        in order to center and fire bullet from the top of the spaceship.'''
        self.bullet_state = True
        self.game_window.blit(self.bullet_img, (self.xcor + 16, self.ycor + 10))
        

    def bullet_boundaries(self):
        '''Simple method to define bullet boundaries. Method will be called when keybinding event for K_SPACE is triggered'''
        if self.ycor <= 0:
            self.ycor = 480
            self.bullet_state = False
        if self.bullet_state:
            self.fire_bullet(self.xcor, self.ycor)
            self.ycor -= self.Ychange
            

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class GameText:
    def __init__(self, game_window):
        self.game_window = game_window

        # Intro screen
        self.title_xcor = 120
        self.title_ycor = 150
        self.title_font = pg.font.Font('freesansbold.ttf', 64)
        self.message1_xcor = 115
        self.message1_ycor = 250
        self.message1_font = pg.font.Font('freesansbold.ttf', 16)
        self.message2_xcor = 200
        self.message2_ycor = 300
        self.message2_font = pg.font.Font('freesansbold.ttf', 32)

        # Score
        self.score_value = 0
        self.score_xcor = 10
        self.score_ycor = 10
        self.score_font = pg.font.Font('freesansbold.ttf', 32)

        # Game over
        self.game_over_xcor = 180
        self.game_over_ycor = 250
        self.game_over_font = pg.font.Font('freesansbold.ttf', 64)
        self.play_again_xcor = 140
        self.play_again_ycor = 324
        self.play_again_font = pg.font.Font('freesansbold.ttf', 32)


    def display_score(self):
        '''Simple method to display the score'''
        render_font = self.score_font.render(f'SCORE: {self.score_value}', True, (GAME_TEXT))
        self.game_window.blit(render_font, (self.score_xcor, self.score_ycor))


    def display_game_over(self):
        '''Simple method to display a game over message and offer the option to play again'''
        render_font1 = self.game_over_font.render('GAME OVER!', True, (GAME_TEXT))
        self.game_window.blit(render_font1, (self.game_over_xcor, self.game_over_ycor))
        render_font2 = self.play_again_font.render('Play Again: Enter / Quit: Escape', True, (GAME_TEXT))
        self.game_window.blit(render_font2, (self.play_again_xcor, self.play_again_ycor))

        
    def intro_screen(self):
        '''Simple method to display an intro screen, explaining the controls to the user, Game will run when keybinding event for K_RETURN
        is triggered'''
        render_font1 = self.title_font.render('SPACE INVADERS', True, (GAME_TEXT))
        self.game_window.blit(render_font1, (self.title_xcor, self.title_ycor))
        render_font2 = self.message1_font.render('Move Left : Left Arrow Key, Move Right: Right Arrow Key, Shoot: Space Bar', True, (GAME_TEXT))
        self.game_window.blit(render_font2, (self.message1_xcor, self.message1_ycor))
        render_font3 = self.message2_font.render('Press Enter To Continue', True, (GAME_TEXT))
        self.game_window.blit(render_font3, (self.message2_xcor, self.message2_ycor))
        pg.display.update()

    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Game:
    def __init__(self, *args):
        pg.init()
        pg.mixer.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((800, 600))
        self.background_img = pg.image.load('Space-Invaders-assets/background.png')
        self.caption = pg.display.set_caption('Space Invaders')
        self.icon = pg.image.load('Space-Invaders-assets/ufo.png')
        pg.display.set_icon(self.icon)
        bg_music = pg.mixer.music.load('Space-Invaders-assets/background.wav')
        pg.mixer.music.play(-1)

        # Game class is a composite for all other classes
        self.player = Spaceship(self.screen)
        self.enemies = Enemies(self.screen)
        self.enemy_hit = pg.mixer.Sound('Space-Invaders-assets/explosion.wav')
        self.bullet = Bullet(self.screen)
        self.game_text = GameText(self.screen)


    def bullet_enemy_collision(self, x1, x2, y1, y2, i):
        '''Simple method for determining whether a collision between the bullet and an enemy has occurred. The equation used calculates
        the distance between two coordinates.'''
        distance = sqrt((self.bullet.xcor - self.enemies.xcor[i])**2 + (self.bullet.ycor - self.enemies.ycor[i])**2)
        if distance <= 27:
            return True
        return False


    def play(self):
        '''All methods will be called here except the Bullet class' fire_bullet() method, this method will be called in the run() method
        where all keybinding events are initialised'''
        

        # Background image
        self.screen.blit(self.background_img, (0, 0))
        # Score
        self.game_text.display_score()
        # player image, movement and boundaries   
        self.player.draw_player()
        self.player.xcor += self.player.lateral_movement
        self.player.player_boundaries()
        # Enemies
        self.enemies.create_enemies()
        self.enemies.movement_and_boundaries()
        # bullet boundaries
        self.bullet.bullet_boundaries()


        '''Move enemies, player and score off the screen should an enemy's y-cor position be greater than or equal to the specified value'''
        for i in range(self.enemies.num_enemies):
            # Game over
            if self.enemies.ycor[i] >= 440:
                self.game_text.display_game_over()
                self.enemies.ycor = [2000 for i in self.enemies.ycor]
                self.game_text.score_xcor = 2000
                self.player.xcor = 2000
                
                
            collision = self.bullet_enemy_collision(self.enemies.xcor[i], self.enemies.ycor[i], self.bullet.xcor, self.bullet.ycor, i)
            if collision:
                # Explosion sound
                self.enemy_hit.play()
                self.bullet.ycor = 480 # After a collision, bullet_ycor goes back to default y-cor position
                self.bullet.bullet_state = False # A collision has occured so we now no longer want the bullet on screen
                self.game_text.score_value += 1
                # Enemy that was hit re-spawns within random position of the given x and y-cor range
                self.enemies.xcor[i] = random.randint(0, 735) 
                self.enemies.ycor[i] = random.randint(50, 150)
                # Draw enemies
            self.enemies.draw_enemies(self.enemies.xcor[i], self.enemies.ycor[i], i)


        pg.display.update()
        self.clock.tick(FPS)


    def run(self):
        

        # GameText class' intro_screen() method, keybinding events determine whether the game runs or not
        intro = True
        while intro:
            self.screen.blit(self.background_img, (0,0))
            self.game_text.intro_screen()
            for event in pg.event.get():
                if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    intro = False

                    
        running = True
        while running:
            

            self.play()
        

            # Event detection 
            for event in pg.event.get():
                # Close window detection
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                    
                
                # Keydown event checks and player movement
                if event.type == pg.KEYDOWN: 
                    if event.key == pg.K_LEFT:
                        self.player.lateral_movement = -9 # Left
                    if event.key == pg.K_RIGHT:
                        self.player.lateral_movement = 9 # Right
                        

                    # Fire bullets
                    if event.key == pg.K_SPACE:
                        # Check whether or not a bullet is already on the screen
                        if not(self.bullet.bullet_state):
                            self.bullet.bullet_sound.play()
                            # Set bullet x-coordinate to current x-coordinate of player
                            self.bullet.xcor = self.player.xcor
                            self.bullet.fire_bullet(self.bullet.xcor, self.bullet.ycor)
                            

                    # Instantiate a Game object so that the game will continue to run after each game over event
                    if event.key == pg.K_RETURN:
                        space_invaders = Game()
                        space_invaders.run()
                        

                    # Exit game after game over event
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()
                        
                        
                # Stop player movement
                if event.type == pg.KEYUP:
                    if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                        self.player.lateral_movement = 0

        
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
space_invaders = Game()
space_invaders.run()
