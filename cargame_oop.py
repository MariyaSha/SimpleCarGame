import pygame
from pygame.locals import *
import random
        
class Window:
    """ application window object """
    def __init__(self):
        # set window parameters
        self.width = 800
        self.height = 800
        self.window = pygame.display.set_mode((self.width, self.height))
        self.window.fill((60, 220, 0))
        
        # set road parameters
        self.road_width = int(self.width/1.6)
        self.roadmark_width = int(self.width/80)
        self.right_lane = self.width/2 + self.road_width/4
        self.left_lane = self.width/2 - self.road_width/4
        
    def draw_background(self):
        """
        a method that draws a road
        """
        # draw road
        pygame.draw.rect(
            self.window,
            (50, 50, 50),
            (self.width/2-self.road_width/2, 0, self.road_width, self.height))
        # draw centre line
        pygame.draw.rect(
            self.window,
            (255, 240, 60),
            (self.width/2 - self.roadmark_width/2, 0, self.roadmark_width, self.height))
        # draw left road marking
        pygame.draw.rect(
            self.window,
            (255, 255, 255),
            (self.width/2 - self.road_width/2 + self.roadmark_width*2, 0, self.roadmark_width, self.height))
        # draw right road marking
        pygame.draw.rect(
            self.window,
            (255, 255, 255),
            (self.width/2 + self.road_width/2 - self.roadmark_width*3, 0, self.roadmark_width, self.height))

class CarGame:
    """ game loop and logic """
    def __init__(self):
        self.player = Player()
        self.enemy_vehicle = EnemyVehicle()
        self.counter = 0
        self.running = False
        self.level = 0
        
        self.start_game()
        self.start_gameloop()
        
    def create_enemy(self):
        """
        a method that generates an enemy object
        """
        # if enemy vehicle is lower than the window (left the scene)
        if self.enemy_vehicle.location[1] > window.height:
            # randomly select lane
            if random.randint(0,1) == 0:
                self.enemy_vehicle.location.center = window.right_lane, -200
            else:
                self.enemy_vehicle.location.center = window.left_lane, -200  
            
    def level_up(self):
        """
        level and difficulty increase logic
        """
        # start counting
        self.counter += 1  

        # increase game speed as count increases
        if self.counter == 5000:
            self.enemy_vehicle.speed += 0.25
            self.level += 1
            # resent counter
            self.counter = 0
            print("level up", self.level)
            
    def key_controls(self):
        """
        a method that stores keyboard logic
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                # collapse the app
                self.running = False
            if event.type == KEYDOWN:
                # move user car to the left
                if event.key in [K_a, K_LEFT]:
                    self.player.location = self.player.location.move([-int(window.road_width/2), 0])
                # move user car to the right
                if event.key in [K_d, K_RIGHT]:
                    self.player.location = self.player.location.move([int(window.road_width/2), 0])
             
            
    def start_game(self):
        """
        a method that initializes a new game
        """
        # initialize pygame
        pygame.display.set_caption("Mariya's car game")
        # initialize game loop parameters
        self.running = True
               
    def start_gameloop(self):
        """
        a method that initiallizes the game loop
        """
        # start game loop
        while self.running:   
            # generate the next enemy
            self.create_enemy()
            # add level up logic
            self.level_up()
            # animate enemy vehicle
            self.enemy_vehicle.location[1] += self.enemy_vehicle.speed
            
            # game over logic
            if self.player.location[0] == self.enemy_vehicle.location[0] and self.enemy_vehicle.location[1] > self.player.location[1] - self.enemy_vehicle.length:
                print("GAME OVER! YOU LOST!")
                break
            
            # initialize key controls
            self.key_controls()
            # draw road
            window.draw_background()
            # place player car
            window.window.blit(self.player.car, self.player.location)
            # place enemy car
            window.window.blit(self.enemy_vehicle.car, self.enemy_vehicle.location)
            # apply changes
            pygame.display.update()

        # collapse application window if game over
        pygame.quit()   

class Player:
    """ player object """
    def __init__(self):
        self.car = pygame.image.load("car.png")
        self.location = self.car.get_rect()
        self.location.center = window.right_lane, window.height*0.8

class EnemyVehicle:
    """ enemy vehicle object """
    def __init__(self):
        self.speed = 1
        self.length = 250
        self.img_path = "otherCar.png"
        self.draw_car()
        
    def draw_car(self):
        self.car = pygame.image.load(self.img_path)
        self.location = self.car.get_rect()
        self.location.center = window.left_lane, window.height*0.2
 
# start game and main loop
if __name__ == "__main__":
    pygame.init()
    window = Window()
    game = CarGame()
