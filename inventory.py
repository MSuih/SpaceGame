def openInventory(player):
    inventoryOpen = True
    while inventoryOpen:
        items = connection.getItemsFor(player)
        for item in items:
            if item.visible: print(item.name)
        break
        #TODO: ask player what to do
        #if command is related to items, execute it
        #loop untill player closes inventory
