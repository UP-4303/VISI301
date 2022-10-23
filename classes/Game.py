import sys
import pygame
from classes.Player import Player
from classes.Monster import Monster
from classes.Size import Size
from classes.Floor import Floor
from classes.Position import Position
from classes.Weapon import Weapon

class Game:
    score: int
    isplaying:bool
    floorList:list[Floor]
    currentFloor:int
    status:str
    # Status :
    # PlayerTurn : Waiting for player to choose an action
    # PlayerMovement : Waiting for player to choose a cell for movement
    # PlayerAttack : Waiting for player to choose a cell for attack
    # MonsterTurn


    def __init__(self):

        # define is the game has begin
        self.isplaying = True
        self.floorList = [Floor()]
        self.currentFloorIndex = 0
        self.currentFloor = self.floorList[self.currentFloorIndex]
        self.score = 0
        #generate the player
        self.player = Player(movementPoints=3)
        self.currentFloor.SetNewObject(Position(0,0), self.player)


        #const needed to draw the map
        self.ecart = 3
        self.top_left_x = 60
        self.top_left_y = 110
        self.large_max_grille = 450

        #TEST A ENLEVER
        self.spawn_monster(position = Position(4,4), weapon=Weapon([[0,1,0],[1,0,1],[0,1,0]], Position(0,0)))
        self.current_monster = Monster()

        self.status = "MonsterTurn"

        self.init_sprite_size()

    def update(self, screen):
        # show the score on the screen
        font = pygame.font.SysFont("monospace", 25, True) #create the font style
        score_text = font.render("Score :" + str(self.score),1, (255,255,255))  #create texte
        screen.blit(score_text, (640,60)) #show the score at the tuple position
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
        self.update_position_sprite()

        for event in pygame.event.get():
            # ferme le jeu quand on le quitte
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                if self.status == "PlayerTurn":
                    self.status = "PlayerMovement"
                if self.status == "PlayerMovement":
                    self.currentFloor.UpdatePlayer(self.player, self.convert_px_in_case(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
                    self.status == "MonsterTurn"
                if self.status == "PlayerAttack":
                    self.convert_px_in_case(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

            # TEST AFFICHAGES
            if event.type == pygame.KEYDOWN:
                # wich one
                if event.key == pygame.K_q:
                    print("Player is hit")
                    for player in self.currentFloor.playerGroup:
                        player.healthPoints = player.healthPoints -1

                elif event.key == pygame.K_s:
                    print("you earn score")
                    self.score = self.score +3
        
        if self.status == "MonsterTurn":
            print("?")
            for monster in self.currentFloor.monsterGroup:
                self.currentFloor.UpdateMonster(monster)
                print("!")
            self.status = "PlayerTurn"


    #Generate a monster
    def spawn_monster(self, position: Position, weapon):
        monster = Monster(weapon=weapon)
        self.currentFloor.SetNewObject(position, monster)
        monster.rect.x, monster.rect.y = self.convert_case_in_px(position)

    def update_position_sprite(self):
        for monster in self.currentFloor.monsterGroup:
            position = monster.position
            monster.rect.x, monster.rect.y = self.convert_case_in_px(position)
        for player in self.currentFloor.playerGroup :
            position = player.position
            player.rect.x, player.rect.y = self.convert_case_in_px(position)

    def init_sprite_size(self):

        x = self.currentFloor.size.width
        y = self.currentFloor.size.height

        larg_case = (self.large_max_grille - ((x + 1) * self.ecart)) / x
        long_case = (self.large_max_grille - ((y + 1) * self.ecart)) / y

        DEFAULT_IMAGE_SIZE = (larg_case, long_case)

        for monster in self.currentFloor.monsterGroup:
          image = monster.image
          image = pygame.transform.scale(image, DEFAULT_IMAGE_SIZE)

          monster.image = image

        for player in self.currentFloor.playerGroup :
            image = player.image
            image = pygame.transform.scale(image, DEFAULT_IMAGE_SIZE)

            player.image = image

    def draw_player_infos(self,screen):

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

    def draw_monster_infos(self,screen):
        # show monster info
        font_small = pygame.font.SysFont("monospace", 20, True)  # create the font style
        name_currentMonster_text = font_small.render("Name :" + str(self.current_monster.name), 1, (255, 255, 255))  # create texte name
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

    def draw_floor(self,screen):
        #draw name of floor
        font_small = pygame.font.SysFont("monospace", 20, True)  # create the font style
        name_currentFloor_text = font_small.render( str(self.currentFloor.name), 1,
                                                     (255, 255, 255))  # create texte name
        screen.blit(name_currentFloor_text, (60, 32))  # show the name at the tuple position

        #var on the screen background
        #top_left_x = 60
        #top_left_y = 110
        #large_max_grille = 450

        #draw the background off the floor
        back_floor = (46, 222, 231)
        floor_position = [self.top_left_x, self.top_left_y,self.large_max_grille, self.large_max_grille]
        pygame.draw.rect(screen, back_floor, floor_position)

        #draw all case

        x= self.currentFloor.size.width
        y= self.currentFloor.size.height


        larg_case = (self.large_max_grille - ((x+1) * self.ecart)) /x
        long_case = (self.large_max_grille - ((y+1) * self.ecart)) / y

        couleur_case = (76, 150, 255)

        for i in range (0, x) :
            for j in range (0, y) :

                top_left_x_case = self.ecart + self.top_left_x + (larg_case * i) +(self.ecart*i)
                top_left_y_case = self.ecart + self.top_left_y + (long_case * j) +(self.ecart*j)

                position_case =[top_left_x_case,top_left_y_case ,larg_case, long_case]
                pygame.draw.rect(screen, couleur_case, position_case)

    #convert postion on the screen to position en the map, -10 -10 if out of map
    def convert_px_in_case(self, px_x, px_y):

        x = self.currentFloor.size.width
        y = self.currentFloor.size.height

        larg_case = (self.large_max_grille - ((x + 1) * self.ecart)) / x
        long_case = (self.large_max_grille - ((y + 1) * self.ecart)) / y

        case_x = int((px_x - self.top_left_x)//(larg_case + self.ecart))
        case_y = int((px_y - self.top_left_y) // (long_case + self.ecart))

        # check if it's out of the map
        if case_x >= x or case_y >= y or case_x<0 or case_y<0:
            case_x = -10
            case_y = -10

        print(case_x, case_y) #Suppr later

        return Position(case_x, case_y)

    def convert_case_in_px(self, position:Position):

        x = self.currentFloor.size.width
        y = self.currentFloor.size.height


        larg_case = (self.large_max_grille - ((x + 1) * self.ecart)) / x
        long_case = (self.large_max_grille - ((y + 1) * self.ecart)) / y

        px_x = position.x * (larg_case + self.ecart) + self.top_left_x
        px_y  = position.y * (long_case + self.ecart) + self.top_left_y

        return px_x, px_y

    def DetectClick(self):
        pygame.event.clear()
        event = pygame.event.wait()
        return event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]
