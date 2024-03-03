var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', function() {
    console.log('Connected to the server');
    try {
        connectIcon.src = '../static/icons/yes.png';
    } catch (error) { console.log(error); }
});

socket.on('disconnect', function() {
    console.log("disconnected to server")

    try {
        connectIcon.src = '../static/icons/delete.png';
    } catch (error) { console.log(error); }
});

socket.on('status_update', function(data) {
    console.log('Status update received:', data);
    if (data.komputer) {
        try {
            connectIcon.src = '../static/icons/yes.png';
        } catch (error) { console.log(error) }
    } else {
        try{
            connectIcon.src = '../static/icons/delete.png';
        } catch (error) { console.log(error) }        
    }
    if (data.mobile) {
        try {
            mobileConnectIcon.src = '../static/icons/yes.png';
        } catch (error) { console.log(error) }
    } else {
        try {
            mobileConnectIcon.src = '../static/icons/delete.png';
        } catch (error) { console.log(error) }
    }
});
