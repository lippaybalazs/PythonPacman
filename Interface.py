from Table import Table

from getkey import getkey
import threading

object_representation = {
    "pacman-left": "\u001b[33m◑\u001b[0m",
    "pacman-right": "\u001b[33m◐\u001b[0m",
    "pacman-down": "\u001b[33m◓\u001b[0m",
    "pacman-up": "\u001b[33m◒\u001b[0m",
    "pacman-whole": "\u001b[33m●\u001b[0m",
    "pacman-left-rage": "\u001b[35m◑\u001b[0m",
    "pacman-right-rage": "\u001b[35m◐\u001b[0m",
    "pacman-down-rage": "\u001b[35m◓\u001b[0m",
    "pacman-up-rage": "\u001b[35m◒\u001b[0m",
    "pacman-whole-rage": "\u001b[35m●\u001b[0m",
    "wall": "\u001b[34m░\u001b[0m",
    "coin": "\u001b[33m⚬\u001b[0m",
    "fruit": "\u001b[34m◈\u001b[0m",
    "ghost-1": "\u001b[31m●\u001b[0m",
    "ghost-2": "\u001b[32m●\u001b[0m",
    "ghost-3": "\u001b[36m●\u001b[0m",
    None: " "
}

def logger(func):
    def inner(table):
        file = open("recording.csv",'a')
        for i in range(len(table.table)):
            for j in range(len(table.table[i])):
                if j % 2 == 0:
                    o = table.table[i][j]
                    if o is None:
                        o = table.transparent_table[i][j]
                    file.write(str(o) + ",")
            file.write("\n")
        file.write("\n")
        func(table)
    return inner

class ConsoleMediator:

    target = None

    def set_target(target):
        ConsoleMediator.target = target
        target.mediator = ConsoleMediator

    def signal_key(key):
        if key == "w":
            ConsoleMediator.target.set_direction_up()
        elif key == "s":
            ConsoleMediator.target.set_direction_down()
        elif key == "a":
            ConsoleMediator.target.set_direction_left()
        elif key == "d":
            ConsoleMediator.target.set_direction_right()

    def signal_score(amount):
        ConsoleInterface.score = amount


class ConsoleInterface:

    score = 0

    def __clear_screen():
        print("\033[2J")

    def __reset_cursor():
        print("\033[0;0H")

    def start():
        open("recording.csv",'w').close()
        ConsoleInterface.__clear_screen()
        threading.Thread(target=ConsoleInterface.keyboard_event_handler).start()

    @logger
    def draw_frame(table: Table):
        ConsoleInterface.__reset_cursor()
        for i in range(len(table.table)):
            row_string = ""
            for j in range(len(table.table[i])):
                o = table.table[i][j]
                if o == None:
                    o = table.transparent_table[i][j]
                row_string += object_representation[o]
            print(row_string)
        print("Score: " + str(ConsoleInterface.score))

    def keyboard_event_handler():
        while True:
            key = getkey()
            ConsoleMediator.signal_key(key)
        
   