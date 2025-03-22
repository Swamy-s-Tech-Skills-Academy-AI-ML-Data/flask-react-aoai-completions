/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    fontFamily: {
      inter: ["Inter", "sans-serif"],
    },
    container: {
      center: true,
      padding: '1rem', // Optional: adds horizontal padding
      screens: {
        sm: '100%',
        md: '100%',
        lg: '1200px',  // Adjust as needed
        xl: '1500px',  // Adjust as needed
        '2xl': '1600px', // Instead of a fixed 1536px, you can set a custom value
      },
    },
    extend: {},
  },
  plugins: [],
}

