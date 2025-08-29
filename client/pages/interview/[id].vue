<template>
  <div v-if="pageLoading" class="d-flex justify-center items-center my-15">
    <v-progress-circular color="blue-lighten-3" indeterminate :size="68" :width="7" />
  </div>
  <div v-else>
    <v-sheet class="d-flex justify-center mt-10">
      <div class="d-flex flex-wrap justify-center w-75">
        <div
          v-for="(question, index) in localQuestions"
          :key="index"
          class="mx-1 my-2 border py-1 pa-3 rounded-xl cursor-pointer"
          :class="`bg-${getChipColor(index)}`"
          outlined
          pill
          @click="changeQuestion(index)"
        >
          Question #{{ index + 1 }}
        </div>
      </div>
    </v-sheet>
    <v-container
      fill-height
      class="d-flex justify-center align-center"
      style="height: 85vh"
    >
      <v-card width="1200" height="600" class="pa-5 d-flex always-opaque" variant="plain">
        <!-- Left Main Section: Record & Pause Buttons -->
        <v-sheet width="20%" class="pa-5 d-flex flex-column align-center">
          <v-btn color="red" class="mb-3" size="default" elevation="5"
            ><v-icon @click="startListening" icon="mdi-microphone"></v-icon
          ></v-btn>
          <v-btn color="red" class="mb-3" size="default" elevation="5"
            ><v-icon @click="stopListening" icon="mdi-square"></v-icon
          ></v-btn>
          <h4>Answer this question</h4>
        </v-sheet>

        <v-divider vertical></v-divider>

        <!-- Right Half: Scrollable Interview Details -->
        <v-sheet
          width="80%"
          class="pa-5 hide-scroll"
          style="max-height: 550px; overflow-y: auto"
        >
          <div class="d-flex justify-center align-center">
            <v-card-title class="text-h6"
              >Question {{ currentQuestion + 1 }}:</v-card-title
            >
            <v-icon @click="startSpeaking" icon="mdi-volume-high"></v-icon>
          </div>
          <v-card-text class="text-body-1">{{
            localQuestions[currentQuestion].questionText
          }}</v-card-text>

          <v-divider class="my-3"></v-divider>

          <div
            v-if="
              localQuestions.length > 0 &&
              localQuestions[currentQuestion].answered == false
            "
          >
            <v-textarea :loading="userAnswerLoading" v-model="userAnswer"></v-textarea>
            <v-btn :loading="userAnswerLoading" @click="submitUserAnswer">Continue</v-btn>
          </div>
          <div v-else>
            <v-list>
              <v-list-item>
                <v-list-item-title class="font-weight-medium text-body-1">
                  Overall Performance:
                </v-list-item-title>
                <v-progress-linear
                  :model-value="
                    getProgressValue(localQuestions[currentQuestion].overallAssessment)
                  "
                  :color="
                    getProgressColor(localQuestions[currentQuestion].overallAssessment)
                  "
                  height="35"
                >
                  <template v-slot:default>
                    <strong>{{
                      localQuestions[currentQuestion].overallAssessment
                    }}</strong>
                  </template>
                </v-progress-linear>
              </v-list-item>

              <v-list-item>
                <v-expansion-panels>
                  <v-expansion-panel collapse-icon="mdi-minus" expand-icon="mdi-plus">
                    <v-expansion-panel-title class="font-weight-bold"
                      >Your answer</v-expansion-panel-title
                    >
                    <v-expansion-panel-text>{{
                      localQuestions[currentQuestion].userAnswer
                    }}</v-expansion-panel-text>
                  </v-expansion-panel>
                </v-expansion-panels>
              </v-list-item>

              <v-list-item>
                <v-expansion-panels>
                  <v-expansion-panel collapse-icon="mdi-minus" expand-icon="mdi-plus">
                    <v-expansion-panel-title class="font-weight-bold"
                      >Quality of Answer</v-expansion-panel-title
                    >
                    <v-expansion-panel-text>{{
                      localQuestions[currentQuestion].qualityOfAnswer
                    }}</v-expansion-panel-text>
                  </v-expansion-panel>
                </v-expansion-panels>
              </v-list-item>

              <v-list-item>
                <v-expansion-panels>
                  <v-expansion-panel collapse-icon="mdi-minus" expand-icon="mdi-plus">
                    <v-expansion-panel-title class="font-weight-bold"
                      >Grammar & Vocabulary</v-expansion-panel-title
                    >
                    <v-expansion-panel-text>{{
                      localQuestions[currentQuestion].grammarAndVocabulary
                    }}</v-expansion-panel-text>
                  </v-expansion-panel>
                </v-expansion-panels>
              </v-list-item>

              <v-list-item>
                <v-expansion-panels>
                  <v-expansion-panel collapse-icon="mdi-minus" expand-icon="mdi-plus">
                    <v-expansion-panel-title class="font-weight-bold"
                      >Constructive Feedback</v-expansion-panel-title
                    >
                    <v-expansion-panel-text>
                      <div
                        class="formatted-answer"
                        v-html="
                          formatGeminiResponse(
                            localQuestions[currentQuestion].constructiveFeedback
                          )
                        "
                      ></div>
                    </v-expansion-panel-text>
                  </v-expansion-panel>
                </v-expansion-panels>
              </v-list-item>

              <v-list-item>
                <v-expansion-panels>
                  <v-expansion-panel collapse-icon="mdi-minus" expand-icon="mdi-plus">
                    <v-expansion-panel-title class="font-weight-bold"
                      >Suggested Answer</v-expansion-panel-title
                    >
                    <v-expansion-panel-text>
                      <div
                        class="formatted-answer"
                        v-html="
                          formatGeminiResponse(
                            localQuestions[currentQuestion].suggestedAnswer
                          )
                        "
                      ></div>
                    </v-expansion-panel-text>
                  </v-expansion-panel>
                </v-expansion-panels>
              </v-list-item>
            </v-list>
          </div>
        </v-sheet>
      </v-card>
    </v-container>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useQuestionsStore } from "~/stores/questionsStore";

