<template>
  <div class="mt-10 w-100 d-flex flex-column justify-center align-center">
    <div class="w-50 custom-border d-flex flex-column justify-center align-center py-10">
      <div class="text-h5 text-center">Get questions from a book</div>
      <div class="text-body-1 text-center mt-10">Upload a book here</div>
      <v-col cols="10" class="">
        <v-file-input
          v-model="uploadedBook"
          :disabled="isLoading"
          flat
          chips
          variant="outlined"
          base-color="blue"
          bg-color="teal-lighten-5"
          prepend-icon="mdi-file"
          density="comfortable"
        ></v-file-input>
      </v-col>

      <v-col cols="12" class="d-flex justify-center">
        <v-btn
          :loading="isPdfUploading"
          variant="flat"
          rounded="xl"
          class="text"
          color="blue"
          @click="submitForm"
          >Get questions</v-btn
        >
      </v-col>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useQuestionsStore } from "~/stores/questionsStore";

const uploadedBook = ref(null);
const error = ref(null);
const questionsStore = useQuestionsStore();
const isLoading = ref(false);
const isPdfUploading = ref(false);
const router = useRouter();

onMounted(() => {
  const cookieValue = useCookie("user_id").value;
  if (!cookieValue) {
    router.push("/login");
  }
});

// Submit function
const submitForm = async () => {
  questionsStore.questions = [];

  isPdfUploading.value = true;
  const interview = await questionsStore.generateQuestionsFromBook(uploadedBook.value);
  isPdfUploading.value = false;

  if (questionsStore.questions.length) {
    router.push(`/interview/${interview.id}`);
  } else {
    error.value = "No questions generated";
  }
};
</script>

<style scoped>
.custom-border {
  border: 3px solid rgb(88, 194, 255);
  border-radius: 15px;
}
</style>
