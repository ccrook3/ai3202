# Casey Moher-Crook
# Assignment 5 - Markov Chains
# Note: I edited the world files to not have whitespace at the bottom
# This made them simpler to parse

# Import the regular expressions library
# This makes parsing the world files easier.
import re
# Also import Sys to allow command line arguments
import sys
if len(sys.argv) != 3:
	print "Proper usage is world_file hueristic (1 or 2)"
	exit(0)
arg1 = sys.argv[1]
epsilon = float(sys.argv[2])

# Open the file and read in its data
with open(arg1, 'r') as world:
	world_data = world.read()

# Parse the data into a long list
world_list = re.split("\s", world_data)

# Convert each String value in the lists to an integer value
i = 0
while i < len(world_list):
	world_list[i] = int(world_list[i])
	i = i + 1

# Turn the World into a nested list/matrix
# Giving our final world structure
i = 0
g = 0
final = [[]]*8
while i != len(world_list):
	final[g] = world_list[i:i+10]
	g = g + 1
	i = i + 10
	
for x in final:
	print x

print
print

#Reward Function
#Tests what is on the grid at the state given
#Returns a number for the reward
def R(s):
    x = s[0]
    y = s[1]
    testVal = final[x][y]
    if (testVal == 0 or testVal == 2):
        return 0
    elif (testVal ==1):
        return -1
    elif (testVal == 3):
        return -2
    elif (testVal == 4):
        return 1
    else:
        return 50

def Wall(s):
    x = s[0]
    y = s[1]
    if final[x][y] == 2:
        return True

def maxT(s, U1):
    x = s[0]
    y = s[1]
    return max(
            up(x,y,U1),down(x,y,U1),left(x,y,U1),right(x,y,U1)
            )

def up(x,y,U1):
    upchance = 0
    leftchance = 0
    rightchance = 0
    if (x != 0 and not Wall((x-1,y))):
        upchance = .8 * U1[(x-1,y)]
    if (y != 0 and not Wall((x,y-1))):
        leftchance = .1 * U1[(x,y-1)]
    if (y != 9 and not Wall((x,y+1))):
        rightchance = .1 * U1[(x,y+1)]
    return upchance + leftchance + rightchance

     
def down(x,y,U1):
    downchance = 0
    leftchance = 0
    rightchance = 0
    if (x != 7 and not Wall((x+1,y))):
        downchance = .8 * U1[(x+1,y)]
    if (y != 0 and not Wall((x,y-1))):
        rightchance = .1 * U1[(x,y-1)]
    if (y != 9 and not Wall((x,y+1))):
        leftchance = .1 * U1[(x,y+1)]
    return downchance + leftchance + rightchance


def left(x,y,U1):
    upchance = 0
    leftchance = 0
    downchance = 0
    if (x != 0 and not Wall((x-1,y))):
        upchance = .1 * U1[(x-1,y)]
    if (y != 0 and not Wall((x,y-1))):
        leftchance = .8 * U1[(x,y-1)]
    if (x != 7 and not Wall((x+1,y))):
        downchance = .1 * U1[(x+1,y)]
    return upchance + leftchance + downchance


def right(x,y,U1):
    upchance = 0
    rightchance = 0
    downchance = 0
    if (x != 0 and not Wall((x-1,y))):
        upchance = .1 * U1[(x-1,y)]
    if (y != 9 and not Wall((x,y+1))):
        rightchance = .8 * U1[(x,y+1)]
    if (x != 7 and not Wall((x+1,y))):
        downchance = .1 * U1[(x+1,y)]
    return upchance + downchance + rightchance

# This is our main loop
gamma = 0.9
def valueIter():
    U1 = dict()
    for x in range(len(final)):
        for y in range(len(final[0])):
            U1[(x,y)] = 0
    while (True):
        U = U1.copy()
        delta = 0
        for x in range(len(final)):
            for y in range(len(final[0])):
                U1[(x,y)] = R((x,y)) + gamma * maxT((x,y),U)
                delta = max(delta, abs(U1[(x,y)] - U[(x,y)]))
        if delta < (epsilon * (1 - gamma) / gamma):
            return U

# Function to help print it all out 
def printU(U):
    x = 0
    y = 0
    printList = list(final)
    for x in range(len(final)):
        for y in range(len(final)):
            printList[x][y] = round(U[(x,y)],1)
    print "Utility List:"
    for x in printList:
        print x
    x = 7
    y = 0
    print "Order of movement:"
    while (x > 0 and y < len(printList)):
        if ( printList[x-1][y] > printList[x][y+1]):
            print "{},{}->{},{} = {}".format(
                    x,y,x-1,y,printList[x-1][y])
            x = x - 1
        else:
            print "{},{}->{},{} = {}".format(
                    x,y,x,y+1,printList[x][y+1])
            y = y + 1

printU(valueIter())
