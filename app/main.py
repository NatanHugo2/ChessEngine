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
def handle_message():
    print('received connect')
    emit('game_state', chess.get_game_state())

@socketio.on('move')
def handle_message(data):
    print('received move: ' + str(data))
    data = data['source'] + data['target']
    chess.make_move(data)
    chess.update_game()
    if(chess.turn == 'b'):
        chess.make_random_move()
        chess.update_game()
    emit('game_state', chess.get_game_state(), broadcast=True)

if __name__ == '__main__':
    socketio.run(app)