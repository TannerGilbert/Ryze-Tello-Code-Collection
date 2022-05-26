<script>
import Commands from "./components/Commands.vue";
import DroneState from "./components/DroneState.vue";

export default {
  components: {
    Commands,
    DroneState,
  },
};
</script>

<template>
  <div>
    <h1>Ryze Tello Drone Control</h1>
    <Commands />
    <DroneState />
  </div>
</template>

<style>
@import "./assets/base.css";

#app {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;

  font-weight: normal;
}
</style>
