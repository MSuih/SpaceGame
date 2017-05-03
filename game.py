import connection

class Player():
    def __init__(self, number, firstName = None, lastName = None):
        self.number = number
        self.firstName = firstName
        self.lastName = lastName

    def getFirstName(self):
        if not self.firstName:
            self.firstName = connection.getFirstNameForPlayer(number)
        return self.firstName
             

# Starts and returns a new game 
# name is a tuple of first and last names
# returns None if game could not be started for some reason
def startNewGame(name):
    first = name[0]
    last = name[1]
    number = connection.createPlayerAndReturnId(first, last)
    player = Player(number, name[first, last)
    return player

# Loads and returns a game from the database
# number is the ID number of this save
# returns None if a save was not found or could not be loaded
def loadSave(number):
    status = connection.doesPlayerExist(number)
    if status: return Player(number)
