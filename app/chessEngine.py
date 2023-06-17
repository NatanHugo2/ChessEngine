from random import choice
import chess
class ChessEngine:
    def __init__(self):
        self.piece_values = {'P': 100, 'N': 280, 'B': 320, 'R': 479, 'Q': 929, 'K': 60000}
        self.pst = {
            'P': [
                [0,  0,  0,  0,  0,  0,  0,  0],
                [-6,  2,  3,  4,  4,  3,  2, -6],
                [-6,  2,  8, 12, 12,  8,  2, -6],
                [-6,  4, 12, 16, 16, 12,  4, -6],
                [-6,  6, 18, 24, 24, 18,  6, -6],
                [-6,  8, 24, 32, 32, 24,  8, -6],
                [-6, 12, 36, 48, 48, 36, 12, -6],
                [0,  0,  0,  0,  0,  0,  0,  0]
            ],
            'N': [  
                [-50, -40, -30, -30, -30, -30, -40, -50],
                [-40, -20,   0,   0,   0,   0, -20, -40],
                [-30,   0,  10,  15,  15,  10,   0, -30],
                [-30,   5,  15,  20,  20,  15,   5, -30],
                [-30,   0,  15,  20,  20,  15,   0, -30],
                [-30,   5,  10,  15,  15,  10,   5, -30],
                [-40, -20,   0,   5,   5,   0, -20, -40],
                [-50, -40, -30, -30, -30, -30, -40, -50]
            ],
            'B': [
                [-20, -10, -10, -10, -10, -10, -10, -20],
                [-10,   0,   0,   0,   0,   0,   0, -10],
                [-10,   0,   5,  10,  10,   5,   0, -10],
                [-10,   5,   5,  10,  10,   5,   5, -10],
                [-10,   0,  10,  10,  10,  10,   0, -10],
                [-10,  10,  10,  10,  10,  10,  10, -10],
                [-10,   5,   0,   0,   0,   0,   5, -10],
                [-20, -10, -10, -10, -10, -10, -10, -20]
            ],
            'R': [
                [0,  0,  0,  5,  5,  0,  0,  0],
                [-5,  0,  0,  0,  0,  0,  0, -5],
                [-5,  0,  0,  0,  0,  0,  0, -5],
                [-5,  0,  0,  0,  0,  0,  0, -5],
                [-5,  0,  0,  0,  0,  0,  0, -5],
                [-5,  0,  0,  0,  0,  0,  0, -5],
                [5, 10, 10, 10, 10, 10, 10,  5],
                [0,  0,  0,  0,  0,  0,  0,  0]
            ],
            'Q': [
                [-20, -10, -10, -5, -5, -10, -10, -20],
                [-10,   0,   0,  0,  0,   0,   0, -10],
                [-10,   0,   5,  5,  5,   5,   0, -10],
                [-5,   0,   5,  5,  5,   5,   0,  -5],
                [0,   0,   5,  5,  5,   5,   0,  -5],
                [-10,   5,   5,  5,  5,   5,   0, -10],
                [-10,   0,   5,  0,  0,   0,   0, -10],
                [-20, -10, -10, -5, -5, -10, -10, -20]
            ],
            'K': [
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-20, -30, -30, -40, -40, -30, -30, -20],
                [-10, -20, -20, -20, -20, -20, -20, -10],
                [20,  20,   0,   0,   0,   0,  20,  20],
                [20,  30,  10,   0,   0,  10,  30,  20]
            ]
        }
        self.pst_b = {piece: [row[::-1] for row in self.pst[piece]] for piece in self.pst}
                
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

    def get_ordered_moves(self):
        moves = self.get_valid_moves()
        ordered_moves = sorted(
            moves,
            key=lambda move: (
                -self.get_captured_piece_value(move),
                self.get_attacker_piece_value(move)
            )
        )
        return ordered_moves

    def get_captured_piece_value(self, move):
        captured_square = chess.Move.from_uci(move).to_square
        captured_piece = self.board.piece_at(captured_square)
        if captured_piece is None:
            return 0
        return captured_piece.piece_type

    def get_attacker_piece_value(self, move):
        from_square = chess.Move.from_uci(move).from_square
        attacker_piece = self.board.piece_at(from_square)
        if attacker_piece is None:
            return 0
        return -attacker_piece.piece_type


    def minimax(self, depth, alpha, beta, isMaximizingPlayer):
        if(depth == 0):
            return self.evaluate()
        
        if(isMaximizingPlayer):
            maxEval = -99999
            moves = self.get_ordered_moves()
            for move in moves:
                self.board.push(chess.Move.from_uci(move))
                value = self.minimax(depth - 1,alpha,beta,False)
                self.board.pop()
                maxEval = max(maxEval,value)
                alpha = max(alpha,value)
                if beta <= alpha:
                    return maxEval
            return maxEval
        
        else:
            minEval = 99999
            moves = self.get_ordered_moves()
            for move in moves:
                self.board.push(chess.Move.from_uci(move))
                value = self.minimax(depth - 1,alpha,beta,True)
                self.board.pop()
                minEval = min(minEval,value)
                beta = min(beta,value)
                if beta <= alpha:
                    return minEval
            return minEval

    def get_best_move(self,depth):
        bestMove = None
        bestValue = -99999
        alpha = -99999
        beta = 99999
        moves = self.get_valid_moves()
        for move in moves:
            self.board.push(chess.Move.from_uci(move))
            value = self.minimax(depth - 1,alpha,beta,False)
            self.board.pop()
            if value > bestValue:
                bestValue = value
                bestMove = move
        return bestMove

    def evaluate(self):
        white_material = self.count_material(chess.WHITE)
        black_material = self.count_material(chess.BLACK)
        pst_evaluation = self.calculate_pst_evaluation(chess.WHITE) - self.calculate_pst_evaluation(chess.BLACK)
        evaluation = white_material - black_material + pst_evaluation
        perspective = 1 if self.turn == 'w' else -1
        return perspective * evaluation
    
    def count_material(self, color):
        material = 0
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece is not None:
                if piece.color == color:
                    material += self.piece_values[piece.symbol().upper()]
                else:
                    material -= self.piece_values[piece.symbol().upper()]
        return material
    
    def calculate_pst_evaluation(self, color):
        pst_evaluation = 0
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece is not None:
                if piece.color == color:
                    rank = chess.square_rank(square)
                    file = chess.square_file(square)
                    pst_evaluation += self.pst[piece.symbol().upper()][rank][file]
                else:
                    rank = chess.square_rank(square)
                    file = chess.square_file(square)
                    pst_evaluation -= self.pst_b[piece.symbol().upper()][rank][file]
        return pst_evaluation

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
