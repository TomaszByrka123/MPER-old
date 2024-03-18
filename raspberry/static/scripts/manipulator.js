//joystick A (podstawa)
var joystickManipulatorA = nipplejs.create({
    zone: document.getElementById("joystick-manipulator-A-container"),
    mode: 'static',
    position: { left: '40%', top: '50%' },
    color: 'blue',
    size: 150
});

//joystick B (przegub)
var joystickManipulatorB = nipplejs.create({
    zone: document.getElementById("joystick-manipulator-B-container"),
    mode: 'static',
    position: { left: '60%', top: '50%' },
    color: 'blue',
    size: 150
});


let isLeftPressed = false;
let isRightPressed = false;
let isLeftPressedCrush = false;
let isRightPressedCrush = false;
let dataManipulator = [0, 0, 0, 0, 0];

joystickManipulatorA.on('move', (event, data) => {
    const angleRadiansA = data.angle.radian;
    const angleDegreesA = ((angleRadiansA * 180) / Math.PI).toFixed();

    //console.log(angleDegrees);

    //ruch w prawo / lewo
    if (angleDegreesA <= 70 || angleDegreesA >= 290) dataManipulator[0] = 2;
    else if (angleDegreesA <= 250 && angleDegreesA >= 110) dataManipulator[0] = 1; 
    else dataManipulator[0] = 0;


    //ruch w góre / dół
    if (angleDegreesA <= 160 && angleDegreesA >= 20) dataManipulator[1] = 2;
    else if (angleDegreesA <= 340 && angleDegreesA >= 200) dataManipulator[1] = 1; 
    else dataManipulator[1] = 0;
});

joystickManipulatorA.on('end', () => {
    dataManipulator[0] = 0;
    dataManipulator[1] = 0;
});


joystickManipulatorB.on('move', (event, data) => {
    const angleRadiansA = data.angle.radian;
    const angleDegreesA = ((angleRadiansA * 180) / Math.PI).toFixed();

    //console.log(angleDegrees);

    //ruch w prawo / lewo
    if (angleDegreesA <= 70 || angleDegreesA >= 290) dataManipulator[0] = 2;
    else if (angleDegreesA <= 250 && angleDegreesA >= 110) dataManipulator[0] = 1; 
    else dataManipulator[0] = 0;


    //ruch w góre / dół
    if (angleDegreesA <= 160 && angleDegreesA >= 20) dataManipulator[2] = 2;
    else if (angleDegreesA <= 340 && angleDegreesA >= 200) dataManipulator[2] = 1; 
    else dataManipulator[2] = 0;
});

joystickManipulatorB.on('end', () => {
    dataManipulator[0] = 0;
    dataManipulator[2] = 0;
});



function send_data_manipulator() {
    //console.log(dataManipulator)
    socket.emit('joystickManipulator', dataManipulator);
}
setInterval(send_data_manipulator, 400);






//strzałki do obrotu grippera

document.addEventListener('keydown', function(event) {
    const direction = event.key.toLowerCase();
    if (direction === 'arrowleft') {
        isLeftPressed = true;
        document.getElementById('leftBtn').classList.add('clicked');
    } else if (direction === 'arrowright') {
        isRightPressed = true;
        document.getElementById('rightBtn').classList.add('clicked');
    }
});
document.addEventListener('keyup', function(event) {
    const direction = event.key.toLowerCase();
    if (direction === 'arrowleft') {
        isLeftPressed = false;
        document.getElementById('leftBtn').classList.remove('clicked');
    } else if (direction === 'arrowright') {
        isRightPressed = false;
        document.getElementById('rightBtn').classList.remove('clicked');
    }
});
document.getElementById('leftBtn').addEventListener('mousedown', function() {
    isLeftPressed = true;
    this.classList.add('clicked');
});
document.getElementById('leftBtn').addEventListener('mouseup', function() {
    isLeftPressed = false;
    this.classList.remove('clicked');
});
document.getElementById('rightBtn').addEventListener('mousedown', function() {
    isRightPressed = true;
    this.classList.add('clicked');
});
document.getElementById('rightBtn').addEventListener('mouseup', function() {
    isRightPressed = false;
    this.classList.remove('clicked');
});
function checkPressedButtons() {
    if (isLeftPressed) {
        dataManipulator[3] = 1;
    }
    if (isRightPressed) {
        dataManipulator[3] = 2;
    }
    if (!isLeftPressed && !isRightPressed) dataManipulator[3] = 0;
}

setInterval(checkPressedButtons, 100);




//strzałki do crush grippera

document.addEventListener('keydown', function(event) {
    const direction = event.key.toLowerCase();
    if (direction === 'arrowup') {
        isLeftPressedCrush = true;
        document.getElementById('leftCrush').classList.add('clicked');
    } else if (direction === 'arrowdown') {
        isRightPressedCrush = true;
        document.getElementById('rightCrush').classList.add('clicked');
    }
});
document.addEventListener('keyup', function(event) {
    const direction = event.key.toLowerCase();
    if (direction === 'arrowup') {
        isLeftPressedCrush = false;
        document.getElementById('leftCrush').classList.remove('clicked');
    } else if (direction === 'arrowdown') {
        isRightPressedCrush = false;
        document.getElementById('rightCrush').classList.remove('clicked');
    }
});
document.getElementById('leftCrush').addEventListener('mousedown', function() {
    isLeftPressedCrush = true;
    this.classList.add('clicked');
});
document.getElementById('leftCrush').addEventListener('mouseup', function() {
    isLeftPressedCrush = false;
    this.classList.remove('clicked');
});
document.getElementById('rightCrush').addEventListener('mousedown', function() {
    isRightPressedCrush = true;
    this.classList.add('clicked');
});
document.getElementById('rightCrush').addEventListener('mouseup', function() {
    isRightPressedCrush = false;
    this.classList.remove('clicked');
});
function checkPressedButtonsCrush() {
    if (isLeftPressedCrush) {
        dataManipulator[4] = 2;
    }
    if (isRightPressedCrush) {
        dataManipulator[4] = 1;
    }
    if (!isLeftPressedCrush && !isRightPressedCrush) dataManipulator[4] = 0;
}

setInterval(checkPressedButtonsCrush, 100);


// Powrót do home
document.getElementById('homeManipButton').addEventListener('click', function() {
    for (var i = 0; i < dataManipulator.length; i++) dataManipulator[i] = 3;
    send_data_manipulator();
    for (var i = 0; i < dataManipulator.length; i++) dataManipulator[i] = 0;
});