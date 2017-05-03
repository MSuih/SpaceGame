import gameParser as parser, enum, main, game, menu, sys, connection

class State(enum.Enum):
    MAINMENU, MENU, GAME, INVENTORY, QUIT = range(5)

def main(): 
    state = State.MENU
    game = None

    print("Welcome to game")
    print("\nSTART - start a new game")
    print("LIST - list saved games")
    print("LOAD number - load a saved game")

    while state != State.QUIT:
        parse = parser.parseCommand(input("=> "))
        if parse.command == parser.Commands.QUIT:
            state = State.QUIT
            print("Saving...")
            connection.saveChanges()
            print("Thank you for playing!")
            sys.exit()
        if state == State.MENU:
            value = menu.processInput(parse)
            if value:
                if isinstance(value, int):
                    save = game.loadSave(value)
                    if save:
                        game = save
                        state = State.GAME
                    else:
                        print("Game not found")
                elif isinstance(value, tuple):
                    print("TODO")
                    # start a new game 
                else:
                    if state == MAINMENU:
                        print("Cannot return - game is not open")
                    else:
                        state = State.GAME
            elif value == None:
                print("Invalid command")
        #elif state == State.GAME:
    return

main()
