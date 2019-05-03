#Stealth Assassin
import pygame   #Imports the pygame module inclulding many in built functions that aids in game design
#import time     #Imports the time module for which I can implement delays into my program
import random
import enum     #Imports the enum modle which is way of storing constant values with a name where enumerated constants can be created
from Wall import wall
from Character import characters

pygame.init()                                                                                                   #Runs pygame
pygame.display.set_caption("Stealth Assassin")                                                                  #Sets the title of the pygame window for the game
clock       = pygame.time.Clock()                                                                               #Intialises the variable to control the game clock (FPS)
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)    #Variable which will set the resolution of the game window and put the window into fullscreen mode

clockrate = 3000



class GameState(enum.Enum): #A class for all of the game states the menu/game can be in
    MENU_PLAYQUIT       = 1 #Each of the following is defining a unique value for the state of the game/menu to each of the enumerations
    MENU_DIFFICULTY     = 2 #^
    MENU_LEVELSELECT    = 3 #^
    GAME_PLAYING        = 4 #^
    GAME_OVER           = 5 #^




class ButtonEvent(enum.IntEnum):  # IntEnum so we can convert back to an int for event posting
    QUIT     = pygame.USEREVENT +  1  #Each of the following is defining a unique value for event codes to which the buttons will send back for each of the enumerations
    PLAY     = pygame.USEREVENT +  2  #^
    EASY     = pygame.USEREVENT +  3  #^
    MEDIUM   = pygame.USEREVENT +  4  #^
    HARD     = pygame.USEREVENT +  5  #^
    VETERAN  = pygame.USEREVENT +  6  #^
    LEVEL1   = pygame.USEREVENT +  7  #^
    LEVEL2   = pygame.USEREVENT +  8  #^
    LEVEL3   = pygame.USEREVENT +  9  #^
    LEVEL4   = pygame.USEREVENT + 10  #^
    CALLMENU = pygame.USEREVENT + 11  #^
    RETRY    = pygame.USEREVENT + 12  #^


class Button: #This class contains methods for buttons including display and functionality

    def __init__(self, buttonname, event_code, buttonx, buttony, buttonwidth, buttonheight, textfile, textx, texty): #Constructor method used to allow classes to intialise attributes
        self.buttonname = buttonname                                                    #Name of the button
        self.rect       = pygame.Rect(buttonx, buttony, buttonwidth, buttonheight)      #Creates a rectangle of whatever dimensions and positioning the button that has been accessed is
        self.text_image = pygame.image.load(textfile + ".png")                          #Button Label
        self.textx      = textx                                                         #X-axis positioning of the text
        self.texty      = texty                                                         #Y-axis positioning of the text
        self.event_code = event_code                                                    #The event code to enable game/menu state changes

    def drawButton(self, screen):                               #Method which creates a button for the menu
        pygame.draw.rect(screen, (0, 0, 0), self.rect)          #Draws a rectangular button which is black and given the size and coordinates which were attributes 
        screen.blit(self.text_image, (self.textx, self.texty))  #Displays the text given coordinates
 
    def checkClick(self, mouse_position):                                                                   #Method which checks if the button has ben pressed within the rectangle's area
        """ Check if the given point is inside our button-rectangle.
            If the click was, post a BUTTON_CLICK_EVENT to the PyGame Event queue and return True
            return False otherwise """
        result = False                                                                                      #Assumes the mouse click is not within the given dimensions unless proven otherwise. If the result is false in the end then the program and UI remain unaffected
        print("HERE")
        if self.rect.collidepoint(mouse_position):                                                          #If the mouse-click is inside our rectangle, post a message to the queue
            pygame.event.post(pygame.event.Event(int(self.event_code), {"button_name" : self.buttonname}))  #Posts the enumerated value depending on which game state it is in along with the button name
            result = True                                                                                   #Result is true therfore action can be taken within the program to progress state
        return result                                                                                       #Returns result so its value is known outside this method



class ButtonSet: # A container class for a bunch of buttons
    
    def __init__(self, *buttons): #Constructor method used to allow classes to intialise attributes
        self.buttons = list(buttons) #An attribute containing a list of similar buttons where it can polymorph

    def anyClicked(self, click_location): #Method which checks if the button has been clicked
        result = False                                  #Assumes that the click is not on the button unless proven otherwise, if it is false in the end then the program remains unchanged
        for b in self.buttons:                          #Iterates through all of the buttons in the list to check if they are clicked upon 
            if b.checkClick(click_location) == True:    #Inherits the method checkClick from button and then sees if the button has been clicked
                result = True                           #Result is true so that particular button can be identified as being clicked    
        return result                                   #Returns the result so the value can be understood outside of the method and class

    def draw(self, screen):         #Method to draw all the necessary buttons to the screen
        for b in self.buttons:      #Iterates through each of the buttons in the necessary set
            b.drawButton(screen)    #Draws each of the buttons from the set to the screen

