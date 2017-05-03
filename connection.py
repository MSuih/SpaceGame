import mysql.connector as mysqlcon, collections

_dbcon = mysqlcon.connect(
    host="localhost",
    user="dbuser",
    password="password",
    db="spacegame",
    buffered=True)

SimplePlayer = collections.namedtuple(
    "SimplePlayer", "number, firstName, lastName, money")

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
    return playerList

def saveChanges():
    _dbcon.commit()

def discardChanges():
    _dbcon.rollback()
