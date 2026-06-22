# GitHub Contribution Scanner

A GitHub contribution visualizer that fetches real contribution data from GitHub and renders it as an animated SVG scanner with contribution analytics.

## Preview

<p align="center">
  <img src="https://github-scanner-psi.vercel.app" alt="GitHub Contribution Scanner">
</p>

> 💡 Click the graph to explore the interactive contribution scanner.

---

## Live Demo

https://github-scanner-psi.vercel.app

---

## Features

* Live GitHub contribution data
* Animated scanner beam effect
* Rolling 365-day contribution graph
* Hover contribution details
* Today activity indicator
* Total contribution count
* Active days analytics
* Current streak tracking
* Longest streak tracking
* Streak date ranges
* Month labels
* Real-time refresh timestamp (IST)
* SVG-based rendering
* Synchronized scanner and glow effects
* Fully automated updates
* Vercel deployment

---

## How It Works

1. Fetches contribution data directly from GitHub.

2. Extracts contribution levels, dates, and activity details.

3. Calculates:

   * Total Contributions
   * Active Days
   * Current Streak
   * Longest Streak

4. Generates a custom animated SVG dashboard.

5. Adds interactive contribution tooltips and today indicators.

6. Applies synchronized scanner and glow effects.

7. Serves the SVG through Flask.

8. Deploys automatically using Vercel.

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
* Daily Contribution Details
* Today's Activity Indicator

---

## License

This project is licensed under the MIT License.

---
