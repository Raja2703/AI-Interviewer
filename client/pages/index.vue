<template>
  <v-container
    fill-height
    class="d-flex justify-center align-center"
    style="height: 100vh"
  >
    <v-card width="800" height="600" class="pa-5 text-center">
      <v-card-title>Start Your Interview Now!</v-card-title>
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
        height="200"
        v-model="jobDescription"
      ></v-textarea>
      <v-row justify="center" class="mt-4">
        <!-- <v-btn variant="outlined" class="mb-2">Upload Resume</v-btn> -->
        <v-file-input
          label="Upload your resume"
          variant="solo"
          density="comfortable"
        ></v-file-input>
        <v-btn variant="flat" color="primary">Start Mock Interview</v-btn>
      </v-row>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, computed } from "vue";

const jobRoles = {
  "Custom Job Description": "Enter a custom job description.",
  "Software Engineer":
    "Responsible for developing, testing, and maintaining software applications.",
  "Data Scientist":
    "Analyzes data to extract insights and build predictive models.",
  "Product Manager":
    "Oversees product development and ensures alignment with business goals.",
  "UI/UX Designer": "Designs user interfaces and enhances user experiences.",
  "DevOps Engineer": "Manages CI/CD pipelines and cloud infrastructure.",
  "Machine Learning Engineer":
    "Develops AI models and optimizes ML algorithms.",
  "Backend Developer":
    "Builds server-side logic and database management systems.",
  "Frontend Developer": "Creates interactive and responsive web applications.",
  "Cybersecurity Analyst": "Protects systems and networks from cyber threats.",
  "Cloud Engineer": "Designs and manages cloud computing environments.",
};

const selectedRole = ref("Custom Job Description");

const jobDescription = computed(() => jobRoles[selectedRole.value] || "");
</script>
