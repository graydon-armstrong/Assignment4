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

#set the screen
screen = pygame.display.set_mode((640,480))

#player class is the sprite the user controls
class Player(pygame.sprite.Sprite):
    def __init__(self):
        #initiate variables
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("player.png")
        self.image.convert()
        transcolor = self.image.get_at((1,1))
        self.image.set_colorkey(transcolor)
        self.rect = self.image.get_rect()
        self.rect.centery = screen.get_height()/2
        self.rect.centerx = 100
        self.dy = 5
        
    def update(self):
        #move towards the mouse at a speed of dy
        mousex, mousey = pygame.mouse.get_pos()
        if self.rect.centery < mousey-5 and self.rect.bottom < 410:
            self.rect.centery += self.dy
        elif self.rect.centery > mousey+5 and self.rect.top > 70:
            self.rect.centery -= self.dy
        
#Enemy class is the cars the player has to avoid or they lose a live
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        #initialize sprite variables
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("enemy.png")
        self.image.convert()
        transcolor = self.image.get_at((1,1))
        self.image.set_colorkey(transcolor)
        self.rect = self.image.get_rect()
        self.dx = -(random.randint(10,15))
        self.reset()
        
    #update the position of the enemy
    def update(self):
        self.rect.centerx += self.dx
        if self.rect.centerx < 0:
            self.reset()
            
    #when the enemy comes to the left side of the screen reset it on the right
    def reset(self):
         self.rect.centerx = 640
         self.dx = -(random.randint(10,15))
         self.rect.centery = random.randrange(70,410,36)
         
# A class for the rewards the player collect to get score
class Reward(pygame.sprite.Sprite):
    def __init__(self):
        #initialize the variables for the sprite
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("money.png")
        self.image.convert()
        transcolor = self.image.get_at((1,1))
        self.image.set_colorkey(transcolor)
        self.rect = self.image.get_rect()
        self.dx = -5
        self.reset()
        
    #update the position of the reward
    def update(self):
        self.rect.centerx += self.dx
        if self.rect.centerx < 0:
            self.reset()
            
    #when the reward comes to the left side of the screen reset it on the right
    def reset(self):
         self.rect.centerx = 640
         self.rect.centery = random.randrange(70,410,36)
         
#a class for the road background
class Road(pygame.sprite.Sprite):
    def __init__(self):
        #initialize the sprite variables
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("road.png")
        self.rect = self.image.get_rect()
        self.dx = -15
        self.reset()
        
    #update the position of the road
    def update(self):
        self.rect.left += self.dx
        if self.rect.left <= -1280:
            self.reset() 
    
    #when the road is at the end of the left reset it on the right so it seems continuous
    def reset(self):
        self.rect.left = 0
        
#A class for displaying the score and lives on screen to the player
class Scoreboard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #initialize the lives, score, and the font
        self.lives = 5
        self.score = 0
        self.font = pygame.font.SysFont("None", 50)
        
    #update the number of lives and the score on the screen
    def update(self):
        self.text = "Cars: %d, Score: %d" % (self.lives, self.score)
        self.image = self.font.render(self.text, 1, (255, 0, 0))
        self.rect = self.image.get_rect()

#A method that controls the Gameplay Screen
def game():
    #change the caption on the game window
    pygame.display.set_caption("Race Car Driver")
    
    #setup the background
    background = pygame.Surface(screen.get_size())
    background.fill((0,0,0))
    screen.blit(background, (0,0))
    
    #initialize the sprites
    player = Player()
    road = Road()
    enemy = {Enemy(),Enemy(),Enemy()}
    reward = {Reward(),Reward(),Reward()}
    scoreboard = Scoreboard()
    
    #add the sprites to groups
    freindSprites = pygame.sprite.Group(road)
    playerSprites = pygame.sprite.Group(player)
    rewardSprites = pygame.sprite.Group(reward)
    enemySprites = pygame.sprite.Group(enemy)
    scoreDisplay = pygame.sprite.Group(scoreboard)
    
    #create the game loop at 30 FPS with quit options
    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                
                
        #check collisions with enemies    
        hitEnemies = pygame.sprite.spritecollide(player, enemySprites, False)
        if hitEnemies:
            for theEnemy in hitEnemies:
                #if the lives are greater than one remove a live aznd reset the enemy
                if scoreboard.lives > 1:
                    scoreboard.lives -= 1
                    theEnemy.reset()
                #else end the game
                else:
                    keepGoing = False
                
        #check collision with the rewards and add score if hit
        hitRewards = pygame.sprite.spritecollide(player, rewardSprites, False)
        if hitRewards:
            for theReward in hitRewards:
                scoreboard.score += 50
                theReward.reset()
                
        #clear the sprites from the last frame
        freindSprites.clear(screen, background)
        playerSprites.clear(screen, background)
        rewardSprites.clear(screen, background)
        enemySprites.clear(screen, background)
        scoreDisplay.clear(screen, background)
        
        #run the update function of all the sprites
        freindSprites.update()
        playerSprites.update()
        rewardSprites.update()
        enemySprites.update()
        scoreDisplay.update()
        
        #draw all the sprites to the screen
        freindSprites.draw(screen) 
        playerSprites.draw(screen)
        rewardSprites.draw(screen)   
        enemySprites.draw(screen)   
        scoreDisplay.draw(screen) 
        
        #flip the screen to the user
        pygame.display.flip()
    #return the score at the end of the game screen
    return scoreboard.score

#A method for the game start screen
def instruction():
    #set the menu font
    menuFont = pygame.font.SysFont(None, 50)
    
    #create the text for the screen
    insLabels = []
    instructions = (
    "Race Car Driver",
    "Instructions:  You are a race car,",
    "driver collecting money",
    "And trying to avoid other cars",
    "The longer you last",
    "the higher your score",
    "Click to Start Game"
    )
    
    for line in instructions:
        tempLabel = menuFont.render(line, 1, (255, 0, 0))
        insLabels.append(tempLabel)
    
    #set the game loop for the start screen and have exit and continue checks
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
        
        #blit all the labels to the screen
        for i in range(len(insLabels)):
            screen.blit(insLabels[i], (50, 150 + 30*i))
            
        #flip the screen to the player
        pygame.display.flip()  
        
    #return if the player wants to play
    return donePlaying   
    
#A method for the Game end screen
def scoreScreen(score):
    
    #create a background so that the game screen is covered
    background = pygame.Surface(screen.get_size())
    background.fill((0,0,0))
    screen.blit(background, (0,0))
    
    #create a font and set the labels
    menuFont = pygame.font.SysFont(None, 50)
    label = menuFont.render("You Lose, Score: " + str(score), 1, (255,0,0))
    label2 = menuFont.render("Click to Play Again", 1 ,(255,0,0))
    
    #create a game loop for the game end screen with exits and continue options
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
                
        #display the labels on the screen
        screen.blit(label,(screen.get_width()/2-label.get_width()/2,screen.get_height()/2-label.get_height()/2))
        screen.blit(label2,(screen.get_width()/2-label.get_width()/2,screen.get_height()/2-label.get_height()/2-30))   
        
        #flip the screen to the player
        pygame.display.flip()   
    #return if the user still wants to play
    return donePlaying

#A function that is the main loop that controls movement between the start screen, gameplay screen, and game end screen
def main():   
    score  = 0
    donePlaying = instruction()
    while not donePlaying: 
        score = game()
        donePlaying = scoreScreen(score)
    
#run the main menthod at the start
if __name__ == "__main__":
    main()