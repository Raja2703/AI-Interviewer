<template>
  <v-container
    fill-height
    class="d-flex justify-center align-center"
    style="height: 85vh"
  >
    <v-card width="1200" height="600" class="pa-5 d-flex">
      <v-sheet
        width="10%"
        class="pa-3 d-flex flex-column align-center hide-scroll"
        style="
          max-height: 550px;
          overflow-y: auto;
          border-right: 1px solid #ddd;
        "
      >
        <v-chip
          v-for="(q, index) in questions"
          :key="index"
          :color="q.answered ? 'green' : 'grey'"
          class="mb-10"
        >
          Question #{{ index + 1 }}
        </v-chip>
      </v-sheet>

      <!-- Left Main Section: Record & Pause Buttons -->
      <v-sheet width="30%" class="pa-5 d-flex flex-column align-center">
        <v-btn color="red" class="mb-3" size="x-large" elevation="5"
          >Record</v-btn
        >
        <v-btn color="grey" size="small" elevation="2">Pause</v-btn>
      </v-sheet>

      <v-divider vertical></v-divider>

      <!-- Right Half: Scrollable Interview Details -->
      <v-sheet
        width="60%"
        class="pa-5 hide-scroll"
        style="max-height: 550px; overflow-y: auto"
      >
        <v-card-title class="text-h6">Question</v-card-title>
        <v-card-text
          >"Describe a time you solved a complex problem at work."</v-card-text
        >

        <v-divider class="my-3"></v-divider>

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
              >Lorem ipsum dolor sit amet, consectetur adipiscing
              elit.</v-card-text
            >
          </v-list-item>

          <v-list-item>
            <v-list-item-title class="font-weight-bold"
              >Grammar & Vocabulary:</v-list-item-title
            >
            <v-card-text
              >Lorem ipsum dolor sit amet, consectetur adipiscing
              elit.</v-card-text
            >
          </v-list-item>

          <v-list-item>
            <v-list-item-title class="font-weight-bold"
              >Constructive Feedback:</v-list-item-title
            >
            <v-card-text
              >Try to provide more concrete examples with clear
              reasoning.</v-card-text
            >
          </v-list-item>

          <v-list-item>
            <v-list-item-title class="font-weight-bold"
              >Suggested Answer:</v-list-item-title
            >
            <v-card-text
              >"During a project deadline crunch, I identified a bottleneck in
              our workflow..."</v-card-text
            >
          </v-list-item>
        </v-list>
      </v-sheet>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from "vue";

const questions = ref([
  { answered: true },
  { answered: false },
  { answered: true },
  { answered: false },
  { answered: false },
]);
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
