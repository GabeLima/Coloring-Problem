#import dfsb


# Take the input file as a string, assume the first line is still N M K
# Return an array of tuples
def constructConstraints(inputFile:str, ticket):
    inputFileArray = inputFile.split('\n')
    constraintTuples = []
    fileHeader = inputFileArray[0].split(' ')
    ticket.numVariables = int(fileHeader[0])
    ticket.numConstraints = int(fileHeader[1])
    ticket.numColors = int(fileHeader[2])
    for x in range(1, len(inputFileArray)):
        constraint = inputFileArray[x].split(' ')
        if constraint[0] == '' or constraint[0] == '\n':
            break
        constraintTuples.append((int(constraint[0]), int(constraint[1])))
    return constraintTuples
