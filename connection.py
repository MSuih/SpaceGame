import mysql.connector as mysqlcon, collections, gameParser as parser

_dbcon = mysqlcon.connect(
    host="localhost",
    user="dbuser",
    password="password",
    db="spacegame",
    buffered=True)

SimplePlayer = collections.namedtuple(
    "SimplePlayer", "number, firstName, lastName, money")
SimpleItem = collections.namedtuple("SimpleItem", "number, name, visible")
RequirementsForNext = collections.namedtuple("RequirementsForNext",
    "nextSituation, requirement, requiredAmount")
MovementToNext = collections.namedtuple("MovementToNext",
    """toSituation, description, requirement, requiredAmount,
        removeItem, rewards, rewardedAmount""")



def saveChanges():
    _dbcon.commit()

def discardChanges():
    _dbcon.rollback()

def deleteSave(number):
    cursor = _dbcon.cursor()
    sql = "DELETE FROM player WHERE id = %i;" % (number,)
    cursor.execute(sql)
    cursor.close()

# Get every player in database
def getPlayers():
    playerList = []
    cursor = _dbcon.cursor()
    sql = "SELECT id, firstName, lastName, money FROM player;"
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        player = SimplePlayer(
            number = row[0],
            firstName = row[1],
            lastName = row[2],
            money = row[3])
        playerList.append(player)
    cursor.close()
    return playerList

# Get information about player
def getPlayer(number):
    cursor = _dbcon.cursor()
    sql = "SELECT id, firstName, lastName, money FROM player WHERE id = " + str(number) + ";"
    cursor.execute(sql)
    row = cursor.fetchone()
    player = None
    if row:
        player = SimplePlayer(
            number = row[0],
            firstName = row[1],
            lastName = row[2],
            money = row[3])
    cursor.close()
    return player

# Get a description of the situation a player is in
def getSituationDescriptionForPlayer(number):
    cursor = _dbcon.cursor()
    sql = """SELECT description FROM situation
        JOIN player ON situation.id = player.situation
        WHERE player.id = %i;""" % (number,)
    cursor.execute(sql)
    description = cursor.fetchone()[0]
    cursor.close()
    return description

# Get the enemy type for the current situation (can be None)
def getEnemyForPlayer(number, isAlive):
    cursor = _dbcon.cursor()
    sql = None
    if isAlive:
        """SELECT lastEncounter FROM Player
            JOIN Ship on Player.lastEncounter = Ship.id
            WHERE id = %i AND health > 0""" % (number,)
    else:
        sql = "SELECT lastEncounter FROM player WHERE id = " + str(number) +";"
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    cursor.close()
    return result

# Is this enemy same enemy type as in this situation
def isCorrectEnemyForSituation(enemy, situation):
    cursor = _dbcon.cursor()
    sql = """SELECT enemy.id FROM enemy
        JOIN enemytype ON enemy.enemyType = enemytype.id
        JOIN situation ON enemytype.id = situation.enemy
        WHERE enemy.id = %i AND situation.id = %i;""" % (enemy, situation)
    cursor.execute(sql)
    return len(cursor.fetchone()) == 0

def createPlayerAndReturnId(firstName, lastName):
    cursor = _dbcon.cursor()
    # find the maxHealth for player ship and use it to set current health
    sqlHealth = "SELECT maxHealth FROM ShipType WHERE id = 1;"
    cursor.execute(sqlHealth)
    try:
        health = cursor.fetchone()[0]
    except TypeError:
        print("ERROR: ShipType 0 does not exist!")
        cursor.close()
        return None
    # create a new ship for the player 
    newship = "INSERT INTO ship (health, shipType) VALUES (%d, 1);" % (health,)
    cursor.execute(newship)
    # get id of the ship created
    number = cursor.lastrowid
    addSystemsAndWeaponsToShip(0, number)
    # create a new player
    newplayer = """INSERT INTO player
        (firstName, lastName, ship) VALUES
        ("%s", "%s", %i);""" % (firstName, lastName, number)
    cursor.execute(newplayer)
    # get last id
    number = cursor.lastrowid
    cursor.close()
    # return id
    return number

# Adds all systems and weapons to ship that are defined for systemtype
def addSystemsAndWeaponsToShip(shiptype, ship):
    cursor = _dbcon.cursor()
    getSystems = """SELECT systemType, maxHealth FROM SystemsForType
        JOIN Systemtype ON SystemsForType.systemType = SystemType.id
        WHERE shipType = %i;""" % (shiptype,)
    cursor.execute(getSystems)
    results = cursor.fetchall()
    for row in results:
        sql = """INSERT INTO System (health, ship, systemtype)
            VALUES (%i, %i, %i)""" % (row[1], ship, row[0])
        cursor.execute(sql)
    getWeapons = """SELECT weapon FROM WeaponsForType
        WHERE shipType = %i;""" % (shiptype,)
    cursor.execute(getWeapons)
    results = cursor.fetchall()
    for row in results:
        sql = """INSERT INTO WeaponsForShip (ship, weapon)
             VALUES (%i, %i)""" % (ship, row[0])
        cursor.execute(sql)
    cursor.close()
    return

def getEnemyForSituation(situation):
    cursor = _dbcon.cursor()
    sql = "SELECT enemy FROM situation WHERE id = %i ;" % (situation, )
    cursor.execute(sql)
    number = cursor.fetchone()
    cursor.close()
    return number

