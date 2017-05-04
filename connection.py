import mysql.connector as mysqlcon, collections

_dbcon = mysqlcon.connect(
    host="localhost",
    user="dbuser",
    password="password",
    db="spacegame",
    buffered=True)

SimplePlayer = collections.namedtuple(
    "SimplePlayer", "number, firstName, lastName, money")


def saveChanges():
    _dbcon.commit()

def discardChanges():
    _dbcon.rollback()
    
def getPlayers():
    playerList = []
    cursor = _dbcon.cursor()
    sql = "SELECT id, firstName, lastName, money FROM player"
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

def getSituationDescriptionForPlayer(number):
    cursor = _dbcon.cursor()
    sql = """SELECT description FROM situation
        JOIN player ON situation.id = player.situation
        WHERE player.id = """ + number
    cursor.execute(sql)
    description = cursor.fetchone()[0]
    cursor.close()
    return description

def getEnemyForPlayer(number):
    cursor = _dbcon.cursor()
    sql = "SELECT lastEncounter FROM player WHERE id = " + str(number)
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    cursor.close()
    return result

def isCorrectEnemyForSituation(enemy, situation):
    cursor = _dbcon.cursor()
    sql = """SELECT enemy.id FROM enemy
        JOIN enemytype ON enemy.enemyType = enemytype.id
        JOIN situation ON enemytype.id = situation.enemy
        WHERE enemy.id = %i AND situation.id = %i""" % (enemy, situation)
    cursor.execute(sql)
    return len(cursor.fetchone()) == 0

def createPlayerAndReturnId(firstName, lastName):
    cursor = _dbcon.cursor()
    # find the maxHealth for player ship and use it to set current health
    sqlHealth = "SELECT maxHealth FROM ShipType WHERE id = 0;"
    cursor.execute(sqlHealth)
    try:
        health = cursor.fetchone()[0]
    except TypeError:
        print("ERROR: ShipType 0 does not exist!")
        return None
    # create a new ship for the player 
    newship = "INSERT INTO ship (health, shipType) VALUES (%d, 0);" % (health,)
    cursor.execute(newship)
    # get id of the ship created
    number = cursor.lastrowid
    addSystemsAndWeaponsToShip(0, number)
    # create a new player
    newplayer = """INSERT INTO player
        (firstName, lastName, ship) VALUES
        (%s, %s, %d);""" % (number, firstName, lastName)
    cursor.execute(newPlayer)
    # get last id
    number = cursor.lastrowid
    cursor.close()
    # return id
    return number

def addSystemsAndWeaponsToShip(shiptype, ship):
    # TODO!
    #find each systemtype for this type
    #create systems from types
    #do the same for weapon types
    return

def getEnemyForSituation(situation):
    cursor = _dbcon.cursor()
    sql = "SELECT enemy FROM situation WHERE id = " + str(situation) + ";"
    cursor.execute(sql)
    number = cursor.fetchone()
    cursor.close()
    return number

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
