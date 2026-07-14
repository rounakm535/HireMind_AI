/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      colors: {
        brand: {
          50: '#f4f6fb',
          100: '#e9edf7',
          200: '#cbd5ee',
          300: '#9cb0de',
          400: '#6886ca',
          500: '#4665b6',
          600: '#344e97',
          700: '#2a3e7c',
          800: '#263667',
          900: '#232f57',
        },
      },
    },
  },
  plugins: [],
}
