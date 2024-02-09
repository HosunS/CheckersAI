from random import randint
from BoardClasses import Move
from BoardClasses import Board
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
from math import sqrt, log
import logging
from copy import deepcopy
import time

# logging.basicConfig(level=logging.DEBUG) #used for testing errors
### will print out log.debug() to debug.log in TOOLS... open seperate term and run tail -f debug.log to track output
logging.basicConfig(filename='debug.log', level=logging.DEBUG, 
                    format='%(message)s')


MAXDEPTH = 16
ITERATIONS = 1000
TIME_LIMIT = 16
# MINMAXDEPTH = 1
EXP_CONST = 2 #range :  ~ higher value encourages exploration, lower value encourages exploitation
# MINMAXITERS = 0


class MCTSnode():
    
    def __init__(self,color,move,parent=None):
        self.color = color
        self.move = move
        self.parent=parent
        self.wins = 0
        self.simulations = 0
        self.children = []
        
    def UCT(self):
        psims = self.parent.simulations if self.parent is not None else 10
        w = self.wins
        s = self.simulations
        # if w < 8:
        #     w = 8
        # if s < 10:
        #     s = 10
        
        uct_value = (w / s) + EXP_CONST * sqrt(log(psims) / s)
        return uct_value

    def getWinRate(self):
        if self.simulations != 0:
            return self.wins / self.simulations
        else:
            return -1
        
        
class StudentAI():

    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2
        self.root = MCTSnode(self.color,-1)
        self.players = {0:"." , 1 : "B" , 2 : "W"}
        self.total_piece = self.board.black_count + self.board.white_count
        self.total_time = time.time()
        self.black = 0
        self.white = 0
        self.tie = 0
        
    def findIndex(self, m): #find index of moves with available moves
        i = 0
        while i != len(self.root.children):
            if self.root.children[i].move.seq == m.seq:
                break
            i += 1
        return i    
            
    
    def select(self): #responsible for finding leaf nodes
        node = self.root
        highestUCTs = []
        
        while len(node.children) != 0: #if there are children...
            possible_moves = self.board.get_all_possible_moves(node.color)
            flat_moves = [move for sublist in possible_moves for move in sublist]
            
            if len(node.children) < len(flat_moves): ## hasnt expanded all the children
                return node
            if len(flat_moves) == 0: #there is atleast one child, because len of node.child is not zero
                node = node.children[0]
            else: #fully expanded
                highestUCTs.clear()
                max_uct = -1
                for child in node.children:
                    uct = child.UCT()
                    if uct == 0:
                        return child
                    elif uct > max_uct:
                        max_uct = uct
                        highestUCTs.clear()
                        highestUCTs.append(child)
                    elif uct == max_uct:
                        highestUCTs.append(child)
                randomindex = randint(0 , len(highestUCTs) -1)
                new_node = highestUCTs[randomindex]
                
                self.board.make_move(new_node.move,node.color)
                node = new_node
        
        return node    
    
    def expand(self,node):
        possible_moves = self.board.get_all_possible_moves(node.color)
        flat_moves = [move for sublist in possible_moves for move in sublist]
        
        if len(flat_moves) == 0: #game over no moves
            if self.board.is_win(self.players[node.color]) != 0:
                return node
            else: #no moves cause of blocks // check if opponent has moves so that we can return that node
                temp_player = self.players[self.opponent[node.color]]
                temp_board = self.board.board
                for r in range(self.board.row):
                    for c in range(self.board.col):
                        if temp_board[r][c].color == temp_player and len(temp_board[r][c].get_possible_moves(self.board)) != 0:
                            new_node = MCTSnode(self.opponent[node.color],-1,node)
                            node.children.append(new_node)
                            return new_node
            
        possible_move = flat_moves[0]
        next_node_moves = []
        for child in node.children:
            next_node_moves.append(child.move.seq)
        for move in flat_moves:
            if next_node_moves.count(move.seq) == 0:
                possible_move = move
                break
            
        childnode = MCTSnode(self.opponent[node.color],possible_move, node)
        node.children.append(childnode)
        self.board.make_move(possible_move,node.color)
        return childnode
        
    
            
    def heuristics(self): #used at end of simulation to get a value of board when the game is not done yet.
        pawn = 1
        king = 3
        vulnerable_penalty = 1
        
        blackScore = 0
        whiteScore = 0

        total_pieces = self.board.black_count + self.board.white_count

        
        
        board_row = self.board.row
        board_col = self.board.col
        board = self.board.board
        #loop through board and for each piece add to score
        for r in range(board_row):
            for c in range(board_col):
                piece = board[r][c]
                
                if piece.color == "W":
                    if piece.is_king:
                        whiteScore += king
                        whiteScore += self.center_focus_score(r,c,board_row)
                    else:
                        whiteScore += (board_row-r-1)*pawn               
                        whiteScore += self.center_focus_score(r,c,board_row)
                
                if piece.color == "B":
                    if piece.is_king:
                        blackScore += king
                        blackScore += self.center_focus_score(r,c,board_row)
                    else:
                        blackScore += r *pawn
                        blackScore += self.center_focus_score(r,c,board_row)
                        
        return  blackScore, whiteScore # return (blackScore , whiteScore)
    
    def center_focus_score(self, row, col, board_size):
        center = board_size / 2 #assuming we have a square board
        distance = abs(center - row - 0.5) + abs(center - col - 0.5) #manhattan distance
        base_center_score = board_size
        return base_center_score - distance
  
    
    
