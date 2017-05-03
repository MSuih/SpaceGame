import collections, enum

# All commands that player can do
class Commands(enum.Enum):
    INVALID, QUIT, GOTO, TALK, INVENTORY = range(0, 5)
    LISTSAVES, LOADGAME, NEWGAME, RETURN = range(5, 9)

# Tuple that contains a command and the target of that command
# ParseResult.command is one of the commands defined above (enum)
# ParseResult.target is a random target for that command (string)
# target is always in lowercase and can be None
ParseResult = collections.namedtuple("ParseResult", "command, target")

# Takes a string and parses it to check for commands
# Command is case-insensitive
# Returns a namedtuple called ParseResult (defined above)
def parseCommand(command):
    splitString = command.split()
    command = Commands.INVALID
    target = " "

    # Parsing first part of string
    firstPart = splitString[0].lower()
    if firstPart == "quit" or firstPart == "exit":
        return ParseResult(command = Commands.QUIT, target = None)
    elif firstPart == "go":
        command = Commands.GOTO
    elif firstPart == "talk":
        command = Commands.TALK
    elif firstPart == "inventory":
        command = Commands.INVENTORY
    elif firstPart == "start":
        command = Commands.NEWGAME
    elif firstPart == "load":
        command = Commands.LOADGAME
    elif firstPart == "return":
        command = Commands.RETURN
    elif firstPart == "listsaves" or firstPart == "list":
        command = Commands.LISTSAVES
    else:
        #Command not found
        return ParseResult(command = Commands.INVALID, target = None)

    if len(splitString) > 1:
        # Checking if command has multiple parts
        secondPart = splitString[1].lower()

        # put rest of the command as target
        if _isPartOfCommand(command, secondPart):
            target = target.join([s.lower() for s in splitString[2:]])
        else:
            target = target.join(s.lower() for s in splitString[1:])
    else: target = None

    return ParseResult(command = command, target = target )

# Commands can contain multiple words
# For example talk can be written as "talk", "talk to" or "talk with"
# Returns True if string is a valid extension to command, otherwise returns false
def _isPartOfCommand(command, string):
    if command == Commands.GOTO:
        return string == "to"
    if command == Commands.TALK:
        if string == "to": return True
        elif string == "with": return True
        return False
    return False


# Testing if the class works as intended
def test():
    testCommands = ["talk man", # Following three should result in talk -> man
                    "TALK WITH MAN",
                    "TaLK tO mAN",
                    "Unknown command", # Following two should return invalid
                    "this command should not exist",
                    "go to location", # Following two should return goto -> location
                    "go location",
                    "quit game", # following two should return exit
                    "exit"]
    for command in testCommands:
        result = parseCommand(command)
        print("Command: " + result.command.name)
        if result.target: print("Target: " + result.target)
        else: print("No target")

# Don't run test when this file is imported to other parts of the program
if __name__ == "__main__":
    test()
