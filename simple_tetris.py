import random, pygame, sys, ctypes
from pygame.locals import *

FPS = 60
CELL_SIZE = 20
CELLS_WIDE = 16
CELLS_HIGH = 24

GRID = []
for x in range(CELLS_WIDE):
	GRID.append([None] * CELLS_HIGH)

WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK
GRID_LINES_COLOR = DARKGRAY

WINDOWWIDTH = CELL_SIZE * CELLS_WIDE
WINDOWHEIGHT = CELL_SIZE * CELLS_HIGH

DEFAULT_SPEED = 650

G_BLOCK = [
	[[0,1,0],[1,1,0],[1,0,0]],
	[[2,0,0],[2,2,0],[0,2,0]],
	[[3,3,0],[0,3,0],[0,3,0]],
	[[4,4,0],[4,0,0],[4,0,0]],
	[[0,5,0],[5,5,5],[0,0,0]],
	[[6,6],[6,6]],
	[[7,0,0,0],[7,0,0,0],[7,0,0,0],[7,0,0,0]],
]

BLOCK_COLOR = [(255,0,0),(255,165,0),(255,255,0),(0,255,0),(0,127,255),(0,0,255),(139,0,255)]

class Block():
	def __init__(self, _type=None, speed=None):
		if _type is None:
			self._type = random.randint(0, 6)
		else:
			self._type = _type

		if speed is None:
			self.speed = DEFAULT_SPEED
		else:
			self.speed = speed
		
		self.block = G_BLOCK[self._type]
		self._len = len(self.block)
		self.pos = []
		for i in range(self._len):
			self.pos.append([7,-1*(i+1)])

	def drop(self):
		if self.isStop():
			return False

		setBlock(True)

		for pos in iter(self.pos):
			pos[1] += 1

		pygame.time.wait(self.speed)
		return True

	def isStop(self):
		skip = []
		for i in range(self._len):
			if self.pos[i][1] < 0:
				continue
			layer = self.block[self._len-i-1]
			for j, _type in enumerate(layer):
				pos = [self.pos[i][0]+j, self.pos[i][1]]
				if (_type != 0 and pos[1]+1 in (-1, CELLS_HIGH)) or (j not in skip and _type != 0 and GRID[pos[0]][pos[1]+1]):
					return True
				if _type != 0:
					skip.append(j)

		return False

	def move(self, is_right=False):
		x = self.pos[0][0]
		for i, layer in enumerate(self.block):
			if self.pos[i][1] >= CELLS_HIGH:
				continue
			for j, _type in enumerate(layer):
				if _type == 0:
					continue
				if is_right:
					if x+j+1 in (-1, CELLS_WIDE) or GRID[x+j+1][self.pos[i][1]]:
						return
				else:
					if x+j-1 in (-1, CELLS_WIDE) or GRID[x+j-1][self.pos[i][1]]:
						return
		
		setBlock(True)
		for pos in iter(self.pos):
			if is_right:
				pos[0] += 1
			else:
				pos[0] -= 1

		if self.pos[0][1] >= CELLS_HIGH-1:
			setBlock(False)

	def change(self):
		if self._type == 5:
			return

		new_block = []
		if self._type == 0 or self._type == 1 or self._type == 6:
			if self.block != G_BLOCK[self._type]:
				new_block = G_BLOCK[self._type]
		if len(new_block) == 0:
			for i in range(self._len):
				new_block.append([])
			for i in range(self._len-1,-1,-1):
				for j, _type in enumerate(self.block[i]):
					new_block[j].append(_type)

		tmp_pos = []
		for i, layer in enumerate(self.block):
			for j, _type in enumerate(layer):
				if _type != 0:
					tmp_pos.append([self.pos[self._len-i-1][0]+j, self.pos[self._len-i-1][1]])
		x = self.pos[0][0]
		for i, layer in enumerate(new_block):
			for j, _type in enumerate(layer):
				if _type == 0:
					continue
				if [x+j,self.pos[i][1]] in tmp_pos:
					continue
				if x+j in (-1, CELLS_WIDE) or GRID[x+j][self.pos[i][1]]:
					return

		setBlock(True)
		self.block = new_block




def setBlock(clear_old):
	for i, pos in enumerate(g_block.pos):
		if pos[1] < 0:
			continue
		block = g_block.block[g_block._len-i-1]
		for j, _type in enumerate(block):
			if _type != 0:
				if clear_old:
					GRID[pos[0]+j][pos[1]] = None
				else:
					GRID[pos[0]+j][pos[1]] = BLOCK_COLOR[_type-1]

def checkCleanLine():
	clean_row = 0
	for i in range(CELLS_HIGH-1,-1,-1):
		flag = True
		for j in range(CELLS_WIDE-1,-1,-1):
			if GRID[j][i+clean_row] is None:
				flag = False
				break

		if flag:
			for j in range(CELLS_WIDE-1,-1,-1):
				GRID[j].pop(i+clean_row)
				GRID[j].insert(0, None)
			clean_row += 1


def gameOver():
	ctypes.windll.user32.MessageBoxA(0, "Don't lose heart, try it again", 'Game Over', 0)

def handleEvents():
	for event in pygame.event.get(): # event handling loop
		if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
			pygame.quit()
			sys.exit()
		elif event.type == KEYDOWN or event.type == KEYUP:
			handleControl(event)

def handleControl(event):
	if event.type == KEYDOWN:
		if event.key == K_LEFT:
			g_block.move()
		elif event.key == K_RIGHT:
			g_block.move(True)
		elif event.key == K_SPACE or event.key == K_UP:
			g_block.change()
		elif event.key == K_DOWN:
			g_block.speed -= 600
	elif event.type == KEYUP and event.key == K_DOWN:
		g_block.speed = DEFAULT_SPEED

def drawGrid():
	DISPLAYSURF.fill(BGCOLOR)
	for x in range(0, WINDOWWIDTH, CELL_SIZE):
		pygame.draw.line(DISPLAYSURF, GRID_LINES_COLOR, (x, 0), (x, WINDOWHEIGHT))
	for y in range(0, WINDOWHEIGHT, CELL_SIZE):
		pygame.draw.line(DISPLAYSURF, GRID_LINES_COLOR, (0, y), (WINDOWWIDTH, y))
	for x in range(0, CELLS_WIDE):
		for y in range(0, CELLS_HIGH):
			if GRID[x][y] is None:
				continue
			color = GRID[x][y]
			darkerColor = (max(color[0] - 50, 0), max(color[1] - 50, 0), max(color[2] - 50, 0))
			pygame.draw.rect(DISPLAYSURF, darkerColor, (x * CELL_SIZE,     y * CELL_SIZE,     CELL_SIZE,     CELL_SIZE    ))
			pygame.draw.rect(DISPLAYSURF, color,       (x * CELL_SIZE + 4, y * CELL_SIZE + 4, CELL_SIZE - 8, CELL_SIZE - 8))




def main():
	global FPSCLOCK, DISPLAYSURF
	global g_block

	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	pygame.display.set_caption('Tetris')
	
	g_block = Block(6)

	while True:
		handleEvents()

		if not g_block.drop():
			checkCleanLine()
			del g_block
			g_block = Block(6)

		setBlock(False)
		drawGrid()

		pygame.display.update()
		FPSCLOCK.tick(FPS)


if __name__ == '__main__':
	main()
