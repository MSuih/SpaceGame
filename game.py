import connection

class Player():
    def __init__(self, number, firstName, lastName):
        self.number = number
        self.firstName = firstName
        self.lastName = lastName

    def printCurrentSituation(self):
        print(connection.getSituationDescriptionForPlayer(self.number))

    def getSituationNumber(self):
        return connection.getSituationOf(self.number)

    def isInCombat(self):
        situation = self.getSituationNumber()
        sit_enemy = connection.getEnemyForSituation(situation)
        return sit_enemy == False
    
    def enemyAlive():
        return connection.getEnemyForPlayer(self.number)

    def hasItem(self, item, amount = 1):
        return connection.hasPlayerAmountOfItem(player, item, amount)

# Starts and returns a new game 
# name is a tuple of first and last names
# returns None if game could not be started for some reason
def startNewGame(name):
    first = name[0]
    last = name[1]
    result = connection.createPlayerAndReturnId(first, last)
    if result:
        player = Player(
            result,
            first,
            last)
        return player
    return None

# Loads and returns a game from the database
# number is the ID number of this save
# returns None if a save was not found or could not be loaded
def loadSave(number):
    status = connection.getPlayer(number)
    if status: return Player(
        status.number, status.firstName, status.lastName)

def canPerformCommand(player, parse):
    attempts = connection.getNextSituation(player.getSituationNumber, parse)
    if not attempts:
        return None
    for attempt in attempts:
        if attempt.requirement:
            if player.hasItem(attempt.requirement, attempt.requiredAmount):
                return True
        else:
            return True
    return False
