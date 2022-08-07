import pygame
import random
import Platform
import Player
import time


W = 600
H = 800


class DoodleJump():
    def __init__(self):
        self.screen = pygame.display.set_mode((W, H))
        pygame.font.init()
        self.score = 0
        self.font = pygame.font.SysFont("Arial", 25)                           
        self.green = pygame.transform.scale(pygame.image.load("game/assets/green.png"), (80,25)).convert_alpha() # Green Platform
        self.blue = pygame.transform.scale(pygame.image.load("game/assets/blue.png"), (80,25)).convert_alpha()                # Blue Moving Platform
        self.red = pygame.transform.scale(pygame.image.load("game/assets/red.png"), (80,25)).convert_alpha()                 # Red Fragile Platform
        self.red_1 = pygame.transform.scale(pygame.image.load("game/assets/redBroken.png"), (80,40)).convert_alpha()         # Red Broken Platform
        self.gravity = 0
        self.camera = 0
        self.platforms = []
        self.time = time.time()
        self.startY = -100


        
    def playerUpdate(self,player):
        # Camera follow player when jumping
        if (player.y - self.camera <=200):
            self.camera -= 8

    def drawPlayer(self, player):
        self.screen.blit(player.player, (player.x, player.y - self.camera))


    # Platform colliders
    def updateplatforms(self,player):
        for p in self.platforms:
            rect = pygame.Rect(p.x + 10, p.y, p.green.get_width() - 25, p.green.get_height() - 20)
            playerCollider = pygame.Rect(player.x, player.y, player.player.get_width() - 10, player.player.get_height())
            
            
            if (rect.colliderect(playerCollider) and player.gravity > 0 and player.y < (p.y - self.camera)):
                # jump when landing on green or blue
                if (p.kind != 2):
                    player.jump = 20
                    player.gravity = 0
                else:
                    p.broken = True

    # Draw generated platforms
    def drawplatforms(self):
        for p in self.platforms:
            y = p.y - self.camera
            if (y > H):
                self.generateplatforms(False)
                self.platforms.pop(0)
                self.score += 10
                self.time = time.time()

             # Blue Platform movement
            if (p.kind == 1):
                p.blueMovement(self.score)    

            if (p.kind == 0):
                self.screen.blit(p.green, (p.x, p.y - self.camera))
            elif (p.kind == 1):
                self.screen.blit(p.blue, (p.x, p.y - self.camera))
            elif (p.kind == 2):
                if (p.broken == False):
                    self.screen.blit(p.red, (p.x, p.y - self.camera))
                else:
                    self.screen.blit(p.red_1, (p.x, p.y - self.camera))
   
    def generateplatforms(self,initial):
        y = 900                     # Generate from bottom of the screen
        start = -100
        if (initial == True):
            self.startY = -100
            # Fill starting screen with platforms

            while (y > -70):
                p = Platform.Platform()
                p.getKind(self.score)
                p.y = y
                p.startY = start
                self.platforms.append(p)
                y -= 30                                 # Generate every 30 pixels 
                start += 30
                self.startY =start
    
                
        else:
            # Creates a platform based on current score 
            p = Platform.Platform()
           
            if (self.score <= 2000):
                difficulty = 50
            elif (self.score < 3000):
                difficulty = 60
            elif (self.score < 4000):
                difficulty = 70
            elif (self.score < 5000):
                difficulty = 80    
            else: 
                difficulty = 90

            p.y = self.platforms[-1].y - difficulty
            self.startY += difficulty
            p.startY = self.startY
            p.getKind(self.score)
            self.platforms.append(p)

    def update(self):
        self.drawplatforms()
        self.screen.blit(self.font.render("Score: " +str(self.score), -1, (0, 0, 0)), (25, 25))

        
    # Run game
    def run(self):
        clock = pygame.time.Clock()
        doodler = Player.Player() 
            
        run = True
        self.generateplatforms(True)
        highestScore = 0
        while run:
            self.screen.fill((255,255,255))
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            currentTime = time.time()
            
            # When doodler is dead, start again
            if(doodler.y >= 800 ):
                self.camera = 0
                self.time = time.time()
                self.score = 0
                self.platforms.clear()
                self.generateplatforms(True)
                doodler = Player.Player()
                                   
            
            self.update()

            self.drawPlayer(doodler)
            self.playerUpdate(doodler)
            self.updateplatforms(doodler)
            doodler.move()

            if(self.score > highestScore):
                highestScore = self.score
            
            
            self.screen.blit(self.font.render("High Score: " +str(highestScore), -1, (0, 0, 0)), (25, 90))
            
           
            pygame.display.update()
            


DoodleJump().run()

        