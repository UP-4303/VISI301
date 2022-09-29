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


def Player(spawnCoordinates:Position, board:Board):
    return PlayerClass(spawnCoordinates, board, [Bloc, MonsterClass], lambda object, direction, HTH, damages: HitStraightLine(object, direction, HTH, damages))

def Monster(spawnCoordinates:Position, board:Board):
    return MonsterClass(spawnCoordinates, board, [Bloc, PlayerClass], lambda object: TargetStraightLine(object, [PlayerClass], 1), lambda object, direction: HitStraightLine(object, direction, True, 1))