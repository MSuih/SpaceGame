import gameParser as parser, enum, main, game, menu, sys, connection, inventory

class State(enum.Enum):
    MAINMENU, MENU, GAME, INVENTORY, QUIT = range(5)

state = State.MAINMENU
player = None

def main():
    global state, player

    print("Welcome to Beyond Infinity")
    _printMenu()

    while state != State.QUIT:
        parse = parser.parseCommand(input("=> "))
        if parse.command == parser.Commands.QUIT:
            state = State.QUIT
            print("Saving...")
            connection.saveChanges()
            print("Thank you for playing!")
            sys.exit()
        if state == State.MENU or state == State.MAINMENU:
            _handleMenu(parse)
        elif state == State.GAME:
            _handleGame(parse)
    return

def _handleMenu(parse):
    global state, player
    
    value = menu.processInput(parse)
    if value:
        if isinstance(value, int):
            save = game.loadSave(value)
            if save:
                player = save
                state = State.GAME
                player.printCurrentSituation()
            else:
                print("Could not retrieve that save.")
        elif isinstance(value, tuple):
            save = game.startNewGame(value)
            if save:
                player = save
                state = State.GAME
                player.printCurrentSituation()
            else:
                print("Could not create a new player")
        else:
            if state == State.MAINMENU:
                print("Cannot return - you have not loaded a save")
            else:
                state = State.GAME
    elif value == None:
        print("Invalid command")

def _handleGame(parse):
    global state, player
    if player.isInCombat():
        number = player.getActiveCombat()
        if number == None:
            _startCombat(player, number)
        if not connection.isCorrectEnemyForSituation(
            number, player.getSituationNumber()):
            _startCombat(player, number)
        elif player.enemyAlive():
            _startCombat(player, number)
        else:
            # Combat has ended
            return
    else:
        if game.isSituationRelatedCommand(parse.command):
            # check if command is possible and execute it
            print("No-op")
        else:
            if parse.command == parser.Commands.INVENTORY:
                inventory.openInventory(player.number)
            elif parse.command == parser.Commands.MENU:
                print("Main menu")
                _printMenu()
                print("RETURN - close menu and return to game")
                state = State.MENU
                

def _printMenu():
    print("\nSTART - start a new player")
    print("LIST - list saved players")
    print("LOAD number - load a saved player")
    print("DELETE number - delete a save")

def _startCombat(player, enemyNumber):
    if enemyNumber == None:
        #TODO: create a new enemy
        enemytype = connection.getEnemyForSituation()
        enemy = connection.createAndReturnEnemy(enemytype)
        player.setEnemy(enemy)
    combat.processCombat(player, player.getEnemy())
    player.printSituationEndtext()

if __name__ == "__main__":
    main()
