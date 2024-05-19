"""
This module houses the RandomAI which makes random moves.

We are following the javadoc docstring format which is:
@param tag describes the input parameters of the function
@return tag describes what the function returns
@raise tag describes the errors this function can raise
"""

from random import randint
from BoardClasses import Move
from BoardClasses import Board
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
class StudentAI():
    """
    This class describes randomAI
    """
    def __init__(self,col,row,p):
        """
        Intializes randomAI
        @param row: no of rows in the board
        @param col: no of columns in the board
        @param p: no of rows to be filled with checker pieces at the start
        @return :
        @raise :
        """
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1} # to switch turns after each turn
        self.color = 2
    def get_move(self,move):
        """
        get_move function for randomAI called from the gameloop in the main module.
        @param move: A Move object describing the move.
        @return res_move: A Move object describing the move manualAI wants to make. This move is a random move from the set of valid moves.
        @raise :
        """
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1
        moves = self.board.get_all_possible_moves(self.color)
        index = randint(0,len(moves)-1)
        inner_index =  randint(0,len(moves[index])-1)
        move = moves[index][inner_index]
        self.board.make_move(move,self.color)
        return move
