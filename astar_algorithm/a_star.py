from glob import glob
from sys import version_info as version
if version[0] == 3:
    # for Python3
    from tkinter import *   # notice lowercase 't' in tkinter here
else:
    # for Python2
    from Tkinter import *   # notice capitalized T in Tkinter



class Node:
    """
    Node object to obtain the various states and attributes of a node
    """
    def __init__(self, x_pos, y_pos, wall, cost, char):
        self.x = x_pos              # X-position in board
        self.y = y_pos              # Y-position in board
        self.g = float('inf')       # cost of getting to this node
        self.h = None               # estimated cost to goal
        self.is_wall = wall         # if True, then it is a wall
        self.parent = None          # pointer to best parent node
        self.cost = cost            # arc_cost?
        self.children = []          # list of all successor nodes
        self.is_goal = False        # Set to True if the node is the goal
        self.char = char

    def f(self):
        return self.g + self.h      # estimated total cost of a solution path

    def __repr__(self):
        return "[" + str(self.x) + "," + str(self.y) + "]"

    def __str__(self):
        return "[" + str(self.x) + "," + str(self.y) + "]"


class Board:
    """
    Create a Board-object to hold the state of the board
    """
    def __init__(self, nodes, start, goal, board_path):
        self.nodes = nodes
        self.start = start  
        self.goal = goal

        self.open_nodes = [start]
        self.closed_nodes = []

        self.name = board_path.strip(".txt")

    def __str__(self):
        return str(self.name.strip("/boards"))


def make_board(board_path):
    """
    Create a board based on reading lines from a .txt-file
    :param board_path: file.txt
    :return: Board
    """
    costs = {'w':100, 'm': 50, 'f': 10, 'g': 5, 'r': 1, '.': 1}
    nodes = []
    start, goal = None, None
    file = open(board_path, "r")
    lines = [line.strip('\n') for line in file]
    for i in range(len(lines)):
        row = []
        for j in range(len(lines[i])):
            letter = lines[i][j]
            if letter in costs.keys():
                cost = costs[letter]
                node = Node(i, j, False, cost, letter)
                row.append(node)
            elif lines[i][j] == "A":
                start = Node(i, j, False, 1, "A")
                #print("-----\tSTART IS SET-----\n", start)
                row.append(start)
            elif lines[i][j] == "B":
                goal = Node(i, j, False, 1, "B")
                goal.is_goal = True
                #print("-----\tGOAL IS SET-----\n", goal)
                row.append(goal)
            elif lines[i][j] == '#':
                wall_node = Node(i, j, True, float('inf'), "#")
                row.append(wall_node)
        nodes.append(row)
    goal.h = 0
    start.h = abs(goal.x - start.x) + abs(goal.y - start.y)
    start.g = 0
    return Board(nodes, start, goal, board_path), nodes 


def a_star(board):
    """
    Basically pseudocode to python implementation of A* algorithm
    (Humble version: my first time implementing A*)
    :param board: Board
    :return: Null
    """
    while True:
        #if not board.open_nodes:
         #   return False
        cur_node = board.open_nodes.pop(0)      # init node
        board.closed_nodes.append(cur_node)     # place it in CLOSED

        if cur_node.is_goal:
            print("A* success!!")
            return make_path(cur_node, board, board.start, board.goal), board.nodes

        generate_all_successors(cur_node, board.nodes)
        for child in cur_node.children:
            if child not in board.closed_nodes and child not in board.open_nodes:
                attach_and_eval(child, cur_node, board)
                board.open_nodes.append(child)
                board.open_nodes.sort(key=lambda x: x.f())  
            elif cur_node.g + child.cost < child.g:
                attach_and_eval(child, cur_node, board)
                if child in board.closed_nodes:
                    propogate_path_improvements(child)



def make_path(cur_node, board, start, goal):
    """
    Iteratively track down the fastest path
    :param cur_node:
    :param board:
    :param start:
    :param goal:
    :return:
    """
    path = []
    while cur_node != board.start:
        path.append([cur_node.x, cur_node.y])
        if cur_node is not goal and cur_node is not start:
            cur_node.char = "•"
        cur_node = cur_node.parent
    return path



def draw_path_console(map):
    """
    :param map:
    :return:
    """
    final = []
    string = ""
    for line in map:
        row = []
        for node in line:
            row.append(node)
            string += node.char
        final.append(row)
        string += "\n"
    print(string)
    return final


def generate_all_successors(node, possible_nodes):
    """
    :param node:
    :param possible_nodes:
    :return:
    """
    for row in possible_nodes:
        for n in row:
            if (n.x == node.x +1 and n.y == node.y) or\
            (n.x == node.x - 1 and n.y == node.y) or\
            (n.x == node.x and n.y == node.y + 1) or\
            (n.x == node.x and n.y == node.y - 1):
                if not n.is_wall:
                    node.children.append(n)
    

def attach_and_eval(child, parent, board):
    """
    :param child:
    :param parent:
    :param board:
    :return:
    """
    child.parent = parent
    child.g = parent.g + child.cost
    child.h = abs(board.goal.x - child.x) + abs(board.goal.y - child.y)


