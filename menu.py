import gameParser as parser, connection

# Processes parsed input
# returns None if nothing happened
# returns true if user wants to return to game
# returns int if user wants to load a game
# returns tuple (firstname, lastname)
def processInput(parse):
    if parse.command == parser.Commands.RETURN:
        return "Boolean is instance of int, so we have to use something else"
    elif parse.command == parser.Commands.LISTSAVES:
        playerList = connection.getPlayers()
        if playerList:
            print("Saved games")
            for p in playerList:
                print(
                    "SAVE %i: %s %s, money: %i"
                    % (p.number, p.firstName, p.lastName, p.money))
        else: print("No saves found")
        return False
    elif parse.command == parser.Commands.LOADGAME:
        if parse.target and parse.target.isdigit():
            return int(parse.target)
        else:
            print("Put save number after LOAD - use LIST to get a list of saves")
            return False
    elif parse.command == parser.Commands.NEWGAME:
        return _askNameFromPlayer()
    elif parse.command == parser.Commands.DELETE:
        if parse.target and parse.target.isdigit():
            connection.deleteSave(int(parse.target))
            print("Save number %s has been deleted" % (parse.target,))
        return False
    else:
        return None

def _askNameFromPlayer():
	print("-- Replace with interduction --")
	first = input("First name: ")
	last = input("Last name: ")
	return (first, last)
