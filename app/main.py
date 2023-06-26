from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send

import chessEngine


app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('chess.html')

chess = chessEngine.ChessEngine()
@socketio.on('connect')
def handle_connect():
    emit('game_state', chess.get_game_state())

@socketio.on('foda')
def lidar_com_foda(msg):
    print(msg)

@socketio.on('move')
def handle_movement(data):
    move = data['source'] + data['target']
    result = chess.make_move(move)
    if(result == False):
        emit('game_state', chess.get_game_state())
        return
    best_move = chess.get_best_move(3)
    result = chess.make_move(best_move)
    emit('game_state', result)

if __name__ == '__main__':
    socketio.run(app)