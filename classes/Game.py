import sys
import pygame
import pathlib
import random

from typing import TypedDict
import json
from math import inf

from classes.BlocObject import BlocObject
from classes.Player import Player
from classes.Monster import Monster
from classes.Size import Size
from classes.Floor import Floor
from classes.Position import Position
from classes.Weapon import Weapon
from classes.PickableObject import PickableObject
from classes.Money import Money
from classes.MovementPotion import MovementPotion
from classes.LifePotion import LifePotion
from classes.Coffre import Coffre
from classes.OpenableObject import OpenableObject
from classes.Vector import Vector
from classes.Event import Event
from classes.EarthQuake import EarthQuake
from classes.AcidRain import AcidRain
from classes.Innondation import Innondation
from classes.Tornado import Tornado

class Game:
    score: int
    isplaying: bool
    floorList: list[Floor]
    currentFloorIndex: int
    currentFloor: Floor
    status: str
    player: Player

    # Status :
    # PlayerTurn : Waiting for player to choose an action
    # PlayerMovement : Waiting for player to choose a cell for movement
    # PlayerAttack : Waiting for player to choose a cell for attack
    # MonsterTurn

    def __init__(self):
        with open('data/weapons.json','r', encoding='utf-8') as dataFile:
            data = dataFile.read()
            weaponsJson = json.loads(data)

        weapons = {}
        for weaponName,weaponValue in weaponsJson.items():
            weapons[weaponName] = Weapon(weaponName, **weaponValue)
        #print(weapons)

        # define is the game has begin

        self.isplaying = False

        self.floorList = []
        #initialisation of floors
        floors_count = 0 # count the number of floors to create by counting files in assets/floors
        for path in pathlib.Path("./assets/floors").iterdir():
            #add the floor in the list
            if (floors_count == 1 or floors_count== 3 or floors_count== 4) :
                condition_ = "allMoney"
            elif (floors_count== 0 or floors_count==5  or floors_count== 6):
                condition_ = "allPotionPicked"
            elif (floors_count == 7):
                condition_ = "survive10"
            else :
                condition_ = "allMonsterkilled"

            self.floorList.append(Floor(name='Floor ' + str(floors_count ), refImg="./"+ str(path), condition = condition_))
            if path.is_file():
                floors_count += 1

        self.currentFloorIndex = 0
        self.currentFloor = self.floorList[self.currentFloorIndex]


        self.score = 0

        # generate the player
        self.player = Player(movementPoints=3, weapon=weapons['Light saber'])
        self.currentFloor.SetNewObject(self.currentFloor.elevatorDOWN, self.player)
        self.currentweapon = self.player.weapon

        # boutons
        self.button_attack = pygame.Rect(710, 630, 50, 20)
        self.button_mvt = pygame.Rect(650, 630, 50, 20)
        self.button_finir = pygame.Rect(770, 630, 50, 20)
        self.button_armes = pygame.Rect(830, 630, 50, 20)
        self.button_annuler = pygame.Rect(890, 630, 50, 20)
        self.quit_bag_button = pygame.Rect(500, 500, 70, 40)

        self.help_button = pygame.Rect(1000, 0, 80, 40)
        self.quit_help_button = pygame.Rect(500, 500, 70, 40)
        self.help_next_button = pygame.Rect(700, 500, 70, 40)

        self.button_let_go_weapon = pygame.Rect(680, 490, 70, 30)

        replay_button = pygame.image.load('assets/Replay.png')
        self.replay_button = pygame.transform.scale(replay_button, (400, 150))
        self.replay_button_rect = replay_button.get_rect()

        # const needed to draw the map
        self.ecart = 3
        self.top_left_x = 60
        self.top_left_y = 110
        self.large_max_grille = 450

        self.larg_case = (self.large_max_grille - ((self.currentFloor.size.width + 1) * self.ecart)) / self.currentFloor.size.width
        self.long_case = (self.large_max_grille - ((self.currentFloor.size.height + 1) * self.ecart)) / self.currentFloor.size.height

        # var to know where we are in the game
        self.turn = 0
        self.status = "PlayerTurn"
        self.has_moved = False
        self.has_attacked = False
        self.won = False
        self.message = " Welcome to a new Floor "
        self.running = True
        self.gameOver= False

        self.bagisopen = False
        self.bag = {'Light saber':weapons['Light saber']}
        self.taillebag = 13
        self.weaponTab = weapons

        self.isAOpenableShowed = False
        self.currentOpenable = None

        self.memorize()

        #Boutique

        self.boutiqueisopen = False
        self.boutique = [EarthQuake(), AcidRain(), Innondation(), Tornado()]
        self.button_buy_event = pygame.Rect(680, 490, 70, 30)
        self.currentEvent = self.boutique[0]
        self.quit_boutique_button = pygame.Rect(500, 500, 70, 40)
        self.eventToExecute =  pygame.sprite.Group()
        self.boutiqueMessage = "Bienvenue dans la boutique"

        # Help
        self.indice_txt_help = 0
        self.helpisopen = False
        self.help_txt = [
                         ["",
                          "Welcome ! ",
                          "",
                          "Here is the summary of what you can found is this tutorial :"
                          "",
                          "- Page 1 : The synopsis and aim of the game",
                          "- Page 2 : How to move and attack",
                          "- Page 3 and 4 : Everything about weapons",
                          "- Page 5: Descriptions of objects you will see",
                          "- Page 6 : How to go to the next floor",
                          "- Page 7 : How to open trunck",
                          "- Page 8 : How to buy events",
                          "- Page 9 : Where do the monsters attack ? ",
                          "- Page 10 : keyboard shortcuts to know",
                          "- Page 11 : Good luck"],

                         ["Welcome in the spaceship. You're the only humain survivor in there. ",
                          "Your aim is to survive, for that you have to join the emergency ",
                          "ejection ship. Unfortunately this is at the last floor of the ship ",
                          "and you are only at the floor 0...",
                          "So your aim is to go up and upper and finally arrived at the top. ",
                          "",
                          "To go to the upper level you have to : ",
                          "         - survive",
                          "         - open the lift by fullfilling the aim",
                          "         - go to the up elevator (represented by a pink box)",
                          "",
                          "You can do a lot of things on every round ",
                          "     - Choose a movement ",
                          "     - Choose to attack with a weapon that you picked in your bag",
                          "     - Open things if you are on it",
                          "     - Buy event in the store ",
                          "",
                          " DO NOT FORGET TO END THE TURN : RETURN KEY OR END BUTTON"
                          ],


                         [
                          "HOW TO MOVE : ",
                          "To choose a movement click on the movement button on the ",
                          "bottom right (or M) and click on the place you want to go to",
                          "if the way is red you don't have enough movement points",
                          "so your movement will not be valid, you will have to ",
                          "choose again.",
                          "",
                          "HOW TO ATTACK : ",
                           "To choose an attack click on the attack button on the ",
                          "bottom right (or A) and click on the place you want to make",
                          "the attack if the are no impacts appearing the attack ",
                          "is not valid, you will have to choose again",
                             "",
                             " DO NOT FORGET TO END THE TURN : RETURN KEY OR END BUTTON"
                          ],
                        ["HOW TO USE YOUR WEAPON : ",
                         "You can use your weapon when you are attacking. After",
                         "clicking on A or on the attack button during your turn",
                         "you are invited to choose where you want to attack",
                         "you can't attack everywhere, you can attack horizontally",
                         "or vertically. The number of box max between you and your",
                         "attack is define in the propertie of the weapon. Next thing",
                         "you have to know is that weapons have two very important ",
                         "caracteristics : the attack pattern who shown the damages ",
                         "caused and the push pattern who show the places where objects",
                         "are going to be propelled away."
                        "",
                         "HOW TO KNOW YOUR WEAPON PROPERTIES :",
                         "Go into your bag and look at the right pannel giving ",
                         "some infos on your current weapon."],


                        ["HOW TO CHANGE WEAPONS :",
                         "To change your current weapon go in your bag by clicking on ",
                         "the bag button or the B key and choose between the weapons ",
                         "you have. ",
                         "",
                         "HOW TO GET MORE WEAPONS : ",
                         "To have more weapons you have to open somme trunk.",
                         "Be careful your bag has limited place, sometimes you'll have",
                         "to drop some of your weapons to grap some more.",
                         "The only one you can't drop if your original weapon."
                         "",
                         ],

                        ["OBJECT THAT YOU CAN FIND ON THE MAP : ",
                         "- Money : when you pick a coin you earn 5 local currency",
                         "- Purple movement potion : when you pick it you earn",
                         "one more movement point, so you can move further ",
                         "- Green life potion : when you pick it your life is  ",
                         "augmented.",
                         "- Wall : can not be picked and you can't go throught them",
                         "but you can break them",
                         "- Trunk : countains object that you can pick up"
                         ],
                        ["HOW TO GO TO THE UPPER FLOOR :",
                         "To go to the upper floor you first have to unlock the lift.",
                         "For that you have to fill the floors aim that you can see on ",
                         "bottom right box of your pannel gaim.",
                         "For examples the aim : kill all monsters indicate that every",
                         "monsters have to be dead to unlock the access to the up lift.",
                         "Once the lift is unlock you can go into it by standing on the ",
                         "pink / light purple box. You will directly arrived at the next ",
                         "floor. If you arrived at the last one you won the game. "

                         ],
                        ["HOW TO SEE WHAT IS IN A TRUNK : ",
                         "To see what is is the trunk click on the P key and to close ",
                         "that view click on the I key",
                         "",
                         "HOW TO OPEN A TRUNK :",
                         "Now that you saw what is inside the trunk you can choose to ",
                         "open it and pick up everything by clicking the O key. Be careful",
                         "once you decided to open it everything is picked. So choose the ",
                         "good time. Opening a trunk full of life potion when your life is ",
                         "full or open a trunk with powerfull weapons when you don't have ",
                         "anymore in your bag are not clever choices. ",
                         "",
                         "The trunk are created randomly so if you replay the game they will",
                         "change"],


                          [
                            "HOW TO BUY EVENTS :",
                            "If you want to make more attacks or if some monsters are",
                            "not accessible you can buy events that will be played at",
                            "the end of your turn.",
                            "To buy them you have to click on the S key and then choose",
                            "which one you want to buy. You can buy up to three events",
                            "per round. The events you have bought will be visible on ",
                            " the bottom right box of the pannel game.",
                              "",
                              " DO NOT FORGET TO END THE TURN : RETURN KEY OR END BUTTON"
                          ],

                        ["HOW TO KNOW WHERE THE MONSTER ATTACK :",
                         "During your turn you can see buy impacts and colors where",
                         "the monsters are going to attack next"],

                        ["Keyboard shortcut to know: ",
                             "RETURN -> End your turn",
                             "BACKSPACE -> To annul the current action",
                             "A -> To choose an attack",
                             "B -> to open the bag where are the weapons",
                             "M -> To choose a movement",
                             "O -> to open something at your position",
                             "P -> to show what is inside the object at your position",
                             "I -> close the preview of what is inside an object",
                             "S -> to open the store to buy event "],

                         [" Good luck"]


                         ]





        # TEST A ENLEVER


        # self.spawn_monster(position=Position(4, 4), movementPoints=5, healthPoints=5, weapon=self.weaponTab['TEST WEAPON'])

        self.current_monster = self.currentFloor.lastMonsterAdded
        self.init_sprite_size()


        self.weaponTab = weapons

    # -------------------------------------------------------------------------------------------------------------------
    # MAIN FONCTION
    # -------------------------------------------------------------------------------------------------------------------

    def update(self, screen):

        # update affichage et update var
        self.elevatorOpen = self.currentFloor.is_condition_fullfilled(self.turn)
        self.draw_everything(screen)
        self.running = True
        self.won = False
        self.arrivedAtElevator = (self.player.position == self.currentFloor.elevatorUP)
        self.currentFloor.checkEveryoneAlive()
        self.gameOver = (self.player.healthPoints<=0)

        if self.arrivedAtElevator and self.elevatorOpen:
            self.goToNextLevel();

        # deal with the bag is open
        if self.bagisopen:
            self.dealWithOpenBag(screen)
        elif self.helpisopen:
            self.dealWithOpenHelp(screen)
        # deal with the boutique open
        elif self.boutiqueisopen:
            self.dealWithOpenBoutique(screen)
        # deal with the situation of winning
        elif self.won :
            self.dealWithWon(screen)

        elif self.gameOver:
            self.dealWithGameOver(screen)

        # deal with the action in the pannel Game, out of the bag and not in a winning situation
        else :
            self.dealWithActionPannelGame(screen)


        if self.status == "MonsterTurn":
            self.monsterTurn()
            #print(self.currentFloor)

        #pre shot the movement
        if self.status == "PlayerMovement":
            self.preShowMovement(screen)
        
        if self.status == "PlayerAttack":
            self.preShowAttack(screen)


        return self.running

    # -------------------------------------------------------------------------------------------------------------------
    # ACTION GESTION
    # -------------------------------------------------------------------------------------------------------------------

    def wantToAttack(self):
        print("vous avez appuy?? sur le bouton attack")
        # check if the player has already attacked during this turn
        if self.has_attacked == False:
            self.status = "PlayerAttack"
            self.message = " Choose where to attack"
        else:
            print("Vous avez deja attaquer vous ne pouvez plus")
            self.message = " You already attacked "
    def wantToOpenTheBag(self):
        print("choose your weapon")
        self.bagisopen = True

    def wantToOpenHelp(self):
        print("help section")
        self.helpisopen = True
    def wantToOpenTheBoutique(self):
        print("Open the boutique")
        self.boutiqueisopen = True
        self.boutiqueMessage = "Welcome in the store"
    def wantToAnnul(self):
        print("Vous avez annul?? l'action")
        self.message = " you cancelled the action"
        self.status = "PlayerTurn"
    def wantToEndTurn(self):
        for event in self.eventToExecute:
            event.appendOnTheFloor(self.currentFloor)
            self.eventToExecute.remove(event)


        print("you pressed end turn")
        self.message = " End of your turn, monsters attacking "
        # Put the variable back to normal
        self.has_moved = False
        self.has_attacked = False
        # Begin the monster turn
        self.status = "MonsterTurn"
        # increase the turn count
        self.turn = self.turn + 1
    def wantToChoseMouvement(self):
        print("you pressed mvt")
        # check if the player has already moved during this turn
        if self.has_moved == False:
            self.message = " Choose where to move"
            self.status = "PlayerMovement"
        else:
            print("you already moved you can't do it twice")
            self.message = " You already moved "

    def replay(self, floorIndex):
        self.player.healthPoints = self.player.maxHealthPoints
        self.player.money = self.memory['money']
        self.bag = self.copie_bag(self.memory['bag'])
        self.score= self.memory['score']
        if (self.memory['mvtPoint'] >4):
            self.player.movementPoints = 4
        else :
            self.player.movementPoints = self.memory['mvtPoint']



        self.currentFloorIndex = floorIndex
        self.currentFloor = self.floorList[self.currentFloorIndex]
        self.currentFloor.replay()
        self.currentFloor.SetNewObject(self.currentFloor.elevatorDOWN, self.player)
        self.larg_case = (self.large_max_grille - (
                (self.currentFloor.size.width + 1) * self.ecart)) / self.currentFloor.size.width
        self.long_case = (self.large_max_grille - (
                (self.currentFloor.size.height + 1) * self.ecart)) / self.currentFloor.size.height
        self.turn = 0
        self.has_moved = False
        self.has_attacked = False
        self.message = " Welcome to this Floor "
        self.currentweapon = self.bag['Light saber']
        self.isAOpenableShowed = False
        self.currentOpenable = None


        self.init_sprite_size()
        self.memorize()




