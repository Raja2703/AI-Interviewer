<template>
  <v-app>
    <v-app-bar class="border" flat>
      <v-app-bar-title class="ml-10 text-blue text-h5"
        >AI Interview Helper</v-app-bar-title
      >

      <div v-for="item in nav">
        <button
          class="mr-10 text-body-1 underline-animated"
          :class="{
            active: `/${item.url}` === route.path,
          }"
          @click="router.push(`/${item.url}`)"
        >
          {{ item.name }}
        </button>
      </div>

      <button
        v-if="!loggedIn"
        class="mr-10 text-black decoration-none text-body-1"
        @click="router.push('/login')"
      >
        Login
      </button>
      <button
        v-else
        class="mr-10 text-black no-underline text-body-1"
        @click="handleLogout"
      >
        Logout
      </button>
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
const route = useRoute();

const nav = ref([
  {
    name: "Dashboard",
    url: "",
  },
  {
    name: "Master a book",
    url: "book",
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
.underline-animated {
  position: relative;
  text-decoration: none;
}

.underline-animated::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: -2px; /* distance from text */
  width: 100%;
  height: 2px;
  background-color: blue;
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.3s ease;
}

.underline-animated.active::after {
  transform: scaleX(1);
}
</style>
