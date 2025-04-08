<template>
  <div class="d-flex h-screen w-screen justify-center align-center">
    <div class="d-flex flex-sm-column w-33 border-md border-black pa-5 ga-sm-2">
      <div class="text-h5">Username</div>
      <v-text-field
        required
        label="rollno"
        variant="outlined"
        v-model="username"
        :error-messages="error"
      ></v-text-field>
      <div class="text-h5">Password</div>
      <v-text-field
        required
        label="password"
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

const router = useRouter();
const loginStore = useLoginStore();

const username = ref("");
const password = ref("");
const error = ref("");

onMounted(() => {
  const cookieValue = useCookie("user_id").value;
  if (cookieValue) {
    router.push("/");
  }
});

const handleLogin = async () => {
  const user = {
    username: username.value,
    password: password.value,
  };

  try {
    const data = await loginStore.login(user);

    if (data.data["status"] == "success") {
      router.push("/");
    } else {
      error.value = data.data["message"];
    }
  } catch (err) {
    console.log(err);
  }
};
</script>
