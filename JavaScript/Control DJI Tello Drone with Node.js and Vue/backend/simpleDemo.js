const dgram = require('dgram');
const wait = require('waait');
const commandDelays = require('./commandDelays');

// Method for handling errors
function handleError(err) {
    if (err) {
        console.log('Error: ' + err);
    }
}

// Create Socket for sending data to the drone
const PORT = 8889;
const HOST = '192.168.10.1';
const drone = dgram.createSocket('udp4');
drone.bind(PORT);

// Get messages from drone
drone.on('message', message => {
    console.log(`Message : ${message}`);
});

// Execute fixed set of commands
const commands = ['command', 'battery?', 'takeoff', 'left 50', 'land'];

let i = 0;

async function go() {
  const command = commands[i];
  const delay = commandDelays[command.split(' ')[0]];
  console.log(`running command: ${command}`);
  drone.send(command, 0, command.length, PORT, HOST, handleError);
  await wait(delay);
  i += 1;
  if (i < commands.length) {
    return go();
  }
  console.log('done!');
}

go();