# Name: Graydon Armstrong
# Date: July 10th, 2013
# Source File: sidescrollerV1.py
# Last Modified By: Graydon Armstrong
# Date Last Modified: July 10th, 2013
# Program description: A side scroller where you must get a high score
# Revision History: Version 1 is making the basic framework

#I - Import and initialize
import pygame, random
pygame.init()

screen = pygame.display.set_mode((640,480))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25,25))
        self.image.fill((0,0,255))
        self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.centery = screen.get_height()/2
        self.rect.centerx = 100
        self.dy = 5
        
    def update(self):
        mousex, mousey = pygame.mouse.get_pos()
        if self.rect.centery < mousey-5:
            self.rect.centery += self.dy
        elif self.rect.centery > mousey+5:
            self.rect.centery -= self.dy
        
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25,25))
        self.image.fill((255,0,0))
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
         self.rect.centery = random.randint(0,480)

def game():
    pygame.display.set_caption("Game")
    
    background = pygame.Surface(screen.get_size())
    background.fill((0,0,0))
    screen.blit(background, (0,0))
    
    player = Player()
    enemy = {Enemy(),Enemy(),Enemy()}
    
    freindSprites = pygame.sprite.Group(player)
    enemySprites = pygame.sprite.Group(enemy)
    
    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        clock.tick(30)
        #pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                
        #check collisions       
        hitEnemies = pygame.sprite.spritecollide(player, enemySprites, False)
        if hitEnemies:
            for theEnemy in hitEnemies:
                theEnemy.reset()
                
        freindSprites.clear(screen, background)
        enemySprites.clear(screen, background)
        
        freindSprites.update()
        enemySprites.update()
        
        freindSprites.draw(screen)     
        enemySprites.draw(screen)   
        
        pygame.display.flip()
        
def instruction():
    menuFont = pygame.font.SysFont(None, 50)
    label = menuFont.render("Click to Start Game", 1, (255,0,0))
    
    keepGoing = True
    
    clock = pygame.time.Clock()
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                keepGoing = False
        
        screen.blit(label,(screen.get_width()/2-label.get_width()/2,screen.get_height()/2-label.get_height()/2))   
        
        pygame.display.flip()     
    
def main():   
    instruction() 
    game()
    
if __name__ == "__main__":
    main()