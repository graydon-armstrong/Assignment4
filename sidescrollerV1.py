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
        
    def update(self):
        mousex, mousey = pygame.mouse.get_pos()
        self.rect.center = (mousex, mousey)
        
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
    enemy = Enemy()
    
    freindSprites = pygame.sprite.Group(player, enemy)
    
    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        clock.tick(30)
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                
        freindSprites.update()
                
        screen.blit(background, (0,0))
        freindSprites.draw(screen)        
        
        pygame.display.flip()
    
def main():
    game()
    
if __name__ == "__main__":
    main()