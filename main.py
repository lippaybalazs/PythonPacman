from Table import Table
from Interface import ConsoleInterface, ConsoleMediator
from Run import GhostObserver, IterativeRunner
from random import choice

import time

game_over = False
next_level = False

def notify_death(character):
    if "pacman" == character:
        global game_over
        game_over = True
    if "board" == character:
        global next_level
        next_level = True

if __name__ == "__main__":
    
    ConsoleMediator.set_target(IterativeRunner)
    IterativeRunner.listen_deaths(GhostObserver.notify_death)
    IterativeRunner.listen_deaths(notify_death)
    ConsoleInterface.start()

    def random_move_ghost1(environment: Table):  
        pac_x = 1
        if environment.pacman[0] <= environment.ghost1[0]:
            pac_x = -1
        pac_y = 1
        if environment.pacman[1] <= environment.ghost1[1]:
            pac_y = -1
        
        while True:
            choices = []
            if random_move_ghost1.tick % 100 > 20:
                choices.extend([(pac_x,0) for _ in range(5)])
                choices.extend([(0,pac_y) for _ in range(5)])
            choices.extend([random_move_ghost1.last_direction for _ in range(5)])
            choices.extend([(0,1),(0,-1),(1,0),(-1,0)])
            direction = choice(choices)
            if environment.get_area(environment.ghost1[0] + direction[0],environment.ghost1[1] +  direction[1]) != "wall":
                break
        random_move_ghost1.last_direction = direction
        random_move_ghost1.tick += 1
        return direction
    random_move_ghost1.last_direction = (0,-1)
    random_move_ghost1.tick = 0
    IterativeRunner.set_ghost1_engine(random_move_ghost1)

    def random_move_ghost2(environment: Table):
        while True:
            choices = [random_move_ghost2.last_direction for _ in range(10)]
            choices.extend([(0,1),(0,-1),(1,0),(-1,0)])
            direction = choice(choices)
            if environment.get_area(environment.ghost2[0] + direction[0],environment.ghost2[1] +  direction[1]) != "wall":
                break
        random_move_ghost2.last_direction = direction
        return direction
    random_move_ghost2.last_direction = (0,-1)
    IterativeRunner.set_ghost2_engine(random_move_ghost2)

    def random_move_ghost3(environment: Table):
        if environment.ghost3 == random_move_ghost3.target:
            random_move_ghost3.target = (19,19)
        tar_x = 1
        if random_move_ghost3.target[0] < environment.ghost3[0]:
            tar_x = -1
        tar_y = 1
        if random_move_ghost3.target[1] < environment.ghost3[1]:
            tar_y = -1
        while True:
            choices = []
            if random_move_ghost1.tick % 100 < 70:
                choices.extend([(tar_x,0) for _ in range(5)])
                choices.extend([(0,tar_y) for _ in range(5)])
            choices.extend([random_move_ghost3.last_direction for _ in range(4)])
            choices.extend([(0,1),(0,-1),(1,0),(-1,0)])
            direction = choice(choices)
            if environment.get_area(environment.ghost3[0] + direction[0],environment.ghost3[1] +  direction[1]) != "wall":
                break
        random_move_ghost3.last_direction = direction
        return direction
    random_move_ghost3.last_direction = (0,-1)
    random_move_ghost3.target = (1,1)
    IterativeRunner.set_ghost3_engine(random_move_ghost3)


    while not game_over:
        main_table = Table.get_instance()
        IterativeRunner.set_environment(main_table)
        GhostObserver.set_environment(main_table)
        next_level = False
        
        while not next_level and not game_over:
            IterativeRunner.act()
            ConsoleInterface.draw_frame(main_table)
            time.sleep(0.5)
    print("Game Over")
