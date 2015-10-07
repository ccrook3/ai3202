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
epsilon = sys.argv[2]

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
# This class helps us keep track of each square
class Square(object):
	def __init__(self, row, col, g, h, parent):
		self.row = row
		self.col = col
		self.g = g
		self.parent = parent

x = 0
y = 0
states = set()
for x in range(len(final)):
    for y in range(len(final[0])):
        states.add((x,y))
print states

#Reward Function
#Tests what is on the grid at the state given
#Returns a number for the reward
def R(s):
    x = s[0]
    y = s[1]
    testVal = final[x][y]
    if (testVal == 0):
        return 0
    elif (testVal ==1):
        return -1
    elif (testVal == 2):
        return -100
    elif (testVal == 3):
        return -2
    else:
        return 1

def maxT(s, U1):
    up = 0
    down = 0
    right = 0
    left = 0
    x = s[0]
    y = s[1]

     
# This is our main loop
# Here, we can define some parameters if we want to change them later
gamma = 0.97
def valueIter():
    U = dict([s,0] for s in states)
    while (True):
        U1 = U.copy()
        delta = 0
        for s in states:
            U1[s] = R(s) + gamma * maxT(s,U1)
            delta = max(delta, abs(U1[s] - U[s]))
        if delta < epsilon * (1 - gamma) / gamma:
            return U

print valueIter()
