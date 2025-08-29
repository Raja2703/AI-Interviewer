// https://nuxt.com/docs/api/configuration/nuxt-config
import vuetify, { transformAssetUrls } from "vite-plugin-vuetify";
export default defineNuxtConfig({
  app: {
    head: {
      title: "AI Interview Helper",
    },
  },
  compatibilityDate: "2024-04-03",
  devtools: { enabled: true },
  build: {
    transpile: ["vuetify"],
  },
  modules: [
    (_options, nuxt) => {
      nuxt.hooks.hook("vite:extendConfig", (config) => {
        // @ts-expect-error
        config.plugins.push(vuetify({ autoImport: true }));
      });
    },
    "@pinia/nuxt",
    "@nuxtjs/google-fonts",
    "@pinia/nuxt",
    //...
  ],
  pinia: {
    storesDirs: ["./stores/**", "./custom-folder/stores/**"],
  },
  css: ["@/assets/main.css"],
  googleFonts: {
    families: {
      Overpass: [100, 300, 400, 600, 700], // Choose weights as needed
    },
    display: "swap",
  },
  vite: {
    vue: {
      template: {
        transformAssetUrls,
      },
    },
  },
});
