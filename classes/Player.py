from classes.Board import Board
from classes.Position import Position
from classes.Vector import Vector

from utils.Pathfinder import Pathfinder

class Player():
    def __init__(self, spawnCoordinates:Position, board:Board, uncrossableTypes:list, hittingFunction):
        # Attributes
        self.coordinates = spawnCoordinates
        self.board = board
        self.healthPoints = 9
        self.movePoints = 3

        self.uncrossableTypes = uncrossableTypes

        self.HittingFunction = hittingFunction

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
        mvtDone = False

        while mvtDone == False:
            pygame.event.clear()
            event = pygame.event.wait()
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                position = pygame.mouse.get_pos()
                # On convertit en coordonées de case la position du click
                position_x = convert_px_in_number(position[0])
                position_y = convert_px_in_number(position[1])
                requestedCoordinates = Vector(position_x, position_y)

                mvtDone, caseOccupied = self.ValidMove(requestedCoordinates)





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
            self.HittingFunction(self, Vector(0,1), True, 1)