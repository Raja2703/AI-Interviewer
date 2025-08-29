<template>
  <div class="p-4">
    <h1 class="text-xl font-bold mb-4">Vue 3 Audio Recorder</h1>

    <button
      @click="startRecording"
      :disabled="isRecording"
      class="px-4 py-2 bg-green-500 text-black rounded mr-2"
    >
      Start Recording
    </button>

    <button
      @click="stopRecording"
      :disabled="!isRecording"
      class="px-4 py-2 bg-red-500 text-black rounded"
    >
      Stop Recording
    </button>

    <div v-if="audioURL" class="mt-4">
      <h2 class="font-semibold">Playback</h2>
      <audio :src="audioURL" controls class="mt-2"></audio>
      <a
        :href="audioURL"
        download="recording.wav"
        class="block mt-2 text-blue-500 underline"
      >
        Download WAV
      </a>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const mediaRecorder = ref(null);
const audioChunks = ref([]);
const audioURL = ref("");
const isRecording = ref(false);

const startRecording = async () => {
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    alert("Your browser does not support audio recording.");
    return;
  }

  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    audioChunks.value = [];

    mediaRecorder.value = new MediaRecorder(stream);

    mediaRecorder.value.ondataavailable = (e) => {
      if (e.data.size > 0) {
        audioChunks.value.push(e.data);
      }
    };

    mediaRecorder.value.onstop = () => {
      const audioBlob = new Blob(audioChunks.value, { type: "audio/wav" });
      audioURL.value = URL.createObjectURL(audioBlob);
    };

    mediaRecorder.value.start();
    isRecording.value = true;
    console.log("Recording started");
  } catch (err) {
    console.error("Error accessing microphone:", err);
  }
};

const stopRecording = () => {
  if (mediaRecorder.value && isRecording.value) {
    mediaRecorder.value.stop();
    isRecording.value = false;
    console.log("Recording stopped");

    mediaRecorder.value.onstop = () => {
      const audioBlob = new Blob(audioChunks.value, { type: "audio/wav" });
      audioURL.value = URL.createObjectURL(audioBlob);

      // Send the audioBlob to the backend after stopping
      sendAudioToBackend(audioBlob);
    };
  }
};

const sendAudioToBackend = async (audioBlob) => {
  const formData = new FormData();
  formData.append("file", audioBlob, "audio.wav");

  try {
    const response = await fetch("http://localhost:8000/transcribe", {
      method: "POST",
      body: formData,
    });

    const result = await response.json();
    console.log("Transcription:", result.text);
    alert(`Transcription: ${result.text}`);
  } catch (error) {
    console.error("Error sending audio:", error);
  }
};
</script>

<style scoped>
button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
