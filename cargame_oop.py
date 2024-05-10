import pygame
from pygame.locals import *
import random

class CarGame:
    def __init__(self, **kwargs):
        # set window parameters
        self.window_width = 800
        self.window_height = 800
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        self.window.fill((60, 220, 0))
        # set road parameters
        self.road_width = int(self.window_width/1.6)
        self.roadmark_width = int(self.window_width/80)
        self.right_lane = self.window_width/2 + self.road_width/4
        self.left_lane = self.window_width/2 - self.road_width/4
        # set game parameters
        self.speed = 1
        self.counter = 0
        self.running = False
    
    def draw_background(self, **kwargs):
        """
        a method that draws a road on the window
        """
        # draw road
        pygame.draw.rect(
            self.window,
            (50, 50, 50),
            (self.window_width/2-self.road_width/2, 0, self.road_width, self.window_height))
        # draw centre line
        pygame.draw.rect(
            self.window,
            (255, 240, 60),
            (self.window_width/2 - self.roadmark_width/2, 0, self.roadmark_width, self.window_height))
        # draw left road marking
        pygame.draw.rect(
            self.window,
            (255, 255, 255),
            (self.window_width/2 - self.road_width/2 + self.roadmark_width*2, 0, self.roadmark_width, self.window_height))
        # draw right road marking
        pygame.draw.rect(
            self.window,
            (255, 255, 255),
            (self.window_width/2 + self.road_width/2 - self.roadmark_width*3, 0, self.roadmark_width, self.window_height))
        
    def draw_game_elements(self, **kwargs):
        """
        a method that draws game elements on top of the road
        """
        # draw road
        scene.draw_background()
        # place car images on the screen
        scene.window.blit(player.player_car, player.player_loc)
        scene.window.blit(enemy.car, enemy.car_loc)
        # apply changes
        pygame.display.update()
        
        
    def start_game(self, **kwargs):
        """
        a method that initializes a new game
        """
        # initialize pygame
        pygame.init()
        pygame.display.set_caption("Mariya's car game")
        # initialize game loop parameters
        self.running = True
        
    def game_loop(self, **kwargs):
        """
        a method that stores the game loop
        """
        # start game loop
        while scene.running:
            # start counting
            self.counter += 1
            # increase game speed as count increases
            if self.counter == 5000:
                scene.speed += 0.15
                # resent counter
                self.counter = 0
                print("level up", scene.speed)

            # animate enemy vehicle
            enemy.car_loc[1] += scene.speed
            if enemy.car_loc[1] > scene.window_height:
                # randomly select lane
                if random.randint(0,1) == 0:
                    enemy.car_loc.center = scene.right_lane, -200
                else:
                    enemy.car_loc.center = scene.left_lane, -200

            # end game logic
            if player.player_loc[0] == enemy.car_loc[0] and enemy.car_loc[1] > player.player_loc[1] - 250:
                print("GAME OVER! YOU LOST!")
                break
            
            self.controls()
            self.draw_game_elements()

        # collapse application window
        pygame.quit()
        
    def controls(self, **kwargs):
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
                    player.player_loc = player.player_loc.move([-int(scene.road_width/2), 0])
                # move user car to the right
                if event.key in [K_d, K_RIGHT]:
                    player.player_loc = player.player_loc.move([int(scene.road_width/2), 0])

class Player:
    def __init__(self, **kwargs):
        self.player_car = pygame.image.load("car.png")
        self.player_loc = self.player_car.get_rect()
        self.player_loc.center = scene.right_lane, scene.window_height*0.8

class Enemy:
    def __init__(self, **kwargs):
        self.car = pygame.image.load("otherCar.png")
        self.car_loc = self.car.get_rect()
        self.car_loc.center = scene.left_lane, scene.window_height*0.2

# initialize objects
scene = CarGame()
player = Player()
enemy = Enemy()

# start game and main loop
if __name__ == "__main__":
    scene.start_game()
    scene.game_loop()
