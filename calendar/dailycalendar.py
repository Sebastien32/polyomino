import os
from datetime import date
import pandas as pd
import itertools as it
import time
import png
import random

from polyomino import TilingProblem
from polyomino.board import Rectangle
from polyomino.constant import PENTOMINOS
from polyomino.constant import MONOMINO
from polyomino.tileset import Tileset

from pretty_poly.png import write_colored_blocks_png

def month_square(month):
	row = (month - 1) // 6
	col = (month - 1) % 6
	return (col, row)

def day_square(day):
	row = (day - 1) // 7 + 2
	col = (day - 1) % 7
	return (col, row)

def test_all_days(tileset):
	start_time = time.perf_counter()
	BOARD = Rectangle(7, 7)
	BOARD = BOARD.remove_all([(6, 0), (6, 1), (3, 6), (4, 6), (5, 6), (6, 6)])
	START_DATE = date(2020, 1, 1)
	END_DATE = date(2020, 12, 31)
	for today in pd.date_range(START_DATE, END_DATE):
		print(today.strftime('%Y-%m-%d'))
		board = BOARD.remove_all([month_square(today.month), day_square(today.day)])
		problem = TilingProblem(board, tileset)
		solution = problem.solve()
		if solution is None:
			return False
		actual = solution.tiling
		assert(len(actual) == tileset.selector_size)
	return True

HEXOMINO_BOX = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
HEXOMINO_FISH = [(0, 0), (0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]
TILES = [
	PENTOMINOS['F'], 
	PENTOMINOS['L'], 
	PENTOMINOS['P'], 
	PENTOMINOS['W'], 
	PENTOMINOS['U'], 
	PENTOMINOS['V'], 
	PENTOMINOS['Y'], 
	PENTOMINOS['F'], 
	MONOMINO]

if __name__ == '__main__2':
	# 12-13 seconds per tiletset, 792 tilesets = 2.8 hours
	# 35 free hexominos = 3*35 = 105 hours = 4 days
	viable_tilesets = set()
	count = 0
	for pentomino_set in it.combinations(PENTOMINOS, 7):
		count += 1
		if ('I' in pentomino_set) or ('T' in pentomino_set):
			continue
		tiles = [PENTOMINOS[k] for k in pentomino_set]
		tiles.append(HEXOMINO_BOX)
		if (test_all_days(Tileset(tiles, [], [], reflections = True))):
			print('Success', count)
			viable_tilesets.add(pentomino_set)
		print(count)

if __name__ == '__main__':
	if (test_all_days(Tileset(TILES, [], [], reflections = True))):
		print('Success!')