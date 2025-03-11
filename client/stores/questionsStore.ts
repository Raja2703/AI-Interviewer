import { defineStore } from "pinia";
import { ref } from "vue";
import axios from "axios";

export const useQuestionsStore = defineStore("questionsStore", () => {
  const questions = ref([]);
  const url = "http://localhost:8000";
  const extracted_text = ref("");
  const keyterms = ref("");
  const curentQuestionIndex = ref(0);

  const uploadFile = async (file: any) => {
    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await axios.post(`${url}/extract_pdf`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      extracted_text.value = response.data;

      return response.data; // Handle response as needed
    } catch (error) {
      console.error("File upload failed:", error);
      throw error;
    }
  };

  const fetchKeywords = async (text: string) => {
    try {
      const response = await axios.post(
        `${url}/llm/extract_key_terms`,
        { retrieved_text: text },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      keyterms.value = response.data;

      return response.data;
    } catch (error) {
      console.error("Failed to fetch keywords:", error);
      throw error;
    }
  };

  const generateQuestions = async (
    name: string,
    jobDescription: string,
    skills: string[],
    experience_years: string
  ) => {
    try {
      const response = await axios.post(
        `${url}/llm/generate_question`,
        {
          name: name,
          career_domain: jobDescription,
          skills: skills,
          experience_years: experience_years,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      const formattedQuestions = response.data["questions"].map((q: any) => ({
        ...q,
        answered: false,
        feedback: {
          overallAssessment: "",
          qualityOfAnswer: "",
          grammarAndVocabulary: "",
          constructiveFeedback: "",
          suggestedAnswer: "",
        },
      }));

      questions.value = formattedQuestions;

      // Store in localStorage
      localStorage.setItem(
        "generatedQuestions",
        JSON.stringify(formattedQuestions)
      );

      localStorage.setItem("currentQuestionIndex", "0");

      return response.data;
    } catch (error) {
      console.error("Failed to generate questions:", error);
      throw error;
    }
  };

  const evaluateAnswer = async (questionIndex: number, userAnswer: string) => {
    const questions = JSON.parse(
      localStorage.getItem("generatedQuestions") || "[]"
    );
    const question: string = JSON.stringify(questions[questionIndex]);
    try {
      console.log(question);

      const response = await axios.post(
        `${url}/llm/evaluate_answer`,
        {
          question_number: question,
          user_answer: userAnswer,
          // user_answer: jobDescription,
          // skills: skills,
          // experience_years: experience_years,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      console.log("Response", response.data);

      return response.data;
    } catch (error) {
      console.error("Failed to generate questions:", error);
      throw error;
    }
  };

  return {
    questions,
    extracted_text,
    keyterms,
    curentQuestionIndex,
    uploadFile,
    fetchKeywords,
    generateQuestions,
    evaluateAnswer,
  };
});
