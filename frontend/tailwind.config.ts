import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        slatepanel: '#111827',
        riskred: '#ef4444',
        signalgreen: '#22c55e'
      }
    }
  },
  plugins: []
};

export default config;
