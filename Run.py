from random import randint
from Table import Table, GhostFactory

class GhostObserver:
    environment: Table = None
    
    def set_environment(environment):
        GhostObserver.environment = environment

    def notify_death(character):
        if character == "ghost-1":
            GhostObserver.environment.ghost1 = (10,10)
            GhostObserver.environment.set_area(10,10,GhostFactory.create_ghost1())
        if character == "ghost-2":
            GhostObserver.environment.ghost2 = (10,10)
            GhostObserver.environment.set_area(10,10,GhostFactory.create_ghost2())
        if character == "ghost-3":
            GhostObserver.environment.ghost3 = (10,10)
            GhostObserver.environment.set_area(10,10,GhostFactory.create_ghost3())


class IterativeRunner:
    
    environment: Table = None
    direction = (0,1)
    tick = 0
    mediator = None
    score = 0
    hunt = 0
    fruit_exists = False
    observers = []
    ghost1_engine = None
    ghost2_engine = None
    ghost3_engine = None

    def set_ghost1_engine(function):
        IterativeRunner.ghost1_engine = function

    def set_ghost2_engine(function):
        IterativeRunner.ghost2_engine = function

    def set_ghost3_engine(function):
        IterativeRunner.ghost3_engine = function

    def set_environment(environment):
        IterativeRunner.environment = environment

    def set_direction_up():
        IterativeRunner.direction = (0,-1)

    def set_direction_down():
        IterativeRunner.direction = (0,1)

    def set_direction_left():
        IterativeRunner.direction = (-1,0)

    def set_direction_right():
        IterativeRunner.direction = (1,0)

    def get_pacman_variation():
        rage = ""
        if IterativeRunner.hunt > 0:
            rage = "-rage"
        if IterativeRunner.tick % 2 == 0:
            return "pacman-whole" + rage
        if IterativeRunner.direction == (0,-1):
            return "pacman-up" + rage
        if IterativeRunner.direction == (0,1):
            return "pacman-down" + rage
        if IterativeRunner.direction == (-1,0):
            return "pacman-left" + rage
        if IterativeRunner.direction == (1,0):
            return "pacman-right" + rage

    def character_died(character):
        for observer in IterativeRunner.observers:
            observer(character)

    def listen_deaths(observer):
        IterativeRunner.observers.append(observer)

    def act():

        # pacman movement
        
        pacman = IterativeRunner.environment.pacman
        to_be_x = pacman[0] + IterativeRunner.direction[0]
        to_be_y = pacman[1] + IterativeRunner.direction[1]
        if IterativeRunner.environment.get_area(to_be_x, to_be_y) != "wall":
            if IterativeRunner.environment.get_area(to_be_x, to_be_y) == "coin":
                IterativeRunner.environment.coin_count -= 1
                IterativeRunner.score += 1
                IterativeRunner.environment.remove_transparent(to_be_x,to_be_y)
                IterativeRunner.mediator.signal_score(IterativeRunner.score)
            if IterativeRunner.environment.get_area(to_be_x, to_be_y) == "fruit":
                IterativeRunner.hunt = 30
                IterativeRunner.fruit_exists = False
                IterativeRunner.environment.remove_transparent(to_be_x,to_be_y)
        
            # Ghost collision
            if IterativeRunner.environment.ghost1 == (to_be_x, to_be_y):
                if IterativeRunner.hunt > 0:
                    IterativeRunner.character_died("ghost-1")
                    IterativeRunner.score += 10
                    IterativeRunner.mediator.signal_score(IterativeRunner.score)
                else:
                    IterativeRunner.character_died("pacman")
            if IterativeRunner.environment.ghost2 == (to_be_x, to_be_y):
                if IterativeRunner.hunt > 0:
                    IterativeRunner.character_died("ghost-2")
                    IterativeRunner.score += 10
                    IterativeRunner.mediator.signal_score(IterativeRunner.score)
                else:
                    IterativeRunner.character_died("pacman")
            if IterativeRunner.environment.ghost3 == (to_be_x, to_be_y):
                if IterativeRunner.hunt > 0:
                    IterativeRunner.character_died("ghost-3")
                    IterativeRunner.score += 10
                    IterativeRunner.mediator.signal_score(IterativeRunner.score)
                else:
                    IterativeRunner.character_died("pacman")
            IterativeRunner.hunt -= 1
        

            IterativeRunner.environment.set_area(pacman[0],pacman[1], None)
            IterativeRunner.environment.pacman = pacman = (to_be_x, to_be_y)
        IterativeRunner.environment.set_area(pacman[0], pacman[1], IterativeRunner.get_pacman_variation())

        # ghost movement

        ghost1 = IterativeRunner.environment.ghost1
        direction1 = IterativeRunner.ghost1_engine(IterativeRunner.environment)
        ghost2 = IterativeRunner.environment.ghost2
        direction2 = IterativeRunner.ghost2_engine(IterativeRunner.environment)
        ghost3 = IterativeRunner.environment.ghost3
        direction3 = IterativeRunner.ghost3_engine(IterativeRunner.environment)

        if IterativeRunner.environment.get_area(ghost1[0], ghost1[1]) == "ghost-1":
            IterativeRunner.environment.set_area(ghost1[0], ghost1[1], None)
        if IterativeRunner.environment.get_area(ghost2[0], ghost2[1]) == "ghost-2":
            IterativeRunner.environment.set_area(ghost2[0], ghost2[1], None)
        if IterativeRunner.environment.get_area(ghost3[0], ghost3[1]) == "ghost-3":
            IterativeRunner.environment.set_area(ghost3[0], ghost3[1], None)

        ignore1 = False
        ignore2 = False
        ignore3 = False

        collision1 = IterativeRunner.environment.get_area(ghost1[0] + direction1[0], ghost1[1] + direction1[1])
        if collision1 is not None and "pacman" in collision1:
            if IterativeRunner.hunt > 0:
                IterativeRunner.character_died("ghost-1")
                IterativeRunner.score += 10
                IterativeRunner.mediator.signal_score(IterativeRunner.score)
                ignore1 = True
            else:
                IterativeRunner.character_died("pacman")
        collision2 = IterativeRunner.environment.get_area(ghost2[0] + direction2[0], ghost2[1] + direction2[1])
        if collision2 is not None and "pacman" in collision2:
            if IterativeRunner.hunt > 0:
                IterativeRunner.character_died("ghost-2")
                IterativeRunner.score += 10
                IterativeRunner.mediator.signal_score(IterativeRunner.score)
                ignore2 = True
            else:
                IterativeRunner.character_died("pacman")
        collision3 = IterativeRunner.environment.get_area(ghost3[0] + direction3[0], ghost3[1] + direction3[1])
        if collision3 is not None and "pacman" in collision3:
            if IterativeRunner.hunt > 0:
                IterativeRunner.character_died("ghost-3")
                IterativeRunner.score += 10
                IterativeRunner.mediator.signal_score(IterativeRunner.score)
                ignore3 = True
            else:
                IterativeRunner.character_died("pacman")

        if not ignore1:
            IterativeRunner.environment.ghost1 = ghost1 = (ghost1[0] + direction1[0], ghost1[1] + direction1[1])
            IterativeRunner.environment.set_area(ghost1[0], ghost1[1], "ghost-1")
        
        if not ignore2:
            IterativeRunner.environment.ghost2 = ghost2 = (ghost2[0] + direction2[0], ghost2[1] + direction2[1])
            IterativeRunner.environment.set_area(ghost2[0], ghost2[1], "ghost-2")
        
        if not ignore3:
            IterativeRunner.environment.ghost3 = ghost3 = (ghost3[0] + direction3[0], ghost3[1] + direction3[1])
            IterativeRunner.environment.set_area(ghost3[0], ghost3[1], "ghost-3")

        
        IterativeRunner.tick += 1
        if IterativeRunner.tick % 60 == 0 and not IterativeRunner.fruit_exists:
            while True:
                rand_x = randint(1,19)
                rand_y = randint(1,19)
                if IterativeRunner.environment.get_area(rand_x, rand_y) == None:
                    break
            IterativeRunner.environment.set_area(rand_x, rand_y, "fruit")
            IterativeRunner.fruit_exists = True

        if IterativeRunner.environment.coin_count == 0:
            IterativeRunner.character_died("board")

            

            
