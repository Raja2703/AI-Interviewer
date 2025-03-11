<template>
  <v-sheet class="d-flex justify-center mt-10">
    <v-chip-group>
      <v-chip
        v-for="(question, index) in questions"
        :key="index"
        class="ma-1"
        :color="question.answered ? 'green' : 'grey'"
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
        v-if="questions.length > 0 && questions[currentQuestion].answered == false"
        width="60%"
        class="pa-5 hide-scroll"
        style="max-height: 550px; overflow-y: auto"
      >
        <v-card-title class="text-h6">Question:</v-card-title>
        <v-card-text>{{ questions[currentQuestion].questionText }}</v-card-text>

        <v-divider class="my-3"></v-divider>

        <v-textarea v-model="userAnswer"></v-textarea>
        <v-btn @click="submitUserAnswer">Continue</v-btn>
      </v-sheet>
      <v-sheet
        v-else
        width="60%"
        class="pa-5 hide-scroll"
        style="max-height: 550px; overflow-y: auto"
      >
        <v-list>
          <v-list-item>
            <v-list-item-title class="font-weight-bold"
              >Overall Performance:</v-list-item-title
            >
            <v-progress-linear model-value="80" color="blue-grey" height="25">
              <template v-slot:default="{ value }">
                <strong>Good</strong>
              </template>
            </v-progress-linear>
          </v-list-item>

          <v-list-item>
            <v-list-item-title class="font-weight-bold"
              >Quality of Answer:</v-list-item-title
            >
            <v-card-text
              >Lorem ipsum dolor sit amet, consectetur adipiscing elit.</v-card-text
            >
          </v-list-item>

          <v-list-item>
            <v-list-item-title class="font-weight-bold"
              >Grammar & Vocabulary:</v-list-item-title
            >
            <v-card-text
              >Lorem ipsum dolor sit amet, consectetur adipiscing elit.</v-card-text
            >
          </v-list-item>

          <v-list-item>
            <v-list-item-title class="font-weight-bold"
              >Constructive Feedback:</v-list-item-title
            >
            <v-card-text
              >Try to provide more concrete examples with clear reasoning.</v-card-text
            >
          </v-list-item>

          <v-list-item>
            <v-list-item-title class="font-weight-bold"
              >Suggested Answer:</v-list-item-title
            >
            <v-card-text
              >"During a project deadline crunch, I identified a bottleneck in our
              workflow..."</v-card-text
            >
          </v-list-item>
        </v-list>
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

const changeQuestion = (index) => {
  currentQuestion.value = index;
  console.log(currentQuestion.value);
};

const submitUserAnswer = () => {
  questionsStore.evaluateAnswer(currentQuestion.value, userAnswer.value);
  userAnswer.value = "";
  currentQuestion.value += 1;
  console.log(currentQuestion.value);
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
