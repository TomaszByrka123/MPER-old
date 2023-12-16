var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', function() {
    console.log('Connected to the server');
});


//joystick
const place = document.getElementById('joystick-container');
const options = {
    zone: place,
    mode: 'static',
    position: { left: '50%', top: '50%' },
    color: 'blue',
    size: 150
};
const joystick = nipplejs.create(options);

let angle_left = 'stop';
let angle_right = 'stop';

joystick.on('move', (event, data) => {
    const angleRadians = data.angle.radian;
    const angleDegrees = ((angleRadians * 180) / Math.PI).toFixed();
    let force = data.force;

    //ALGORYTM DO ZAMIANY DANYCH Z JOYSTICKA NA MOC SILNIKOW W ŁAZIKU (TE DANE MOGĄ ZOSTAĆ JUŻ PRZESŁANE DO RASPBERRY A POTEM DO ARDUINO)
    var prawy = 100; 
    var lewy = 100;

    //skret w prawo
    if (angleDegrees <= 15 || angleDegrees >= 345) {
        prawy = -100;
        lewy = 100;
    } 
    //skret w lewo
    else if (angleDegrees <= 195 && angleDegrees >= 165) {   
        prawo = 100;
        lewy = -100;
    } 
    //jazda do przodu
    else if (angleDegrees >= 15 && angleDegrees <= 165) {
        roznica = 90 - angleDegrees;
        if (roznica < 0) {
            //lewo
            lewy = lewy + (roznica * 100) / 75;
        } else {
            //prawo
            prawy = prawy - (roznica * 100) / 75;
        }
    } 
    //jazda do tylu
    else {
        roznica = 270 - angleDegrees;
        if (roznica > 0){
            //lewo
            lewy = lewy - (roznica * 100) / 75;
            lewy = lewy * -1;
            prawy = prawy * -1;
        } else {
            //prawo
            prawy = prawy + (roznica * 100) / 75;
            lewy = lewy * -1;
            prawy = prawy * -1;
        }
    }

    if (force > 2) {
        force = 2;
    }

    prawy+=100;
    lewy+=100;

    angle_left = (lewy * force / 2).toFixed(0);
    angle_right = (prawy * force / 2).toFixed(0);
    //console.log(" lewy: ", angle_left, "prawy: ", angle_right);
});

joystick.on('end', () => {
    console.log('Joystick Released');
    angle_left = 'stop';
    angle_right = 'stop';
});

function send_data() {
    if (angle_left != 'stop') {
        socket.emit('joystick', {left: angle_left, right: angle_right});
        //{left: angle_left, right: angle_right}
    }
}
setInterval(send_data, 50);