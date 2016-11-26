from hlt import *
from networking import *
import random
import numpy as np

myID, gameMap = getInit()
sendInit("GBot")

def move_towards_location(start, stop):

	if stop.x > start.x:
		return Move(start, EAST)
	elif stop.x < start.x:
		return Move(start, WEST)
	if stop.y > start.y:
		return Move(start, SOUTH)
	elif stop.y < start.y:
		return Move(start, NORTH)

	return Move(start, STILL)	  


def move(location):
	site = gameMap.getSite(location)
	neighbors = []

	if site.strength == 0:
		return Move(location, STILL)

	neighbor_ds  = []
	neighbor_strengths = []
	enemy_neigbor = False
	for d in CARDINALS:
		neighbour_site = gameMap.getSite(location, d)
		if neighbour_site.owner != myID and neighbour_site.strength < site.strength:
			neighbor_strengths.append(neighbour_site.strength)
			neighbor_ds.append(d)
		elif neighbour_site.owner != myID:
			enemy_neigbor = True

	if neighbor_strengths:
		i = np.argmax(neighbor_strengths)
		return Move(location, neighbor_ds[i])

	if enemy_neigbor:
		return Move(location, STILL)

	if site.strength > site.production * 5:
		return move_towards_location(location, enemy_pos)

	return Move(location, STILL)

while True:
	moves = []
	gameMap = getFrame()
	for y in range(gameMap.height):
		for x in range(gameMap.width):
			location = Location(x, y)
			if gameMap.getSite(location).owner == myID:
				moves.append(move(location))
			elif gameMap.getSite(location).owner != 0:
				enemy_pos = location
	sendFrame(moves)