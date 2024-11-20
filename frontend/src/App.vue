<template>
  <div class="app-container">
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
  background: rgb(2,0,36);
background: linear-gradient(172deg, rgba(2,0,36,1) 0%, rgba(41,41,221,1) 0%, rgba(0,212,255,1) 100%);  
  margin: 0; 
}

.app-container {
  max-width: 480px; 
  margin: 0 auto; 
  padding: 16px;
  background-color: white; 
}
</style>
