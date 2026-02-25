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
* Also works on **Android** using e.g. Pydroid 3 or Termux.

### 2. Run the Script
Simply execute the script using Python:

```bash
python3 localhoster.py
```

### 3. Usage & Navigation

LocalHoster follows a two-step process: selecting your directory via terminal and then hosting it for your local network.

#### Step 1: Terminal Navigation
After launching the script, you are in an interactive shell mode. You can navigate your file system before the server goes live:
* **Browse:** Use the `cd <path>` command to move into the directory you want to host.
* **List:** The script automatically displays the current folder's content (like `ls -alh` or `dir`) so you always know where you are.
* **Start Hosting:** Once you are in the correct directory, type `host`, `run`, or simply press **Enter**.

#### Step 2: Accessing the Host
Once the server is active, it will display a status block with your local network details:
* **Local URL:** You will see an address like `http://192.168.x.x:8000`.
* **Cross-Device Access:** Open this URL in the browser of **any device** (Smartphone, Tablet, or another Laptop) that is connected to the same Wi-Fi/LAN network.
* **Control:** Use the Web UI to browse files, or press `CTRL+C` in your terminal to stop the server and return to the navigation mode.