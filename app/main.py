from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send

import chessEngine

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('chess.html')

chess = chessEngine.ChessEngine()
teste = chess.move_generator(2)
print(teste)
@socketio.on('connect')
def handle_connect():
    emit('game_state', chess.get_game_state())

@socketio.on('move')
def handle_movement(data):
    move = data['source'] + data['target']
    chess.make_move(move)
    chess.update_game()
    if(chess.turn == 'b'):
        chess.make_random_move()
        chess.update_game()
    emit('game_state', chess.get_game_state(), broadcast=True)

if __name__ == '__main__':
    socketio.run(app)