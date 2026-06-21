# GitHub Contribution Scanner

A GitHub contribution visualizer that fetches real contribution data from GitHub and renders it as an animated SVG scanner with contribution analytics.

## Preview

<p align="center">
  <img src="https://github-scanner-psi.vercel.app" alt="GitHub Contribution Scanner">
</p>

---

## Live Demo

https://github-scanner-psi.vercel.app

---

## Features

* Live GitHub contribution data
* Animated scanner beam effect
* Rolling 365-day contribution graph
* Total contribution count
* Active days analytics
* Current streak tracking
* Longest streak tracking
* Streak date ranges
* Month labels
* Real-time refresh timestamp (IST)
* SVG-based rendering
* Fully automated updates
* Vercel deployment

---

## How It Works

1. Fetches contribution data directly from GitHub.
2. Extracts contribution levels and activity dates.
3. Calculates:

   * Total Contributions
   * Active Days
   * Current Streak
   * Longest Streak
4. Generates a custom animated SVG dashboard.
5. Applies synchronized scanner and glow effects.
6. Serves the SVG through Flask.
7. Deploys automatically using Vercel.

---

## Tech Stack

* Python
* Flask
* Requests
* BeautifulSoup4
* SVG
* Vercel

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

## Analytics Included

* Total Contributions
* Active Days
* Current Contribution Streak
* Longest Contribution Streak
* Contribution Date Ranges
* Last Refresh Timestamp

---

## License

This project is licensed under the MIT License.

---
