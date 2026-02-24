# LocalHoster 🚀

**LocalHoster** is a lightweight, enhanced Python-based HTTP server designed for rapid local file sharing and directory browsing. It goes beyond the standard `http.server` by providing a modern, dark-themed Web UI, a responsive grid gallery, and an integrated terminal-based file navigator.

---

## ✨ Features

* **Interactive CLI Navigator:** Built-in shell to `cd` into directories before hosting, supporting tab-completion and `ls`-style previews.
* **Modern Web UI:** A sleek, dark-mode interface optimized for both Desktop and Mobile.
* **Smart Gallery View:**
    * Automatic image previews for `.jpg`, `.png`, `.gif`, and `.webp`.
    * Dynamic grid layout (1 to 5 columns) with client-side persistence (`localStorage`).
    * Responsive "Zoom" controls to adjust thumbnail sizes on the fly.
* **Clean Logging:** Smart console output that filters out noisy requests (like `.ico` or `.map` files) and highlights file access.
* **Zero Dependencies:** Runs on standard Python 3.x libraries—no `pip install` required.

---

## 🚀 Quick Start

### 1. Requirements
* **Python 3.6+**
* Works on **Windows, macOS, and Linux**.
* Also works on **Android*** using e.g. Pydroid 3 or Termux.

### 2. Run the Script
Simply execute the script using Python:

```bash
python3 localhoster.py