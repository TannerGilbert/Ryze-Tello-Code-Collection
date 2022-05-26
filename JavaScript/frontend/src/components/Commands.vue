<script>
export default {
  methods: {
    sendCommand: function (command) {
      console.log(`Sending the command ${command}`);
      this.$socketio.emit("command", command);
    },
  },
};
</script>

<template>
  <div>
    <button @click="sendCommand('takeoff')">Takeoff</button>
    <button @click="sendCommand('land')">Land</button>
    <button @click="sendCommand('emergency')">Emergency</button>
    <button @click="sendCommand('ccw 90')">⟲90°</button>
    <button @click="sendCommand('cw 90')">⟳90°</button>

    <button @click="sendCommand('right 50')">Right 50cm</button>
    <button @click="sendCommand('left 50')">Left 50cm</button>
    <button @click="sendCommand('forward 50')">Forward 50cm</button>
    <button @click="sendCommand('back 50')">Back 50cm</button>
    <button @click="sendCommand('up 50')">Up 50cm</button>
    <button @click="sendCommand('down 50')">Down 50cm</button>

    <button @click="sendCommand('flip l')">Flip Left</button>
    <button @click="sendCommand('flip r')">Flip Right</button>
    <button @click="sendCommand('flip f')">Flip Forward</button>
    <button @click="sendCommand('flip b')">Flip Backward</button>
  </div>
</template>