const questionsStore = useQuestionsStore();
const localQuestions = ref([]);
const currentQuestion = ref(0);
const userAnswer = ref("");
const userAnswerLoading = ref(false);
const route = useRoute();
const pageLoading = ref(true);
const router = useRouter();
let recognition = null;

const changeQuestion = (index) => {
  currentQuestion.value = index;
};

const getChipColor = (index) => {
  if (index === currentQuestion.value) {
    return localQuestions.value[index].answered ? "green-darken-2" : "blue";
  }
  return localQuestions.value[index].answered ? "green" : "";
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
  const interviewId = route.params.id;
  const question = localQuestions.value[currentQuestion.value];

  userAnswerLoading.value = true;
  await questionsStore.evaluateAnswer(question, userAnswer.value, interviewId);
  userAnswer.value = "";

  userAnswerLoading.value = false;

  try {
    const interview = await questionsStore.getInterviewDetails(route.params.id);
    localQuestions.value = interview.questions;
    currentQuestion.value = interview.nextQuestion.questionNumber - 1;
  } catch (err) {
    console.log(err);
  }
};

onMounted(async () => {
  const cookieValue = useCookie("user_id").value;
  if (!cookieValue) {
    router.push("/login");
  }
  try {
    const interview = await questionsStore.getInterviewDetails(route.params.id);
    localQuestions.value = interview.questions;
    currentQuestion.value = interview.nextQuestion.questionNumber - 1;
  } catch (error) {
    console.error("Error loading interview:", error);
  } finally {
    pageLoading.value = false;
  }
});

const startListening = () => {
  if (!window.SpeechRecognition && !window.webkitSpeechRecognition) {
    alert("Speech Recognition is not supported in this browser.");
    return;
  }

  recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
  recognition.continuous = true;
  recognition.interimResults = false;
  recognition.lang = "en-US";

  console.log(recognition);

  recognition.onresult = (event) => {
    console.log(event.results[event.results.length - 1][0].transcript);

    userAnswer.value =
      userAnswer.value + event.results[event.results.length - 1][0].transcript;
  };

  recognition.onerror = (event) => {
    console.error("Speech Recognition Error:", event.error);
  };

  recognition.start();
};

const stopListening = () => {
  if (recognition) recognition.stop();
};

const startSpeaking = () => {
  console.log("speaking");
  const utterance = new SpeechSynthesisUtterance(
    localQuestions.value[currentQuestion.value].questionText
  );
  speechSynthesis.speak(utterance);
};

function formatGeminiResponse(rawText) {
  // Remove markdown asterisks used for bold (**) or list markers (*)
  let cleanText = rawText
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>") // bold text
    .replace(/^\s*\*\s*/gm, "") // remove leading * from bullet points
    .replace(/`/g, ""); // remove backticks from code

  // Split by line breaks to identify paragraphs
  const lines = cleanText.split("\n");

  // Build HTML output
  let html = "";
  lines.forEach((line) => {
    if (line.trim() === "") {
      html += "<br>"; // add a line break between paragraphs
    } else if (/^[-–•]\s/.test(line)) {
      html += `<li>${line.replace(/^[-–•]\s/, "")}</li>`;
    } else {
      html += `<p>${line.trim()}</p>`;
    }
  });

  // Wrap list items in <ul> if any <li> is present
  if (html.includes("<li>")) {
    html = html.replace(/(<li>.*<\/li>)/gs, "<ul>$1</ul>");
  }

  return html;
}
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

.always-opaque {
  opacity: 1 !important;
}

.formatted-answer {
  padding: 8px;
  line-height: 1.6;
  white-space: normal;
  word-break: break-word;
}
</style>
