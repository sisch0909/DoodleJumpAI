import math
import pygame



class Player():
    def __init__(self):
        self.screen = pygame.display.set_mode((600, 800))
        pygame.sprite.Sprite.__init__(self)
        self.player = pygame.transform.scale(pygame.image.load("game/assets/player.png"), (80,80)).convert_alpha()        # Facing Right
        self.x = 300            # Current X position
        self.y = 550              # Current Y position
        self.startY = 300
        self.direction = 0          # direction facing; 0 is right; 1 is left
        self.xvel = 0
        self.jump = 0
        self.gravity = 0

    def move(self):

        if self.jump == 0: 
            self.gravity += 0.5
            self.y += self.gravity
            self.startY -= self.gravity

        elif self.jump > 0:
            self.jump -= 1
            self.y -= self.jump
            
            self.startY += self.jump

        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT]:
            if self.xvel < 10:
                self.xvel += 1
                self.direction = 0
        elif key[pygame.K_LEFT]:
            if self.xvel > -10:
                self.xvel -= 1
            self.direction = 1
        else:
            if self.xvel > 0:
                self.xvel -= 1
            elif self.xvel < 0:
                self.xvel += 1
        
        self.x += self.xvel
        
        # When at the edge of the screen go to the other side
        if self.x > 650:
            self.x = -50
        elif self.x < -50:
            self.x = 650


