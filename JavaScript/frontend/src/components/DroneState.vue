<script>
export default {
  data: function () {
    return {
      status: "Disconnected",
      droneState: "",
    };
  },
  mounted() {
    // react when a status or dronestate message is received
    this.$socketio.on("status", (status) => {
      this.status = status;
    });
    this.$socketio.on("dronestate", (droneState) => {
      this.droneState = droneState;
    });
  },
};
</script>

<template>
  <div>
    <p>Status: {{ status }}</p>

    <div id="droneState">
      <p>Battery: {{ droneState.bat }}</p>
      <p>Pitch: {{ droneState.pitch }}</p>
      <p>Roll: {{ droneState.roll }}</p>
      <p>Yaw: {{ droneState.yaw }}</p>
      <p>Height: {{ droneState.h }}</p>
    </div>
  </div>
</template>
