<template>
  <div v-if="loading" class="d-flex justify-center w-screen mt-15">
    <tr>
      <v-progress-circular color="blue-lighten-3" indeterminate :size="48" :width="6" />
    </tr>
  </div>
  <div v-else class="d-flex justify-center mt-10 mb-15">
    <v-table class="w-75" fixed-header>
      <thead>
        <tr class="text-h6">
          <th class="text-left">Date</th>
          <th class="text-left">Name</th>
          <th class="text-left">Completed</th>
          <th class="text-center">See interview</th>
        </tr>
      </thead>
      <tbody v-if="interviews.values" class="text-center">
        <tr class="text-subtitle-1" v-for="interview in interviews" :key="interview.id">
          <td>{{ formatDateText(interview.created_at) }}</td>
          <td>{{ interview.id }}</td>
          <td>{{ interview.isCompleted ? "Yes" : "No" }}</td>
          <td class="py-3 text-center">
            <v-btn
              icon="mdi-location-enter"
              @click="takeToInterview(interview.id)"
            ></v-btn>
          </td>
        </tr>
      </tbody>
      <tbody v-else class="text-center">
        <tr class="text-subtitle-1">
          <td colspan="4">No interviews found.</td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useQuestionsStore } from "~/stores/questionsStore";
import { formatDateText } from "~/utils/formatDate";

const router = useRouter();
const questionsStore = useQuestionsStore();
const interviews = ref(false);
const loading = ref(true);

onMounted(async () => {
  const cookieValue = useCookie("user_id").value;
  if (!cookieValue) {
    router.push("/login");
  }

  try {
    let response = await questionsStore.getAllInterviews();
    console.log(response);
    if (response.status != 204) {
      interviews.value = response
    }
    else{
      interviews.value = false
    }
    loading.value = false;
  } catch (err) {
    console.log(err);
  }
});

const takeToInterview = (interviewId) => {
  router.push(`/interview/${interviewId}`);
};
</script>
