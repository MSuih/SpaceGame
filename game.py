import connection

class Player():
    def __init__(self, number, firstName, lastName, money = None):
        self.number = number
        self.firstName = firstName
        self.lastName = lastName
        self.money = money

    def printCurrentSituation(self):
        print(connection.getSituationDescriptionForPlayer(self.number))

    def getSituationNumber(self):
        if not self.situation:
            self.situation = connection.getSituationForPlayer(number)
        return self.situation

    def isInCombat(self):
        situation = self.getSituationNumber()
        sit_enemy = connection.getEnemyNumberForSituation()
        return sit_enemy == False

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

# Checks if the command is situation-related 
def isSituationalCommand(command):
    print("TODO: situtional command check")
    return False
    
