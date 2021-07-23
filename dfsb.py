import time

import constraints
import sys
#import statistics

class ticket:
    numVariables = 0
    numConstraints = 0
    numColors = 0


global constraintsList  # Array of tuples containing constraints
global badAC3
global statesExplored


# Returns an array of tuple constraints
# Also sets the global variables, numVaraibles, numConstraints, and numColors
def manage_file(inputFile):
    fileObject = open(inputFile, "r")
    text = fileObject.read().replace('\t', ' ')
    return constraints.constructConstraints(text, ticket)


def causesViolation(constraint1, constraint2, currentColorArray):
    if currentColorArray[constraint1] == -1 or currentColorArray[constraint2] == -1:
        return False
    elif currentColorArray[constraint1] == currentColorArray[constraint2]:
        return True
    return False


def generateChild(currentColorArray, variable, color):
    # Copy the list
    newList = []
    for value in range(ticket.numVariables):
        newList.append(currentColorArray[value])
    newList[variable] = color
    return newList


# Returns a list of lists, where the sublists are potential variations that ARE NOT violation checked
# Where the variable denotes the index of the color we're changing
def generateChildren(currentColorArray, variable):
    tempList = []
    for color in range(ticket.numColors):
        tempList.append(generateChild(currentColorArray, variable, color))
    return tempList # return a list of lists


def isSolution(currentColorArray):
    for constraint in constraintsList:
        if causesViolation(constraint[0], constraint[1], currentColorArray):  # if theres a violation, not a sln
            return False
    for color in currentColorArray:
        if color == -1:  # if the color hasnt been assigned yet, its not a solution
            return False
    return True  # if it passes the 2 loops above, its a legit sln


def DFSB(currentColorArray):
    global statesExplored
    statesExplored += 1
    if isSolution(currentColorArray):
        return currentColorArray
    for constraint in constraintsList:
        if causesViolation(constraint[0], constraint[1], currentColorArray):  # if theres a violation, break out
            return False

    for x in range(len(currentColorArray)):
        color = currentColorArray[x]
        if color == -1:
            potentialColors = generateChildren(currentColorArray, x)
            for childColorArray in potentialColors:
                solution = DFSB(childColorArray)  # Solution is what we get from calling DFSB
                if solution != False:  # If its not false, its a solution we have
                    return solution
    return False


# DFSB++ starts here
# Returns a list of lists where the length = numVariables
# and the sublists contain the colors each variable can take
def generateAC3():
    AC3 = []
    # generate the potential colors list
    potentialColors = []
    for y in range(ticket.numColors):
        potentialColors.append(y)
    for z in range(ticket.numVariables):
        AC3.append(potentialColors)
    return AC3


# Returns a list such that the indices represent variables and
# the values of each index represent the number of edges
# connected to that variable
def generateEdgePointers():
    global constraintsList
    pointerList = []
    for x in range(ticket.numVariables):
        pointerList.append(0)
    for constraint in constraintsList:
        pointerList[constraint[0]] += 1
        pointerList[constraint[1]] += 1
    return pointerList


# returns the new AC3 such that the adjacent nodes to the variable
# cannot have the same color, hence they're removed
def removeColorsFromAC3(AC3, variable, color):
    # clone the AC3 because we're gonna need to keep the original in case this
    # route doesnt go well
    global constraintsList
    global badAC3
    newAC3 = []
    for y in range(ticket.numVariables):
        sublist = AC3[y]
        tempList = []
        for value in sublist:
            tempList.append(value)
        newAC3.append(tempList)
    for constraint in constraintsList:
        if constraint[0] == variable: # remove the color from the other variable
            if color in newAC3[constraint[1]]:
                newAC3[constraint[1]].remove(color)
                if len(newAC3[constraint[1]]) == 0:
                    return False
        elif constraint[1] == variable: # remove the color from the other variable
            if color in newAC3[constraint[0]]:
                newAC3[constraint[0]].remove(color)
                if len(newAC3[constraint[0]]) == 0:
                    return False
    return newAC3


# Returns the total # of colors of this AC3
# Use this to sort the color we choose later
def countTotalColors(AC3):
    temp = 0
    for y in range(ticket.numVariables):
        temp += len(AC3[y])
    return temp


def sortSecond(val):
    return countTotalColors(val[1])


