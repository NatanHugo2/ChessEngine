var socket = io();

function onDrop (source, target, piece, newPos, oldPos, orientation) {
    socket.emit('move', {
        source: source,
        target: target,
        piece: piece,
        newPos: Chessboard.objToFen(newPos),
        oldPos: Chessboard.objToFen(oldPos),
        orientation: orientation
    });
}

var config = {
    draggable: true,
    position: 'start',
    onDrop: onDrop,
    sparePieces: true,
    pieceTheme: '/static/img/chesspieces/wikipedia/{piece}.png',
}

var board = Chessboard('myBoard', config)

socket.on('game_state', function(msg) {
    board.position(msg);
});

