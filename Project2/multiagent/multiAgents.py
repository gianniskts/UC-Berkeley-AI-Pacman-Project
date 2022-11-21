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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
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
        newGhostStates = successorGameState.getGhostStates()

        "*** YOUR CODE HERE ***"
        score = 0
        distance = 0
        oldFood = currentGameState.getFood().asList()   # food with current state
        newFood = successorGameState.getFood().asList() # food with next state
        ateFood = False # flag 

        if action == 'Stop':
            return -99999999

        if len(newFood) < len(oldFood):   # if pacman ate a food by doing this move
            ateFood = True
        
        if ateFood:
            score += 200
        
        for food in newFood:
            distance = manhattanDistance(newPos, food)
            score += 100/distance

        for ghost in newGhostStates:
            ghostPos = ghost.getPosition()
           
            if newPos == ghostPos and ghost.scaredTimer == 0:
                return -999999999

            elif newPos == ghostPos and ghost.scaredTimer != 0:
                score += 100

        return score


def scoreEvaluationFunction(currentGameState: GameState):
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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def maxValue(state, pacmanID, depth):
            legalActions = state.getLegalActions(pacmanID)
            value = -9999999999
            bestAction = None

            for action in legalActions:
                succState = state.generateSuccessor(pacmanID, action)
                tempValue, NULLaction = minimax(succState, pacmanID+1, depth)
                
                if tempValue > value:
                    value = tempValue
                    bestAction = action
            
            return (value, bestAction)


        def minValue(state, pacmanID, depth):
            legalActions = state.getLegalActions(pacmanID)
            value = 9999999999
            bestAction = None

            for action in legalActions:
                succState = state.generateSuccessor(pacmanID, action)
                tempValue, NULLaction = minimax(succState, pacmanID+1, depth)
                
                if tempValue < value:
                    value = tempValue
                    bestAction = action
            
            return (value, bestAction)

        def minimax(gameState, agentID, depth):
            if agentID >= gameState.getNumAgents():
                depth += 1
                agentID = 0

            if gameState.isWin() or gameState.isLose() or (depth == self.depth):
                return (self.evaluationFunction(gameState), None)
            if agentID == 0:
                return maxValue(gameState, agentID, depth)
            else:
                return minValue(gameState, agentID, depth)
        
        return minimax(gameState, 0, 0)[1]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maxValue(gameState, pacmanID, depth, a, b):
            maxValue = -9999999999
            bestAction = None
            legalActions = gameState.getLegalActions(pacmanID)

            for action in legalActions:
                succState = gameState.generateSuccessor(pacmanID, action)
                tempValue, NULLaction = minimax(succState, pacmanID+1, depth, a, b)
                
                maxValue = max(tempValue, maxValue)
                if maxValue == tempValue:
                    bestAction = action

                a = max(a, maxValue)

                if a > b:
                    return (maxValue, bestAction)
            
            return (maxValue, bestAction)

        def minValue(gameState, pacmanID, depth, a, b):
            minValue = 9999999999
            bestAction = None
            legalActions = gameState.getLegalActions(pacmanID)

            for action in legalActions:
                succState = gameState.generateSuccessor(pacmanID, action)
                tempValue, NULLaction = minimax(succState, pacmanID+1, depth, a, b)
                
                minValue = min(tempValue, minValue)
                if minValue == tempValue:
                    bestAction = action

                b = min(b, minValue)

                if b < a:
                    return (minValue, bestAction)
            
            return (minValue, bestAction)

        def minimax(gameState, agentID, depth, a, b):
            if agentID >= gameState.getNumAgents():
                depth += 1
                agentID = 0

            if gameState.isWin() or gameState.isLose() or (depth == self.depth):
                return (self.evaluationFunction(gameState), None)
            if agentID == 0:
                return maxValue(gameState, agentID, depth, a, b)
            else:
                return minValue(gameState, agentID, depth, a, b)
        
        return minimax(gameState, 0, 0, -999999, 999999)[1]


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def maxValue(gameState, pacmanID, depth):
            maxValue = -9999999999
            bestAction = None
            legalActions = gameState.getLegalActions(pacmanID)

            for action in legalActions:
                succState = gameState.generateSuccessor(pacmanID, action)
                tempValue, NULLaction = expectimax(succState, pacmanID+1, depth)
                
                maxValue = max(tempValue, maxValue)
                if maxValue == tempValue:
                    bestAction = action

            
            return (maxValue, bestAction)

        def chanceValue(gameState, pacmanID, depth):
            average = 0
            bestAction = None
            legalActions = gameState.getLegalActions(pacmanID)
            probability = 1.0/len(legalActions)
            
            for action in legalActions:
                succState = gameState.generateSuccessor(pacmanID, action)
                tempScore, NULLaction = expectimax(succState, pacmanID+1, depth)

                average += tempScore*probability

            return (average, None)


        def expectimax(gameState, agentID, depth):
            if agentID >= gameState.getNumAgents():
                depth += 1
                agentID = 0

            if gameState.isWin() or gameState.isLose() or (depth == self.depth):
                return (self.evaluationFunction(gameState), None)
            if agentID == 0:
                return maxValue(gameState, agentID, depth)
            else:
                return chanceValue(gameState, agentID, depth)
        
        return expectimax(gameState, 0, 0)[1]

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    foodList = currentGameState.getFood().asList()
    newPos = currentGameState.getPacmanPosition()

    foodDistances     = []
    ghostDistances    = []
    captuleDistances  = []
    minFoodDist    = 9999999
    minGhostDist   = 9999999
    minCaptuleDist = 9999999

    captules = currentGameState.getCapsules()
    captulesCount = len(currentGameState.getCapsules())
    foodCount = len(foodList)
    ghosts = currentGameState.getGhostPositions()

    if currentGameState.isWin():    return 9999999
    elif currentGameState.isLose():    return -9999999
    else:
        for food in foodList:
            minFoodDist = min(manhattanDistance(food, newPos), minFoodDist)    

        for captule in captules:
            minCaptuleDist = min(manhattanDistance(captule, newPos), minCaptuleDist)    

        for ghost in ghosts:
            minGhostDist = min(manhattanDistance(ghost, newPos), minGhostDist)
            
        if minGhostDist == 0:
            return -9999999

        score = currentGameState.getScore()
        
        evaluation = 0.01 * score + 0.0001 * minGhostDist + 1/minFoodDist*10 + 1/(minCaptuleDist+0.1)*1000 + 1/(foodCount+0.1)*9999 + 1/(captulesCount+0.1)*5000
        
        return evaluation

# Abbreviation
better = betterEvaluationFunction
