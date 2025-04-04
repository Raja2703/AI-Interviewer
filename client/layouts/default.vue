<script setup lang="ts">
import GoogleButton from "~/components/GoogleButton.vue";
</script>

<template>
  <v-app>
    <v-app-bar flat>
      <v-app-bar-title class="ml-10">AI Interview Helper</v-app-bar-title>
      <RouterLink class="mr-10 text-black no-underline" to="/history">History</RouterLink>
      <button class="mr-10">Dashboard</button>
      <button class="mr-10">Account</button>
      <RouterLink class="mr-10 text-black no-underline" to="/login">Login</RouterLink>
    </v-app-bar>
    <v-main>
      <div class="five-color-line"></div>
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
        <a target="_blank" class="text-white text-decoration-none">Monikashri</a>
      </span>
    </v-footer>
  </v-app>
</template>

<style>
.five-color-line {
  width: 100%;
  height: 5px;
  background: repeating-linear-gradient(
    to right,
    orange 0%,
    orange 20%,
    red 20%,
    red 40%,
    green 40%,
    green 60%,
    lightgreen 60%,
    lightgreen 80%,
    yellow 80%,
    yellow 100%
  );
}
</style>
