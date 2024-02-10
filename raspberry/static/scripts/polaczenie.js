var socket = io.connect('http://' + document.domain + ':' + location.port);
var connectIcon = document.getElementById('connection-icon');

socket.on('connect', function() {
    connectIcon.src = '../static/icons/yes.png';
    console.log('Connected to the server');
});

socket.on('disconnect', function() {
    connectIcon.src = '../static/icons/delete.png';
    console.log("disconnected to server")
});