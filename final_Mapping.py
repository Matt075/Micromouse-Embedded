''' Functions to map the maze as the micromouse navigates '''

import math

def initMaze():
	''' - Initialize 2D list to store data about each box in the maze
		- Each element in the list stores information in this order respectively
		[checked?, up, bottom, left, right, distance to centre, available for reentry?]
	'''
	maze_list = [ [[False,True,True,True,True,0,True] for y in range(16)] for x in range(16)]
	
	#all of the outer edges have walls
	maze_list[7][7][1] = False
	maze_list[7][7][4] = False
	maze_list[7][8][2] = False
	maze_list[7][8][4] = False
	maze_list[8][7][1] = False
	maze_list[8][7][3] = False
	maze_list[8][8][2] = False
	maze_list[8][8][3] = False
	
	''' The shortest distance from the current position to one of the four center tiles is assigned
		to be the shortest distance from that position to the center '''
	for i in range(16):
		for j in range(16):
			a = round(math.sqrt((7-i)*(7-i) + (7-j)*(7-j)), 2)
			b = round(math.sqrt((7-i)*(7-i) + (8-j)*(8-j)), 2)
			c = round(math.sqrt((8-i)*(8-i) + (7-j)*(7-j)), 2)
			d = round(math.sqrt((8-i)*(8-i) + (8-j)*(8-j)), 2)
			maze_list[i][j][5] = min(a,b,c,d)
			
	return maze_list		

''' Return the attributes of the current position '''
def checked(list):
	return list[0]
	
def upWall(list):
	return list[1]

def bottomWall(list):
	return list[2]

def leftWall(list):
	return list[3]
	
def rightWall(list):
	return list[4]

def distToCenter(list):
	return list[5]

def available(list):
	return list[6]

''' Output the map into a txt file '''
def printMaze(mazeMap,file):
	print>>file,'+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+'
	
	for i in reversed(range(16)):
		nextLine = '|'
		for j in range(16):
			if not available(mazeMap[j][i]):
				nextLine += ' X ' 
			elif checked(mazeMap[j][i]):
				nextLine += ' * '
			else:
				nextLine += '   '
			if rightWall(mazeMap[j][i]):
				nextLine += '|'
			else:
				nextLine += ' '
		print>>file,nextLine
		
		nextLine = '+'
		for j in range(16):
			if bottomWall(mazeMap[j][i]):
				nextLine += '---+'
			else:
				nextLine += '   +'
		print>>file,nextLine
