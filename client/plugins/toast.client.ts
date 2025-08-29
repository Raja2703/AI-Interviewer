import "vue-toastification/dist/index.css";
import Toast, { type PluginOptions } from "vue-toastification";

const options: PluginOptions = {
  timeout: 3000,
  closeOnClick: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: false,
  pauseOnHover: true,
  pauseOnFocusLoss: true,
  maxToasts: 5,
  hideProgressBar: false,
  icon: true,
}

export default defineNuxtPlugin((app) => {
  app.vueApp.use(Toast, options);
});
