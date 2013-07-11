# Name: Graydon Armstrong
# Date: July 11th, 2013
# Source File: sidescrollerV1.py
# Last Modified By: Graydon Armstrong
# Date Last Modified: July 11th, 2013
# Program description: A side scroller where you must get a high score
# Revision History: Version 2 is added final graphics to the game, sound, and final polish

#I - Import and initialize
import pygame, random
pygame.init()

screen = pygame.display.set_mode((640,480))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25,25))
        self.image.fill((0,255,255))
        self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.centery = screen.get_height()/2
        self.rect.centerx = 100
        self.dy = 5
        
    def update(self):
        mousex, mousey = pygame.mouse.get_pos()
        if self.rect.centery < mousey-5 and self.rect.bottom < 410:
            self.rect.centery += self.dy
        elif self.rect.centery > mousey+5 and self.rect.top > 70:
            self.rect.centery -= self.dy
        
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25,25))
        self.image.fill((255,0,0))
        self.image.convert()
        self.rect = self.image.get_rect()
        self.dx = -12
        self.reset()
        
    def update(self):
        self.rect.centerx += self.dx
        if self.rect.centerx < 0:
            self.reset()
            
    def reset(self):
         self.rect.centerx = 640
         self.rect.centery = random.randint(70,410)
         
class Reward(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25,25))
        self.image.fill((0,255,0))
        self.image.convert()
        self.rect = self.image.get_rect()
        self.dx = -5
        self.reset()
        
    def update(self):
        self.rect.centerx += self.dx
        if self.rect.centerx < 0:
            self.reset()
            
    def reset(self):
         self.rect.centerx = 640
         self.rect.centery = random.randint(70,410)
         
class Road(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("road.gif")
        self.rect = self.image.get_rect()
        self.dx = -5
        self.reset()
        
    def update(self):
        self.rect.left += self.dx
        if self.rect.left <= -1280:
            self.reset() 
    
    def reset(self):
        self.rect.left = 0
        
class Scoreboard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.lives = 5
        self.score = 0
        self.font = pygame.font.SysFont("None", 50)
        
    def update(self):
        self.text = "Cars: %d, Score: %d" % (self.lives, self.score)
        self.image = self.font.render(self.text, 1, (255, 255, 0))
        self.rect = self.image.get_rect()

def game():
    pygame.display.set_caption("Game")
    
    background = pygame.Surface(screen.get_size())
    background.fill((0,0,0))
    screen.blit(background, (0,0))
    
    player = Player()
    road = Road()
    enemy = {Enemy(),Enemy(),Enemy()}
    reward = {Reward(),Reward(),Reward()}
    scoreboard = Scoreboard()
    
    freindSprites = pygame.sprite.Group(road)
    playerSprites = pygame.sprite.Group(player)
    rewardSprites = pygame.sprite.Group(reward)
    enemySprites = pygame.sprite.Group(enemy)
    scoreDisplay = pygame.sprite.Group(scoreboard)
    
    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        clock.tick(30)
        #pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                
                
        #check collisions       
        hitEnemies = pygame.sprite.spritecollide(player, enemySprites, False)
        if hitEnemies:
            for theEnemy in hitEnemies:
                if scoreboard.lives > 1:
                    scoreboard.lives -= 1
                    theEnemy.reset()
                else:
                    keepGoing = False
                
        hitRewards = pygame.sprite.spritecollide(player, rewardSprites, False)
        if hitRewards:
            for theReward in hitRewards:
                scoreboard.score += 50
                theReward.reset()
                
        freindSprites.clear(screen, background)
        playerSprites.clear(screen, background)
        rewardSprites.clear(screen, background)
        enemySprites.clear(screen, background)
        scoreDisplay.clear(screen, background)
        
        freindSprites.update()
        playerSprites.update()
        rewardSprites.update()
        enemySprites.update()
        scoreDisplay.update()
        
        freindSprites.draw(screen) 
        playerSprites.draw(screen)
        rewardSprites.draw(screen)   
        enemySprites.draw(screen)   
        scoreDisplay.draw(screen) 
        
        pygame.display.flip()
    return scoreboard.score
        
def instruction():
    menuFont = pygame.font.SysFont(None, 50)
    label = menuFont.render("Click to Start Game", 1, (255,0,0))
    
    keepGoing = True
    
    clock = pygame.time.Clock()
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                donePlaying = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                keepGoing = False
                donePlaying = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                    donePlaying = True
        
        screen.blit(label,(screen.get_width()/2-label.get_width()/2,screen.get_height()/2-label.get_height()/2))   
        
        pygame.display.flip()  
        
    return donePlaying   
    
def scoreScreen(score):
    
    background = pygame.Surface(screen.get_size())
    background.fill((0,0,0))
    screen.blit(background, (0,0))
    
    menuFont = pygame.font.SysFont(None, 50)
    label = menuFont.render("You Lose, Score: " + str(score), 1, (255,0,0))
    
    keepGoing = True
    
    clock = pygame.time.Clock()
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                donePlaying = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                keepGoing = False
                donePlaying = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                    donePlaying = True
                
        
        screen.blit(label,(screen.get_width()/2-label.get_width()/2,screen.get_height()/2-label.get_height()/2))   
        
        pygame.display.flip()   
        
    return donePlaying

def main():   
    score  = 0
    donePlaying = instruction()
    while not donePlaying: 
        score = game()
        donePlaying = scoreScreen(score)
    
if __name__ == "__main__":
    main()