# first iteration we wil be looking for opponents move (white) since we are testing with black
    #Random moves simulate
    def simulate(self,node):
        color = node.color
        winner = self.board.is_win(self.players[color])
        depth = 0
        turn_with_no_capture = 0
        ## keep playing until win/loss/ reach depth and use heuristic
        while winner == 0 and depth < MAXDEPTH:
            possible_moves = self.board.get_all_possible_moves(color)
            moves = [move for sublist in possible_moves for move in sublist]
            if len(moves) != 0: #we have moves
                randomindex = randint(0,len(moves) -1)
                self.board.make_move(moves[randomindex],color) #moves[randomindex] for random move
            
            winner = self.board.is_win(self.players[color])
            color = self.opponent[color]
            depth += 1
            
        if winner == 0: #check who won according to heuristic
        # heuristics
            scoreBlack, scoreWhite = self.heuristics()
            if scoreBlack > scoreWhite:  # Compares black with white
                winner = 1
            elif scoreBlack == scoreWhite:
                winner = self.color
            else:
                winner = 2
        elif winner == -1:
                winner = self.color

        if winner == 1:
            self.black += 1
        elif winner == 2:
            self.white += 1
        elif winner == .5:
            self.tie +=1
            
        return winner

                
    def backpropogation(self,result,node):
        while node != self.root:
            node.simulations += 1
            if result != node.color:
                node.wins += 1
            node = node.parent

        node.simulations +=1
        if result != node.color:
            node.wins += 1
        
    
    def MCTS(self,moves):
        # logging.debug(len(moves)) #get rid of after testing
        
        if len(moves) < 4:
            TIME_LIMIT = 5
        else:
            TIME_LIMIT = 14
        if (time.time() - self.total_time)/60 > 3:
            TIME_LIMIT = 4
            
        start_time = time.time() #start time
        orig_board = deepcopy(self.board) # keep a copy of the board, that way we can come back to it to find the best move
        iterations = 0

        # total_pieces = self.board.black_count + self.board.white_count
        # if total_pieces == self.total_piece:
        #     MAXDEPTH = 10
        # elif self.total_piece/2 < total_pieces < self.total_piece:
        #     MAXDEPTH = 14
        # else:
        #     MAXDEPTH = 14
        
        for _ in range(ITERATIONS):
            select = self.select()
            expand = self.expand(select)
            result = self.simulate(expand)
            self.backpropogation(result,expand)
            self.board = deepcopy(orig_board)
            iterations += 1
            if time.time() - start_time >= TIME_LIMIT:
                break
        #testing
        # logging.debug("ROOT: wins %s sims %s color %s move %s", self.root.wins, self.root.simulations,self.players[self.root.color], self.root.move)
        # logging.debug("COUNT: %s ", iterations)
        # logging.debug("simulations : white %s , black %s , tie %s" , self.white , self.black, self.tie)
        self.white = 0
        self.black = 0
        self.tie = 0
        
        if len(self.root.children) == 0: ## no children to root
            randomindex = randint(0,len(moves)-1)
            best_move = moves[randomindex]
        else:
            # best_move = max(self.root.children, key=lambda child: child.wins / child.simulations if child.simulations > 0 else 0).move
            bestwins = -1
            i = 0
            while i != len(self.root.children):
                #get rid of after testing
                # logging.debug(" %s %s wins %s sims %s ratio %s"  , i , self.root.children[i].move , self.root.children[i].wins,self.root.children[i].simulations , self.root.children[i].wins/self.root.children[i].simulations)
                if self.root.children[i].getWinRate() >= bestwins:
                    bestwins = self.root.children[i].getWinRate()
                    best_move = self.root.children[i].move
                i += 1
        
        del orig_board
        return best_move

    
    def get_move(self, move):
        # If opponent has made a move, update the tree
        if len(move) != 0:
            self.board.make_move(move, self.opponent[self.color])
            child_found = False

            for child in self.root.children:
                if child.move.seq == move.seq:
                    self.root = child
                    child_found = True
                    break

            if not child_found:
                # opponent's move is not a child of the root, so create a new root
                self.root = MCTSnode(self.color, move)

        # if its the start of the game or after the opponents move was not in the children
        else:
            self.color = 1
            self.root.color = 1

        possible_moves = self.board.get_all_possible_moves(self.root.color)
        moves = [move for sublist in possible_moves for move in sublist]

        if len(moves) == 1:
            move = moves[0]
        else:
            move = self.MCTS(moves)

        self.board.make_move(move, self.color)

        # update root to the child node that corresponds to the chosen move
        # if no such child, create a new root for the next move
        child_found = False
        for child in self.root.children:
            if child.move.seq == move.seq:
                self.root = child
                child_found = True
                break

        if not child_found:
            self.root = MCTSnode(self.opponent[self.color], move)
            
        # logging.debug("elapsed Total time:  %s \n" , (time.time() - self.total_time)/60)
        return move
    
