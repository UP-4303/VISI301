from mainImport import *

if __name__ == '__main__':
    # Constantes
    NB_COL = 10
    NB_ROW = 4
    CELL_SIZE = 40
    SCREEN = pygame.display.set_mode(size=(15 * CELL_SIZE, 15 * CELL_SIZE))

    # Variables pour pygame
    timer = pygame.time.Clock()
    game_on = True #on creer une variable booléen pour que la fenetre reste ouverte
    
    pygame.init()
    
    # Ici s'exécutera le code principal. Pour l'instant, contient les codes de test.
    board = Board((10,10))
    toUpdate = []
    player = Player(Position(1,1), board)
    toUpdate.append(player)
    monster = Monster(Position(1,6), board)
    toUpdate.append(monster)
    monster2 = Monster(Position(1,3), board)
    toUpdate.append(monster2)

    print(board.all)

    while game_on:
        for event in pygame.event.get():
            # ferme le jeu quand on le quitte
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        for updatingObject in toUpdate:
            updatingObject.PlayTurn()

        SCREEN.fill(pygame.Color("white"))  # on change la couleur de l'element
        show_grid(board, SCREEN, CELL_SIZE)
        pygame.display.update()  # met a jour la fenetre et redessine les elements
        timer.tick(60)  # duree du game loop