const dgram = require("dgram");
const app = require("express")();
const http = require("http").Server(app);
const io = require("socket.io")(http, {
  cors: {
    origin: "http://localhost:3000",
    methods: ["GET", "POST"],
  },
});
const throttle = require("lodash/throttle");

// Method for handling errors
function handleError(err) {
  if (err) {
    console.log("Error: " + err);
  }
}

// Method to parse State
function parseState(state) {
  return state
    .split(";")
    .map((x) => x.split(":"))
    .reduce((data, [key, value]) => {
      data[key] = value;
      return data;
    }, {});
}

// Create Socket for sending data to the drone
const PORT = 8889;
const HOST = "192.168.10.1";
const drone = dgram.createSocket("udp4");
drone.bind(PORT);

drone.send("command", 0, "command".length, PORT, HOST, handleError);
drone.send("streamon", 0, "streamon".length, PORT, HOST, handleError);

// Get messages from drone and send them to the webpage
drone.on("message", (message) => {
  console.log(`Message : ${message}`);
  io.sockets.emit("status", message.toString());
});

// Create Socket for getting data from drone
const droneState = dgram.createSocket("udp4");
droneState.bind(8890);

// Get status-messages from drone and send them to the webpage
droneState.on(
  "message",
  throttle((state) => {
    const formattedState = parseState(state.toString());
    io.sockets.emit("dronestate", formattedState);
  }, 100)
);

// Set up socket
io.on("connection", (socket) => {
  socket.on("command", (command) => {
    console.log("command Sent from browser");
    console.log(command);
    drone.send(command, 0, command.length, PORT, HOST, handleError);
  });

  socket.emit("status", "CONNECTED");
});

http.listen("8100", () => {
  console.log("Socket.io server running");
});
