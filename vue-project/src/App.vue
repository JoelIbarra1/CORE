<template>
  <div class="app">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App'
};
</script>

<style>
body {
  font-family: Arial, sans-serif;
  margin: 0;
  background: #f0f0f0;
}
.app {
  padding: 2rem;
  max-width: 900px;
  margin: auto;
}
</style>