# IIT Bombay — Turf Booking Automation

Automates the turf slot booking process on the IIT Bombay Gymkhana sports portal so you never have to fill the same form repeatedly.

---

## What It Does

Fills and submits the turf booking form at [gymkhana.iitb.ac.in/sports/turfbooking](https://gymkhana.iitb.ac.in/sports/turfbooking) on your behalf. It enters your name, roll number, LDAP ID, co-players' roll numbers, player count, and chosen time slot — then checks the Terms & Conditions box and hits Book.

Two versions are available:

| File | Interface | Best For |
|---|---|---|
| `main.py` | Terminal (command-line) | Quick one-off bookings |
| `turf_booking.py` | Desktop GUI (Tkinter) | Comfortable, visual use |

---

## Why Use This

- The booking portal requires filling 5+ fields every single time.
- This tool pre-fills everything and lets you pick a slot in one click.
- The GUI version shows live status updates as the booking progresses.
- Runs in the background — you can watch the browser fill itself out.

---

## Requirements

**Python 3.8+** is required. Install the dependencies below:

```bash
pip install selenium
```

**Google Chrome** must be installed on your machine.

**ChromeDriver** must match your Chrome version.
Download it from [chromedriver.chromium.org](https://chromedriver.chromium.org/downloads) and place it in your system `PATH`, or use the auto-manager:

```bash
pip install webdriver-manager
```

> The `tkinter` module (used by the GUI version) comes pre-installed with standard Python on Windows and macOS. On Linux, install it with:
> ```bash
> sudo apt install python3-tk
> ```

---

## Setup

1. **Clone or download** this repository.

2. **Open the file you want to use** — `main.py` (terminal) or `turf_booking.py` (GUI).

3. **For `main.py`**, edit these lines near the top with your details:

   ```python
   name       = "Your Full Name"
   rollNum    = "23B1234"          # your roll number
   otherRoll  = "23B0001, 23B0002" # comma-separated co-player roll numbers
   numPlayer  = 6                  # total number of players
   ```

4. **For `turf_booking.py`**, no editing needed — fill everything in the GUI at runtime.

---

## How to Run

**Terminal version:**
```bash
python main.py
```
The script will open Chrome, fill the form, print available slots, ask you to enter a slot number (1–14), and submit the booking.

**GUI version:**
```bash
python turf_booking.py
```
A window will open. Fill in your details, click a time slot, accept the terms, and press **BOOK SLOT**. The status bar at the bottom shows live progress.

---

## Available Time Slots

| # | Slot |
|---|------|
| 1 | 6:30 AM – 7:30 AM |
| 2 | 7:30 AM – 8:30 AM |
| 3 | 8:30 AM – 9:30 AM |
| 4 | 9:30 AM – 10:30 AM |
| 5 | 10:30 AM – 11:30 AM |
| 6 | 11:30 AM – 12:30 PM |
| 7 | 12:30 PM – 1:30 PM |
| 8 | 1:30 PM – 2:30 PM |
| 9 | 2:30 PM – 3:30 PM |
| 10 | 3:30 PM – 5:00 PM |
| 11 | 5:00 PM – 6:00 PM |
| 12 | 6:00 PM – 7:00 PM |
| 13 | 7:00 PM – 8:00 PM |
| 14 | 8:00 PM – 9:30 PM |

---

## Notes

- A Chrome browser window will open visibly — this is expected.
- Do not click inside the browser window while the script is running.
- If a slot is already booked or unavailable, the portal will show an alert which the script will automatically dismiss.
- Your LDAP ID is auto-generated as `<rollnumber>@iitb.ac.in`.

---

## Disclaimer

This tool is for personal convenience only. It interacts with the official IIT Bombay sports portal and does not bypass any authentication or access controls. Use responsibly and in accordance with the Institute's booking policies.