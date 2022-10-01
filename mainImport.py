import pygame
import sys
import random

from classes.Bloc import Bloc as Bloc
from classes.Board import Board
from classes.Monster import Monster as MonsterClass
from classes.Player import Player as PlayerClass
from classes.Position import Position

from utils.FightPatterns import TargetStraightLine
from utils.FightPatterns import HitStraightLine
from utils.gestiongrille import *

# Constantes
NB_COL = 10
NB_ROW = 4
CELL_SIZE = 40
SCREEN = pygame.display.set_mode(size=(15 * CELL_SIZE, 15 * CELL_SIZE))


def Player(spawnCoordinates:Position, board:Board):
    return PlayerClass(spawnCoordinates, board, [Bloc, MonsterClass], lambda object, direction, HTH, damages: HitStraightLine(object, direction, HTH, damages), lambda px: convert_px_in_number(px, CELL_SIZE), DetectClick, MousePosition)

def Monster(spawnCoordinates:Position, board:Board):
    return MonsterClass(spawnCoordinates, board, [Bloc, PlayerClass], lambda object: TargetStraightLine(object, [PlayerClass], 1), lambda object, direction: HitStraightLine(object, direction, True, 1))