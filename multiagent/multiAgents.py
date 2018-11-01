# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
         # P A C M A N  Point of View
        maxValue = float("-inf")
        maxAction = Directions.STOP
        for action in gameState.getLegalActions(0):
            nextState = gameState.generateSuccessor(0, action)

            nextValue = self.minimax(nextState, 0, 1)
            if nextValue > maxValue:
                maxValue = nextValue
                maxAction = action
        return maxAction

    def minimax(self, state, depth, agentIndex):
        if depth == self.depth or state.isWin() or state.isLose() or state.getLegalActions(agentIndex) == 0:
            return self.evaluationFunction(state)
        if agentIndex < 1:
            return self.max_value(state, depth)
        else:
            return self.min_value(state, depth, agentIndex)

    # P A C M A N
    def max_value(self, state, currentDepth):
        v = float("-inf")
        for action in state.getLegalActions(0):
            v = max(v, self.minimax(state.generateSuccessor(0, action), currentDepth, 1))
        return v

    # G H O S T
    def min_value(self, state, currentDepth, agentIndex):
        v = float("inf")

        for action in state.getLegalActions(agentIndex):
            if agentIndex == state.getNumAgents()-1:
                v = min(v, self.minimax(state.generateSuccessor(agentIndex, action), currentDepth + 1, 0))

            else:
                v = min(v, self.minimax(state.generateSuccessor(agentIndex, action),currentDepth,agentIndex + 1))
        return v


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        return self.alpha_beta(gameState)

    def alpha_beta(self, state):
        maxValue = float("-inf")
        alpha = float("-inf")
        beta = float("inf")
        maxAction = Directions.STOP

        # Iterate throguh legal actions down the three
        for action in state.getLegalActions(0):
            nextState = state.generateSuccessor(0, action)
            nextValue = self.getValue(nextState, 0, 1, alpha, beta)
            if nextValue > maxValue:
                maxValue = nextValue
                maxAction = action
            alpha = max(alpha, maxValue)
        return maxAction

    # Help function
    def getValue(self, gameState, currentDepth, agentIndex, alpha, beta):
        if currentDepth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        elif agentIndex == 0:
            return self.max_value(gameState, currentDepth, alpha, beta)
        else:
            return self.min_value(gameState, currentDepth, agentIndex, alpha, beta)

    # P A C M A N
    def max_value(self, gameState, currentDepth, alpha, beta):
        maxVal = float("-inf")
        for action in gameState.getLegalActions(0):
            # find max value for pacman
            maxVal = max(maxVal,
                         self.getValue(gameState.generateSuccessor(0, action), currentDepth, 1, alpha, beta))
            # check for possible pruning
            if maxVal > beta:
                return maxVal
            alpha = max(alpha, maxVal)
        return maxVal

    # G H O S T
    def min_value(self, gameState, currentDepth, agentIndex, alpha, beta):
        minVal = float("inf")
        for action in gameState.getLegalActions(agentIndex):
            if agentIndex == gameState.getNumAgents() - 1:
                minVal = min(minVal,
                             self.getValue(gameState.generateSuccessor(agentIndex, action), currentDepth + 1, 0, alpha, beta))
            else:
                minVal = min(minVal, self.getValue(gameState.generateSuccessor(agentIndex, action), currentDepth, agentIndex + 1, alpha, beta))
            if minVal < alpha:
                return minVal
            beta = min(beta, minVal)
        return minVal