# GitHub Contribution Scanner

A live cyber-themed GitHub contribution visualizer that fetches real contribution data directly from GitHub and renders it as an animated SVG scanner.

## Preview

<p align="center">
  <img src="https://github-scanner-psi.vercel.app" alt="GitHub Contribution Scanner">
</p>

---

## Live Demo

https://github-scanner-psi.vercel.app

---


## Features

- Live GitHub contribution data
- Automatic daily updates
- Rolling 365-day contribution window
- Animated scanner beam effect
- Contribution count display
- Month labels
- Last updated timestamp
- SVG-based rendering
- Vercel deployment

---

## How It Works

1. Fetches contribution data from GitHub.
2. Parses contribution levels and dates.
3. Generates a custom SVG contribution graph.
4. Applies animated scanner effects.
5. Serves the SVG through a Flask application.
6. Deploys automatically on Vercel.

---

## Tech Stack

- Python
- Flask
- BeautifulSoup4
- Requests
- SVG
- Vercel

---

## Project Structure

```text
github-scanner
│
├── api
│   └── index.py
│
├── src
│   └── generate_svg.py
│
├── README.md
├── requirements.txt
└── .gitignore
```

---
