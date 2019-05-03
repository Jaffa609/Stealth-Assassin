import pygame, random

class wall(pygame.sprite.Sprite):   #Wall class for the wall which inherits the sprite class 
    def __init__(self, model): #Constructor method used to allow the class to intialise attributes
        super().__init__() #Inherits the sprite super class
        
        self.model = model                                                  #Attribute of an object which loads in their model
        self.image = pygame.image.load(self.model + ".png").convert_alpha() #Sets the image of the object as their model which is loaded in, their alpha is converted so transparent pixels from the image are kept
        self.mask  = pygame.mask.from_surface(self.image)                   #Creates a mask for each object for collisions so unique shapes can still have perfect collisions
        self.rect  = self.image.get_rect()                                  #Gets the rectangle of the object
        
    def drawEscape(self, wallSetGroup):
        for x in range(1,10000):
            self.rect.x = random.randint(55, 1800)
            self.rect.y = random.randint(55, 860)
            wallList = wallSetGroup.sprites()
            if not pygame.sprite.collide_mask(self, wallList[0]):
                break
            else:
                self.rect.x, self.rect.y = 60, 60
