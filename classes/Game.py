
import pygame
from classes.Player import Player
from classes.Monster import Monster
from classes.Size import Size
from classes.Floor import Floor
class Game:
    score: int
    isplaying:bool
    floorList:list[Floor]
    currentFloor:int

    def __init__(self, floorList:list[Floor]=[],currentFloornb=0):
        # define is the game has begin
        self.isplaying = True
        self.floorList = floorList
        self.currentFloornb = currentFloornb
        self.score = 0
        #generate the player
        self.player = Player()
        self.list_player = pygame.sprite.Group()
        #keep all the monsters in a groupe
        self.all_monsters = pygame.sprite.Group()
        self.current_monster = Monster()

        #TEST A ENLEVER
        self.spawn_monster()
        floor = Floor("Floor0", size=Size(3,3))
        self.floorList = [floor]
        self.currentFloor =self.floorList[self.currentFloornb];




    def update(self, screen):
        # show the score on the screen
        font = pygame.font.SysFont("monospace", 25, True) #create the font style
        score_text = font.render("Score :" + str(self.score),1, (255,255,255))  #create texte
        screen.blit(score_text, (640,60)) #show the score at the tuple position

        # show player info
        self.draw_player_infos(screen)

        # show monster info
        self.draw_monster_infos(screen)

        # show monstres (maybe better in main)
        self.all_monsters.draw(screen)

        # show the player
        self.list_player.draw(screen)

        # show floor
        self.draw_floor(screen)



    #Generate a monster
    def spawn_monster(self):
        monster = Monster()
        self.all_monsters.add(monster)

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

    def draw_floor(self,screen):
        top_left_x = 60
        top_left_y = 110
        large_max_grille = 390
        #draw the background off the floor
        back_floor = (46, 222, 231)
        floor_position = [top_left_x, top_left_y, top_left_x + large_max_grille, large_max_grille]
        pygame.draw.rect(screen, back_floor, floor_position)

        #draw case

        x= self.currentFloor.size.width
        y= self.currentFloor.size.height

        ecart = 3
        larg_case = (large_max_grille - ((x+1) * ecart)) /x
        long_case = (large_max_grille - ((y+1) * ecart)) / y

        couleur_case = (76, 150, 255)

        for i in range (0, x-1) :
            for j in range (0, y-1) :
                print(i, j)
                top_left_x_case = top_left_x + (larg_case * i) +(ecart*i)
                top_left_y_case = top_left_y + (long_case * j) +(ecart*j)
                print(top_left_x_case, top_left_y_case)
                position_case =[top_left_x_case,top_left_y_case ,top_left_x_case + larg_case, long_case]
                pygame.draw.rect(screen, couleur_case, position_case)


        print("LLLLLLLLLLLL")