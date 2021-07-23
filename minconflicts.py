import statistics
import sys
import time

import constraints
#import math
import random


class ticket:
    numVariables = 0
    numConstraints = 0
    numColors = 0


global constraintsList
global statesExplored


def manage_file(inputFile):
    fileObject = open(inputFile, "r")
    text = fileObject.read().replace('\t', ' ')
    return constraints.constructConstraints(text, ticket)


# Returns a list of lists, where the sublists are potential variations that ARE NOT violation checked
# Where the variable denotes the index of the color we're changing
def generateChild(currentColorArray, variable, color):
    # Copy the list
    newList = []
    for value in range(ticket.numVariables):
        newList.append(currentColorArray[value])
    newList[variable] = color
    return newList


# Returns True if the current color array violates the passed constraint combination (u,v)
def causesViolation(constraint1, constraint2, currentColorArray):
    if currentColorArray[constraint1] == -1 or currentColorArray[constraint2] == -1:
        return False
    elif currentColorArray[constraint1] == currentColorArray[constraint2]:
        return True
    return False


# Returns true if this color array is the solution, i.e. there are no violations and there are no
# unassigned variables (-1's)
def isSolution(currentColorArray):
    for constraint in constraintsList:
        if causesViolation(constraint[0], constraint[1], currentColorArray):  # if theres a violation, not a sln
            return False
    for color in currentColorArray:
        if color == -1:  # if the color hasnt been assigned yet, its not a solution
            return False
    return True  # if it passes the 2 loops above, its a legit sln


# Returns the total number of violations in a given color array
# Used as a heuristic for minconflicts
def countTotalViolations(currentColorArray):
    temp = 0
    for constraint in constraintsList:
        if causesViolation(constraint[0], constraint[1], currentColorArray):
            temp += 1
    return temp


# Randomly pick a variable that is violating constraints
def randomlyPickVar(currentColorArray):
    tempList = []
    for constraint in constraintsList:
        if causesViolation(constraint[0], constraint[1], currentColorArray):
            tempList.append(constraint[0])
            tempList.append(constraint[1])
    return tempList[random.randrange(0, len(tempList))]


# Randomly choose a color to assign a variable
def findColor(variable, currentColorArray):
    initialViolations = countTotalViolations(currentColorArray)
    tempList = []
    for color in range(ticket.numColors):
        currentColorArray[variable] = color
        k = countTotalViolations(currentColorArray)
        if k <= initialViolations:
            tempList.append(color)
    return tempList[random.randrange(0, len(tempList))]


# This is where the acutal minconflicts algorithm is taking place.
def minConflicts(colorArray):
    global constraintsList
    global statesExplored
    # assign each variable to a random value
    for value in range(ticket.numVariables):
        colorArray[value] = random.randrange(0, ticket.numColors)
    while not isSolution(colorArray):
        statesExplored += 1
        # Pick a variable at random that has a constraint violated
        rv = randomlyPickVar(colorArray)
        # Find a color for this variable that minimizes the total number of violated constraints
        color = findColor(rv, colorArray)
        colorArray[rv] = color
        if statesExplored % 15000 > 10000: #randomly restart
            return True
    return colorArray


def fileOutFormat(solutionArray):
    solution = ""
    for color in solutionArray:
        solution += str(color)
        solution += '\n'
    return solution


if __name__ == '__main__':  # Run the actual file
    startTime = time.time()
    global statesExplored
    statesExplored = 0
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]
    constraintsList = manage_file(inputFile)
    # print(ticket.numVariables)
    currentColorArray = []
    for k in range(ticket.numVariables):
        currentColorArray.append(-1)
    # print(currentColorArray)
    solution = minConflicts(currentColorArray)
    while solution == True and statesExplored < 100000:
        solution = minConflicts(currentColorArray)
    if solution == True:
        solution = False
    f = open(outputFile, "w")
    if solution == False:
        solution = "No answer"
    else:
        solution = fileOutFormat(solution)
    print("States explored %s" % statesExplored)
    f.write(solution)
    endTime = time.time()
    totalTime = str(int(round((endTime * 1000) - (startTime * 1000))))
    print("Time %s ms" % totalTime)
    #     tempList.append(int(totalTime))
    #     tempList2.append(int(statesExplored))
    # print("Mean States Explored: %s +- %s" % (statistics.mean(tempList2), statistics.stdev(tempList2)))
    # print("Mean Time: %s +- %s" % (statistics.mean(tempList), statistics.stdev(tempList)))