/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './404.html', './investori.html', './investori-zamer.html', './investori-zaklad.html', './investori-scenare.html', './struktura-webu.html', './galerie.html'],
  theme: {
    extend: {
      colors: {
        plum: 'var(--accent)',
        'plum-deep': 'var(--plum-deep)',
        rose: 'var(--rose)',
        cream: 'var(--cream)',
        fg: 'var(--fg)',
        'fg-muted': 'var(--fg-muted)',
        bg: 'var(--bg)',
        'bg-muted': 'var(--bg-muted)',
        'accent-rule': 'var(--accent-rule)',
        'border-muted': 'var(--border-muted)',
      },
      fontFamily: {
        sans: ['Atyp Special', 'system-ui', '-apple-system', 'Segoe UI', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
