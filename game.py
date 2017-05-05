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
        return connection.hasPlayerAmountOfItem(self.number, item, amount)

    def removeItem(self, item, amount = 1):
        connection.removeItemFromPlayer(item, self.number, amount)

    def addItem(self, item, amount = 1):
        connection.addItemToPlayer(item, self.number, amount)

    def performCommand(self, reqForNext):
        fullmove = connection.getFullMove(self.getSituationNumber(),reqForNext)
        if fullmove.removeItem:
            self.removeItem(fullmove.requirement, fullmove.requiredAmount)
        if fullmove.rewards:
            self.addItem(fullmove.rewards, fullmove.rewardedAmount)
        connection.updateSituationForPlayer(fullmove.toSituation, self.number)
        return fullmove.description
            

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

# Can player perform this command?
# returns none if parse is not valid for this location
# returns False if player is missing an item
# returns RequirementsForNext if command can be performed 
def canPerformCommand(player, parse):
    attempts = connection.getNextSituation(player.getSituationNumber(), parse)
    if not attempts:
        return None
    for attempt in attempts:
        if not attempt.requirement or player.hasItem(attempt.requirement, attempt.requiredAmount):
            return attempt
    return False
