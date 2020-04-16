import io from 'socket.io-client';

const socket = io('http://localhost:8100');

export default socket;