"""
    def addButton(self, b): #Method to add a new button to the set if need be
        #Add a new button to out set, but not if we have it already
        if b not in self.buttons: #Checks first the new button doesn't exist in the set
            self.buttons.append(b) #Adds the button to the set
"""




class DisplayImage: #This class contains methods required to load images into the game
    
    def __init__(self, image):  #Constructor method used to allow the class to intialise attributes
        self.image = pygame.image.load(image + ".png").convert_alpha() #Defines filename as the filename attribute passed through

    def LoadImage(self, xpos, ypos): #This method will load images into the game displaying them
        screen.blit(self.image, (xpos, ypos))  #Image is displayed to coordinates which were attributes that were defined prior
        




Background          = DisplayImage('Background')            #This object is the background to the menu
AssassinModel       = DisplayImage('Assassin')              #This object is the assassin model displayed in the menu
ButtonBox           = DisplayImage('ButtonBox')             #This object is the box that contains where the buttons are in the menu
StealthAssassinText = DisplayImage('StealthAssassinText')   #This object is the text that displays the title on the menu
ResultBox           = DisplayImage('ResultBox')
WinText             = DisplayImage('win')
LoseText            = DisplayImage('loss')
LevelHUD            = DisplayImage('level')

Background          .LoadImage(0,0)     #Loads background through class and methods
AssassinModel       .LoadImage(988,532) #Loads the assassin model through class and methods
ButtonBox           .LoadImage(63,424)  #Loads button box through class and methods
StealthAssassinText .LoadImage(60,124)  #Loads the text for the menu through the class and methods


PlayButton = Button('playbutton',   ButtonEvent.PLAY,  133,477,756,223,'Playtext',387,545) #Creates play button      
QuitButton = Button('quitbutton',   ButtonEvent.QUIT,  133,731,756,223,'Quittext',387,806) #Creates quit button
play_quit_buttons = ButtonSet(PlayButton, QuitButton) #Creates a button set for the first stage of the menu

EasyButton    = Button('easybutton',    ButtonEvent.EASY,     133,477,362,223, 'Easytext',    214,548)  #Creates easy button
MediumButton  = Button('mediumbutton',  ButtonEvent.MEDIUM,   533,477,362,223, 'Mediumtext',  560,548)  #Creates medium button
HardButton    = Button('hardbutton',    ButtonEvent.HARD,     133,731,362,223, 'Hardtext',    214,806)  #Creates hard button
VeteranButton = Button('veteranbutton', ButtonEvent.VETERAN,  533,731,362,223, 'Veterantext', 537,806)  #Creates veteran button
difficulty_buttons = ButtonSet(EasyButton, MediumButton, HardButton, VeteranButton) #Creates a button set for the difficulty stage of the menu

OneButton   = Button('onebutton',   ButtonEvent.LEVEL1, 133,477,362,223, 'Onetext',  287,550)   #Creates the level 1 button
TwoButton   = Button('twobutton',   ButtonEvent.LEVEL2, 533,477,362,223, 'Twotext',  693,550)   #Creates the level 2 button
ThreeButton = Button('threebutton', ButtonEvent.LEVEL3, 133,731,362,223, 'Threetext',285,810)   #Creates the level 3 button
FourButton  = Button('fourbutton',  ButtonEvent.LEVEL4, 533,731,362,223, 'Fourtext', 685,810)   #Creates the level 4 button
level_buttons = ButtonSet(OneButton, TwoButton, ThreeButton, FourButton) #Creates a button set for the level selection stage of the menu

CallMenuButton = Button('menuButton',  ButtonEvent.CALLMENU, 670, 744,250,128, 'menuText',  744, 793)
RetryButton    = Button('retryButton', ButtonEvent.RETRY,    1000,744,250,128, 'retryText', 1067,789)
gameOver_buttons = ButtonSet(CallMenuButton, RetryButton)


wallSet1 = wall("WallSet1") #Creates the object which will be the level 1 inner walls
wallSet2 = wall("WallSet2")
wallSet3 = wall("WallSet3")
wallSet4 = wall("WallSet4")
wallSetGroup = pygame.sprite.Group() #Creates a group for the wall sets which will test collision against characters

characterSet = pygame.sprite.Group() #Creates a group for all the characters to test collision against the walls
NPCSet = pygame.sprite.Group() #Creates a group for all the non playable characters to generate their positions seperate to the player

