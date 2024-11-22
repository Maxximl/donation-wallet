<template>
    <div>
      <h1 class="text-4xl font-semibold text-darkBlue mb-4 text-center">
        {{ organization.name }}
      </h1>
      <p class="text-gray-700 text-center">
        {{ organization.description }}
      </p>
    </div>
  </template>
  
  <script setup>
  defineProps({
    organization: {
      type: Object,
      required: true,
    },
  })
  </script>