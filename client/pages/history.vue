<template>
  <v-navigation-drawer :width="280" class="border">
    <v-list-item class="text-h5 py-4">Interview History</v-list-item>
    <v-divider></v-divider>
    <v-list-item v-for="(history, index) in historyOfUser" link class="py-3 px-5 text-h6"
      >List item 1</v-list-item
    >
  </v-navigation-drawer>
  <template>
    <v-sheet>
      <v-chip-group class="d-flex">
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
    <v-container fill-height class="d-flex" style="margin: 0">
      <v-card width="1200" height="600" class="pa-5 d-flex" variant="plain">
        <v-sheet
          width="60%"
          class="pa-5 hide-scroll"
          style="max-height: 550px; overflow-y: auto"
        >
          <!-- <v-card-title class="text-h6 m-0 pa-0">Question {{ currentQuestion + 1 }}:</v-card-title> -->
          <v-card-title class="text-h4 m-0 pa-0">Question 1:</v-card-title>
          <!-- <v-card-text class="text-h5">{{ questions[currentQuestion].questionText }}</v-card-text> -->
          <div class="text-h5">Question goes here</div>

          <v-divider class="my-3"></v-divider>

          <!-- <div
            v-if="questions.length > 0 && questions[currentQuestion].answered == false"
          >
            <v-textarea :loading="userAnswerLoading" v-model="userAnswer"></v-textarea>
            <v-btn :loading="userAnswerLoading" @click="submitUserAnswer">Continue</v-btn>
          </div> -->
          <div>
            <v-list>
              <v-list-item>
                <v-list-item-title class="font-weight-bold text-h5">
                  Overall Performance:
                </v-list-item-title>
                <v-progress-linear height="25">
                  <template v-slot:default>
                    <!-- <strong>{{
                      questions[currentQuestion].feedback.overallAssessment
                    }}</strong> -->
                    adwad
                  </template>
                </v-progress-linear>
              </v-list-item>

              <v-list-item>
                <v-list-item-title class="font-weight-bold text-h5"
                  >Your Answer:</v-list-item-title
                >
                <!-- <v-card-text class="text-h6 pa-0 py-1">{{ questions[currentQuestion].userAnswer }}</v-card-text> -->
                <v-card-text class="text-h6 pa-0 py-1">User answer</v-card-text>
              </v-list-item>

              <v-list-item>
                <v-list-item-title class="font-weight-bold text-h5"
                  >Quality of Answer:</v-list-item-title
                >
                <!-- <v-card-text class="text-h6">{{
                  questions[currentQuestion].feedback.qualityOfAnswer
                }}</v-card-text> -->
                wadw
              </v-list-item>

              <v-list-item>
                <v-list-item-title class="font-weight-bold text-h5"
                  >Grammar & Vocabulary:</v-list-item-title
                >
                <!-- <v-card-text class="text-h6">{{
                  questions[currentQuestion].feedback.grammarAndVocabulary
                }}</v-card-text> -->
                awdwa
              </v-list-item>

              <v-list-item>
                <v-list-item-title class="font-weight-bold text-h5"
                  >Constructive Feedback:</v-list-item-title
                >
                <!-- <v-card-text class="text-h6">{{
                  questions[currentQuestion].feedback.constructiveFeedback
                }}</v-card-text> -->
                wadwad
              </v-list-item>

              <v-list-item>
                <v-list-item-title class="font-weight-bold text-h5"
                  >Suggested Answer:</v-list-item-title
                >
                <!-- <v-card-text class="text-h6">{{
                  questions[currentQuestion].feedback.suggestedAnswer
                }}</v-card-text> -->
                wadwd
              </v-list-item>
            </v-list>
          </div>
        </v-sheet>
      </v-card>
    </v-container>
  </template>
</template>

<script setup>
import { ref } from "vue";
import { useQuestionsStore } from "~/stores/questionsStore";

const questionsStore = useQuestionsStore();
const questions = ref([]);
const currentQuestion = ref(0);
const userAnswer = ref("");
const userAnswerLoading = ref(false);
const historyOfUser = ref([{ id: 1 }, { id: 2 }]);

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
