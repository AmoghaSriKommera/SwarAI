/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          light: '#6366f1', // Indigo 500
          DEFAULT: '#4f46e5', // Indigo 600
          dark: '#4338ca', // Indigo 700
        },
        secondary: {
          light: '#a5b4fc', // Indigo 300
          DEFAULT: '#818cf8', // Indigo 400
          dark: '#6366f1', // Indigo 500
        },
        user: {
          light: '#e0f2fe', // Sky 100
          DEFAULT: '#bae6fd', // Sky 200
          dark: '#7dd3fc', // Sky 300
        },
        ai: {
          light: '#f5f3ff', // Violet 50
          DEFAULT: '#ede9fe', // Violet 100
          dark: '#ddd6fe', // Violet 200
        },
        // Background color classes
        'user-light': '#e0f2fe',
        'ai-light': '#f5f3ff'
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'bounce-slow': 'bounce 2s infinite',
      },
      height: {
        'screen-90': '90vh',
      }
    },
  },
  plugins: [],
}