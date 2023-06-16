var socket = io();

//receive a message and console.log it to the console
// socket.on('connect', function(msg) {
//     console.log(msg);
// });



function onDrop (source, target, piece, newPos, oldPos, orientation) {
    //emit a message to the server that a move has been made
    socket.emit('move', {
        source: source,
        target: target,
        piece: piece,
        newPos: Chessboard.objToFen(newPos),
        oldPos: Chessboard.objToFen(oldPos),
        orientation: orientation
    });
    //get move socket response from server
    socket.on('move', function(msg) {
        console.log(msg);
        board.position(msg.newPos);
    }
    );
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
    console.log(msg);
    board.position(msg);
});

