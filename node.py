"""
Arunima Mittra
AXM170025
CS 6364: Artificial Intelligence 
Homework 1

"""

from copy import deepcopy
from numpy import empty
import math

"""
    This class contains functions and variables that store data for each node in the search tree.
"""


class Node:
    """Initialize node instance with:
      - 1-D array of int start sequence
      - pointer to parent node (or None)
            - current depth is parent depth + 1
      - the sequence of moves to reach this state (letters, D - fown, U - up, etc)
      Additional data for astar:
      - goal_state: each node contains the array for the goal state
      - heur: 0 or 1 for manhattan vs. misplaced tiles
    """

    def __init__(self, puzzle, parent=None, move=""):
        self.state = puzzle
        self.zero = puzzle.index(0)
        self.parent = parent
        self.depth = 0
        self.goal_state = []
        self.heur = 0
        if parent is None:
            self.depth = 0
            self.moves = move
        else:
            if (isinstance(parent, Node)):
                self.depth = parent.depth + 1
                self.moves = parent.moves + move

        """
        Functions to calculate the 1-D array for the next possible moves from the current node.
        Right/Left by using % 3
        Up/Down by using / 3
        """

    def right(self):
        if self.zero % 3 == 0 or self.zero % 3 == 1:
            new = deepcopy(self.state)
            temp = new[self.zero + 1]
            new[self.zero] = temp
            new[self.zero + 1] = 0
            node = Node(new, self, "R")
            node.heur = self.heur
            if self.goal_state is not empty:
                node.goal_state = self.goal_state
            return node

    def left(self):
        if self.zero % 3 == 1 or self.zero % 3 == 2:
            new = deepcopy(self.state)
            temp = new[self.zero - 1]
            new[self.zero] = temp
            new[self.zero - 1] = 0
            node = Node(new, self, "L")
            node.heur = self.heur
            if self.goal_state is not empty:
                node.goal_state = self.goal_state
            return node

    def down(self):
        if self.zero < 6:
            new = deepcopy(self.state)
            temp = new[self.zero + 3]
            new[self.zero] = temp
            new[self.zero + 3] = 0
            node = Node(new, self, "D")
            node.heur = self.heur
            if self.goal_state is not empty:
                node.goal_state = self.goal_state
            return node

    def up(self):
        if self.zero > 2:
            new = deepcopy(self.state)
            temp = new[self.zero - 3]
            new[self.zero] = temp
            new[self.zero - 3] = 0
            node = Node(new, self, "U")
            node.heur = self.heur
            if self.goal_state is not empty:
                node.goal_state = self.goal_state
            return node

    """Checks whether the current node is the goal
    """

    def isGoalState(self, goal=None):
        if goal:
            self.goal_state = goal
        return self.state == self.goal_state

    """Returns a list of valid moves from the current node
    """

    def validMoves(self):
        valid = []
        valid.append(self.right())
        valid.append(self.up())
        valid.append(self.left())
        valid.append(self.down())
        return valid

    def nextMoves(self):
        order = []
        children = self.validMoves()
        if children is empty:
            return None

        for c in children:
            if(isinstance(c, Node)):
                if c.zero != self.zero:
                    order.append(c)
        return order

    """Converts array to output string matrix
    """

    def __str__(self) -> str:
        ret = "\n"
        for index, num in enumerate(self.state):
            val = str(num)
            if num == 0:
                val = "*"
            if (index + 1) % 3 != 0:
                ret = ret + " " + val
            else:
                ret = ret + " " + val + "\n"
        return ret

    """Calculates manhattan dist by finding (x,y) for both nodes and using the 
        distance formula

        Returns a number
    """

    def manhattan_dist(self, goal=None):
        if goal:
            self.goal_state = goal.state
        result = 0
        for s_pos in range(9):
            curr = self.state[s_pos]
            g_pos = self.goal_state.index(curr)
            result += math.pow(abs((s_pos % 3) - (g_pos % 3)), 2) + \
                math.pow(abs((s_pos/3) - (g_pos / 3)), 2)
        return result

    """Compares current node to goal and counts the number of indices that are not matching
        """

    def misplaced_tiles(self, goal=None):
        if goal:
            self.goal_state = goal.state
        count = 0
        for i, val in enumerate(self.state):
            if self.goal_state[i] != val:
                count += 1
        return count

    """Comparator functions to be used while building the min-heap for astar
    """

    def __lt__(self, other):
        if isinstance(other, Node):
            if self.heur == 0:
                return self.manhattan_dist() < other.manhattan_dist()
        return self.misplaced_tiles() < other.misplaced_tiles()

    def __gt__(self, other):
        if isinstance(other, Node):
            if self.heur == 0:
                return self.manhattan_dist() > other.manhattan_dist()
            return self.misplaced_tiles() > other.misplaced_tiles()

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.state == other.state or self.manhattan_dist() == other.manhattan_dist() or other.misplaced_tiles() == self.misplaced_tiles()