target = characters("target", 1) #Creates the target object
characterSet.add(target) #Adds the target into the character group
player = characters("player", 2) #Creates the object which is the player that the user plays as
characterSet.add(player) #Adds the player into the group

guardSet = pygame.sprite.Group() #Creates a seperate group from characters for the guards so they can be tested as a group against the player
guard1 = characters("guard", 1)
guard2 = characters("guard", 1)
guard3 = characters("guard", 1)
guard4 = characters("guard", 1)
guard5 = characters("guard", 1)
guard6 = characters("guard", 1)
guardSet.add(guard1, guard2, guard3, guard4, guard5, guard6)



game_state  = GameState.MENU_PLAYQUIT   #The game state is set to be the first one                         
done        = False                     #The game loop's conditions meet to iterate until stated otherwise

while not done: #Game loop

    for event in pygame.event.get():    #Retrieves the events as the program runs
        if event.type == pygame.QUIT:   #Checks if the event was to quit out of pygame
            done = True                 #Exits the game loop
            
        elif event.type == pygame.MOUSEBUTTONUP:    #If the mouse has been clicked and released
            click_location = pygame.mouse.get_pos() #Gets the coordinates of the mouse

            # send the mouse-click location to the correct button-set depending on the state
            if game_state == GameState.MENU_PLAYQUIT:           #If the game is within the first stage
                play_quit_buttons.anyClicked(click_location)    #Uses the play and quit button set to check if either were clicked
                
            elif game_state == GameState.MENU_DIFFICULTY:       #If the game is within the difficulty stage
                difficulty_buttons.anyClicked(click_location)   #Uses the difficulty button set to check if any of these were clicked
                
            elif game_state == GameState.MENU_LEVELSELECT:      #If the game is within the level selection stage
                level_buttons.anyClicked(click_location)        #Uses the level button set to check if any of these buttons were clicked
                
            elif game_state == GameState.GAME_PLAYING:          #If the game is currently being played (out of menu)
                pass
            
            elif game_state == GameState.GAME_OVER:             #If the game has been finished
                gameOver_buttons.anyClicked(click_location)



        elif event.type == ButtonEvent.QUIT:                                                                    #If the event posted back was to quit the program
            done = True                                                                                         #Exits the game loop
            
        elif event.type == ButtonEvent.PLAY:                                                                    #If the event posted back was to proceed through the menu
            game_state = GameState.MENU_DIFFICULTY                                                              #The game state has now progressed onto the difficulty stage
            
        elif event.type in [ButtonEvent.EASY, ButtonEvent.MEDIUM, ButtonEvent.HARD, ButtonEvent.VETERAN]:       #If the event posted back was to do with the difficulty
            game_state = GameState.MENU_LEVELSELECT         #The game state should progress again onto the level selection
            # NOTE: This could be simpler with a dictionary of { event : difficulty-level }
            
            if event.type == ButtonEvent.EASY:              #If the event posted back was for the easy difficulty
                game_difficulty = 1                         #The game difficulty is set to 1
                
            elif event.type == ButtonEvent.MEDIUM:          #If the event posted back was for the easy difficulty
                game_difficulty = 2                         #The game difficulty is set to 2
                
            elif event.type == ButtonEvent.HARD:            #If the event posted back was for the easy difficulty
                game_difficulty = 3                         #The game difficulty is set to 3
                
            elif event.type == ButtonEvent.VETERAN:         #If the event posted back was for the easy difficulty
                game_difficulty = 4                         #The game difficulty is set to 4

            for guard in range(0,(game_difficulty+2)):
                guardList = guardSet.sprites()
                guardX = guardList[0]
                guardX.kill()
                
            for guard in guardSet.sprites():
                characterSet.add(guard)

            for character in characterSet.sprites(): #Loops through all the sprites in the character group
                if character == player: #If the character is the player
                    pass #Do nothing with it (skip adding it into the NPC group)
                else: #If not the player
                    NPCSet.add(character) #Add the charcter into the non playable character group
                    
        elif event.type in [ButtonEvent.LEVEL1, ButtonEvent.LEVEL2, ButtonEvent.LEVEL3, ButtonEvent.LEVEL4]:    #If the event posted back was to do with the level selection
            game_state = GameState.GAME_PLAYING             #The game state can be progressed into the game now

            if event.type == ButtonEvent.LEVEL1:            #If the event posted back was for level 1
                game_level = 1                              #The game level is set to 1
                wallSetGroup.add(wallSet1)
            elif event.type == ButtonEvent.LEVEL2:          #If the event posted back was for level 2
                game_level = 2                              #The game level is set to 2
                wallSetGroup.add(wallSet2)
                
            elif event.type == ButtonEvent.LEVEL3:          #If the event posted back was for level 3
                game_level = 3                              #The game level is set to 3
                wallSetGroup.add(wallSet3)
                
            elif event.type == ButtonEvent.LEVEL4:          #If the event posted back was for level 4
                game_level = 4                              #The game level is set to 4
                wallSetGroup.add(wallSet4)

            for character in characterSet: #For all the characters in the group
                character.move(guardSet, NPCSet, wallSetGroup) #Gives all the characters a starting position        
            LevelHUD.LoadImage(0,0)
            #pygame.time.set_timer(pygame.USEREVENT, (random.randint(1,5)*1000))

        elif event.type in [ButtonEvent.CALLMENU, ButtonEvent.RETRY]:
            print("YAS")
            if event.type == ButtonEvent.CALLMENU:
                import menu
            if event.type == ButtonEvent.RETRY:
                game_state = GameState.GAME_PLAYING 
                
    if game_state == GameState.MENU_PLAYQUIT:       #Checks if the game state is in the play and quite phase
        ButtonBox.LoadImage(63,424)                 #Redraws the button box to hide previous buttons
        play_quit_buttons.draw(screen)         #Draws the play and quit buttons from their button set
        
    elif game_state == GameState.MENU_DIFFICULTY:   #Checks if the game state is in the difficulty phase
        ButtonBox.LoadImage(63,424)                 #Redraws the button box to hide previous buttons
        difficulty_buttons.draw(screen)        #Draws the difficulty buttons from their button set
        
    elif game_state == GameState.MENU_LEVELSELECT:  #Checks if the game state is in the level selection phase
        ButtonBox.LoadImage(63,424)                 #Redraws the button box to hide previous buttons
        level_buttons.draw(screen)              #Draws the level buttons from their button set
        
    elif game_state == GameState.GAME_PLAYING:      #Checks if the game state is in the game playing phase
        keys = pygame.key.get_pressed() #Fetches all the keys that have been pressed within the clock
        if event.type == pygame.USEREVENT or event.type == pygame.KEYDOWN:
            for self in NPCSet:
                self.randomMove()
            #pygame.time.set_timer(pygame.USEREVENT, (random.randint(1,5)*1000))
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]: #If pygame is quit or the escape key is pressed
            done = True #The boolean for the game loop is now false so the loop ends

        moveSet = [] #List for the moves pressed within the clock by the player which will be appended
        
        if keys[pygame.K_LEFT]: #If the left arrow key is pressed
            moveSet.append("left") #The 'left' move is added into the list
            
        if keys[pygame.K_RIGHT]: #If the right arrow key is pressed
            moveSet.append("right") #The 'right' move is added into the list
                
        if keys[pygame.K_UP]: #If the up arrow key is pressed
            moveSet.append("up") #The 'up' move is added into the list

        if keys[pygame.K_DOWN]: #If the down arrow key is pressed
            moveSet.append("down") #The 'down' move is added into the list

        for self in NPCSet:
            self.checkCollision(self.moveSet, wallSetGroup, NPCSet)

        player.checkCollision(moveSet, wallSetGroup, NPCSet) #Takes in the moves made by the user and checks if they are valid moves, if so then the player moves 

        if keys[pygame.K_LSHIFT]: #If the left shift key is pressed
            player.setSpeed(player.runSpeed) #The player moves faster
        else:
            player.setSpeed(player.tempSpeed) #The player reverts back to their original speed if the key is not pressed

        if player.killTarget(characterSet, NPCSet, target):
            escape = wall("escape")
            escapeGroup = pygame.sprite.Group(escape)
            escape.drawEscape(wallSetGroup)

        try:
            if pygame.sprite.collide_mask(player, escape):
                gameResult = "win"
                game_state = GameState.GAME_OVER
        except:
            pass
            
        LevelHUD.LoadImage(0,0)
        wallSetGroup.draw(screen)   #Redraws the innerwalls
        try:
            escapeGroup.draw(screen)
        except:
            pass
        characterSet.draw(screen)   #Redraws all sprites with any updates
            
        
    elif game_state == GameState.GAME_OVER:         #Checks if the game state is finished from the game
        ResultBox.LoadImage(560,102)
        if gameResult == "win":
            WinText .LoadImage(673,240)
        elif gameResult == "loss":
            LoseText.LoadImage(238,162)
        gameOver_buttons.draw(screen)

    pygame.display.flip()                           #Updates the pygame screen with anything drawn
    clock.tick_busy_loop(clockrate)                 #Limit FPS


pygame.quit()                                       #Quits out of pygame
