import numpy as np
import matplotlib.pyplot as plt


def game_of_life(board):
	neighbors = np.zeros(board.shape, dtype=int)
	for i in range(board.shape[0]):
		for j in range(board.shape[1]):
			for x in [-1, 0, 1]:
				for y in [-1, 0, 1]:
					if x == 0 and y == 0:
						continue
					nx, ny = i + x, j + y
					if nx < 0 or ny < 0 or nx == board.shape[0] or ny == board.shape[1]:
						continue
					neighbors[i, j] += board[nx, ny]

	for i in range(board.shape[0]):
		for j in range(board.shape[1]):
			if board[i, j] and not (neighbors[i, j] == 2 or neighbors[i, j] == 3):
				board[i, j] = 0
			elif neighbors[i, j] == 3:
				board[i, j] = 1

	return board


def visualize(board):
	plt.imshow(board)
	plt.show()


if __name__ == "__main__":
	board = np.random.choice([0, 1], size=(10, 10))
	visualize(board)
	for _ in range(10):
		board = game_of_life(board)
		visualize(board)
