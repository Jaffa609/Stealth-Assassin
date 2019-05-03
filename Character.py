import pygame, random

class characters(pygame.sprite.Sprite): #Character class for the sprites which has to inherit the sprite class
    def __init__(self, model, speed): #Constructor method used to allow the class to intialise attributes
        super().__init__()  #Inherits the sprite super class
        
        self.model = model                                                  #Attribute of an object which loads in their model
        self.image = pygame.image.load(self.model + ".png").convert_alpha() #Sets the image of the object as their model which is loaded in, their alpha is converted so transparent pixels from the image are kept
        self.mask  = pygame.mask.from_surface(self.image)                   #Creates a mask for each object for collisions so unique shapes can still have perfect collisions
        self.rect  = self.image.get_rect()                                  #Gets the rectangle of the object

        self.speed = speed                                                  #Attribute for the speed of an object
        self.tempSpeed = self.speed                                         #An attribute which acts as a save for the original speed to revert to if the object's speed is changed during the game
        self.runSpeed = self.speed * 2                                      #Gives the character their sprinting speed
        self.moveSet = [0, 0]

    def moveRight(self, pixels):    #Method for moving the object right taking in by how much the object should move as pixels
        self.rect.x += pixels

    def moveLeft(self, pixels):     #Method for moving the object left taking in by how much the object should move as pixels
        self.rect.x -= pixels

    def moveUp(self, pixels):       #Method for moving the object up taking in by how much the object should move as pixels
        self.rect.y -= pixels

    def moveDown(self, pixels):     #Method for moving the object down taking in by how much the object should move as pixels
        self.rect.y += pixels

    def move(self, guardSet, NPCSet, wallSetGroup):   #Method to move the object to a different location
        if self in guardSet:                        #If the character is in the guard group
            self.rect.x = random.randint(600, 1850)     #Draw the character to start in the middle of the level
        elif self in NPCSet:                        #If the character is the target
            self.rect.x = random.randint(1400, 1850)    #Draw the character to start at the right side of the level
        else:                                       #If the character is the player 
            self.rect.x = random.randint(55, 90)        #Draw the charaacter to start at the left side of the level
        self.rect.y = random.randint(55, 890)           #Draws all the characters randomly between the the top and bottom of the level

        if pygame.sprite.spritecollide(self, wallSetGroup, False, pygame.sprite.collide_mask): #Checks if the position the character is drawn to is in a wall
            self.move(guardSet, NPCSet, wallSetGroup) #If it is in the wall then get new coordinates to draw this sprite

    def setSpeed(self, speed):  #Method for changing the speed of the object
        self.speed = speed

    def checkCollision(self, direction, wallSetGroup, NPCSet): #Method to check if the object collides with the wall so it can prevent objects in walls
        if direction == None:
            direction = self.moveSet
        for move in direction:  #Takes in a list of moves that the object is making
            #Checks what move that is and moves it in that direction.
            if move == "left":
                self.moveLeft(self.speed)
            if move == "right":
                self.moveRight(self.speed)
            if move == "up":
                self.moveUp(self.speed)
            if move == "down":
                self.moveDown(self.speed)
            """
(((self == player in characterSet.sprites() or self in guardSet) and pygame.sprite.spritecollide(self, guardSet, False, pygame.sprite.collide_mask))
            or (self in guardSet and pygame.sprite.spritecollide(self, NPCSet, False, pygame.sprite.collide_mask))
            or
            """
            if pygame.sprite.spritecollide(self, wallSetGroup, False, pygame.sprite.collide_mask):
                #If the move causes the wall and object to collide then that move is reverted
                if move == "left":
                    self.moveRight(self.speed)
                if move == "right":
                    self.moveLeft(self.speed)
                if move == "up":
                    self.moveDown(self.speed)
                if move == "down":
                    self.moveUp(self.speed)
                if self in NPCSet:
                    self.randomMove()
            
    def randomMove(self):
        moveX = [None, "left", "right"]
        moveY = [None, "up", "down"]
        self.moveSet[0] = moveX[random.randint(0,2)]
        self.moveSet[1] = moveY[random.randint(0,2)]

    """
    def detectionCone(self):
        self.cone = pygame.image.load("detection.png").convert_alpha()
        self.coneMask = pygame.mask.from_surface(self.cone)
    """

    def killTarget(self, characterSet, NPCSet, target):
        if pygame.sprite.collide_mask(self, target) and target in characterSet.sprites():
            bloodyTarget = characters("bloodyTarget", 0)
            bloodyTarget.rect.x, bloodyTarget.rect.y = target.rect.x, target.rect.y
            pygame.sprite.Sprite.kill(target)
            characterSet.remove(self)
            characterSet.add(self)
            characterSet.add(bloodyTarget)
            return True
