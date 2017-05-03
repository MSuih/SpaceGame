import connection

class Player():
    def __init__(self, number, firstName, lastName, money = None):
        self.number = number
        self.firstName = firstName
        self.lastName = lastName
        self.money = money

# Starts and returns a new game 
# name is a tuple of first and last names
# returns None if game could not be started for some reason
def startNewGame(name):
    first = name[0]
    last = name[1]
    result = connection.createPlayerAndReturnId(first, last)
    if result:
        player = Player(
            result.number,
            result.firstName,
            result.lastName,
            result.money)
        return player
    return None

# Loads and returns a game from the database
# number is the ID number of this save
# returns None if a save was not found or could not be loaded
def loadSave(number):
    status = connection.getPlayer(number)
    if status: return Player(number)
