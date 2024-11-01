<template>
  <div class="container">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
body {
  background-color: blue;
  margin: 0; 
}

.container {
  max-width: 480px; 
  margin: 0 auto; 
  padding: 16px;
  background-color: white; 
}
</style>
