import random


def generate_board(*, level="easy"):
  gen_range = (level == "easy") and (35, 45) or (50, 60)
  board = [[0]*9 for _ in range(9)]
  shuffled = list(range(1, 10))
  random.shuffle(shuffled)
  board[0] = shuffled
  random.shuffle(shuffled)
  complete(board, shuffled)
  
  count = random.randint(*gen_range)
  for _ in range(count):
    r, c = random.randrange(9), random.randrange(9)
    board[r][c] = 0
  
  return board


def complete(board, shuffled):
  pos = find_empty(board)
  if not pos:
    return True

  row, col = pos
  for num in shuffled:
    if is_valid(board, num, pos):
      board[row][col] = num
      
      if complete(board, shuffled):
        return True

      board[row][col] = 0
  return False
  

def is_valid(board, num, pos):
  # check the row
  for c in range(len(board[0])):
    if pos[1] != c and board[pos[0]][c] == num:
      return False

  # check the column
  for r in range(len(board)):
    if pos[0] != r and board[r][pos[1]] == num:
      return False
  
  # check the box itself
  box_r = pos[0] // 3
  box_c = pos[1] // 3
  
  for r in range(box_r*3, box_r*3 + 3):
    for c in range(box_c*3, box_c*3 + 3):
      if (r, c) != pos and board[r][c] == num:
        return False
  
  return True
      

def find_empty(board):
  for r in range(len(board)):
    for c in range(len(board[0])):
      if board[r][c] == 0:
        return (r, c)


def is_empty(board):
  for r in range(len(board)):
    for c in range(len(board[0])):
      if board[r][c]:
        return False
  return True