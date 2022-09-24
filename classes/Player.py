from classes.Board import Board
from classes.Position import Position
from classes.Vector import Vector

from utils.Pathfinder import Pathfinder

class Player():
    def __init__(self, spawnCoordinates:Position, board:Board, uncrossableTypes:list):
        # Attributes
        self.coordinates = spawnCoordinates
        self.board = board
        self.healthPoints = 9
        self.movePoints = 3

        self.uncrossableTypes = uncrossableTypes

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
    def Move(self, vector:Vector):
        self.board.MoveObject(self.coordinates, self.coordinates + vector)
        self.coordinates.Move(vector)
    
    # Check if the destination case is occupied and move only if possible
    def CheckAndMove(self, vector:Vector):
        if not self.board.IsCaseOccupied(self.coordinates + vector) or vector == Vector(0,0):
            self.Move(vector)
            didItMove = True
        else:
            didItMove = False
        return didItMove

    
    # Request the real player where to move
    def RequestMove(self):
        print(f'Actual position : ({self.coordinates.x},{self.coordinates.y}).\n Where do you want to move ?')
        requestedCoordinates = Vector(int(input('Axe X : ')),int(input('Axe Y : ')))
        validMove, caseOccupied = self.ValidMove(requestedCoordinates)
        while not(validMove):
            if caseOccupied:
                print('Case is already occupied.')
            else:
                print(f'You only have {self.movePoints} movement points.')
            print('Where do you want to go ? ')
            requestedCoordinates.x = int(input('Axe X : '))
            requestedCoordinates.y = int(input('Axe Y : '))
            validMove, caseOccupied = self.ValidMove(requestedCoordinates)
        print('Movement done !')


    # Return two booleans "This move is valid" and "Case already occupied"
    def ValidMove(self, vector:Vector):
        if len(Pathfinder(self.board, self, [self.coordinates + vector], self.uncrossableTypes).value) <= self.movePoints:
            caseOccupied = not(self.CheckAndMove(vector))
            validMove = not(caseOccupied)
        else:
            caseOccupied = False
            validMove = False
        return validMove, caseOccupied
        

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