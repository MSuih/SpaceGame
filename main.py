import gameParser as parser, enum, main, game, menu, sys, connection

class State(enum.Enum):
    MAINMENU, MENU, GAME, INVENTORY, QUIT = range(5)

def main(): 
    state = State.MENU
    player = None

    print("Welcome to Beyond Infinity")
    print("\nSTART - start a new player")
    print("LIST - list saved players")
    print("LOAD number - load a saved player")

    while state != State.QUIT:
        parse = parser.parseCommand(input("=> "))
        if parse.command == parser.Commands.QUIT:
            state = State.QUIT
            print("Saving...")
            connection.saveChanges()
            print("Thank you for playing!")
            sys.exit()
        if state == State.MENU:
            _handleMenu(parse)
        elif state == State.GAME:
            _handleGame(parse)
    return

def _handleMenu(parse):
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
            if state == MAINMENU:
                print("Cannot return - you have not loaded a save")
            else:
                state = State.GAME
    elif value == None:
        print("Invalid command")

def _handleGame(parse):
    if player.isInCombat():
        combat.processCombat()
    else:
        if game.isSituationalCommand(parse.command):

if __name__ == "__main__":
    main()
