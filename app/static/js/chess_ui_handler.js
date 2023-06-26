var socket = io();

function onDrop (source, target, piece, newPos, oldPos, orientation) {
    socket.emit('move', {
        source: source,
        target: target,
        piece: piece,
        newPos: Chessboard.objToFen(newPos),
        oldPos: Chessboard.objToFen(oldPos),
        orientation: orientation,
        
    });
    board.draggable = false;
}
function getLocalStream(){}
socket.emit("foda",{naosei})
var config = {
    draggable: true,
    position: 'start',
    onDrop: onDrop,
    pieceTheme: '/static/img/chesspieces/custom/{piece}.png',
}

var board = Chessboard('myBoard', config)

socket.on('game_state', function(msg) {
    board.position(msg);
    board.draggable = true;
});

