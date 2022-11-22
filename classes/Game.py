import sys
import pygame

from typing import TypedDict
import json

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

        self.floorList = [Floor(name='Floor 0', size= Size(6,6),elevatorUP= Position(5,5),elevatorDOWN =Position(0,0)),
                          Floor(name='Floor 1', size= Size(10,10),elevatorUP= Position(6,6),elevatorDOWN= Position(0,4)),
                          Floor(name='Floor 2', size= Size(15,15),elevatorUP= Position(14,7),elevatorDOWN = Position(0,7))]
        self.currentFloorIndex = 0
        self.currentFloor = self.floorList[self.currentFloorIndex]
        self.score = 0

        # generate the player
        self.player = Player(movementPoints=3, weapon=weapons['TEST WEAPON'])
        self.currentFloor.SetNewObject(self.currentFloor.elevatorDOWN, self.player)
        self.currentweapon = self.player.weapon

        # boutons
        self.button_attack = pygame.Rect(710, 630, 50, 20)
        self.button_mvt = pygame.Rect(650, 630, 50, 20)
        self.button_finir = pygame.Rect(770, 630, 50, 20)
        self.button_armes = pygame.Rect(830, 630, 50, 20)
        self.button_annuler = pygame.Rect(890, 630, 50, 20)
        self.quit_bag_button = pygame.Rect(500, 500, 70, 40)

        self.button_let_go_weapon = pygame.Rect(680, 490, 70, 30)

        # const needed to draw the map
        self.ecart = 3
        self.top_left_x = 60
        self.top_left_y = 110
        self.large_max_grille = 450

        self.larg_case = (self.large_max_grille - ((self.currentFloor.size.width + 1) * self.ecart)) / self.currentFloor.size.width
        self.long_case = (self.large_max_grille - ((self.currentFloor.size.height + 1) * self.ecart)) / self.currentFloor.size.height

        # var to know where we are in the game
        self.turn = 0
        self.status = "MonsterTurn"
        self.has_moved = False
        self.has_attacked = False
        self.won = False
        self.message = " Welcome to a new Floor "
        self.running = True

        self.bagisopen = False
        self.bag = weapons
        self.taillebag = 13
        self.weaponTab = weapons

        self.isAOpenableShowed = False
        self.currentOpenable = None



        # TEST A ENLEVER
        self.spawn_monster(position=Position(4, 4), movementPoints=5, weapon=weapons['TEST WEAPON'])
        self.spawn_pickableObject(position=Position(2, 2), objectType='Money' )
        self.spawn_pickableObject(position=Position(4, 4), objectType='LifePotion')
        self.spawn_coffre(position=Position(2,0),  object_type_inside= [self.weaponTab["TEST WEAPON 1"], 'Money'] )
        self.current_monster = self.currentFloor.lastMonsterAdded
        self.init_sprite_size()



        self.weaponTab = weapons

    # -------------------------------------------------------------------------------------------------------------------
    # MAIN FONCTION
    # -------------------------------------------------------------------------------------------------------------------

    def update(self, screen):

        # update affichage et update var
        self.draw_everything(screen)
        self.running = True
        self.won = False
        self.arrivedAtElevator = (self.player.position == self.currentFloor.elevatorUP)
        self.currentFloor.checkEveryoneAlive()


        if self.arrivedAtElevator:
            self.goToNextLevel();

        # deal with the bag is open
        if self.bagisopen:
            self.dealWithOpenBag(screen)

        # deal with the situation of winning
        elif self.won :
            self.dealWithWon(screen)

        # deal with the action in the pannel Game, out of the bag and not in a winning situation
        else :
            self.dealWithActionPannelGame(screen)


        if self.status == "MonsterTurn":
            self.monsterTurn()

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
        print("vous avez appuyé sur le bouton attack")
        # check if the player has already attacked during this turn
        if self.has_attacked == False:
            self.status = "PlayerAttack"
            self.message = " Choisissez où vous voulez attaquer"
        else:
            print("Vous avez deja attaquer vous ne pouvez plus")
            self.message = " Vous essayer d'attaquer mais vous avez déjà attaqué "
    def wantToOpenTheBag(self):
        print("vous choisissez votre arme")
        self.bagisopen = True
    def wantToAnnul(self):
        print("Vous avez annulé l'action")
        self.message = " Vous avez annulé l'action"
        self.status = "PlayerTurn"
    def wantToEndTurn(self):
        print("vous avez appuyé sur le bouton finir tour")
        self.message = " Fin de votre tour, la main est aux monstree "
        # Put the variable back to normal
        self.has_moved = False
        self.has_attacked = False
        # Begin the monster turn
        self.status = "MonsterTurn"
        # increase the turn count
        self.turn = self.turn + 1
    def wantToChoseMouvement(self):
        print("vous avez appuyé sur le bouton mvt")
        # check if the player has already moved during this turn
        if self.has_moved == False:
            self.message = " Choisissez où vous voulez vous déplacer"
            self.status = "PlayerMovement"
        else:
            print("Vous avez deja bougé vous ne pouvez plus")
            self.message = " Vous essayer de vous déplacer mais vous avez deja bougé "

    # -------------------------------------------------------------------------------------------------------------------
    # DECOUPE FONCTION UDATE
    # -------------------------------------------------------------------------------------------------------------------

    def dealWithWon(self,screen):
        self.draw_won(screen)
        print("vous avez gagné !")

    def dealWithOpenBag(self, screen):
        self.draw_bag(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                print("aurevoir")
            # Deal with click if we are in the bag
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                print("you clicked in the bag")

                if self.button_let_go_weapon.collidepoint(pygame.mouse.get_pos()):
                    self.letGo(self.currentweapon)

                for arme in self.bag:
                    if self.bag[arme].button.collidepoint(pygame.mouse.get_pos()):
                        print("Vous avez cliqué sur l'arme : " + self.weaponTab[arme].name)
                        self.currentweapon = self.weaponTab[arme]
                        self.player.weapon = self.weaponTab[arme]

                # Detect if the player push the end turn button
                if self.quit_bag_button.collidepoint(pygame.mouse.get_pos()):
                    print("vous avez appuyé sur le bouton quitter le sac")
                    # Put the variable back to normal
                    self.bagisopen = False

    def dealWithActionPannelGame(self, screen):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                print("aurevoir")
               # Deal with click if we are in the game pannel
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:

                if self.status == "PlayerTurn":
                    print("C'est au tour du joueur")
                    self.message = " A vous de jouez"

                if self.button_annuler.collidepoint(pygame.mouse.get_pos()):
                    self.wantToAnnul()

                # The player is moving
                if self.status == "PlayerMovement" :
                    self.currentFloor.UpdatePlayer(self.player, self.MouseBoardPosition())
                    self.has_moved = True

                    print("Le joueur a choisit un deplacement")
                    self.message = " Vous avez choisit un deplacement"

                    self.status = "PlayerTurn"

                # The player is attacking
                if self.status == "PlayerAttack" :
                    self.currentFloor.PlayerAttack(self.player, self.MouseBoardPosition())
                    self.draw_attack(self.player,self.MouseBoardPosition(), screen)
                    self.has_attacked = True

                    print("Le joueur a choisit une attack ")
                    self.message = " Vous avez choisit une attack"

                    self.status = "PlayerTurn"

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


            elif event.type == pygame.KEYDOWN:
                #raccourci clavier
                if event.key == pygame.K_a :
                    self.wantToAttack()
                elif event.key == pygame.K_b:
                    self.wantToOpenTheBag()
                elif event.key == pygame.K_m:
                    self.wantToChoseMouvement()
                elif event.key == pygame.K_RETURN and self.won == False:
                    self.wantToEndTurn()
                elif event.key == pygame.K_BACKSPACE :
                    self.wantToAnnul()
                elif event.key == pygame.K_q:
                    print("Player is hit")
                    for player in self.currentFloor.playerGroup:
                        player.healthPoints = player.healthPoints - 1
                elif event.key == pygame.K_s:
                    print("you earn score")
                    self.score = self.score + 3
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
            self.message = " Welcome to a new Floor "

            self.isAOpenableShowed = False
            self.currentOpenable = None
            self.init_sprite_size()
        else:
            self.won = True


    def openObject(self, position):
        res = self.currentFloor.openOpenableObject(position, self)
        if (res == False):
            self.message = "Aucun objet à ouvrir à votre position"
        elif not(res == None):
            for weapon in res:
                self.pickUp(weapon)
        self.currentOpenable = None
    def showInsideObject(self, position, screen):
        res = self.currentFloor.showInsideOpenableObject(position, screen)

        if (res == False):
            self.message = "Aucun objet à montrer à votre position"
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
            if not(monster.attackVector==None):
                position = monster.position + monster.attackVector
                #position = monster.position
                self.draw_attack(monster, position, screen )
    # -------------------------------------------------------------------------------------------------------------------
    # SPAWN
    # -------------------------------------------------------------------------------------------------------------------

    # Generate a monster
    def spawn_monster(self, position: Position, movementPoints: int = 0, weapon: Weapon = Weapon('Not A Weapon')):
        monster = Monster(movementPoints=movementPoints, weapon=weapon)
        self.currentFloor.SetNewObject(position, monster)
        monster.rect.x, monster.rect.y = self.convert_case_in_px(position)

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


    # -------------------------------------------------------------------------------------------------------------------
    # BAG GESTION
    # -------------------------------------------------------------------------------------------------------------------
    def pickUp(self,weapon):
        if (len(self.bag)<self.taillebag):
            self.bag[weapon.name] = weapon

    # We can let go a weapon to have more space in the bag.
    # We will return at the basic weapon that we can not remove
    def letGo(self, weapon):
        if not(weapon.name=="BASIC WEAPON"):

            del self.bag[weapon.name]
            self.currentweapon = self.bag["BASIC WEAPON"]

    # -------------------------------------------------------------------------------------------------------------------
    # DRAW ON THE SCREEN
    # -------------------------------------------------------------------------------------------------------------------

    #draw all basics elements
    def draw_everything(self, screen):
        # show the score on the screen
        font = pygame.font.SysFont("monospace", 25, True)  # create the font style
        score_text = font.render("Score :" + str(self.score), 1, (255, 255, 255))  # create texte
        screen.blit(score_text, (640, 60))  # show the score at the tuple position

        # show the number of the turn
        turn_text = font.render("Turn :" + str(self.turn), 1, (255, 255, 255))  # create texte
        screen.blit(turn_text, (640, 100))  # show the turn at the tuple position

        # show floor
        self.draw_floor(screen)
        self.preshot_monster_attack( screen)

        # show player info
        self.draw_player_infos(screen)

        # show monster info
        self.draw_monster_infos(screen)

        # show the objects
        self.currentFloor.staticObjectGroup.draw(screen)
        # show monstres (maybe better in main)
        self.currentFloor.monsterGroup.draw(screen)

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

        if self.isAOpenableShowed:
            self.currentOpenable.showInside(screen)

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

   #draw monster info
    def draw_monster_infos(self, screen):
        # show monster info
        font_small = pygame.font.SysFont("monospace", 20, True)  # create the font style
        name_currentMonster_text = font_small.render("Name :" + str(self.current_monster.name), 1,
                                                     (255, 255, 255))  # create texte name
        screen.blit(name_currentMonster_text, (650, 420))  # show the name at the tuple position

        description_currentMonster_text = font_small.render("Description :" + str(self.current_monster.description), 1,
                                                            (255, 255, 255))  # create texte description
        screen.blit(description_currentMonster_text, (650, 440))  # show the name at the tuple position

        health_currentMonster_text = font_small.render("Health :", 1, (255, 255, 255))  # create texte health
        screen.blit(health_currentMonster_text, (650, 460))  # show the health at the tuple position

        # Create player health bar
        bar_back_color = (253, 250, 217)  # couleur 46, 222, 231
        bar_color = (148, 255, 0)  # couleur 46, 222, 231
        bar2_back_position = [750, 470, 180, 7]  # x, y, w, h
        bar2_position = [750, 470, (self.current_monster.healthPoints / self.current_monster.maxHealthPoints) * 180,
                         7]  # x, y, w, h

        # Draw player helth bar
        pygame.draw.rect(screen, bar_back_color, bar2_back_position)
        pygame.draw.rect(screen, bar_color, bar2_position)

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
        weapon_name_txt = font_small.render("Surpasse objstacle :" + str(self.currentweapon.GetAttackPattern()['overObstacles']), 1, (38, 0, 153))
        screen.blit(weapon_name_txt, (610, 215))

        # draw the distance capacity
        weapon_name_txt = font_small.render(
            "Distance :" + str(self.currentweapon.GetAttackPattern()['distance']), 1, (38, 0, 153))
        screen.blit(weapon_name_txt, (610, 245))

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
        couleur_case_un = (255, 51, 51)

        for l in range(0, len(pattern)):
            ligne = pattern[l]
            for c in range(0, len(ligne)):
                if ligne[c] == 0 :
                    couleur_case = couleur_case_zero
                else :
                    couleur_case = couleur_case_un

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


    def draw_message(self, screen):
        font_small = pygame.font.SysFont("monospace", 17, True)  # create the font style
        message_text = font_small.render(self.message, 1,
                                                     (255, 255, 255))  # create texte name
        screen.blit(message_text, (70, 580))  # show the name at the tuple position

    def draw_attack(self, attaquant, positionAttack, screen):
        vector = positionAttack - attaquant.position
        pattern = attaquant.weapon.GetAttackPattern()

        if isinstance(attaquant, Monster):
            couleur_case = (139, 192, 252)
            imageImpact = pygame.transform.scale(pygame.image.load("./assets/impact.png"),
                                                 (self.larg_case, self.long_case))
        elif isinstance(attaquant, Player):
            couleur_case = (249, 248, 116)
            imageImpact = pygame.transform.scale(pygame.image.load("./assets/impact4.png"),
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

                                            top_left_x_case = self.ecart + self.top_left_x + (self.larg_case * checkingPosition.x) + (
                                                        self.ecart * checkingPosition.x)
                                            top_left_y_case = self.ecart + self.top_left_y + (self.long_case * checkingPosition.y) + (
                                                        self.ecart * checkingPosition.y)
                                            screen.blit(imageImpact, (top_left_x_case, top_left_y_case))




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

