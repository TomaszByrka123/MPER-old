var joystickPodwozie = nipplejs.create({
    zone: document.getElementById("joystick-podwozie-container"),
    mode: 'static',
    position: { left: '50%', top: '70%' },
    color: 'blue',
    size: 150
});

let angle_left = 100;
let angle_right = 100;

joystickPodwozie.on('move', (event, data) => {
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

    angle_left = (lewy * force / 2).toFixed(0);
    angle_right = (prawy * force / 2).toFixed(0);

    //dodanie 100
    angle_left = parseInt(angle_left) + 100;
    angle_right = parseInt(angle_right) + 100;
    //console.log(" lewy: ", angle_left, "prawy: ", angle_right);
});

joystickPodwozie.on('end', () => {
    //console.log('Joystick Released');
    angle_left = 100;
    angle_right = 100;
});

function send_data_podwozie() {
    //console.log(mobileConnection);
    if (!mobileConnection) socket.emit('joystickPodwozie', {left: angle_left, right: angle_right});
}
setInterval(send_data_podwozie, 400);
