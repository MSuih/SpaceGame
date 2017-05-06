import gameParser as parser, connection

# Opens the inventory and lets player interact with it
# Returns once player requirests it, allowing player to do multiple things to his invenory
def openInventory(player):
    inventoryOpen = True
    while inventoryOpen:
        items = connection.getItemsForPlayer(player, True)
        print("Items in inventory: ")
        if items:
            for item in iterms:
                print(item.name)
        else:
            print("Your inventory is empty")
        parse = parser.parseCommand(
            input("What do you want to do? (RETURN to close): "))
        if parse.command == parser.Commands.RETURN:
            inventoryOpen = False
        elif parse.command == parser.Commands.USE:
            if not connection.playerHasItem(parse.target):
                print("You do not have %s in your inventory" % (parse.target,))
            else:
                print("TODO: Handle item use")
        #FUTURE: inspect? other commands?

