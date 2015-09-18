
class Square(object):
	def __init__(self, row, col, g, h, parent):
		self.row = row
		self.col = col
		self.g = g
		self.h = h
		self.parent = parent
		
openlist = []
closedlist = []
final = []

def A_Star2():
	start = Square(7,0,0,0,None)
	openlist.append(start)
	i = start
	while len(openlist) != 0:
		openlist.remove(i)
		closedlist.append(i)
		if i.row == 0 and i.col == 9:
			break
		i = A_Star_Helper(i)
	closedlist.append(i)
	end = None
	for x in closedlist:
		if x.row == 0 and x.col == 9:
			end = x
			break
	print "Nodes visited, working backwards:"
	print_list(end)
	print "Total Cost = {}".format(end.g)
	print "Locations Evaluated: {}".format(len(closedlist))

def print_list(end):
	while end.parent != None:
		print 'Row={} Col={}'.format(
			end.row,end.col)
		end = end.parent
	print "Row=7 Col=0"


def A_Star_Helper(q):
	#~ openlist.remove(q)
	#~ closedlist.append(q) # Put q in the closed list
	adj = find_adj(q) # Find all adjacent candidates for open list
	#Make sure g of duplicate squares isn't better with new parent q
	# Remove duplicate squares from adjacent list
	for x in openlist:
		for y in adj:
			if x.row == y.row and x.col == y.col:
				if x.g > y.g:
					x.parent = q
					x.g = y.g + q.g
					adj.remove(y)
				else:
					adj.remove(y)
	#Add all remaining adj nodes to the openlist. Calculate h
	for x in adj:
		x.h = hueristic2(x)
		openlist.append(x)
	
	# Find the smallest f in the openlist
	smallestf = Square(0,0,float("Inf"),0,None)
	for x in openlist:
		f = x.g + x.h
		if f < smallestf.g + smallestf.h:
			smallestf = x
	return smallestf

# Function for the manhattan hueristic
def hueristic2(node):
	row = node.row
	col = node.col
	total = 0
	# Traverse the matrix upwards diagonally, first
	while row > 0 and col < 9:
		row = row - 1
		col = col + 1
		total = total + 14
	# Then finish off the rows and columns
	while row > 0:
		row = row - 1
		total = total + 10
	while col < 9:
		col = col + 1
		total = total + 10
	return total


def find_adj(center):
	# Store the location of the center node.
	row = center.row
	col = center.col
	g = center.g
	# Create a candidate list that we will store the possible
	# adjacent vertices in.
	candidate_list = []
	
	# First check the bounds of all the adjecent squares
	# We start with the row below the current, then move to the row
	# above it, and then check the two squares beside the current one
	if row - 1 >= 0:
		if col - 1 >= 0 and col - 1 <= 9 and final[row-1][col-1] != 2:
			candidate_list.append(Square(row - 1, col -1, find_g_diag(g,row - 1,col - 1), 0, center))
		if col >= 0 and col <= 9 and final[row-1][col] != 2:
			candidate_list.append(Square(row - 1, col, find_g(g,row - 1,col), 0, center))
		if col + 1 >=0 and col + 1 <= 9 and final[row-1][col+1] != 2:
			candidate_list.append(Square(row - 1, col + 1, find_g_diag(g,row - 1,col + 1), 0, center))
	if row + 1 <= 7:
		if col - 1 >= 0 and col - 1 <= 9 and final[row+1][col-1] != 2:
			candidate_list.append(Square(row + 1, col -1, find_g_diag(g,row + 1,col - 1), 0, center))
		if col >=0 and col <= 9 and final[row+1][col] !=2:
			candidate_list.append(Square(row + 1, col, find_g(g,row + 1,col), 0, center))
		if col + 1 >=0 and col + 1 <= 9 and final[row+1][col+1] != 2:
			candidate_list.append(Square(row + 1, col + 1, find_g_diag(g,row + 1,col + 1), 0, center))
	if col - 1 >= 0 and final[row][col-1] != 2:
		candidate_list.append(Square(row, col - 1, find_g(g,row,col - 1), 0, center))
	if col + 1 <= 9 and final[row][col+1] != 2:
		candidate_list.append(Square(row, col + 1, find_g(g,row,col + 1), 0, center))
	
	# Prune our candidate list of squares which are on the closed list
	for y in closedlist:
		for x in candidate_list:
			if x.row == y.row and x.col == y.col:
				candidate_list.remove(x)
								
	return candidate_list

def find_g_diag(g,row,col):
	if final[row][col]==0:
		return g+14
	if final[row][col]==1:
		return g+24

def find_g(g,row,col):
	if final[row][col]==0:
		return g+10
	if final[row][col]==1:
		return g+20