# Put the memory on date to save the state of the game
    def memorize(self):
        self.memory = {'money': self.player.money,
                       'bag': self.copie_bag(self.bag),
                       'score': self.score,
                       'mvtPoint' : self.player.movementPoints}

    def copie_bag(self, bag):
        newBag = bag.copy()
        return newBag




    # -------------------------------------------------------------------------------------------------------------------
    # DECOUPE FONCTION UDATE
    # -------------------------------------------------------------------------------------------------------------------

    def dealWithGameOver(self, screen):
        self.draw_gameOver(screen)
        print("GameOver")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                print("good bye")
                # Deal with click if we are in the Game Over
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:

                if self.replay_button_rect.collidepoint(pygame.mouse.get_pos()):
                    self.replay(self.currentFloorIndex)

    def dealWithWon(self,screen):
        self.draw_won(screen)
        print("You won!")

    def dealWithOpenBag(self, screen):
        self.draw_bag(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                print("good bye")
            # Deal with click if we are in the bag
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                print("you clicked in the bag")

                if self.button_let_go_weapon.collidepoint(pygame.mouse.get_pos()):
                    self.letGo(self.currentweapon)

                for arme in self.bag:
                    if self.bag[arme].button.collidepoint(pygame.mouse.get_pos()):
                        print("You clicked on the weapon : " + self.weaponTab[arme].name)
                        self.currentweapon = self.weaponTab[arme]
                        self.player.weapon = self.weaponTab[arme]

                # Detect if the player push the end turn button
                if self.quit_bag_button.collidepoint(pygame.mouse.get_pos()):
                    print("you left the bag")
                    # Put the variable back to normal
                    self.bagisopen = False

    def dealWithOpenHelp(self, screen):
        self.draw_help(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                print("good bye")

            # Deal with click if we are in the help
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                print("you clicked in the help")



                # Detect if the player push the quit button
                if self.quit_help_button.collidepoint(pygame.mouse.get_pos()):
                    print("you left the help")
                    # Put the variable back to normal
                    self.helpisopen = False
                    self.indice_txt_help = 0

                if self.help_next_button.collidepoint(pygame.mouse.get_pos()):
                    # change the text
                    self.indice_txt_help = (self.indice_txt_help + 1) % len(self.help_txt)
    def dealWithOpenBoutique(self, screen):

        self.draw_boutique(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                print("Good bye")
            # Deal with click if we are in the boutique
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                print("you clicked in the boutique")

                if self.button_buy_event.collidepoint(pygame.mouse.get_pos()):
                    self.buy_event(self.currentEvent)

                for i in range(0, len(self.boutique)):
                    if self.boutique[i].button.collidepoint(pygame.mouse.get_pos()):
                        print("You clicked on the event: " + self.boutique[i].name)
                        self.currentEvent= self.boutique[i]

                # Detect if the player push the quit boutique button
                if self.quit_boutique_button.collidepoint(pygame.mouse.get_pos()):
                    print("you left the store")
                    # Put the variable back to normal
                    self.boutiqueisopen = False

    def dealWithActionPannelGame(self, screen):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                print("Goodbye")
               # Deal with click if we are in the game pannel
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:

                if self.status == "PlayerTurn":
                    print("It's player's turn")
                    self.message = " Your turn !"

                if self.button_annuler.collidepoint(pygame.mouse.get_pos()):
                    self.wantToAnnul()

                # The player is moving
                if self.status == "PlayerMovement" :
                    path = self.currentFloor.Pathfinder(self.player.position, self.MouseBoardPosition())
                    pathLength = self.currentFloor.PathLength(path)
                    if pathLength <= self.player.movementPoints:

                        self.currentFloor.UpdatePlayer(self.player, self.MouseBoardPosition())
                        self.has_moved = True

                        print("You choosed a movement")
                        self.message = " You choosed a movement"
                        self.status = "PlayerTurn"
                    else :
                        print("Non valid movement, try again")
                        self.message = " Non valid movement, try again"




                # The player is attacking
                if self.status == "PlayerAttack" :
                    vector = self.MouseBoardPosition() - self.player.position
                    pattern = self.player.weapon.GetAttackPattern()
                    attackValid = False
                    if vector.CollinearToAxis():
                        if "distance" in pattern:
                            if abs(vector) <= pattern["distance"]:
                                attackValid = True

                    if (attackValid):

                        self.currentFloor.PlayerAttack(self.player, self.MouseBoardPosition())
                        self.draw_attack(self.player,self.MouseBoardPosition(), screen)
                        self.has_attacked = True

                        print("You choosed an attack")
                        self.message = " You choosed an attack"

                        self.status = "PlayerTurn"
                    else :
                        print("Non valid attack, try again")
                        self.message = " Non valid attack, try again"


                # Detect if the player push the mouvement button
                if self.button_mvt.collidepoint(pygame.mouse.get_pos()):
                   self.wantToChoseMouvement()

                # Detect if the player push the attack button or cltck on the A
                if self.button_attack.collidepoint(pygame.mouse.get_pos()):
                    self.wantToAttack()

                # Detect if the player push the end turn button
                if self.button_finir.collidepoint(pygame.mouse.get_pos()):
                    self.wantToEndTurn()

                #Detect if the player push the weapon choice button
                if self.button_armes.collidepoint(pygame.mouse.get_pos()):
                    self.wantToOpenTheBag()

                # Detect if the player push the help button
                if self.help_button.collidepoint(pygame.mouse.get_pos()):
                    self.wantToOpenHelp()


            elif event.type == pygame.KEYDOWN:
                #raccourci clavier
                if event.key == pygame.K_a :
                    self.wantToAttack()
                elif event.key == pygame.K_b:
                    self.wantToOpenTheBag()
                elif event.key == pygame.K_h:
                    self.wantToOpenHelp()
                elif event.key == pygame.K_m:
                    self.wantToChoseMouvement()
                elif event.key == pygame.K_RETURN and self.won == False:
                    self.wantToEndTurn()
                elif event.key == pygame.K_BACKSPACE :
                    self.wantToAnnul()
                elif event.key == pygame.K_s:
                    self.wantToOpenTheBoutique()
                elif event.key == pygame.K_q: #-------------------------------Enlever apres test--------------------------------------------------
                    self.player.healthPoints -=5
                elif event.key == pygame.K_o:
                    self.openObject(self.player.position)
                elif event.key == pygame.K_p:
                    self.showInsideObject(self.player.position, screen)
                elif event.key == pygame.K_i:
                    self.isAOpenableShowed = False

    def goToNextLevel(self):
        if self.currentFloorIndex < len(self.floorList)-1:
            self.currentFloorIndex += 1
            self.currentFloor = self.floorList[self.currentFloorIndex]
            self.currentFloor.SetNewObject(self.currentFloor.elevatorDOWN, self.player)
            self.larg_case = (self.large_max_grille - (
                    (self.currentFloor.size.width + 1) * self.ecart)) / self.currentFloor.size.width
            self.long_case = (self.large_max_grille - (
                    (self.currentFloor.size.height + 1) * self.ecart)) / self.currentFloor.size.height
            self.turn = 0
            self.has_moved = False
            self.has_attacked = False
            self.message = " Welcome to this Floor "

            if (self.player.movementPoints > 4):
                self.player.movementPoints = 4


            self.isAOpenableShowed = False
            self.currentOpenable = None
            self.init_sprite_size()
        else:
            self.won = True

        self.memorize()

    def openObject(self, position):
        res = self.currentFloor.openOpenableObject(position, self)
        if (res == False):
            self.message = "Nothing to open here"
        elif not(res == None):
            for weapon in res:
                self.pickUp(weapon)
            self.isAOpenableShowed = False
        self.currentOpenable = None

    def buy_event(self, event):
        print(self.eventToExecute.has(event))
        print(len(self.eventToExecute) >= 3)
        if (self.eventToExecute.has(event)):
            self.boutiqueMessage = "You already bought this one"
            print("You already bought this event")
        elif (len(self.eventToExecute) >= 3):
            self.boutiqueMessage = "You already bought 3 events"
            print("You already bought 3 events")
        elif (self.player.money < event.price):
            self.boutiqueMessage = "Not enough money "
            print("You don't have enough money to buy this")
        else:
            self.player.money = self.player.money - event.price
            self.eventToExecute.add(event)
            self.boutiqueMessage = "You bought this event : " + event.name

    def showInsideObject(self, position, screen):
        res = self.currentFloor.showInsideOpenableObject(position, screen)

        if (res == False):
            self.message = "Nothing to show here"
        else :
            self.isAOpenableShowed = True
            self.currentOpenable = self.currentFloor.getStaticObjects(position)

    def monsterTurn(self):
        for monster in self.currentFloor.monsterGroup:
            self.currentFloor.Attack(monster, monster.attackVector)
        for monster in self.currentFloor.monsterGroup:
            self.currentFloor.UpdateMonster(monster)
        self.status = "PlayerTurn"

    def preShowMovement(self, screen):
        path = self.currentFloor.Pathfinder(self.player.position, self.MouseBoardPosition())
        pathLength = self.currentFloor.PathLength(path)
        if pathLength <= self.player.movementPoints:
            color = (0, 255, 0)
        else:
            color = (255, 0, 0)
        x = self.currentFloor.size.width
        y = self.currentFloor.size.height
        for pathPoint in path:
            pathPointRect = pygame.Rect(self.ecart + self.top_left_x + (pathPoint['position'].x * (self.ecart + self.long_case)),
                                        self.ecart + self.top_left_y + (pathPoint['position'].y * (self.ecart + self.larg_case )),
                                        self.long_case, self.larg_case)
            pygame.draw.rect(screen, color, pathPointRect)

    def preShowAttack(self, screen):
        positionMouse = self.convert_px_in_case(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        self.draw_attack(self.player, positionMouse, screen )

    def preshot_monster_attack(self, screen):
        for monster in self.currentFloor.monsterGroup:
            # vector and pattern are just shorthands
            vector = monster.attackVector
            pattern = monster.weapon.GetAttackPattern()

            # Update the attack vector if infinite distance
            if vector != None:
                if pattern["distance"] == inf:
                    normalized = vector.Normalize()
                    raycast = normalized
                    while (monster.position + raycast).InBoard(self.currentFloor.size) and self.currentFloor.GetObject(monster.position + raycast) == None:
                        raycast += normalized
                    if (monster.position + raycast).InBoard(self.currentFloor.size):
                        vector = raycast
                    else:
                        vector = None

            # Update the value
            monster.attackVector = vector
            # Pattern don't need to be updated, as it never changes
            
            # Draw if there is a vector
            if monster.attackVector != None:
                position = monster.position + monster.attackVector
                #position = monster.position
                self.draw_attack(monster, position, screen )
    # -------------------------------------------------------------------------------------------------------------------
    # SPAWN
    # -------------------------------------------------------------------------------------------------------------------

    # Generate a monster
    def spawn_monster(self, name:str="Monster", description:str="Lorem Ipsum", imageLink:str="./assets/monster.png", healthPoints=1, position: Position=Position(0,0), movementPoints: int = 0, weapon: Weapon = Weapon('Not A Weapon')):
        monster = Monster(name=name, description=description, imageLink=imageLink, healthPoints=healthPoints, movementPoints=movementPoints, weapon=weapon)
        self.currentFloor.SetNewObject(position, monster)
        monster.rect.x, monster.rect.y = self.convert_case_in_px(position)

    def spawn_bloc(self, name:str="Bloc", description:str="Just a massive bloc. You can't go through it.", imageLink:str="./assets/wall.png", healthPoints:int=1, position:Position=Position(0,0)):
        bloc = BlocObject(name=name, description=description, imageLink=imageLink, healthPoints=healthPoints, position=position)
        self.currentFloor.SetNewObject(position, bloc)
        bloc.rect.x, bloc.rect.y = self.convert_case_in_px(position)

    # Generate a pickeable object : money, potions
    def spawn_pickableObject(self, position: Position, objectType: str='Money'):
        if objectType == 'Money':
            object = Money()
        elif objectType == 'MovementPotion':
            object = MovementPotion()
        elif objectType == 'LifePotion':
            object = LifePotion()
        else :
            object = Money()

        self.currentFloor.SetNewObject(position, object)
        object.rect.x, object.rect.y = self.convert_case_in_px(position)

    # Generate a coffre
    def spawn_coffre(self, position: Position, object_type_inside:list):
        insideTheBox = []
        # Rempli le tableau du contenu du coffre
        for objectType in object_type_inside:
            if objectType == 'Money':
                object = Money()
            elif objectType == 'MovementPotion':
                object = MovementPotion()
            elif objectType == 'LifePotion':
                object = LifePotion()
            else:
                object = objectType


            insideTheBox.append(object)

        coffre = Coffre(position,insideTheBox)
        coffre.rect.x, coffre.rect.y = self.convert_case_in_px(position)
        self.currentFloor.SetNewObject(position, coffre)


    # -------------------------------------------------------------------------------------------------------------------
    # SPRITE GESTION
    # -------------------------------------------------------------------------------------------------------------------

    def update_position_sprite(self):
        for monster in self.currentFloor.monsterGroup:
            position = monster.position
            monster.rect.x, monster.rect.y = self.convert_case_in_px(position)
        for player in self.currentFloor.playerGroup:
            position = player.position
            player.rect.x, player.rect.y = self.convert_case_in_px(position)
        for object in self.currentFloor.staticObjectGroup:
            position = object.position
            object.rect.x, object.rect.y = self.convert_case_in_px(position)
        for block in self.currentFloor.blockGroup:
            position = block.position
            block.rect.x, block.rect.y = self.convert_case_in_px(position)


    def init_sprite_size(self):

        DEFAULT_IMAGE_SIZE = (self.larg_case, self.long_case)

        for monster in self.currentFloor.monsterGroup:
            image = monster.image
            image = pygame.transform.scale(image, DEFAULT_IMAGE_SIZE)
            monster.image = image

        for player in self.currentFloor.playerGroup:
            image = player.image
            image = pygame.transform.scale(image, DEFAULT_IMAGE_SIZE)

            player.image = image

        for object in self.currentFloor.staticObjectGroup:
            image = object.image
            image = pygame.transform.scale(image, DEFAULT_IMAGE_SIZE)

            object.image = image

        for block in self.currentFloor.blockGroup:
            image = block.image
            image = pygame.transform.scale(image, DEFAULT_IMAGE_SIZE)

            block.image = image


    # -------------------------------------------------------------------------------------------------------------------
    # BAG GESTION
    # -------------------------------------------------------------------------------------------------------------------
    def pickUp(self,weapon):
        if (len(self.bag)<self.taillebag):
            self.bag[weapon.name] = weapon

    # We can let go a weapon to have more space in the bag.
    # We will return at the basic weapon that we can not remove
    def letGo(self, weapon):
        if not(weapon.name=="Light saber"):

            del self.bag[weapon.name]
            self.currentweapon = self.bag["Light saber"]

    # -------------------------------------------------------------------------------------------------------------------
    # DRAW ON THE SCREEN
    # -------------------------------------------------------------------------------------------------------------------

    #draw all basics elements
    def draw_everything(self, screen):
        # show the score on the screen
        font = pygame.font.SysFont("monospace", 25, True)  # create the font style
        #score_text = font.render("Score :" + str(self.score), 1, (255, 255, 255))  # create texte
        #screen.blit(score_text, (640, 60))  # show the score at the tuple position

        # show the number of the turn
        turn_text = font.render("Turn :" + str(self.turn), 1, (255, 255, 255))  # create texte
        screen.blit(turn_text, (640, 60))  # show the turn at the tuple position

        # show floor
        self.draw_floor(screen)

        # draw monsters' attacks
        self.preshot_monster_attack(screen)

        # show player info
        self.draw_player_infos(screen)

        # show monster info
        #self.draw_monster_infos(screen)

        # show floor infos
        self.draw_floor_infos(screen)
        # show the objects
        self.currentFloor.staticObjectGroup.draw(screen)
        # show monstres
        self.currentFloor.monsterGroup.draw(screen)
        # show the blocks
        self.currentFloor.blockGroup.draw(screen)
        # show the player
        self.currentFloor.playerGroup.draw(screen)

        # update position of every images
        self.update_position_sprite()

        # Draw buttons
        self.draw_buttons(screen)

        #draw the current weapon infos
        self.draw_weapon_info(screen)

        # draw the life bars next to the monstrers
        self.currentFloor.draw_monsters_lifebars(screen, self.larg_case)

        # draw the life bars next to the pickables objects
        self.currentFloor.draw_staticObjects_lifebars(screen, self.larg_case)

        # draw the message for the player
        self.draw_message(screen)


        # draw the events bought
        self.draw_events_to_execute(screen);

        if self.isAOpenableShowed:
            self.currentOpenable.showInside(screen)

        self.draw_attack_color_code( screen)

    #draw players infos in the up case
    def draw_player_infos(self, screen):

        # show players info
        font_small = pygame.font.SysFont("monospace", 20, True)  # create the font style
        name_player_text = font_small.render("Name :" + str(self.player.name), 1, (255, 255, 255))  # create texte name
        screen.blit(name_player_text, (650, 160))  # show the name at the tuple position
        money_player_text = font_small.render("Money :" + str(self.player.money), 1,
                                              (255, 255, 255))  # create texte money
        screen.blit(money_player_text, (650, 180))  # show the money at the tuple position
        health_player_text = font_small.render("Health :", 1, (255, 255, 255))  # create texte health
        screen.blit(health_player_text, (650, 220))  # show the health at the tuple position

        # Create player health bar
        bar_back_color = (253, 250, 217)  # couleur 46, 222, 231
        bar_back_position = [750, 230, 180, 7]  # x, y, w, h

        bar_color = (148, 255, 0)  # couleur 46, 222, 231
        bar_position = [750, 230, (self.player.healthPoints / self.player.maxHealthPoints) * 180, 7]  # x, y, w, h

        # Draw player helth bar
        pygame.draw.rect(screen, bar_back_color, bar_back_position)
        pygame.draw.rect(screen, bar_color, bar_position)

    #draw buttons on the right down
    def draw_buttons(self, screen):
        font_small = pygame.font.SysFont("monospace", 15, True)  # create the font style

        pygame.draw.rect(screen, (0, 124, 124), self.button_mvt)
        txt_button_mvt = font_small.render("mvt", 1, (255, 255, 255))
        screen.blit(txt_button_mvt, (650, 630))

        pygame.draw.rect(screen, (0, 124, 124), self.button_finir)
        txt_button_finir = font_small.render("end", 1, (255, 255, 255))
        screen.blit(txt_button_finir, (770, 630))

        pygame.draw.rect(screen, (0, 124, 124), self.button_attack)
        txt_button_attack = font_small.render("fight", 1, (255, 255, 255))
        screen.blit(txt_button_attack, (710, 630))

        pygame.draw.rect(screen, (0, 124, 124), self.button_armes)
        txt_button_armes = font_small.render("bag", 1, (255, 255, 255))
        screen.blit(txt_button_armes, (830, 630))

        pygame.draw.rect(screen, (0, 124, 124), self.button_annuler)
        txt_button_armes = font_small.render("annul", 1, (255, 255, 255))
        screen.blit(txt_button_armes, (890, 630))

        font_big = pygame.font.SysFont("monospace", 25, True)  # create the font style

        pygame.draw.rect(screen, (0, 124, 124), self.help_button)
        txt_button_armes = font_big.render("Tuto", 1, (255, 255, 255))
        screen.blit(txt_button_armes, (1010, 7))


   #draw monster info
    def draw_monster_infos(self, screen):
        # show monster info
        font_small = pygame.font.SysFont("monospace", 20, True)  # create the font style
        name_currentMonster_text = font_small.render("Name :" + str(self.current_monster.name), 1,
                                                     (255, 255, 255))  # create texte name
        screen.blit(name_currentMonster_text, (650, 420))  # show the name at the tuple position



        health_currentMonster_text = font_small.render("Health :", 1, (255, 255, 255))  # create texte health
        screen.blit(health_currentMonster_text, (650, 450))  # show the health at the tuple position

        # Create player health bar
        bar_back_color = (253, 250, 217)  # couleur 46, 222, 231
        bar_color = (148, 255, 0)  # couleur 46, 222, 231
        bar2_back_position = [750, 460, 180, 7]  # x, y, w, h
        bar2_position = [750, 460, (self.current_monster.healthPoints / self.current_monster.maxHealthPoints) * 180,
                         7]  # x, y, w, h

        # Draw player helth bar
        pygame.draw.rect(screen, bar_back_color, bar2_back_position)
        pygame.draw.rect(screen, bar_color, bar2_position)

    def draw_floor_infos(self, screen):
        font_small = pygame.font.SysFont("monospace", 20, True)  # create the font style
        name_currentFloor_text = font_small.render("Name :" + self.currentFloor.name, 1, (255, 255, 255))  # create texte name
        screen.blit(name_currentFloor_text, (670, 400))  # show the name at the tuple position

        condition_text = font_small.render("Aim :" + self.currentFloor.condition_txt(), 1, (255, 255, 255))  # create texte
        screen.blit(condition_text, (650, 430))  # show the text at the tuple position

        if self.elevatorOpen :
            elevator_text = font_small.render("Elevator open", 1,
                                               (0, 255, 0))  # create texte
        else :
            elevator_text = font_small.render("Elevator closed" , 1,
                                              (255, 0, 0))  # create texte health
        screen.blit(elevator_text, (650, 460))  # show the health at the tuple position

    def draw_weapon_info(self,screen):
        font_small = pygame.font.SysFont("monospace", 20, True)  # create the font style
        name_currentMonster_text = font_small.render("Name :" + str(self.currentweapon.name), 1,
                                                     (255, 255, 255))  # create texte name
        screen.blit(name_currentMonster_text, (705, 250))  # show the name at the tuple position

        # draw image
        taille = 50
        DEFAULT_IMAGE_SIZE = (taille, taille)
        back_color = (253, 250, 217)
        x = 650
        y = 250
        back_square_pos = [x, y, taille, taille]  # x, y, w, h
        pygame.draw.rect(screen, back_color, back_square_pos)
        image_arme = pygame.image.load(self.currentweapon.imageLink)  # import image
        image_arme = pygame.transform.scale(image_arme, DEFAULT_IMAGE_SIZE)
        screen.blit(image_arme, (x, y))

    #draw the floor
    def draw_floor(self, screen):
        # draw name of floor
        font_small = pygame.font.SysFont("monospace", 20, True)  # create the font style
        name_currentFloor_text = font_small.render(str(self.currentFloor.name), 1,
                                                   (255, 255, 255))  # create texte name
        screen.blit(name_currentFloor_text, (60, 32))  # show the name at the tuple position

        # draw the background off the floor
        back_floor = (46, 222, 231)
        floor_position = [self.top_left_x, self.top_left_y, self.large_max_grille, self.large_max_grille]
        pygame.draw.rect(screen, back_floor, floor_position)

        # draw all case
        x = self.currentFloor.size.width
        y = self.currentFloor.size.height

        couleur_case = (76, 150, 255)

        for i in range(0, x):
            for j in range(0, y):
                if (Position(i,j)==self.currentFloor.elevatorUP):
                    couleur_case = (200, 161, 249)
                elif (Position(i,j)==self.currentFloor.elevatorDOWN):
                    couleur_case = (137, 118, 171)
                else :
                    couleur_case = (76, 150, 255)


                top_left_x_case = self.ecart + self.top_left_x + (self.larg_case * i) + (self.ecart * i)
                top_left_y_case = self.ecart + self.top_left_y + (self.long_case * j) + (self.ecart * j)

                position_case = [top_left_x_case, top_left_y_case, self.larg_case, self.long_case]
                pygame.draw.rect(screen, couleur_case, position_case)

    #draw an end won screen
    def draw_won(self, screen):
        # Draw won background
        won_background = pygame.image.load('assets/won.png')  # import background
        screen.blit(won_background, (0, 0))

    # draw the game over screen and replay button
    def draw_gameOver(self, screen):
        self.replay_button_rect.x = (screen.get_width() // 2) - (self.replay_button.get_width() // 2)
        self.replay_button_rect.y = (screen.get_height()) - (self.replay_button.get_height() + 22)

        gameOver_background = pygame.image.load('assets/gameOver.png')  # import background
        screen.blit(gameOver_background, (0, 0))
        screen.blit(self.replay_button, self.replay_button_rect)


    #draw the current weapon when the bag is open
    def draw_current_weapon(self, screen):
        # Font style creation
        font_large = pygame.font.SysFont("monospace", 25, True)  # create the font style
        font_medium = pygame.font.SysFont("monospace", 17, True)  # create the font style
        font_small = pygame.font.SysFont("monospace", 15, True)  # create the font style

        # draw the back square
        back_color = (204, 255, 255)
        back_square_pos = [600, 170, 320, 360]  # x, y, w, h
        pygame.draw.rect(screen, back_color, back_square_pos)


        #Draw the image of the weapon
        DEFAULT_IMAGE_SIZE = (50, 50)
        x = 860
        y = 180
        image_arme = pygame.image.load(self.currentweapon.imageLink)  # import image
        image_arme = pygame.transform.scale(image_arme, DEFAULT_IMAGE_SIZE)
        screen.blit(image_arme, (x, y))

        # draw the title of the current weapon
        weapon_name_txt = font_large.render(self.currentweapon.name, 1, (38, 0, 153))
        screen.blit(weapon_name_txt, (610, 180))

        #draw the over obstacle capacity
        #weapon_name_txt = font_small.render("Surpasse objstacle :" + str(self.currentweapon.GetAttackPattern()['overObstacles']), 1, (38, 0, 153))
        #screen.blit(weapon_name_txt, (610, 215))

        couleur_case_zero = (76, 150, 255)
        couleur_case_un = (255, 195, 0)
        couleur_case_deux = (255, 154, 0)
        couleur_case_trois = (255, 115, 0)
        couleur_case_quatre = (229, 42, 12)
        couleur_case_cinq = (174, 19, 19)

        pygame.draw.rect(screen, couleur_case_un, (610, 240, 30, 20))
        txt = font_medium.render("1", 1, (255, 255, 255))
        screen.blit(txt, (620, 240))

        pygame.draw.rect(screen, couleur_case_deux, (640, 240, 30, 20))
        txt = font_medium.render("2", 1, (255, 255, 255))
        screen.blit(txt, (650, 240))

        pygame.draw.rect(screen, couleur_case_trois, (670, 240, 30, 20))
        txt = font_medium.render("3", 1, (255, 255, 255))
        screen.blit(txt, (680, 240))

        pygame.draw.rect(screen, couleur_case_quatre, (700, 240, 30, 20))
        txt = font_medium.render("4", 1, (255, 255, 255))
        screen.blit(txt, (710, 240))

        pygame.draw.rect(screen, couleur_case_cinq, (730, 240, 30, 20))
        txt = font_medium.render("5", 1, (255, 255, 255))
        screen.blit(txt, (740, 240))


        # draw the distance capacity
        weapon_name_txt = font_small.render(
            "Distance :" + str(self.currentweapon.GetAttackPattern()['distance']), 1, (38, 0, 153))
        screen.blit(weapon_name_txt, (610, 215))

        #draw the attack pattern
        weapon_attack_pattern_txt = font_small.render("Attack Pattern : ", 1, (38, 0, 153))
        screen.blit(weapon_attack_pattern_txt, (610, 280))
        self.draw_pattern(screen, self.currentweapon.GetAttackPattern()['damages'], 800, 280, 100, self.currentweapon.GetAttackPattern()['center'], self.currentweapon.imageLink)

        # draw the push pattern
        weapon_push_pattern_txt = font_small.render("Push Pattern : ", 1, (38, 0, 153))
        screen.blit(weapon_push_pattern_txt, (610, 415))
        self.draw_pattern(screen, self.currentweapon.GetAttackPattern()['push'], 800, 415, 100,
                          self.currentweapon.GetAttackPattern()['pushCenter'], self.currentweapon.imageLink)

        #draw the button to let go a weapon
        pygame.draw.rect(screen, (153, 179, 255), self.button_let_go_weapon)
        txt_button_let_go = font_medium.render("Lacher", 1, (255, 255, 255))
        screen.blit(txt_button_let_go, (683, 493))

    def draw_current_event(self, screen):
        # Font style creation
        font_large = pygame.font.SysFont("monospace", 25, True)  # create the font style
        font_medium = pygame.font.SysFont("monospace", 17, True)  # create the font style
        font_small = pygame.font.SysFont("monospace", 15, True)  # create the font style

        # draw the back square
        back_color = (204, 255, 255)
        back_square_pos = [600, 170, 320, 360]  # x, y, w, h
        pygame.draw.rect(screen, back_color, back_square_pos)


        #Draw the image of the event
        DEFAULT_IMAGE_SIZE = (50, 50)
        x = 860
        y = 180
        image_event = pygame.image.load(self.currentEvent.imageLink)  # import image
        image_event = pygame.transform.scale(image_event, DEFAULT_IMAGE_SIZE)
        screen.blit(image_event, (x, y))

        # draw the title of the current event
        event_name_txt = font_large.render(self.currentEvent.name, 1, (38, 0, 153))
        screen.blit(event_name_txt, (610, 180))

        # draw the description of the event
        event_description_txt = font_small.render(self.currentEvent.description, 1, (38, 0, 153))
        screen.blit(event_description_txt, (610, 245))

        # draw the pricz of the event
        event_price_txt = font_small.render("Price : " + (str) (self.currentEvent.price), 1, (38, 0, 153))
        screen.blit(event_price_txt, (610, 270))

        #draw the pattern
        event_action = font_small.render("Action : ", 1, (38, 0, 153))
        screen.blit(event_action, (610, 300))
        #+++++++++AJOUTER AFFICHAGE DE L4ACTION
        #self.draw_pattern(screen, self.currentweapon.GetAttackPattern()['damages'], 800, 280, 100, self.currentweapon.GetAttackPattern()['center'], self.currentweapon.imageLink)


        #draw the button to buy the event
        pygame.draw.rect(screen, (153, 179, 255), self.button_buy_event)
        txt_button_buy = font_medium.render("Buy", 1, (255, 255, 255))
        screen.blit(txt_button_buy, (683, 493))

    #draw the pattern of attack of a weapon
    def draw_pattern(self, screen, pattern, x_pos, y_pos , size, center, imageLink):

        # draw the background off the pattern
        back_floor_color = (46, 222, 231)
        floor_position = [x_pos, y_pos, size, size]
        pygame.draw.rect(screen, back_floor_color, floor_position)

        #define var
        nbLigne = len(pattern)
        nbCol = len(pattern[0])
        ecart = 2
        larg_case = (size - ((nbCol + 1) * ecart)) / nbCol
        long_case = (size - ((nbLigne + 1) * ecart)) / nbLigne

        couleur_case_zero = (76, 150, 255)
        couleur_case_un = (255, 195, 0)
        couleur_case_deux = (255, 154, 0)
        couleur_case_trois = (255, 115, 0)
        couleur_case_quatre = (229, 42, 12)
        couleur_case_cing = (174, 19, 19)

        for l in range(0, len(pattern)):
            ligne = pattern[l]
            for c in range(0, len(ligne)):
                if ligne[c] == 0 :
                    couleur_case = couleur_case_zero
                elif ligne[c] == 1 :
                    couleur_case = couleur_case_un
                elif ligne[c] == 2 :
                    couleur_case = couleur_case_deux
                elif ligne[c] == 3 :
                    couleur_case = couleur_case_trois
                elif ligne[c] == 4 :
                    couleur_case = couleur_case_quatre
                else :
                    couleur_case = couleur_case_cing


                # find the coordinates of the cases
                top_left_x_case = ecart + x_pos + (larg_case * l) + (ecart * l)
                top_left_y_case = ecart + y_pos + (long_case * c) + (ecart * c)

                #draw each square
                position_case = [top_left_x_case, top_left_y_case, larg_case, long_case]
                pygame.draw.rect(screen, couleur_case, position_case)

                #Marque le centre avec image de l'arme
                if c == center[1] and l == center[0]:
                    image_arme = pygame.image.load(imageLink)  # import image
                    image_arme = pygame.transform.scale(image_arme, (long_case, larg_case))
                    screen.blit(image_arme, ( top_left_x_case, top_left_y_case))


    #draw bag when is open
    def draw_bag(self, screen):



        font_large = pygame.font.SysFont("monospace", 25, True)  # create the font style
        font_small = pygame.font.SysFont("monospace", 10, True)  # create the font style

        #Draw the background of the bag
        bag_background = pygame.image.load('assets/inventaire.png')  # import background
        screen.blit(bag_background, (0, 0))

        #draw the quit button
        pygame.draw.rect(screen, (0, 124, 124), self.quit_bag_button)
        txt_button_quit = font_large.render("Quit", 1, (255, 255, 255))
        screen.blit(txt_button_quit, (500, 500))

        # draw the weapons
        taille = 60
        DEFAULT_IMAGE_SIZE = (taille, taille)
        back_color = (204, 255, 255)
        x_start = 170
        y_start = 170
        ecart = 40
        compte_arme = 0
        x = x_start
        y = y_start

        for arme in self.bag :
            if (compte_arme % 4) == 0 :
                if not (compte_arme == 0):
                    x = x_start
                    y = y + ecart + taille

            else :

                x = x + ecart + taille

            if self.bag[arme] == self.currentweapon :
                back_color = (217, 204, 255)
            else :
                back_color = (204, 255, 255)

            back_square_pos = [x, y, taille, taille]  # x, y, w, h
            pygame.draw.rect(screen, back_color, back_square_pos)

            image_arme = pygame.image.load(self.bag[arme].imageLink)  # import image
            image_arme = pygame.transform.scale(image_arme, DEFAULT_IMAGE_SIZE)
            screen.blit(image_arme, (x, y))

            txt_arme = font_small.render(self.bag[arme].name, 1, (255, 255, 255))
            screen.blit(txt_arme, (x, y + taille))

            self.bag[arme].button = pygame.Rect(x, y, taille, taille)

            compte_arme = compte_arme + 1

        self.draw_current_weapon(screen);

    #draw boutique when is open
    def draw_boutique(self, screen):

        font_large = pygame.font.SysFont("monospace", 25, True)  # create the font style
        font_medium = pygame.font.SysFont("monospace", 15, True)  # create the font style
        font_small = pygame.font.SysFont("monospace", 10, True)  # create the font style

        #Draw the background of the boutique
        boutique_background = pygame.image.load('assets/inventaire.png')  # import background
        screen.blit(boutique_background, (0, 0))

        #draw the quit button
        pygame.draw.rect(screen, (0, 124, 124), self.quit_boutique_button)
        txt_button_quit = font_large.render("Quit", 1, (255, 255, 255))
        screen.blit(txt_button_quit, (500, 500))

        #draw your money
        money_player_text = font_large.render("Money :" + str(self.player.money), 1,
                                              (255, 255, 255))  # create texte money
        screen.blit(money_player_text, (300, 165))  # show the money at the tuple position

        #draw message
        message_text = font_medium.render(self.boutiqueMessage, 1,(255, 255, 255))
        screen.blit(message_text, (170, 450))

        # draw the events
        taille = 60
        DEFAULT_IMAGE_SIZE = (taille, taille)
        back_color = (204, 255, 255)
        x_start = 170
        y_start = 300
        ecart = 40
        compte_event = 0
        x = x_start
        y = y_start

        for i in range (0, len(self.boutique)) :
            event = self.boutique[i]
            if (compte_event % 4) == 0 :
                if not (compte_event == 0):
                    x = x_start
                    y = y + ecart + taille

            else :

                x = x + ecart + taille

            if event == self.currentEvent :
                back_color = (217, 204, 255)
            else :
                back_color = (204, 255, 255)

            back_square_pos = [x, y, taille, taille]  # x, y, w, h
            pygame.draw.rect(screen, back_color, back_square_pos)

            image_event= pygame.image.load(event.imageLink)  # import image
            image_event = pygame.transform.scale(image_event, DEFAULT_IMAGE_SIZE)
            screen.blit(image_event, (x, y))

            txt_event = font_small.render(event.name, 1, (255, 255, 255))
            screen.blit(txt_event, (x, y + taille))

            event.button = pygame.Rect(x, y, taille, taille)

            compte_event = compte_event + 1

        self.draw_current_event(screen);

    # draw help when is open
    def draw_help(self, screen):
        font_large = pygame.font.SysFont("monospace", 25, True)  # create the font style
        font_medium = pygame.font.SysFont("monospace", 15, True)  # create the font style
        font_small = pygame.font.SysFont("monospace", 10, True)  # create the font style

        # Draw the background of the boutique
        help_background = pygame.image.load('assets/inventaire.png')  # import background
        screen.blit(help_background, (0, 0))

        # draw the quit button
        pygame.draw.rect(screen, (0, 124, 124), self.quit_help_button)
        txt_button_quit = font_large.render("Quit", 1, (255, 255, 255))
        screen.blit(txt_button_quit, (500, 500))

        # draw the next button
        pygame.draw.rect(screen, (0, 124, 124), self.help_next_button)
        txt_button_next = font_large.render("Next", 1, (255, 255, 255))
        screen.blit(txt_button_next, (700, 500))

        self.draw_text(screen, self.help_txt[self.indice_txt_help], 20, 160, 160, 20)


    def draw_text(self, screen, tab_txt, size, start_x, start_y, ecart):
        font = pygame.font.SysFont("monospace", size, True)  # create the font style
        count_line = 0
        for l in range(0, len(tab_txt)):
            txt_line = font.render(tab_txt[l], 1, (255, 255, 255))
            screen.blit(txt_line, (start_x, start_y + ecart* count_line))
            count_line += 1

    def draw_message(self, screen):
        font_small = pygame.font.SysFont("monospace", 17, True)  # create the font style
        message_text = font_small.render(self.message, 1,
                                                     (255, 255, 255))  # create texte name
        screen.blit(message_text, (70, 580))  # show the name at the tuple position

    # draw the attack
    def draw_attack(self, attaquant, positionAttack, screen):
        vector = positionAttack - attaquant.position
        pattern = attaquant.weapon.GetAttackPattern()

        if isinstance(attaquant, Monster):
            couleur_case = (139, 192, 252)
            imageImpact1 = pygame.transform.scale(pygame.image.load("./assets/impact_monstre_1.png"),
                                                 (self.larg_case, self.long_case))
            imageImpact2 = pygame.transform.scale(pygame.image.load("./assets/impact_monstre_2.png"),
                                                 (self.larg_case, self.long_case))
            imageImpact3 = pygame.transform.scale(pygame.image.load("./assets/impact_monstre_3.png"),
                                                  (self.larg_case, self.long_case))
            imageImpact4 = pygame.transform.scale(pygame.image.load("./assets/impact_monstre_4.png"),
                                                  (self.larg_case, self.long_case))
            imageImpact5 = pygame.transform.scale(pygame.image.load("./assets/impact_monstre_5.png"),
                                                  (self.larg_case, self.long_case))

        elif isinstance(attaquant, Player):
            couleur_case = (249, 248, 116)
            imageImpact1 = pygame.transform.scale(pygame.image.load("./assets/impact_player_1.png"),
                                                  (self.larg_case, self.long_case))
            imageImpact2 = pygame.transform.scale(pygame.image.load("./assets/impact_player_2.png"),
                                                  (self.larg_case, self.long_case))
            imageImpact3 = pygame.transform.scale(pygame.image.load("./assets/impact_player_3.png"),
                                                  (self.larg_case, self.long_case))
            imageImpact4 = pygame.transform.scale(pygame.image.load("./assets/impact_player_4.png"),
                                                  (self.larg_case, self.long_case))
            imageImpact5 = pygame.transform.scale(pygame.image.load("./assets/impact_player_5.png"),
                                                  (self.larg_case, self.long_case))
        #controle structure made in PlayerAttack() in the floor
        if vector.CollinearToAxis():
            if "distance" in pattern:
                if abs(vector) <= pattern["distance"]:
                    attaquant.weapon.Action("onAttack", attaquant)
                    pattern = attaquant.weapon.GetAttackPattern()

                    if pattern != {}:
                        if "push" in pattern:
                            for x in range(len(pattern["push"])):
                                for y in range(len(pattern["push"][x])):
                                    checkingPosition = Position(
                                        x - pattern["pushCenter"][0] + attaquant.position.x + vector.x,
                                        y - pattern["pushCenter"][1] + attaquant.position.y + vector.y)
                                    if checkingPosition.InBoard(self.currentFloor.size):
                                        if not (pattern["push"][x][y] == 0):

                                            top_left_x_case = self.ecart + self.top_left_x + (
                                                        self.larg_case * checkingPosition.x) + (
                                                                      self.ecart * checkingPosition.x)
                                            top_left_y_case = self.ecart + self.top_left_y + (
                                                        self.long_case * checkingPosition.y) + (
                                                                      self.ecart * checkingPosition.y)
                                            position_case = [top_left_x_case, top_left_y_case, self.larg_case,
                                                             self.long_case]
                                            pygame.draw.rect(screen, couleur_case, position_case)

                        if "damages" in pattern:
                            for x in range(len(pattern["damages"])):
                                for y in range(len(pattern["damages"][x])):
                                    checkingPosition = Position(
                                        x - pattern["center"][0] + attaquant.position.x + vector.x,
                                        y - pattern["center"][1] + attaquant.position.y + vector.y)
                                    if checkingPosition.InBoard(self.currentFloor.size):
                                        if not(pattern["damages"][x][y]==0):
                                            if (pattern["damages"][x][y]==1) :
                                                imageImpact = imageImpact1
                                            elif (pattern["damages"][x][y]==2) :
                                                imageImpact = imageImpact2
                                            elif (pattern["damages"][x][y]==3) :
                                                imageImpact = imageImpact3
                                            elif (pattern["damages"][x][y]==4) :
                                                imageImpact = imageImpact4
                                            elif (pattern["damages"][x][y]==5) :
                                                imageImpact = imageImpact5

                                            top_left_x_case = self.ecart + self.top_left_x + (self.larg_case * checkingPosition.x) + (
                                                        self.ecart * checkingPosition.x)
                                            top_left_y_case = self.ecart + self.top_left_y + (self.long_case * checkingPosition.y) + (
                                                        self.ecart * checkingPosition.y)
                                            screen.blit(imageImpact, (top_left_x_case, top_left_y_case))

    def draw_events_to_execute(self, screen):

        font_small = pygame.font.SysFont("monospace", 20, True)  # create the font style
        event_txt = font_small.render("Event bought:", 1, (255, 255, 255))  # create texte health
        screen.blit(event_txt, (650, 490))  # show the health at the tuple position

        taille = 50
        DEFAULT_IMAGE_SIZE = (taille, taille)
        back_color = (204, 255, 255)
        x_start = 700
        y_start = 520
        ecart = 10
        compte_event = 0
        x = x_start
        y = y_start

        for event in self.eventToExecute:
            if not(compte_event ==0):
                x = x + ecart + taille

            back_square_pos = [x, y, taille, taille]  # x, y, w, h
            pygame.draw.rect(screen, back_color, back_square_pos)

            image_event = pygame.image.load(event.imageLink)  # import image
            image_event = pygame.transform.scale(image_event, DEFAULT_IMAGE_SIZE)
            screen.blit(image_event, (x, y))

            compte_event = compte_event + 1

    def draw_attack_color_code(self, screen):

        font_medium = pygame.font.SysFont("monospace", 17, True)  # create the font style
        x = 90
        y = 70
        taille = (40, 40)
        imageImpact1M = pygame.transform.scale(pygame.image.load("./assets/impact_monstre_1.png"),
                                               taille)
        imageImpact2M = pygame.transform.scale(pygame.image.load("./assets/impact_monstre_2.png"),
                                               taille)
        imageImpact3M = pygame.transform.scale(pygame.image.load("./assets/impact_monstre_3.png"),
                                               taille)
        imageImpact4M = pygame.transform.scale(pygame.image.load("./assets/impact_monstre_4.png"),
                                               taille)
        imageImpact5M = pygame.transform.scale(pygame.image.load("./assets/impact_monstre_5.png"),
                                               taille)
        imageImpact1P = pygame.transform.scale(pygame.image.load("./assets/impact_player_1.png"),
                                               taille)

        imageImpact2P = pygame.transform.scale(pygame.image.load("./assets/impact_player_2.png"),
                                               taille)

        imageImpact3P = pygame.transform.scale(pygame.image.load("./assets/impact_player_3.png"),
                                               taille)

        imageImpact4P = pygame.transform.scale(pygame.image.load("./assets/impact_player_4.png"),
                                               taille)

        imageImpact5P = pygame.transform.scale(pygame.image.load("./assets/impact_player_5.png"),
                                               taille)

        tab = [imageImpact1P, imageImpact2P, imageImpact3P, imageImpact4P, imageImpact5P, imageImpact1M, imageImpact2M,
               imageImpact3M, imageImpact4M, imageImpact5M]

        for i in range(len(tab)):
            screen.blit(tab[i], (x + 40 * i, y))
            txt = font_medium.render(str((i % 5) + 1), 1, (255, 255, 255))
            screen.blit(txt, (x + 40 * i, y + 20))


    #-------------------------------------------------------------------------------------------------------------------
    #CONVERSIONS AND CLICK UTILS
    #-------------------------------------------------------------------------------------------------------------------

    # convert position on the screen to position en the map, -10 -10 if out of map
    def convert_px_in_case(self, px_x, px_y):

        x = self.currentFloor.size.width
        y = self.currentFloor.size.height

        case_x = int((px_x - self.top_left_x) // (self.larg_case + self.ecart))
        case_y = int((px_y - self.top_left_y) // (self.long_case + self.ecart))

        # check if it's out of the map
        if case_x >= x or case_y >= y or case_x < 0 or case_y < 0:
            case_x = -10
            case_y = -10

        # print(case_x, case_y) #Suppr later

        return Position(case_x, case_y)

    # convert case of the floor to position on the screen in px
    def convert_case_in_px(self, position: Position):

        x = self.currentFloor.size.width
        y = self.currentFloor.size.height

        px_x = position.x * (self.larg_case + self.ecart) + self.top_left_x
        px_y = position.y * (self.long_case + self.ecart) + self.top_left_y

        return px_x, px_y

    def DetectClick(self):
        pygame.event.clear()
        event = pygame.event.wait()
        return event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]

    # return the case where the mouse is
    def MouseBoardPosition(self):
        return self.convert_px_in_case(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])