def propogate_path_improvements(node):
    """
    :param node:
    :return:
    """
    for child in node.children:
        if node.g + child.cost < child.g:
            child.parent = node
            child.g = node.g + child.cost
            propogate_path_improvements(child)


def draw_task_1(map, grid):
    """
    Using tkinter to visually plot the maze
    :param map:
    :param grid:
    :return:
    """
    master = Tk()
    w = Canvas(master, width=600, height=210)
    w.pack()

    # Creating the grid
    for i in range(0, 601, 30):
        w.create_line(i, 0, i, 210, fill="black")
    for i in range(0, 211, 30):
        w.create_line(0, i, 600, i, fill="black")

    # Drawing the initial canvas, then running the algorithm, and filling it in
    for j in range(len(map)):
        for i in range(len(map[0])):
            if map[j][i].char == "#":
                w.create_rectangle(i * 30, j * 30, (i + 1) * 30, (j + 1) * 30, fill="grey")
            elif map[j][i].char == ".":
                w.create_rectangle(i * 30, j * 30, (i + 1) * 30, (j + 1) * 30, fill="white")
            elif map[j][i].char == "A":
                w.create_rectangle(i * 30, j * 30, (i + 1) * 30, (j + 1) * 30, fill="red")
                w.create_text(i * 30 + 15, j * 30 + 15, font="Times 20", text="A")
            elif map[j][i].char == "B":
                w.create_rectangle(i * 30, j * 30, (i + 1) * 30, (j + 1) * 30, fill="light green")
                w.create_text(i * 30 + 15, j * 30 + 15, font="Times 20", text="B")
    for j in range(len(grid)):
            for i in range(len(grid[0])):
                if grid[j][i].char == "•":
                    w.create_rectangle(i * 30, j * 30, (i + 1) * 30, (j + 1) * 30, fill="black")
                    w.create_text(i * 30 + 15, j * 30 + 15, font="Times 20", text="•", fill="white")
                elif grid[j][i].char == "x":
                    w.create_text(i * 30 + 15, j * 30 + 15, font="Times 20", text="x")
                elif grid[j][i].char == "*":
                    w.create_text(i * 30 + 15, j * 30 + 15, font="Times 20", text="*")
    mainloop()


def draw_task_2(map, grid):
    """
    Using tkinter to visually plot the maze
    :param map:
    :param grid:
    :return:
    """
    master = Tk()
    w = Canvas(master, width=800, height=200)
    w.pack()

    # Creating the grid
    for i in range(0, 801, 20):
        w.create_line(i, 0, i, 200, fill="black")
    for i in range(0, 201, 20):
        w.create_line(0, i, 800, i, fill="black")
    # Drawing the initial canvas, then running the algorithm, and filling it in
    for j in range(len(map)):
        for i in range(len(map[0])):
            if map[j][i].char == "w":
                w.create_rectangle(i * 20, j * 20, (i + 1) * 20, (j + 1) * 20, fill="blue")
            elif map[j][i].char == "r":
                w.create_rectangle(i * 20, j * 20, (i + 1) * 20, (j + 1) * 20, fill="chocolate")
            elif map[j][i].char == "f":
                w.create_rectangle(i * 20, j * 20, (i + 1) * 20, (j + 1) * 20, fill="dark green")
            elif map[j][i].char == "g":
                w.create_rectangle(i * 20, j * 20, (i + 1) * 20, (j + 1) * 20, fill="light green")
            elif map[j][i].char == "m":
                w.create_rectangle(i * 20, j * 20, (i + 1) * 20, (j + 1) * 20, fill="grey")
            elif map[j][i].char == "A":
                w.create_rectangle(i * 20, j * 20, (i + 1) * 20, (j + 1) * 20, fill="red")
                w.create_text(i * 20+ 10, j * 20 + 10, font="Times 20", text="A")
            elif map[j][i].char == "B":
                w.create_rectangle(i * 20, j * 20, (i + 1) * 20, (j + 1) * 20, fill="yellow")
                w.create_text(i * 20 + 10, j * 20 + 10, font="Times 20", text="B")
    for j in range(len(grid)):
            for i in range(len(grid[0])):
                if grid[j][i].char == "•":
                    w.create_rectangle(i * 20, j * 20, (i + 1) * 20, (j + 1) * 20, fill="black")
                    w.create_text(i * 20 + 10, j * 20 + 10, font="Times 20", text="•", fill="white")
                elif grid[j][i].char == "x":
                    w.create_text(i * 20 + 10, j * 20 + 10, font="Times 20", text="x")
                    w.create_text(i * 20 + 10, j * 20 + 10, font="Times 20", text="*")
    mainloop()


def main():
    files1 = glob(r'./boards/boards1/*.txt')
    for file in files1:
        board, nodes = make_board(file)
        path, map = a_star(board)
        final = draw_path_console(map)
        draw_task_1(map, final)

    files2 = glob(r'./boards/boards2/*.txt')
    for file in files2:
        board, nodes = make_board(file)
        path, map = a_star(board)
        final = draw_path_console(map)
        draw_task_2(map, final)

main()