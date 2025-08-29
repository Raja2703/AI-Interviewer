<template>
  <div class="d-flex h-screen w-screen justify-center align-center">
    <div class="d-flex flex-sm-column w-33 custom-border pa-5 ga-sm-2">
      <div class="text-h5 text-blue">Username</div>
      <v-text-field
        required
        label="Register Number"
        variant="outlined"
        v-model="username"
        :error-messages="error"
      ></v-text-field>
      <div class="text-h5 text-blue">Password</div>
      <v-text-field
        required
        label="Password"
        variant="outlined"
        type="password"
        v-model="password"
        :error-messages="error"
      ></v-text-field>
      <v-btn variant="tonal" @click="handleLogin">login</v-btn>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useLoginStore } from "~/stores/loginStore";
import { useToast } from "vue-toastification";

const router = useRouter();
const route = useRoute();
const loginStore = useLoginStore();
const toast = useToast();

const username = ref("");
const password = ref("");
const error = ref("");

onMounted(() => {
  const cookieValue = useCookie("user_id").value;
  if (cookieValue) {
    router.push("/");
  }

  window.addEventListener("keydown", keydownHandler);
});

onUnmounted(() => {
  window.removeEventListener("keydown", keydownHandler);
});

const keydownHandler = (e) => {
  if (e.key === "Enter" && route.name === "login") {
    handleLogin();
  }
};

const handleLogin = async () => {
  const user = {
    username: username.value,
    password: password.value,
  };

  try {
    const data = await loginStore.login(user);

    if (data.data["status"] == "success") {
      router.push("/");
      toast.success("Logged in successfully");
    } else {
      error.value = data.data["message"];
    }
  } catch (err) {
    console.log(err);
  }
};
</script>

<style scoped>
.custom-border {
  border: 2px solid rgb(42, 122, 168);
  border-radius: 7px;
}
</style>
