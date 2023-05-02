# Partial implementation of reversi game tree search programming exercises
# Copyright Joseph Kendall-Morwick 2023
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

# https://www.mathsisfun.com/games/reversi.html


# Assignment instructions: 
# your task in this assignment is to implement the evaluation function.
# implement it in such a way that the winner is properly determined 
# from leaf nodes and that a good estimate is used such that 
# an agent using this evaluation function would be competitive 
# against simple agents. That is, it should out perform 
# random guessing readily and also out perform an agent that 
# greedily chooses the move that captures the most pieces.

from masProblem import Node
from ast import literal_eval
from masMiniMax import minimax_alpha_beta

# game board states are represented as a 8-tuple of 8-tuples, 
# each containing an 'X', an 'O', or None 
# 'X' is the first (red) player and 'O' is the second (blue) player

initial_game_board = (
  (None,)*8, 
  (None,)*8, 
  (None,)*8, 
  (None, None, None, 'X', 'O', None, None, None),
  (None, None, None, 'O', 'X', None, None, None),
  (None,)*8, 
  (None,)*8, 
  (None,)*8)


def print_game_board(board):
    v = lambda c: '.' if not c else c  # draw 'None' as a dot
    print('   01234567')	
    for r in range(len(board)):
      row = board[r]
      print(r, ' ', end='')
      for col in row:
        print(v(col), end="")
      print("")

def coordinates_in_range(x, y):
    return x >= 0 and x < 8 and y >= 0 and y < 8

def update_board_from_move(x, y, token, board):
    if not coordinates_in_range(x, y):
      return None
    if board[y][x]:
      return None # space is occupied
    
    opponent_token = 'X' if token == 'O' else 'O'
    move = x, y
    board = list(map(list, board)) # make board modifiable
    valid_move = False
    board[y][x] = token
    for dx in range(-1,2,1):
      for dy in range(-1, 2, 1):
        if not dx and not dy: continue
        # determine if placement would surround opponent tokens
        x, y = move

        while coordinates_in_range(x+dx, y+dy) and board[y+dy][x+dx] == opponent_token:
          x += dx
          y += dy
        
        # capture opponent tokens
        if (x,y) != move and coordinates_in_range(x+dx, y+dy) and board[y+dy][x+dx] == token:
          valid_move = True
          x, y = move
          while coordinates_in_range(x+dx, y+dy) and board[y+dy][x+dx] == opponent_token:
            x += dx
            y += dy
            board[y][x] = token
            
    if valid_move:
      return tuple(map(tuple, board))
        
class Reversi(Node):
  def __init__(self, isMax=True, move=None, prior_moves=[], new_board=initial_game_board):
    """Initializes game state.
       isMax is true when it is X's turn and false otherwise
       move is a 2-tuple of coordinates on the board (column, row)
       prior_moves is a list of moves taken to reach this game state
       new_board is a game board as described above"""
    super().__init__(str(move), isMax)
    self.prior_moves = [move] + prior_moves if move else []
    self.board = new_board
    self.isMax = isMax

    # validate input
    assert len(self.board) == 8
    for row in self.board:
      assert len(row)==8

    # process move from prior player
    if move:
      assert coordinates_in_range(move[0], move[1])
      token = 'O' if isMax else 'X'
      self.board = update_board_from_move(move[0], move[1], token, new_board)
    
  def children(self):
    """overrides parent method to simply generate child nodes from legal moves"""
    any_moves = False
    for move in self.legal_moves():
      any_moves = True
      yield Reversi(not self.isMax, move, self.prior_moves, self.board)
    if not any_moves:
      nn = Reversi(not self.isMax,None, self.prior_moves, self.board)
      if nn.legal_moves(): # game not over since opponent can play
        yield nn
  
  def is_leaf(self):
    """in tic-tac-toe, this is a leaf node if there are no moves left"""
    if list(self.legal_moves()): # not a leaf if we can make a move
      return False
    nn = Reversi(not self.isMax, None, self.prior_moves, self.board) 
    return not list(nn.legal_moves()) # game over if neither we nor opponent can move
      
  def legal_moves(self):
    """generates all legal moves (2-tuples of coordinates) for the current board state"""
    for x in range(8): 
      for y in range(8): # check every tile to see if it is a legal move
        if not self.board[y][x] and update_board_from_move(x, y, 'X' if self.isMax else 'O', self.board):
          yield (x, y)

  def evaluate(self):
    """returns the evaluation for this node if it is a leaf"""
    x_count = sum(row.count('X') for row in self.board)
    o_count = sum(row.count('O') for row in self.board)

    if self.is_leaf():
        if x_count > o_count:
            return 1
        elif x_count < o_count:
            return -1
        else:
            return 0
    else:
        token_difference = x_count - o_count
        weight = 1
        return token_difference * weight
    return 0 

n = Reversi()
while not n.is_leaf():
  if not n.isMax:
    print('players turn')
    print_game_board(n.board)
    print("legal moves:", list(n.legal_moves()))
    if list(n.legal_moves()):
      move = literal_eval(input("enter move: "))
      n = Reversi(True, move, n.prior_moves, n.board)
    else:
      print('player must pass')
      n = Reversi(True, None, n.prior_moves, n.board)
  else:
    print('computers turn')
    print_game_board(n.board)
    print("legal moves:", list(n.legal_moves()))
    res = minimax_alpha_beta(n, max_depth=2)
    res = res[1]
    if res:
      print('computer chooses', res[0])
      move = literal_eval(res[0])
      n = Reversi(False, move, n.prior_moves, n.board)
    else:
      print('computer must pass')
      n = Reversi(False, None, n.prior_moves, n.board)

print('final state:')
print_game_board(n.board)
print(n.evaluate())

