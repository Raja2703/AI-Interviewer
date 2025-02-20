<script setup lang="ts">
import GoogleButton from "~/components/GoogleButton.vue";
</script>

<template>
  <v-app>
    <v-app-bar>
      <v-app-bar-title class="ml-10">AI Interview Helper</v-app-bar-title>
      <button class="mr-10">Dashboard</button>
      <button class="mr-10">Account</button>
      <GoogleButton class="mr-10" />
    </v-app-bar>
    <v-main>
      <slot />
    </v-main>
    <v-footer
      app
      class="d-flex justify-space-between bg-grey-darken-3 text-white px-4 py-3"
    >
      <span>&copy; {{ new Date().getFullYear() }} AI Interview Helper</span>

      <span>
        Developed by
        <a target="_blank" class="text-white text-decoration-none">Shazz</a>
        ,
        <a target="_blank" class="text-white text-decoration-none">Raja</a>
        &
        <a target="_blank" class="text-white text-decoration-none"
          >Monikashri</a
        >
      </span>
    </v-footer>
  </v-app>
</template>
