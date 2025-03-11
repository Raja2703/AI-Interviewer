<template>
  <v-sheet class="d-flex justify-center mt-10">
    <v-chip-group>
      <v-chip
        v-for="(question, index) in questions"
        :key="index"
        class="ma-1"
        :color="getChipColor(index)"
        outlined
        pill
        @click="changeQuestion(index)"
      >
        Question #{{ index + 1 }}
      </v-chip>
    </v-chip-group>
  </v-sheet>
  <v-container
    fill-height
    class="d-flex justify-center align-center"
    style="height: 85vh"
  >
    <v-card width="1200" height="600" class="pa-5 d-flex" variant="plain">
      <!-- Left Main Section: Record & Pause Buttons -->
      <v-sheet width="30%" class="pa-5 d-flex flex-column align-center">
        <v-btn color="red" class="mb-3" size="x-large" elevation="5"
          ><v-icon icon="mdi-microphone"></v-icon
        ></v-btn>
        <h3>Answer this question</h3>
      </v-sheet>

      <v-divider vertical></v-divider>

      <!-- Right Half: Scrollable Interview Details -->
      <v-sheet
        width="60%"
        class="pa-5 hide-scroll"
        style="max-height: 550px; overflow-y: auto"
      >
        <v-card-title class="text-h6">Question {{ currentQuestion + 1 }}:</v-card-title>
        <v-card-text>{{ questions[currentQuestion].questionText }}</v-card-text>

        <v-divider class="my-3"></v-divider>

        <div v-if="questions.length > 0 && questions[currentQuestion].answered == false">
          <v-textarea :loading="userAnswerLoading" v-model="userAnswer"></v-textarea>
          <v-btn :loading="userAnswerLoading" @click="submitUserAnswer">Continue</v-btn>
        </div>
        <div v-else>
          <v-list>
            <v-list-item>
              <v-list-item-title class="font-weight-bold">
                Overall Performance:
              </v-list-item-title>
              <v-progress-linear
                :model-value="
                  getProgressValue(questions[currentQuestion].feedback.overallAssessment)
                "
                :color="
                  getProgressColor(questions[currentQuestion].feedback.overallAssessment)
                "
                height="25"
              >
                <template v-slot:default>
                  <strong>{{
                    questions[currentQuestion].feedback.overallAssessment
                  }}</strong>
                </template>
              </v-progress-linear>
            </v-list-item>

            <v-list-item>
              <v-list-item-title class="font-weight-bold">Your Answer:</v-list-item-title>
              <v-card-text>{{ questions[currentQuestion].userAnswer }}</v-card-text>
            </v-list-item>

            <v-list-item>
              <v-list-item-title class="font-weight-bold"
                >Quality of Answer:</v-list-item-title
              >
              <v-card-text>{{
                questions[currentQuestion].feedback.qualityOfAnswer
              }}</v-card-text>
            </v-list-item>

            <v-list-item>
              <v-list-item-title class="font-weight-bold"
                >Grammar & Vocabulary:</v-list-item-title
              >
              <v-card-text>{{
                questions[currentQuestion].feedback.grammarAndVocabulary
              }}</v-card-text>
            </v-list-item>

            <v-list-item>
              <v-list-item-title class="font-weight-bold"
                >Constructive Feedback:</v-list-item-title
              >
              <v-card-text>{{
                questions[currentQuestion].feedback.constructiveFeedback
              }}</v-card-text>
            </v-list-item>

            <v-list-item>
              <v-list-item-title class="font-weight-bold"
                >Suggested Answer:</v-list-item-title
              >
              <v-card-text>{{
                questions[currentQuestion].feedback.suggestedAnswer
              }}</v-card-text>
            </v-list-item>
          </v-list>
        </div>
      </v-sheet>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from "vue";
import { useQuestionsStore } from "~/stores/questionsStore";

const questionsStore = useQuestionsStore();
const questions = ref();
const currentQuestion = ref(0);
const userAnswer = ref("");
const userAnswerLoading = ref(false);

const changeQuestion = (index) => {
  currentQuestion.value = index;
};

const getChipColor = (index) => {
  if (index === currentQuestion.value) {
    return questions.value[index].answered ? "light-green" : "blue";
  }
  return questions.value[index].answered ? "green" : "grey";
};

const getProgressValue = (assessment) => {
  switch (assessment) {
    case "Excellent":
      return 100;
    case "Good":
      return 80;
    case "Fair":
      return 50;
    case "Poor":
      return 20;
    default:
      return 0;
  }
};

const getProgressColor = (assessment) => {
  switch (assessment) {
    case "Excellent":
      return "green";
    case "Good":
      return "blue";
    case "Fair":
      return "orange";
    case "Poor":
      return "red";
    default:
      return "grey";
  }
};

const submitUserAnswer = async () => {
  userAnswerLoading.value = true;
  await questionsStore.evaluateAnswer(currentQuestion.value, userAnswer.value);
  userAnswer.value = "";
  // currentQuestion.value += 1;
  questions.value = JSON.parse(localStorage.getItem("generatedQuestions"));
  currentQuestion.value = Number(localStorage.getItem("currentQuestionIndex"));
  console.log("==>", currentQuestion.value);
  userAnswerLoading.value = false;
};

onBeforeMount(() => {
  questions.value = JSON.parse(localStorage.getItem("generatedQuestions"));
  currentQuestion.value = Number(localStorage.getItem("currentQuestionIndex"));
  // console.log(questions.value[currentQuestion]);
  // console.log(currentQuestion);
});
</script>

<style scoped>
/* Hide scrollbar while allowing scrolling */
.hide-scroll {
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* Internet Explorer 11 */
}

.hide-scroll::-webkit-scrollbar {
  display: none; /* Chrome, Safari */
}
</style>
