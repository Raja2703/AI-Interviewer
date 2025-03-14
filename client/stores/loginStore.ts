import { defineStore } from "pinia";
import axios from "axios";

export const useLoginStore = defineStore("loginStore", () => {
  const url = "http://localhost:8000";

  const login = async (user: any) => {
    const data = await axios.post("http://localhost:8000/login", {
      username: user.username,
      password: user.password,
    });

    return data
  }

  return {
    login
  };
});
