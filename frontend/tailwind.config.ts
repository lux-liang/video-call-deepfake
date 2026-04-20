import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./lib/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        canvas: "rgb(var(--canvas) / <alpha-value>)",
        ink: "rgb(var(--ink) / <alpha-value>)",
        sand: "rgb(var(--sand) / <alpha-value>)",
        rust: "rgb(var(--rust) / <alpha-value>)",
        teal: "rgb(var(--teal) / <alpha-value>)",
        line: "rgb(var(--line) / <alpha-value>)",
      },
      boxShadow: {
        panel: "0 20px 60px rgba(16, 24, 32, 0.10)",
      },
      borderRadius: {
        "4xl": "2rem",
      },
      backgroundImage: {
        grid: "linear-gradient(to right, rgba(44, 56, 71, 0.08) 1px, transparent 1px), linear-gradient(to bottom, rgba(44, 56, 71, 0.08) 1px, transparent 1px)",
      },
    },
  },
  plugins: [],
};

export default config;
