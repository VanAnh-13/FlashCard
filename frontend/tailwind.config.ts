import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: '#2b6cee',
        'background-light': '#f6f6f8',
        'background-dark': '#101622',
        success: '#50C878',
        error: '#E57373',
        coral: '#ff9b85',
      },
      fontFamily: {
        display: ['Lexend', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
export default config
