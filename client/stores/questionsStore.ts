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
        withCredentials: true,
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
          withCredentials: true,
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
          withCredentials: true,
        }
      );

      const formattedQuestions = response.data["questions"].map((q: any) => ({
        ...q,
      }));

      questions.value = formattedQuestions;

      return response.data;
    } catch (error) {
      console.error("Failed to generate questions:", error);
      throw error;
    }
  };

  const getInterviewDetails = async (interviewId: number) => {
    try {
      const response = await axios.get(`${url}/user/${interviewId}`, {
        headers: {
          "Content-Type": "application/json",
        },
        withCredentials: true,
      });

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
          withCredentials: true,
        }
      );

      questions[questionIndex].answered = true;
      questions[questionIndex].feedback = response.data["feedback"];
      questions[questionIndex].userAnswer = userAnswer;

      localStorage.setItem("generatedQuestions", JSON.stringify(questions));
      localStorage.setItem("currentQuestionIndex", String(questionIndex + 1));

      // console.log("Response", response.data);

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
    getInterviewDetails,
  };
});
