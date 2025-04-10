<template>
  <v-app>
    <v-app-bar flat>
      <v-app-bar-title class="ml-10">AI Interview Helper</v-app-bar-title>

      <div v-for="item in nav">
        <button class="mr-10" @click="router.push(`/${item.url}`)">
          {{ item.name }}
        </button>
      </div>

      <button
        v-if="!loggedIn"
        class="mr-10 text-black decoration-none"
        @click="router.push('/login')"
      >
        Login
      </button>
      <button v-else class="mr-10 text-black no-underline" @click="handleLogout">
        Logout
      </button>
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

<script setup>
import { ref } from "vue";
import { useLoginStore } from "~/stores/loginStore";

const loggedIn = ref(false);
const loginStore = useLoginStore();
const router = useRouter();

const nav = ref([
  {
    name: "Dashboard",
    url: "",
  },
  {
    name: "History",
    url: "history",
  },
]);

onMounted(async () => {
  const cookieValue = useCookie("user_id").value;
  if (!cookieValue) {
    router.push("/login");
  } else {
    loggedIn.value = true;
  }
});

const handleLogout = async () => {
  try {
    await loginStore.logout();
  } catch (err) {
    console.log(err);
  }
};
</script>

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
