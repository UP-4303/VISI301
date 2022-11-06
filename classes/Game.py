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



class Game:
    score: int
    isplaying: bool
    floorList: list[Floor]
    currentFloor: int
    status: str

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
            weapons[weaponName] = Weapon(weaponName, './assets/weapon1.png', **weaponValue)
        print(weapons)

        # define is the game has begin
        self.isplaying = False

        self.floorList = [Floor()]
        self.currentFloorIndex = 0
        self.currentFloor = self.floorList[self.currentFloorIndex]
        self.score = 0

        # generate the player
        self.player = Player(movementPoints=3, weapon=weapons['TEST WEAPON'])
        self.currentFloor.SetNewObject(Position(0, 0), self.player)
        self.currentweapon = self.player.weapon
        # boutons
        self.button_attack = pygame.Rect(710, 630, 50, 20)
        self.button_mvt= pygame.Rect(650, 630, 50, 20)
        self.button_finir = pygame.Rect(770, 630, 50, 20)
        self.button_armes = pygame.Rect(830, 630, 50, 20)
        self.button_annuler = pygame.Rect(890, 630, 50, 20)
        self.quit_bag_button = pygame.Rect(500, 500, 70, 40)

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

        self.bagisopen = False
        self.bag = []


        # TEST A ENLEVER
        self.spawn_monster(position=Position(4, 4), movementPoints=5, weapon=weapons['TEST WEAPON'])
        self.current_monster = Monster()
        self.init_sprite_size()



        self.weaponTab = weapons



    def update(self, screen):
        # update affichage
        self.draw_everything(screen)
        running = True
        if self.bagisopen:
            self.draw_bag(screen)

        # deal with quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if self.bagisopen :
                # Deal with click if we are in the bag
                if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    print("you clicked in the bag")

                    for arme in self.weaponTab :
                       if self.weaponTab[arme].button.collidepoint(pygame.mouse.get_pos()):
                           print("Vous avez cliqué sur l'arme : " + self.weaponTab[arme].name)
                           self.currentweapon = self.weaponTab[arme]



                    # Detect if the player push the end turn button
                    if self.quit_bag_button.collidepoint(pygame.mouse.get_pos()):
                        print("vous avez appuyé sur le bouton quitter le sac")
                        # Put the variable back to normal
                        self.bagisopen = False

            else :
               # Deal with click if we are in the game pannel
                if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:

                    if self.status == "PlayerTurn":
                        print("C'est au tour du joueur")

                    if self.button_annuler.collidepoint(pygame.mouse.get_pos()):
                        print("Vous avez annulé l'action")
                        self.status = "PlayerTurn"

                    # The player is moving
                    if self.status == "PlayerMovement" :
                        self.currentFloor.UpdatePlayer(self.player, self.MouseBoardPosition())
                        self.has_moved = True

                        print("Le joueur a choisit un deplacement")

                        self.status = "PlayerTurn"

                    # The player is attacking
                    if self.status == "PlayerAttack" :
                        self.MouseBoardPosition()

                        self.has_attacked = True
                        print("Le joueur a choisit une attack ")

                        self.status = "PlayerTurn"
                    # Detect if the player push the mouvement button
                    if self.button_mvt.collidepoint(pygame.mouse.get_pos()):
                        print("vous avez appuyé sur le bouton mvt")
                        # check if the player has already moved during this turn
                        if self.has_moved == False:
                            self.status = "PlayerMovement"
                        else:
                            print("Vous avez deja bougé vous ne pouvez plus")


                    # Detect if the player push the attack button
                    if self.button_attack.collidepoint(pygame.mouse.get_pos()):
                        print("vous avez appuyé sur le bouton attack")
                        #check if the player has already attacked during this turn
                        if self.has_attacked == False :
                            self.status = "PlayerAttack"
                        else :
                            print("Vous avez deja attaquer vous ne pouvez plus")

                    # Detect if the player push the end turn button
                    if self.button_finir.collidepoint(pygame.mouse.get_pos()):
                        print("vous avez appuyé sur le bouton finir tour")
                        #Put the variable back to normal
                        self.has_moved = False
                        self.has_attacked = False
                        #Begin the monster turn
                        self.status = "MonsterTurn"
                        #increase the turn count
                        self.turn = self.turn + 1

                    #Detect if the player push the weapon choice button
                    if self.button_armes.collidepoint(pygame.mouse.get_pos()):
                        print("vous choisissez votre arme")
                        self.bagisopen = True

                ### TEST AFFICHAGES
                if event.type == pygame.KEYDOWN:
                    # wich one
                    if event.key == pygame.K_q:
                        print("Player is hit")
                        for player in self.currentFloor.playerGroup:
                            player.healthPoints = player.healthPoints - 1

                    elif event.key == pygame.K_s:
                        print("you earn score")
                        self.score = self.score + 3

        if self.status == "MonsterTurn":
            for monster in self.currentFloor.monsterGroup:
                self.currentFloor.UpdateMonster(monster)
            self.status = "PlayerTurn"

        #pre shot the movement
        if self.status == "PlayerMovement":
            path = self.currentFloor.Pathfinder(self.player.position, self.MouseBoardPosition())
            pathLength = self.currentFloor.PathLength(path)
            if pathLength <= self.player.movementPoints:
                color = (0,255,0)
            else:
                color = (255,0,0)
            x = self.currentFloor.size.width
            y = self.currentFloor.size.height
            larg_case = (self.large_max_grille - ((x + 1) * self.ecart)) / x
            long_case = (self.large_max_grille - ((y + 1) * self.ecart)) / y
            for pathPoint in path:
                pathPointRect = pygame.Rect(self.top_left_x+(pathPoint['position'].x*(self.ecart+long_case+1)), self.top_left_y+(pathPoint['position'].y*(self.ecart+larg_case+1)), long_case, larg_case)
                pygame.draw.rect(screen, color, pathPointRect)


        return running

    # return the case where the mouse is
    def MouseBoardPosition(self):
        return self.convert_px_in_case(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])

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

        # show player info
        self.draw_player_infos(screen)

        # show monster info
        self.draw_monster_infos(screen)

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


    # Generate a monster
    def spawn_monster(self, position: Position, movementPoints: int = 0,
                      weapon: Weapon = Weapon([[0]], Position(0, 0))):
        monster = Monster(movementPoints=movementPoints, weapon=weapon)
        self.currentFloor.SetNewObject(position, monster)
        monster.rect.x, monster.rect.y = self.convert_case_in_px(position)

    def update_position_sprite(self):
        for monster in self.currentFloor.monsterGroup:
            position = monster.position
            monster.rect.x, monster.rect.y = self.convert_case_in_px(position)
        for player in self.currentFloor.playerGroup:
            position = player.position
            player.rect.x, player.rect.y = self.convert_case_in_px(position)

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

        pygame.draw.rect(screen, (255, 0, 0), self.button_mvt)
        txt_button_mvt = font_small.render("mvt", 1, (255, 255, 255))
        screen.blit(txt_button_mvt, (650, 630))

        pygame.draw.rect(screen, (0, 255, 0), self.button_finir)
        txt_button_finir = font_small.render("end", 1, (255, 255, 255))
        screen.blit(txt_button_finir, (770, 630))

        pygame.draw.rect(screen, (0, 0, 255), self.button_attack)
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
                top_left_x_case = self.ecart + self.top_left_x + (self.larg_case * i) + (self.ecart * i)
                top_left_y_case = self.ecart + self.top_left_y + (self.long_case * j) + (self.ecart * j)

                position_case = [top_left_x_case, top_left_y_case, self.larg_case, self.long_case]
                pygame.draw.rect(screen, couleur_case, position_case)

    #draw bag when is open
    def draw_bag(self, screen):


        font_small = pygame.font.SysFont("monospace", 25, True)  # create the font style

        #Draw the background of the bag
        bag_background = pygame.image.load('assets/inventaire.png')  # import background
        screen.blit(bag_background, (0, 0))

        #draw the quit button
        pygame.draw.rect(screen, (0, 124, 124), self.quit_bag_button)
        txt_button_quit = font_small.render("Quit", 1, (255, 255, 255))
        screen.blit(txt_button_quit, (500, 500))

        # draw the weapons
        taille = 90
        DEFAULT_IMAGE_SIZE = (taille, taille)
        back_color = (253, 250, 217)
        x_start = 170
        y_start = 170
        ecart = 40
        compte_arme = 0
        x = x_start
        y = y_start

        for arme in self.weaponTab :
            if (compte_arme % 6) == 0 :
                if not (compte_arme == 0):
                    x = x_start
                    y = y + ecart + taille

            else :

                x = x + ecart + taille

            back_square_pos = [x, y, taille, taille]  # x, y, w, h
            pygame.draw.rect(screen, back_color, back_square_pos)

            image_arme = pygame.image.load(self.weaponTab[arme].imageLink)  # import image
            image_arme = pygame.transform.scale(image_arme, DEFAULT_IMAGE_SIZE)
            screen.blit(image_arme, (x, y))


            self.weaponTab[arme].button = pygame.Rect(x, y, taille, taille)

            compte_arme = compte_arme + 1


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