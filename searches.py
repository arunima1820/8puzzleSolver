"""
Arunima Mittra
AXM170025
CS 6364: Artificial Intelligence 
Homework 1

"""

import node
import math
import heapq

"""Iteratively calls dfs() with an increasing max_depth limit
"""


def ids(start_node, goal_state):
    for i in range(14):
        val = dfs(start_node, goal_state, (i+1))
        if val:
            return val
    return None


"""Runs a Depth-First Search for the goal. Does not always have the best results.
    Also used in IDS.

    Algo:
    - Generate list of next nodes to go to, add them to stack
    - Go through each depth-sequence till goal or depth = 15
    - backtrack to last un-explored depth and search again
"""


def dfs(start_node, goal_state, max_depth=15):
    leaves = []
    leaves.append(start_node)
    visited = []
    depth = 0
    count_moves = 0
    output = ""
    while True:
        if not leaves:
            return None
        current = leaves.pop()
        count_moves = count_moves + 1
        if(isinstance(current, node.Node)):
            if current.isGoalState(goal_state.state):
                prnt_node = current
                while prnt_node.parent:
                    output = str(prnt_node) + output
                    prnt_node = prnt_node.parent
                print(output)
                print("Found at Depth:", depth)
                return current, count_moves
            elif current.state in visited:
                continue
            elif current.state not in visited:
                depth = current.depth
                visited.append(current.state)
                if depth < max_depth:
                    children = current.nextMoves()
                else:
                    if current.parent:
                        children = current.parent.nextMoves()
                while children:
                    leaves.append(children.pop())


"""Runs either manhattan or misplaced tiles heuristic.
    Using min-heap to store the sorted states by their distance to goal.
    Pop the min-val from heap and process:
        - generate children, calculate their distance
        - add them to min-heap

"""


def astar(start_node, goal_node, heur):
    leaves = []
    visited = []
    start_node.goal_state = goal_node.state
    start_node.heur = heur
    depth = 0
    count_moves = 0
    output = ""
    heapq.heapify(leaves)
    heapq.heappush(leaves, start_node)
    while True:
        current = heapq.heappop(leaves)
        count_moves = count_moves + 1
        depth = current.depth
        if current.isGoalState():
            prnt_node = current
            while prnt_node.parent:
                output = str(prnt_node) + output
                prnt_node = prnt_node.parent
            print(output)
            print("Found at Depth:", depth)
            return current, count_moves
        elif current.state not in visited and depth < 15:
            visited.append(current.state)
            next_nodes = current.nextMoves()
            next_nodes = [x for x in next_nodes if x.state not in visited]
            if next_nodes:
                [heapq.heappush(leaves, x) for x in next_nodes]
