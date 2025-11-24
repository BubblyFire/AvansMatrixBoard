console.log("hello from main.js");

const PAINT = 'Drawing';
const ERASE = 'Erasing';
let gridTileMode = PAINT

let draw = false;

const userColor = document.getElementById('colorPicker');
const tileMode = document.getElementById('modeDisplay');
const grid = document.getElementById('pixelCanvas');

let mouseIsDown = false;
const rows = 30; // TODO Retrieve from Flask
const columns = 30; // TODO Retrieve from Flask
while (grid.hasChildNodes()) {
    grid.removeChild(grid.lastChild);
}

let tableRows = '';
let r = 1;
while (r <= rows) {
    tableRows += '<tr>';
    for (let c=1; c <= columns; c++) {
        tableRows += '<td></td>';
    }
    tableRows += '</tr>';
    r += 1;
}
grid.insertAdjacentHTML('afterbegin', tableRows);

window.addEventListener("mousedown", function(event) {
    event.preventDefault();
    draw = true;
});
window.addEventListener("mouseup", function(event) {
    event.preventDefault();
    draw = false;
});

grid.addEventListener("mouseover", function(event) {
    event.preventDefault();
    if (!draw) {
        return;
    }
    paintEraseTiles(event.target);
    sendUpdate();
});
grid.addEventListener("mousedown", function(event) {
    event.preventDefault();
    paintEraseTiles(event.target);
    sendUpdate();
});

function sendUpdate() {
    let tiles = grid.getElementsByTagName('td');
    let gridArray = [];
    for(let i = 0; i < tiles.length; i++) {
        gridArray.push(tiles[i].style.backgroundColor);
    }

    $.ajax({ 
        url: '/sendtoboard', 
        type: 'POST',
        contentType: 'application/json', 
        
        data: JSON.stringify({ 'value': gridArray }), 
        success: function(response) { 
            console.log('success'); 
        }, 
        error: function(error) { 
            console.log(error); 
        } 
    }); 
}

function paintEraseTiles(targetCell) {
    if (targetCell.nodeName === 'TD') {
        targetCell.style.backgroundColor = gridTileMode === PAINT ? userColor.value : 'transparent';
    } else {
        console.log("Nice try: " + targetCell.nodeName + " talk to the hand!");
    }
}

userColor.oninput = function (event){
    gridTileMode = PAINT;
    tileMode.innerHTML = ' ' + gridTileMode;
};

document.getElementById('clearButton').addEventListener('click', function() {
    let tiles = grid.getElementsByTagName('td');
    for(let i = 0; i < tiles.length; i++) {
        tiles[i].style.backgroundColor = 'transparent';
    }
    sendUpdate();
    sendUpdate();
});
document.getElementById('drawButton').addEventListener('click', function() {
    gridTileMode = PAINT;
    tileMode.innerHTML = ' ' + gridTileMode;
});
document.getElementById('eraseButton').addEventListener('click', function() {
    gridTileMode = ERASE;
    tileMode.innerHTML = ' ' + gridTileMode;
});
