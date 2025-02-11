# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    # create a Stack to keep track of nodes we are going to explore
    fringe = util.Stack()

    # we will push in tuples (coordinates, pass) in the stack
    fringe.push((problem.getStartState(), [], 0))

    node, actions, allcost = fringe.pop()

    visited_nodes = [node] #to keep track or explored nodes

    while (not problem.isGoalState(node)):

        successors = problem.getSuccessors(node)
        for next_node, action, cost in successors:

            if (not next_node in visited_nodes):
                fringe.push((next_node, actions + [action], allcost + cost))
                visited_nodes.append(next_node)

        # all actions
        node, actions, allcost = fringe.pop()

    return actions

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # create a Queue to keep track of nodes we are going to explore
    fringe = util.Queue()

    # we will push in tuples (coordinates, pass) in the stack
    fringe.push((problem.getStartState(), [], 0))

    node, actions, allcost = fringe.pop()

    visited_nodes = [node]  # to keep track or explored nodes

    while (not problem.isGoalState(node)):

        successors = problem.getSuccessors(node)
        for next_node, action, cost in successors:

            if (not next_node in visited_nodes):
                fringe.push((next_node, actions + [action], allcost + cost))
                visited_nodes.append(next_node)

        # all actions
        node, actions, allcost = fringe.pop()

    return actions


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # create a Queue to keep track of nodes we are going to explore
    fringe = util.PriorityQueue()

    # we will push in tuples (coordinates, pass) in the stack
    fringe.push((problem.getStartState(), [], 0), 0)

    node, actions, allcost = fringe.pop()
    visited_nodes = [
        (node, 0)]  # with cost why do I have to do that? => would be better to add them when state is unpacked
    # print "pop ",allcost
    while (not problem.isGoalState(node)):

        successors = problem.getSuccessors(node)
        for next_nodes, action, cost in successors:
            #
            already_seen = False
            total_cost = problem.getCostOfActions(actions + [action])
            for i in range(len(visited_nodes)):
                state_tmp, cost_tmp = visited_nodes[i]
                if (next_nodes == state_tmp) and (total_cost >= cost_tmp):
                    already_seen = True
            if (not already_seen):
                fringe.push((next_nodes, actions + [action], total_cost), total_cost)
                visited_nodes.append((next_nodes, total_cost))
                # calculate "create cost ",total_cost+cost
        # print "All actions: ",allactions
        node, actions, allcost = fringe.pop()

    return actions


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    # util.raiseNotDefined()
    # print "Enter aStarSearch..."

    # create a Queue to keep track of nodes we are going to explore
    fringe = util.PriorityQueue()

    # we will push in tuples (coordinates, pass) in the stack
    fringe.push((problem.getStartState(), [], 0), 0)

    node, actions, allcost = fringe.pop()
    visited_nodes = [
        (node, 0)]  # with cost why do I have to do that? => would be better to add them when state is unpacked
    while (not problem.isGoalState(node)):

        successors = problem.getSuccessors(node)

        for next_nodes, action, cost in successors:
            already_seen = False
            total_cost = problem.getCostOfActions(actions + [action])
            for i in range(len(visited_nodes)):
                state_tmp, cost_tmp = visited_nodes[i]
                if (next_nodes == state_tmp) and (total_cost >= cost_tmp):
                    already_seen = True
            if (not already_seen):
                total_cost = problem.getCostOfActions(actions + [action])
                fringe.push((next_nodes, actions + [action], total_cost),
                            total_cost + heuristic(next_nodes, problem))
                visited_nodes.append((next_nodes, total_cost))
                # calculate "create cost ",total_cost+cost
        node, actions, allcost = fringe.pop()

    return actions




# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
