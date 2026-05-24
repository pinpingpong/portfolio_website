# Lim Pin Xiu — Portfolio

A minimalist, dark-mode portfolio website built with HTML, Tailwind CSS (CDN), and vanilla JS.

## Stack
- HTML5 + CSS3 (custom properties)
- Tailwind CSS via CDN
- Google Fonts (Syne + DM Mono + DM Sans)
- Zero build step — pure static

## Deploy to Vercel

### Option 1: CLI
```bash
npm i -g vercel
vercel --prod
```

### Option 2: GitHub → Vercel Dashboard
1. Push this repo to GitHub
2. Go to https://vercel.com/new
3. Import the GitHub repo
4. Framework preset: **Other** (static site)
5. Output directory: `.` (root)
6. Hit Deploy

## Local Preview
```bash
npm install
cp .env.example .env
# edit .env and add your Gemini API key
npm run dev
```

If you only want to preview the static site without the API, you can still use:
```bash
npm run serve
```

## Push to GitHub
```bash
git init
git add .
git commit -m "initial: portfolio site"
git remote add origin https://github.com/pinpingpong/<your-repo-name>.git
git push -u origin main
```
