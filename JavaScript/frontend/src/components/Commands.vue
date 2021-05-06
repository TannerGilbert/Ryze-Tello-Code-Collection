<template>
    <div>
        <button v-on:click="sendCommand('takeoff')">Takeoff</button>
        <button v-on:click="sendCommand('land')">Land</button>
        <button v-on:click="sendCommand('emergency')">Emergency</button>
        <button v-on:click="sendCommand('ccw 90')">⟲90°</button>
        <button v-on:click="sendCommand('cw 90')">⟳90°</button>

        <button v-on:click="sendCommand('right 50')">Right 50cm</button>
        <button v-on:click="sendCommand('left 50')">Left 50cm</button>
        <button v-on:click="sendCommand('forward 50')">Forward 50cm</button>
        <button v-on:click="sendCommand('back 50')">Back 50cm</button>
        <button v-on:click="sendCommand('up 50')">Up 50cm</button>
        <button v-on:click="sendCommand('down 50')">Down 50cm</button>

        <button v-on:click="sendCommand('flip l')">Flip Left</button>
        <button v-on:click="sendCommand('flip r')">Flip Right</button>
        <button v-on:click="sendCommand('flip f')">Flip Forward</button>
        <button v-on:click="sendCommand('flip b')">Flip Backward</button>
    </div>
</template>

<script>
import socket from '../../socket';

export default {
    name: 'Commands',
    methods: {
        sendCommand: function(command) {
            console.log(`Sending the command ${command}`);
            socket.emit('command', command)
        }
    }
}
</script>