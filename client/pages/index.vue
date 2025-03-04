<template>
  <div class="background-soft">
    <v-container
      fill-height
      class="d-flex justify-center align-center"
      style="height: 100vh"
    >
      <div class="custom-border">
        <v-card max-width="600" min-height="400" class="pa-5 text-center">
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
          ></v-textarea>
          <v-row justify="center" class="mt-4">
            <v-slider
              v-model="yearsOfExperience"
              min="0"
              max="20"
              step="1"
              color="teal-darken-4"
              label="Years of Experience"
              thumb-size="12"
              thumb-color="blue"
            >
              <template v-slot:thumb-label="{ modelValue }">
                <v-icon size="20" color="red">mdi-star</v-icon>
                <!-- Custom Icon -->
              </template>
            </v-slider>
            <v-col cols="12">
              <v-file-input
                v-model="uploadedFile"
                label="Upload your resume"
                flat
                variant="outlined"
                base-color="green"
                bg-color="teal-lighten-5"
                prepend-icon="mdi-file"
                density="comfortable"
                @change="handleResumeUpload"
              ></v-file-input>
            </v-col>
            <v-col cols="12">
              <v-btn
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

const selectedRole = ref("Custom Job Description");
const jobDescription = computed(() => jobRoles[selectedRole.value] || "");
const uploadedFile = ref(null);
const yearsOfExperience = ref(0);

// Handle file upload
const handleResumeUpload = (event) => {
  uploadedFile.value = event;
};

// Submit function
const submitForm = () => {
  console.log("Job Role:", selectedRole.value);
  console.log("Job Description:", jobDescription.value);
  console.log(
    "Uploaded File:",
    uploadedFile.value ? uploadedFile.value.name : "No file uploaded"
  );
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
