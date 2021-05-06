const dgram = require('dgram');

// Method to parse State
function parseState(state) {
    return state
      .split(';')
      .map(x => x.split(':'))
      .reduce((data, [key, value]) => {
        data[key] = value;
        return data;
    }, {});
}

// Method for handling errors
function handleError(err) {
    if (err) {
        console.log('Error: ' + err);
    }
}

// Initializing drone for developer mode
const HOST = '192.168.10.1';
const drone = dgram.createSocket('udp4');
drone.bind(8889);
drone.send('command', 0, 'command'.length, 8889, HOST, handleError);

// Create Socket for getting data from drone
const PORT = 8890;
const droneState = dgram.createSocket('udp4');
droneState.bind(PORT);

// Get messages from drone
droneState.on('message', message => {
    console.log(`Message : ${JSON.stringify(parseState(message.toString()))}`);
})