# Sort by the total colors each child would have
# Gonna be in pairs of (color array, new AC3)
def generateSortedChildren(variable, AC3, currentColorArray):
    global statesExplored
    statesExplored += 1
    tempList = []
    canAppend = True
    global badAC3
    print("AC3 at variable %s has potential colors %s" % (variable, AC3[variable]))
    for color in range(ticket.numColors): #AC3[variable]
        child = generateChild(currentColorArray, variable, color)
        newAC3 = removeColorsFromAC3(AC3, variable, color)
        if type(newAC3) == bool:
            canAppend = False
        if canAppend:
            tempList.append((child, newAC3, countTotalColors(newAC3)))
        canAppend = True
    tempList.sort(key=sortSecond, reverse=True)
    temp = " "
    for value in tempList:
        temp += str(value[2]) + " "
    print(temp)
    return tempList


# If any of the items in the AC3 are empty,
# it means we broke a constraint
def brokeAC3(AC3):
    for item in AC3:
        #print(len(item))
        if len(item) == 0:
            return True
    return False


def findMostConstrainedV(AC3, currentColorArray):
    maxLength = 100
    maxIndex = -1
    for y in range(ticket.numVariables):
        if len(AC3[y]) <= maxLength and currentColorArray[y] == -1:
            maxLength = len(AC3[y])
            maxIndex = y
    return maxIndex


def listMostConstrained(AC3, currentColorArray, pointerList):
    copiedList = []
    for x in range(ticket.numVariables):
        copiedList.append(currentColorArray[x])
    tempList = []
    variable = findMostConstrainedV(AC3, copiedList)
    while variable != -1:
        copiedList[variable] = 0
        tempList.append(variable)
        variable = findMostConstrainedV(AC3, copiedList)
    for x in range(len(tempList) - 1):
        if pointerList[tempList[x]] < pointerList[tempList[x+1]] and len(AC3[tempList[x]]) == len(AC3[tempList[x + 1]]) :
            tempList[x], tempList[x+1] = tempList[x+1], tempList[x-1]
    return tempList


# Look at code to see matching definitions
# #1- Check for violations, if there is return false
# #2- if theres no violations, lightly check for a solution (no unassigned variables, i.e. no -1)
# #3- Generate a list of the most constrained variables by looking at the unassigned variables with the least
#     Possible colors and breaking ties from there
# #4- Generate children sorted by least constraining value
#     A tuple is returned in the order (newColorArray- used to test solutions, newAC3- used to check
#     constraint violation in combination w/ the constraintList, happens when we remove from the AC3)
def DFSBPlus(currentColorArray, pointerList, AC3, depth):
    print("Depth: %s" % depth)
    for constraint in constraintsList: # #1
        if causesViolation(constraint[0], constraint[1], currentColorArray):
            print("Constraint violation")
            return False
    if -1 not in currentColorArray: # #2
        return currentColorArray
    mostConstrainedList = listMostConstrained(AC3, currentColorArray, pointerList) # #3
    for variable in mostConstrainedList:
        #print("Most constrained variable %s" % variable)
        sortedChildren = generateSortedChildren(variable, AC3, currentColorArray)# #4
        for child in sortedChildren:
            newColorArray = child[0]
            #print("New color array %s" % newColorArray)
            newAC3 = child[1]
            #print("New AC3 %s" % newAC3)
            solution = DFSBPlus(newColorArray, pointerList, newAC3, depth + 1)
            print("Solution %s" % solution)
            if solution != False:
                return solution
    return False





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
    mode = int(sys.argv[3])  # 0 for plain DFSB, 1 for DFSB++
    constraintsList = manage_file(inputFile)
    #print(ticket.numVariables)
    currentColorArray = []
    for k in range(ticket.numVariables):
        currentColorArray.append(-1)
    #print(currentColorArray)
    solution = False
    if mode == 0:
        solution = DFSB(currentColorArray)
    elif mode == 1:
        global badAC3
        badAC3 = False
        AC3 = generateAC3()
        pointerList = generateEdgePointers()
        #print(pointerList)
        solution = DFSBPlus(currentColorArray, pointerList, AC3, 0)
    f = open(outputFile, "w")
    if solution == False:
        solution = "No answer"
    else:
        solution = fileOutFormat(solution)
    f.write(solution)
    endTime = time.time()
    totalTime = str(int(round((endTime * 1000) - (startTime * 1000))))
    print("Time %s ms" % totalTime)
    # print("Mean States Explored: %s +- %s" % (statistics.mean(tempList2), statistics.stdev(tempList2)))
    # print("Mean Time: %s +- %s" % (statistics.mean(tempList), statistics.stdev(tempList)))
    #print("Mean: %s" % statistics.mean(tempList))
