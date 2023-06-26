from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send

import chessEngine

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('chess.html')

@app.route('/jogar')
def jogo():
    return render_template('jogo.html')

chess = chessEngine.ChessEngine()
@socketio.on('connect')
def handle_connect():
    emit('game_state', chess.get_game_state())

@socketio.on('move')
def handle_movement(data):
    move = data['source'] + data['target']
    chess.make_move(move)
    chess.update_game()
    if(chess.turn == 'b'):
        move = chess.get_best_move(3)
        chess.make_move(move)
        chess.update_game()
    emit('game_state', chess.get_game_state(), broadcast=True)
if __name__ == '__main__':
    socketio.run(app)