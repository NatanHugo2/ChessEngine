from random import choice
import chess
class ChessEngine:
    def __init__(self):
        self.board = chess.Board()
        self.valid_moves = self.get_valid_moves()
        self.move = None
        self.move_made = False
        self.game_over = False
        self.turn = 'w'
        self.winner = None
        self.move_stack = []
        self.move_stack.append(self.board.fen())

    def get_valid_moves(self):
        return [str(move) for move in self.board.legal_moves]

    def move_generator(self, depth):
        if(depth == 0):
            return 1
        moves = self.get_valid_moves()
        numPositions = 0
        for move in moves:
            self.board.push(chess.Move.from_uci(move))
            numPositions += self.move_generator(depth - 1)  
            self.board.pop()
        return numPositions

    def make_random_move(self):
        if self.game_over:
            return
        self.move = choice(self.valid_moves)

    def make_move(self, move):
        if self.game_over:
            return
        self.move = move

    def update_game(self):
        if self.move is None:
            return
        if self.move not in self.valid_moves:
            return
        self.board.push(chess.Move.from_uci(self.move))
        self.move_stack.append(self.board.fen())
        self.valid_moves = self.get_valid_moves()
        self.move_made = True
        self.move = None

        if self.board.is_game_over():
            self.game_over = True
            if self.board.is_checkmate():
                self.winner = 'w' if self.turn == 'b' else 'b'
            else:
                self.winner = 'draw'

        self.turn = 'w' if self.turn == 'b' else 'b'

    def get_game_state(self):
        return self.board.fen()

    def get_move_made(self):
        return self.move_made

    def get_game_over(self):
        return self.game_over

    def get_winner(self):
        return self.winner

    def get_turn(self):
        return self.turn

    def get_move_stack(self):
        return self.move_stack
    
    def get_board(self):
        return self.board
    
    def get_move(self):
        return self.move
    
    def get_move_made(self):
        return self.move_made
    
    def get_game_over(self):
        return self.game_over
