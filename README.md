# Contract Management System

A complete data entry, photo capture, search, and Excel export system.

**Stack:** Python (Flask) backend, SQLite database, HTML/Tailwind CSS/JavaScript frontend.

---

## 📁 Project Structure

```
contract_management_system/
├── app.py                  # Flask application (routes, database, export logic)
├── requirements.txt        # Python dependencies
├── run.bat                 # Double-click launcher for Windows
├── database.db             # SQLite database (auto-created on first run)
├── templates/
│   ├── base.html            # Shared layout with sidebar
│   ├── login.html           # Login page
│   ├── dashboard.html       # Dashboard with stats + recent records
│   ├── data_entry.html      # Data entry form + webcam capture
│   └── search.html          # Search bar + card/table results
├── static/
│   ├── css/style.css        # Custom styling on top of Tailwind
│   ├── js/app.js            # Sidebar toggle logic
│   ├── js/data_entry.js     # Webcam capture + form submit logic
│   ├── js/search.js         # Live search + rendering logic
│   └── uploads/             # Captured/uploaded photos are saved here
└── exports/                 # Generated Excel files land here before download
```

---

## 🚀 Quick Start (Windows)

1. Make sure **Python 3.10+** is installed and added to PATH
   (download from https://www.python.org/downloads/ — check "Add Python to PATH" during install).
2. Double-click **`run.bat`**.
   - It creates a virtual environment (first run only)
   - Installs Flask, OpenCV, Pillow, pandas, and openpyxl automatically
   - Starts the local server
   - Opens your default browser at `http://127.0.0.1:5000`
3. Log in with the default credentials:
   - **Username:** `admin`
   - **Password:** `admin123`

To stop the server, close the black command-prompt window.

---

## 🖥️ Manual Setup (macOS/Linux or manual Windows setup)

```bash
cd contract_management_system
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

---

## 🔑 Changing the login credentials

Open `app.py` and edit these two lines near the top:

```python
USERNAME = 'admin'
PASSWORD = 'admin123'
```

For real deployments, also change `app.secret_key` to a long random string.

---

## ✨ Features

- **Sidebar navigation** — Dashboard, Data Entry, Search, Export, Logout (collapsible via the ☰ button)
- **Login/logout system** — session-based auth; all pages require login
- **Data Entry form** — Contract ID, Contract Name, Contract Amount, Premium, Others, Total Amount (auto-calculated, editable), Email, Phone
- **Live webcam preview** — click "Start Camera" → "Take Photo" to capture directly in the browser (uses the standard `getUserMedia` browser API, so it works with any webcam without extra native drivers)
- **Upload alternative** — pick an existing image file instead of using the camera
- **Photo storage** — every photo is saved to `static/uploads/` with a unique filename, and that filename is linked to its record in SQLite
- **Search page** — search by Contract ID, Contract Name, Email, or Phone; toggle between a profile-card view and a table view; photos are shown inline with each result
- **Export to Excel** — one click reads the entire SQLite database and downloads a formatted `.xlsx` file (auto column widths, all fields included)
- **Delete records** — remove a record (and its photo file) directly from the search results

---

## 📝 Notes

- Live webcam capture uses your browser's own camera API for reliability across systems. `opencv-python` and `Pillow` are included in `requirements.txt` in case you want to extend the backend later with server-side image processing (thumbnails, filters, compression, etc.) — swap in a call like `cv2.imread()`/`PIL.Image.open()` inside the `/api/contracts` route where the photo file is saved.
- Your browser will ask for camera permission the first time you click "Start Camera" — click **Allow**.
- The database file `database.db` and the `static/uploads/` folder are created automatically the first time you run the app.
- All amounts are formatted with the ₱ (PHP) symbol by default — change the templates/`static/js` files if you'd like a different currency symbol.
