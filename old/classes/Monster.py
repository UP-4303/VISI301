import pygame # a retirer plus tard

from classes.Board import Board
from classes.Position import Position
from classes.Vector import Vector


from utils.Pathfinder import Pathfinder

class Monster():
    def __init__(self, spawnCoordinates:Position, board:Board, uncrossableTypes:list, targetingFunction, hittingFunction):
        # Attributes
        self.coordinates = spawnCoordinates
        self.board = board
        self.healthPoints = 9
        self.maxHealthPoints = 10
        self.movePoints = 3
        self.uncrossableTypes = uncrossableTypes

        self.TargetingFunction = targetingFunction
        self.HittingFunction = hittingFunction

        # Treating creation on board
        if self.board.IsCaseOccupied(self.coordinates):
            print("MONSTER : SPAWN CASE ALREADY OCCUPIED")
        else:
            self.board.NewObject(self.coordinates, self)

    # Delete the monster on the board. Don't call this method if the monster is not on the board
    def DelFromBoard(self, reason:str):
        self.board.DeleteObject(self.coordinates)
        print(f"MONSTER : {reason}")

    # Use pathfinding to go to the nearest target position
    def Move(self):
        targets = self.TargetingFunction(self)
        if targets != []:
            path = Pathfinder(self.board, self, targets, self.uncrossableTypes)
            movePoints = self.movePoints
            newCoordinates = path.value[min(movePoints, len(path.value)-1)].coordinates
            while self.board.get(newCoordinates) != None and self.board.get(newCoordinates) != self:
                movePoints -= 1
                newCoordinates = path.value[min(movePoints, len(path.value)-1)].coordinates
            self.board.MoveObject(self.coordinates, newCoordinates)
            self.coordinates = newCoordinates

    # Decrease health
    def TakeDamage(self, amount:int):
        self.healthPoints -= amount

    # Increase health
    def RecoverHealth(self, amount:int):
        self.healthPoints += amount

    # The main code of the monster, that will be called every turn (actually just check the health)
    def PlayTurn(self):
        # Check health. If the monster is dead, it will be deleted. Else, play normally
        if self.healthPoints <= 0:
            self.DelFromBoard('MONSTER IS DEAD')
        else:
            self.Move()
            self.HittingFunction(self, Vector(0,-1))



    # Gestion de la barre de vie

    def update_health_bar(self, surface, CELL_SIZE):
        # de finition caracteristique bar
        bar_color = (255, 0, 0) #couleur
        bar_position = [self.coordinates.x* CELL_SIZE, self.coordinates.y * CELL_SIZE, (self.healthPoints) * (CELL_SIZE/self.maxHealthPoints), 7] #x, y, w, h

        # dessiner la barre
        pygame.draw.rect(surface, bar_color, bar_position)
