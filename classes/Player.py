import pygame # a enlever plus tard

from classes.Board import Board
from classes.Position import Position
from classes.Vector import Vector

from utils.Pathfinder import Pathfinder

class Player():
    def __init__(self, spawnCoordinates:Position, board:Board, uncrossableTypes:list, hittingFunction, convertPxInNumber, detectClick, mousePosition):
        # Attributes
        self.coordinates = spawnCoordinates
        self.board = board
        self.healthPoints = 9
        self.maxHealthPoints = 10
        self.movePoints = 3

        self.uncrossableTypes = uncrossableTypes

        self.HittingFunction = hittingFunction
        self.ConvertPxInNumber = convertPxInNumber
        self.DetectClick = detectClick
        self.MousePosition = mousePosition

        # Treating creation on board
        if self.board.IsCaseOccupied(self.coordinates):
            self.__del__("SPAWN CASE ALREADY OCCUPIED")
        else:
            self.board.NewObject(self.coordinates, self)

    # Delete the player and print a message for debug purpose
    def __del__(self, reason:str="Player deleted"):
        print(reason)

    # Delete the player and it's board self. Don't call this method if the player is not on the board
    def DelFromBoard(self,reason:str):
        self.board.DeleteObject(self.coordinates)
        self.__del__(reason)

    # Just move the player. USE IT CAUTIOUSLY (it can delete another object on the board)
    def Move(self, position:Position):
        self.board.MoveObject(self.coordinates, position)
        self.coordinates.Move(position - self.coordinates)
    
    # Check if the destination case is occupied and move only if possible
    def CheckAndMove(self, position:Position):
        if not self.board.IsCaseOccupied(position) or self.coordinates == position:
            self.Move(position)
            didItMove = True
        else:
            didItMove = False
        return didItMove

    
    # Request the real player where to move
    def RequestMove(self):
        mvtDone = False

        while mvtDone == False:
            if self.DetectClick():
                mousePosition = self.MousePosition()
                # On convertit en coordonées de case la position du click
                position_x = self.ConvertPxInNumber(mousePosition[0])
                position_y = self.ConvertPxInNumber(mousePosition[1])

                print(position_x, position_y)


                if position_x >= 0 and position_x < self.board.size[0] and position_y >= 0 and position_y < self.board.size[1]:
                    requestedCoordinates = Position(position_x, position_y)
                    mvtDone = self.ValidMove(requestedCoordinates)

    # Check if the move is valid and do it, then return a boolean true if the movment is valid 
    def ValidMove(self, position:Position):
        if len(Pathfinder(self.board, self, [position], self.uncrossableTypes).value) <= self.movePoints:
            validMove = self.CheckAndMove(position)
        else:
            validMove = False
        return validMove
        

    # Decrease health
    def TakeDamage(self, amount:int):
        self.healthPoints -= amount

    # Increase health
    def RecoverHealth(self, amount:int):
        self.healthPoints += amount
    
    # The main code of the player, that will be called every turn (actually just check the health)
    def PlayTurn(self):
        # Check health. If the player is dead, it will be deleted. Else, play normally
        if self.healthPoints <= 0:
            self.DelFromBoard('PLAYER IS DEAD')
        else:
            self.RequestMove()
            self.HittingFunction(self, Vector(0,1), True, 1)

    def update_health_bar(self, surface, CELL_SIZE):
        # definition caracteristique bar
        bar_color = (0, 255, 255)  # couleur
        bar_position = [self.coordinates.y * CELL_SIZE, self.coordinates.x * CELL_SIZE,
                        (self.healthPoints) * (CELL_SIZE / self.maxHealthPoints), 7]  # x, y, w, h

        # dessiner la barre
        pygame.draw.rect(surface, bar_color, bar_position)