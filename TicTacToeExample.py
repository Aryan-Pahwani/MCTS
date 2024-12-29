from random import choice
from collections import namedtuple

TTT = namedtuple("TicTacToe", "winner is_terminal turn table")


class TicTacToe(TTT, Node):
    def get_children(board):
        if board.is_terminal: # Terminal Has No Children
            return set()

        return { 
            board.make_move(i) for i, value in enumerate(board.table) if value is None
        }
    
    def find_random_child(board):
        if board.is_terminal: # Terminal Has No Children
            return None  
        empty_spots = [i for i, value in enumerate(board.table) if value is None]
        return board.make_move(choice(empty_spots))

    def reward(board):
      if board.turn is (not board.winner): # When the opps Won :(
        return -1
      if board.winner is None: # Tie
        return 0

    def get_is_terminal(board):
        return board.is_terminal

    def make_move(board, i):
        table = board.table[:i] + (board.turn,) + board.table[i+1 :]
        turn = not board.turn
        winner = TicTacToe.determine_winner(table)

        is_terminal = (winner is not None) or not any(t is None for t in table)

        return TicTacToe(table=table, turn=turn, winner=winner, is_terminal=is_terminal)
 
    def determine_winner(table):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]

        for i, j, k in win_conditions:
            a, b, c = table[i], table[j], table[k]
            if False is a is b is c:  
                return False
            if True is a is b is c:  
                return True
        return None    

    def __repr__(board):
        to_char = lambda t: ("X" if t is True else ("O" if t is False else " "))
        rows = [[to_char(board.table[3 * row + col]) for col in range(3)] for row in range(3)]
        return ("\n"+"\n".join(str(i + 1) + " " + " ".join(row) for i, row in enumerate(rows))+ "\n  1 2 3\n")

def Initiate_TicTacToe():
    return TicTacToe(table=(None,) * 9, turn=True, winner=None, is_terminal=False)

def Game():
    tree = MCTS()
    board = Initiate_TicTacToe()
    print(board)
    while True: # GAME LOOP
        x_y = input("enter x y: ")
      
        y,x = map(int, x_y.split(" "))
      
        index = 3 * (x - 1) + (y - 1)

      
        if board.table[index] is not None:
            raise RuntimeError("Invalid move")
        else:
          board = board.make_move(index)
        if board.is_terminal:
          break

        for _ in range(50):
            tree.do_rollout(board)
          
        print(board)
        board = tree.Selection(board)
      
        print(board)
      
        if board.is_terminal:
            break
          
    print("- - -\n", board, "- - -\n")
    if board.winner == None:
      print("Tie!")
    else:
      print("X Wins!" if board.winner else "O Wins!")

if __name__=='__main__':
  Game()
