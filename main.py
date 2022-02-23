"""
Arunima Mittra
AXM170025
CS 6364: Artificial Intelligence 
Homework 1

"""

import node
import sys
import searches as s

"""Driver program for the 8-puzzle search.
    Can process multiple line-delimited start states from input file
"""


def main():
    search = sys.argv[1]
    with open(str(sys.argv[2])) as file:
        inputs = file.readlines()
    inputs = [line.strip() for line in inputs]
    inputs = [(t.replace("*", str(0))).split(" ") for t in inputs]
    goal = node.Node(list([1, 2, 3, 8, 0, 4, 7, 6, 5]))

    for inp in inputs:
        start = node.Node(list(map(int, inp)))
        try:
            if search == "ids":
                output, total = s.ids(start, goal)
            elif search == "dfs":
                output, total = s.dfs(start, goal)
            elif search == "astar1":
                output, total = s.astar(start, goal, 0)
            elif search == "astar2":
                output, total = s.astar(start, goal, 1)
            else:
                print(
                    "Error. Please enter one search function: ids, dfs, astar1, astar2")
        except:
            print("Solution not found within depth 15 or there was an error.")
        else:
            print("Steps to reach goal:", output.moves)
            print("Total moves:", total)
    return


if __name__ == "__main__":
    main()