# Creates a new instance of enemytype
def createAndReturnEnemy(enemyType):
    cursor = _dbcon.cursor()
    sqlHealth = "SELECT maxHealth FROM ShipType WHERE id = " +str(enemytype)+";"
    cursor.execute(sql)
    health = cursor.fetchone()[0]
    sqlShip = "INSERT INTO ship (health, shipType) VALUES (" + str(health) + str(enemyType) + ");"
    cursor.execute(sql)
    enemy = cursor.lastrowid
    addSystemsAndWeaponsToShip(enemytype, enemy)
    cursor.close()
    return enemy

def getItemsForPlayer(player, visibleOnly):
    items = []
    cursor = _dbcon.cursor()
    sql = ""
    if visibleOnly:
        sql = """SELECT item.id, item.name, item.visible FROM item
            JOIN owneditems ON item.id = owneditems.item
            WHERE owneditems.player = %i AND item.visible = TRUE;""" % (player,)
    else:
        sql = """SELECT item.id, item.name, item.visible FROM item
            JOIN owneditems ON item.id = owneditems.item
            WHERE owneditems.player = %i;""" % (player,)
    cursor.execute(sql)
    for row in cursor.fetchall():
        item = SimpleItem(row[0], row[1], row[2])
        items.append(item)
    cursor.close()
    return items

# Check if player has a item with a certain name
def playerHasItem(player, itemname):
    cursor = _dbcon.cursor()
    sql = """SELECT owneditems.item FROM owneditems
        JOIN items ON owneditems.item = items.id
        WHERE owneditems.player = %i
        AND items.name == "%s" ;""" % (player, itemname)
    cursor.execute(sql)
    result = bool(cursor.fetchone())
    cursor.close()
    return result

def removeItemFromPlayer(player, item, amount):
    cursor = _dbcon.cursor()
    sql = """DELETE FROM OwnedItems
        WHERE player = %i AND item = %i
        LIMIT %i;""" % (player, item, amount)
    cursor.execute(sql)
    cursor.close()
    
def addItemToPlayer(item, player, amount):
    cursor = _dbcon.cursor()
    sql = """INSERT INTO OwnedItems (player, item)
        VALUES (%i, %i);""" % (player, item)
    for i in range(amount):
        cursor.execute(sql)
    cursor.close()

# Check if player has certain amount of a item or more
def hasPlayerAmountOfItem(player, item, amount):
    cursor = _dbcon.cursor()
    sql = """SELECT count(item) FROM OwnedItems
        WHERE player = %i AND item = %i;""" % (player, item)
    cursor.execute(sql)
    result = cursor.fetchone()
    if result:
        result = result[0] >= amount
    cursor.close()
    return result

def getSituationOf(player):
    cursor = _dbcon.cursor()
    sql = "SELECT situation FROM Player WHERE id = %i;" % (player,)
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    cursor.close()
    return result

def updateSituationForPlayer(newSituation, player):
    cursor = _dbcon.cursor()
    sql = "UPDATE Player SET situation = %i WHERE id = %i" % (newSituation, player)
    cursor.execute(sql)
    cursor.close()

# Player has given a command for moving from one situation to another
# Get a list of where player could end up and what items are required for that
def getNextSituation(situation, parse):
    lista = []
    cursor = _dbcon.cursor()
    cnum = _getDBNumberForCommand(parse.command)
    sql = """SELECT toSituation, requires, requiredAmount FROM NextSituation
        WHERE fromSituation = %i AND command = %i AND target = "%s"
        ORDER BY requires IS NULL,
          requiredAmount;""" % (situation, cnum, parse.target)
    cursor.execute(sql)
    for row in cursor.fetchall():
        lista.append(
            RequirementsForNext(
                nextSituation = row[0],
                requirement = row[1],
                requiredAmount = row[2]))
    cursor.close()
    return lista

# Get more information about a move to next situation
# reqForNext is an object returned by getNextSituation()
def getFullMove(currentSituation, reqForNext):
    cursor = _dbcon.cursor()
    reqOrNone = "= " + str(reqForNext.requirement) if reqForNext.requirement else "IS NULL"
    sql = """SELECT toSituation, description,
    requires, requiredAmount, removeItem, rewards, rewardedAmount
    FROM NextSituation
    WHERE fromSituation = %i AND toSituation = %i
    AND requires %s AND requiredAmount = %i;""" %(currentSituation,
            reqForNext.nextSituation, reqOrNone, reqForNext.requiredAmount)
    cursor.execute(sql)
    result = cursor.fetchone()
    fullmove = MovementToNext(
        toSituation = result[0],
        description = result[1],
        requirement = result[2],
        requiredAmount = result[3],
        removeItem = result[4],
        rewards = result[5],
        rewardedAmount = result[6])
    cursor.close()
    return fullmove

# Get the ID number for this command
# Caches the id numbers into a cache so that db is not queried every single time
_commandcache = {}
def _getDBNumberForCommand(command):
    if not _commandcache:
        dblist = _getCommands()
        parlist = parser.Commands
        for dbcom in dblist:
            for parcom in parlist:
                if parcom.name.lower() == dbcom.name.lower():
                    _commandcache[parcom] = dbcom.value
                    break
            
    return _commandcache[command]

# Gets a list of all commands that are stored in the database
DBCommands = collections.namedtuple("DBCommands", "name, value")
def _getCommands():
    lista = []
    cursor = _dbcon.cursor()
    sql = "SELECT id, command FROM Command"
    cursor.execute(sql)
    for row in cursor.fetchall():
        lista.append(DBCommands(name = row[1], value = row[0]))
    cursor.close()
    return lista
