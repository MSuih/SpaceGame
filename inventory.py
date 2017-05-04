import gameParser as parser, connection

def openInventory(player):
    inventoryOpen = True
    while inventoryOpen:
        items = connection.getItemsFor(player)
        print("Items in inventory: ")
        for item in items:
            if item.visible: print(item.name)
        parse = parser.parseCommand(
            input("What do you want to do? (RETURN to close): "))
        if parse.command == parser.Commands.RETURN:
            inventoryOpen = False
        elif parse.command == parser.Commands.USE:
            if not connection.playerHasItem()
            # TODO: Check if item is usable
            # and if player really has it in inventory
            # if true, use it
            # else print error
        #FUTURE: inspect? other commands?

