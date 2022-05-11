
class GhostFactory:
    def create_ghost1():
        return "ghost-1"
    def create_ghost2():
        return "ghost-2"
    def create_ghost3():
        return "ghost-3"


class Table:

    template = None

    def __init__(self):
        self.table = []
        self.transparent_table = []
        self.pacman = None
        self.ghost1 = None
        self.ghost2 = None
        self.ghost3 = None
        self.coin_count = 0

    def set_area(self, x, y, o):
        if o == "fruit" or o == "coin":
            if o == "coin":
                self.coin_count += 1
            self.transparent_table[y][x*2] = o
        else:
            self.table[y][x*2] = o
            if o == "wall" or o == None:
                self.table[y][x*2+1] = o
        
    def remove_transparent(self, x, y):
        self.transparent_table[y][x*2] = None

    def get_area(self, x, y):
        o = self.table[y][x*2]
        if o is None:
            o = self.transparent_table[y][x*2]
        return o

    def deep_clone(self):
        t = Table()
        for row in self.table:
            new_row = []
            for column in row:
                new_row.append(column)
            t.table.append(new_row)
        for row in self.transparent_table:
            new_row = []
            for column in row:
                new_row.append(column)
            t.transparent_table.append(new_row)
        t.pacman = self.pacman
        t.ghost1 = self.ghost1
        t.ghost2 = self.ghost2
        t.ghost3 = self.ghost3
        t.coin_count = self.coin_count
        return t

    def get_instance():
        return Table.template.deep_clone()

    

Table.template = Table()

# dimensions
height = 21
width = 42

for _ in range(height):
    Table.template.table.append([None for _ in range(width)])
    Table.template.transparent_table.append([None for _ in range(width)])

# outer walls
for i in range(height):
    Table.template.table[i][0] = "wall"
    Table.template.table[i][width - 1] = "wall"
    Table.template.table[i][1] = "wall"
    Table.template.table[i][width - 2] = "wall"
for i in range(width):
    Table.template.table[0][i] = "wall"
    Table.template.table[height - 1][i] = "wall"

# pacman start
Table.template.set_area(10,12,"pacman-whole")
Table.template.pacman = (10,12)

# ghost start

Table.template.set_area(9,10,GhostFactory.create_ghost1())
Table.template.ghost1 = (9,10)
Table.template.set_area(10,10,GhostFactory.create_ghost2())
Table.template.ghost2 = (10,10)
Table.template.set_area(11,10,GhostFactory.create_ghost3())
Table.template.ghost3 = (11,10)

# inner walls

for i in [1,19]:
    for j in [8,9,10,11,12]:
        Table.template.set_area(i,j,"wall")
for i in [2,4,16,18]:
    for j in [2,3,4,5,6,8,9,10,11,12,14,15,16,17,18]:
        Table.template.set_area(i,j,"wall")
for i in [3,17]:
    for j in [8,9,10,11,12,14,15,16,17,18]:
        Table.template.set_area(i,j,"wall")
for i in [6,14]:
    for j in [2,3,4,5,7,8,9,11,12,13,15,16,17,18]:
        Table.template.set_area(i,j,"wall")
for i in [7,13]:
    for j in [2,3,4,5,7]:
        Table.template.set_area(i,j,"wall")
for i in [8,12]:
    for j in [7,9,10,11,13,15,17,19]:
        Table.template.set_area(i,j,"wall")
for i in [9,11]:
    for j in [2,3,4,5,7,9,11,13,15,17,19]:
        Table.template.set_area(i,j,"wall")
for i in [10]:
    for j in [11,15,19]:
        Table.template.set_area(i,j,"wall")

# coins

for i in [1,19]:
    for j in [1,2,3,4,5,6,7,13,14,15,16,17,18,19]:
        Table.template.set_area(i,j,"coin")
for i in [2,4,16,18]:
    for j in [1,7,13,19]:
        Table.template.set_area(i,j,"coin")
for i in [3,17]:
    for j in [1,2,3,4,5,6,7,13,19]:
        Table.template.set_area(i,j,"coin")
for i in [5,15]:
    for j in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]:
        Table.template.set_area(i,j,"coin")
for i in [6,14]:
    for j in [1,6,10,14,19]:
        Table.template.set_area(i,j,"coin")
for i in [7,13]:
    for j in [1,6,13,14,15,16,17,18,19]:
        Table.template.set_area(i,j,"coin")
for i in [8,12]:
    for j in [1,2,3,4,5,6,14,16,18]:
        Table.template.set_area(i,j,"coin")
for i in [9,11]:
    for j in [1,6,14,16,18]:
        Table.template.set_area(i,j,"coin")
for i in [10]:
    for j in [1,2,3,4,5,6,7,13,14,16,17,18]:
        Table.template.set_area(i,j,"coin")





