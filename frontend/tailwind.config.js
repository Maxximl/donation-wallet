/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#0663ef',
        lightBg: '#f1f2f4',
        darkBlue: '#0a2896',
        accent: '#00aaff',
        muted: '#566bb7',
      },
    },
  },
  plugins: [],
}
