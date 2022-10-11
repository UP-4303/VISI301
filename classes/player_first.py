import pygame

#Player class
class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.health = 100
        self.max_health = 100
        self.attack = 10
        self.velocity = 5
        self.image = pygame.image.load('assets/player.png')
        self.rect = self.image.get_rect()


#Utile : nous pouvons créer des groupes avec pygame.sprite.Group()
#all_player.add(player)
#all_player.draw(screen)
# for player in all_player :
# self.all_players.remove(self)

# Pour redimentioner une image
#self.image = pygame.transform.scale (self.image, (50, 50))
