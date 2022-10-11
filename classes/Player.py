from classes.Character import Character
from classes.Position import Position
#Player class
class Player(Character):

    def __init__(self, name:str="Moveable", description:str="Lorem Ipsum", imageLink:str="./assets/carreblanc.png", healthPoints:int=0, position:Position=Position(0,0), movementPoints:int=0, attack:int=10):
        super().__init__(name, description, imageLink, healthPoints, position, movementPoints, attack)


#Utile : nous pouvons créer des groupes avec pygame.sprite.Group()
#all_player.add(player)
#all_player.draw(screen)
# for player in all_player :
# self.all_players.remove(self)

# Pour redimentioner une image
#self.image = pygame.transform.scale (self.image, (50, 50))
