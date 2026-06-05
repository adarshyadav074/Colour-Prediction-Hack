# 🎲 Pure Random Baseline Tester | WinGo 1M

A lightweight Python Flask web application designed to generate pure random predictions for 1-Minute Colour Prediction games. It tracks live server results, matches them against its own random guesses, and maintains a real-time history table. 

**🚨 DISCLAIMER:** This project is built strictly for **EDUCATIONAL and AWARENESS purposes**. It is designed to establish a "Baseline Mathematical Win Rate" (usually ~50%) to demonstrate how pure Random Number Generators (RNG) work. It does NOT guarantee profits and does not promote gambling. 

---

## 📌 Overview

Before building complex Machine Learning or Deep Learning models to predict game outcomes, Data Scientists need a "Baseline Model." This application serves as that baseline. It uses Python's native `random` logic to blindly guess the next Size (BIG/SMALL) and Numbers, helping developers calculate the absolute minimum win rate governed by pure luck.

---

## 🎯 Supported Platforms

Out of the box, the `API_URL` in this code is configured to fetch live data for:
* **Yaarwin**
* **Jaiclub**

---

## 🕵️‍♂️ How to Adapt for ANY Other Website

If you want to use this baseline tester for a different color prediction website, you just need to replace the `API_URL` variable in the code. Here is how you can easily extract the API URL from any site:

1. **Open the Website:** Go to the 1-Minute Wingo/Color Prediction page of your target website.
2. **Open Developer Tools:** Right-click anywhere on the page and select **Inspect** (or press `F12` / `Ctrl+Shift+I`).
3. **Go to the Network Tab:** Click on the **Network** tab at the top of the Developer Tools panel.
4. **Filter by Fetch/XHR:** Click on the **Fetch/XHR** filter to only see data requests.
5. **Wait for the Countdown:** Wait for the game timer to hit `00:00` and refresh the data.
6. **Find the API:** You will see a new network request pop up (usually named something like `GetHistoryIssuePage`, `history`, `gameRecord`, or `list`). 
7. **Copy the URL:** Click on that specific request, go to the **Headers** section, copy the `Request URL`, and replace the existing `API_URL` string in the `app.py` script with this new URL.
