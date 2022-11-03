from classes.Character import Character
from classes.Position import Position
from classes.Weapon import Weapon
#Player class
class Player(Character):

    def __init__(self, name:str="Player", description:str="Lorem Ipsum", imageLink:str="./assets/player.png", healthPoints:int=10, position:Position=Position(0,0), movementPoints:int=0, weapon:Weapon=Weapon()):
        super().__init__(name, description, imageLink, healthPoints, position, movementPoints, weapon)
        self.money = 0
        self.rect.x = self.position.x
        self.rect.y = self.position.y


#Utile : nous pouvons créer des groupes avec pygame.sprite.Group()
#all_player.add(player)
#all_player.draw(screen)
# for player in all_player :
# self.all_players.remove(self)

# Pour redimentioner une image
#self.image = pygame.transform.scale (self.image, (50, 50))
