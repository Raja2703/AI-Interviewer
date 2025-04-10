<template>
  <div class="background-soft">
    <v-container fill-height class="d-flex justify-center align-center">
      <div class="custom-border">
        <v-card
          :loading="isLoading"
          max-width="600"
          min-height="400"
          class="pa-5 text-center"
        >
          <div class="font-weight-black text-h5">
            Start Your Interview Now! <v-icon></v-icon>
          </div>
          <div>etc...</div>
          <v-sheet outlined class="pa-3 mt-4">
            <v-chip-group column>
              <v-chip
                v-for="(desc, role) in jobRoles"
                :key="role"
                class="ma-1"
                outlined
                @click="selectedRole = role"
                :color="selectedRole === role ? 'primary' : ''"
              >
                {{ role }}
              </v-chip>
            </v-chip-group>
          </v-sheet>
          <v-textarea
            variant="outlined"
            label="Job Description"
            min-height="600"
            v-model="jobDescription"
            flat
            :disabled="isLoading"
          ></v-textarea>
          <v-row justify="center" class="mt-4">
            <v-slider
              v-model="yearsOfExperience"
              :disabled="isLoading"
              min="0"
              max="20"
              step="1"
              color="teal-darken-4"
              :label="'Years of Experience: ' + yearsOfExperience"
              thumb-size="12"
              thumb-color="blue"
            >
            </v-slider>
            <v-col cols="12">
              <div class="mb-4">upload your resume here</div>
              <v-file-input
                v-model="uploadedResume"
                :disabled="isLoading"
                flat
                chips
                variant="outlined"
                base-color="green"
                bg-color="teal-lighten-5"
                prepend-icon="mdi-file"
                density="comfortable"
              ></v-file-input>
              <div class="text-h6">OR</div>
            </v-col>
            <div>get questions from a book</div>
            <v-col cols="12">
              <v-file-input
                v-model="uploadedBook"
                :disabled="isLoading"
                flat
                chips
                variant="outlined"
                base-color="green"
                bg-color="teal-lighten-5"
                prepend-icon="mdi-file"
                density="comfortable"
              ></v-file-input>
            </v-col>
            <span v-if="error" class="text-red-lighten-1 mt-4"
              ><v-icon icon="mdi-information"></v-icon>{{ error }}</span
            >
            <v-col cols="12">
              <v-btn
                :loading="isPdfUploading"
                variant="flat"
                rounded="xl"
                class="text"
                color="primary"
                @click="submitForm"
                >Start your Interview</v-btn
              >
            </v-col>
          </v-row>
        </v-card>
      </div>
    </v-container>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useQuestionsStore } from "~/stores/questionsStore";

const selectedRole = ref("Custom Job Description");
const jobDescription = computed(() => jobRoles[selectedRole.value] || "");
const uploadedResume = ref(null);
const uploadedBook = ref(null);
const yearsOfExperience = ref(0);
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
  if (uploadedResume.value) {
    if (!selectedRole.value || !jobDescription.value || !uploadedResume.value) {
      error.value = "Please fill all the fields";
      return;
    }

    isLoading.value = true;
    isPdfUploading.value = true;

    await questionsStore.uploadFile(uploadedResume.value);
    await questionsStore.fetchKeywords(questionsStore.extracted_text);

    const interview = await questionsStore.generateQuestions(
      questionsStore.keyterms.name,
      selectedRole.value,
      questionsStore.keyterms.skills,
      String(yearsOfExperience.value)
    );

    isPdfUploading.value = false;

    if (questionsStore.questions.length) {
      router.push(`/interview/${interview.id}`);
    } else {
      error.value = "No questions generated";
    }
    isLoading.value = false;
  } else if (uploadedBook.value) {
    isPdfUploading.value = true;
    const interview = await questionsStore.generateQuestionsFromBook(uploadedBook.value);
    isPdfUploading.value = false;

    if (questionsStore.questions.length) {
      router.push(`/interview/${interview.id}`);
    } else {
      error.value = "No questions generated";
    }
  } else {
    error.value = "Please upload resume or a book";
  }
};
</script>

<style scoped>
.custom-border {
  border-right: 7px dashed lightseagreen;
  border-bottom: 7px dashed lightseagreen;
  border-radius: 15px;
}
.background-soft {
  background-color: rgb(217, 241, 241);
}
</style>
