import tkinter as tk
from tkinter import messagebox
import threading
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By
from time import sleep

# Data 
SLOTS = [
    "6:30 AM - 7:30 AM",
    "7:30 AM - 8:30 AM",
    "8:30 AM - 9:30 AM",
    "9:30 AM - 10:30 AM",
    "10:30 AM - 11:30 AM",
    "11:30 AM - 12:30 PM",
    "12:30 PM - 1:30 PM",
    "1:30 PM - 2:30 PM",
    "2:30 PM - 3:30 PM",
    "3:30 PM - 5:00 PM",
    "5:00 PM - 6:00 PM",
    "6:00 PM - 7:00 PM",
    "7:00 PM - 8:00 PM",
    "8:00 PM - 9:30 PM",
]

# Colors 
BG         = "#12151f"
CARD       = "#1c2133"
ACCENT     = "#00e5a0"
ACCENT_DIM = "#00b87f"
TEXT       = "#e8edf5"
MUTED      = "#6b7a99"
ENTRY_BG   = "#252d42"
BORDER     = "#2e3a52"
SLOT_AVAIL = "#1a8c6e"
SLOT_SEL   = "#00e5a0"
SLOT_SEL_FG= "#0d1117"
WARN_BG    = "#2a1f10"
WARN_FG    = "#f0a030"

selected_slot = {"index": None, "btn": None}


def on_slot_click(idx, btn):
    if selected_slot["btn"] is not None:
        selected_slot["btn"].config(bg=SLOT_AVAIL, fg=TEXT)
    selected_slot["index"] = idx + 1
    selected_slot["btn"]   = btn
    btn.config(bg=SLOT_SEL, fg=SLOT_SEL_FG)


def set_status(msg, color=ACCENT):
    status_lbl.config(text=msg, fg=color)


def run_booking(name, roll_num, other_rolls, num_players, slot_index):
    def task():
        book_btn.config(state="disabled")
        set_status("⏳  Opening browser...", WARN_FG)
        try:
            driver = webdriver.Chrome()
            driver.get("https://gymkhana.iitb.ac.in/sports/turfbooking")

            set_status("⏳  Filling in details...", WARN_FG)
            driver.find_element(By.XPATH, "/html/body/div/div/main/div/form/div[1]/input").send_keys(name)
            driver.find_element(By.XPATH, "/html/body/div/div/main/div/form/div[2]/input").send_keys(roll_num)
            driver.find_element(By.XPATH, "/html/body/div/div/main/div/form/div[3]/input").send_keys(roll_num + "@iitb.ac.in")
            driver.find_element(By.XPATH, "/html/body/div/div/main/div/form/div[4]/input").send_keys(other_rolls)
            driver.find_element(By.XPATH, "/html/body/div/div/main/div/form/div[5]/input").send_keys(num_players)

            set_status("⏳  Selecting time slot...", WARN_FG)
            slot = driver.find_element(By.XPATH, f"/html/body/div/div/main/div/form/div[6]/button[{slot_index}]")
            driver.execute_script("arguments[0].scrollIntoView(true);", slot)
            driver.execute_script("arguments[0].click();", slot)

            try:
                driver.switch_to.alert.accept()
            except NoAlertPresentException:
                pass

            check = driver.find_element(By.XPATH, "/html/body/div/div/main/div/form/div[7]/input")
            driver.execute_script("arguments[0].scrollIntoView(true);", check)
            driver.execute_script("arguments[0].click();", check)

            set_status("⏳  Submitting booking...", WARN_FG)
            book = driver.find_element(By.XPATH, "/html/body/div/div/main/div/form/button")
            driver.execute_script("arguments[0].scrollIntoView(true);", book)
            driver.execute_script("arguments[0].click()", book)

            try:
                driver.switch_to.alert.accept()
            except NoAlertPresentException:
                pass

            set_status("✅  Booking submitted successfully!", ACCENT)
            sleep(5)
            driver.quit()

        except Exception as e:
            set_status(f"❌  Error: {e}", "#e05555")
        finally:
            book_btn.config(state="normal")

    threading.Thread(target=task, daemon=True).start()



#  ROOT

root = tk.Tk()
root.title("IIT Bombay — Turf Booking")
root.configure(bg=BG)
root.minsize(460, 500)


canvas = tk.Canvas(root, bg=BG, highlightthickness=0, bd=0)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview,
                          bg=CARD, troughcolor=BG, activebackground=ACCENT)
canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

inner = tk.Frame(canvas, bg=BG)
inner_id = canvas.create_window((0, 0), window=inner, anchor="nw")

inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.bind("<Configure>",lambda e: canvas.itemconfig(inner_id, width=e.width))
canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1,  "units"))
canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))


F_TITLE   = ("Segoe UI", 20, "bold")
F_SUB     = ("Segoe UI", 9)
F_SECTION = ("Segoe UI", 10, "bold")
F_LABEL   = ("Segoe UI", 9)
F_ENTRY   = ("Segoe UI", 11)
F_SLOT    = ("Segoe UI", 9, "bold")
F_BTN     = ("Segoe UI", 12, "bold")


def divider(parent, label):
    row = tk.Frame(parent, bg=BG)
    row.pack(fill="x", padx=20, pady=(16, 6))
    tk.Label(row, text=label, bg=BG, fg=ACCENT, font=F_SECTION).pack(side="left")
    tk.Frame(row, bg=BORDER, height=1).pack(side="left", fill="x", expand=True, padx=(8,0), pady=5)


def field(parent, label, default="", readonly=False, textvariable=None):
    wrap = tk.Frame(parent, bg=BG)
    wrap.pack(fill="x", padx=20, pady=(0, 8))
    tk.Label(wrap, text=label, bg=BG, fg=MUTED, font=F_LABEL, anchor="w").pack(fill="x")
    kw = dict(bg=ENTRY_BG, fg=TEXT if not readonly else MUTED,
              font=F_ENTRY, relief="flat",
              highlightthickness=1, highlightbackground=BORDER,
              highlightcolor=ACCENT)
    if textvariable:
        e = tk.Entry(wrap, textvariable=textvariable, state="readonly",
                     readonlybackground=ENTRY_BG, **kw)
    else:
        e = tk.Entry(wrap, insertbackground=ACCENT, **kw)
        if default:
            e.insert(0, default)
    e.pack(fill="x", ipady=7)
    return e




hdr = tk.Frame(inner, bg=CARD, pady=20)
hdr.pack(fill="x")
tk.Label(hdr, text="⚽", bg=CARD, fg=ACCENT, font=("Segoe UI", 30)).pack()
tk.Label(hdr, text="Turf Booking", bg=CARD, fg=TEXT, font=F_TITLE).pack()
tk.Label(hdr, text="Institute Sports Council  ·  IIT Bombay",
         bg=CARD, fg=MUTED, font=F_SUB).pack(pady=(3,0))


divider(inner, "Personal Details")

entry_name    = field(inner, "Name")
entry_roll    = field(inner, "Roll Number")

ldap_var = tk.StringVar()
def update_ldap(*_):
    ldap_var.set(entry_roll.get().strip() + "@iitb.ac.in")
entry_roll.bind("<KeyRelease>", update_ldap)

field(inner, "LDAP ID  (auto-filled)", readonly=True, textvariable=ldap_var)
entry_other   = field(inner, "Roll Numbers of Players  (comma separated)")
entry_players = field(inner, "Number of Players", default="0")

divider(inner, "Available Slots")

grid = tk.Frame(inner, bg=BG)
grid.pack(fill="x", padx=16, pady=(0, 8))
grid.columnconfigure(0, weight=1)
grid.columnconfigure(1, weight=1)

for idx, slot_text in enumerate(SLOTS):
    r, c = divmod(idx, 2)
    cell = tk.Frame(grid, bg=BG, padx=4, pady=4)
    cell.grid(row=r, column=c, sticky="nsew")
    cell.columnconfigure(0, weight=1)

    btn = tk.Button(
        cell,
        text=f"{slot_text}\nStatus: available",
        bg=SLOT_AVAIL, fg=TEXT,
        font=F_SLOT, relief="flat", bd=0,
        cursor="hand2", pady=10,
        activebackground="#22b589", activeforeground=TEXT,
        wraplength=190, justify="center"
    )
    btn.pack(fill="x")
    btn.config(command=lambda i=idx, b=btn: on_slot_click(i, b))

divider(inner, "Terms & Conditions")

terms_var = tk.BooleanVar()
tk.Checkbutton(
    inner, variable=terms_var,
    text="I accept the Terms and Conditions mentioned in the Rulebook",
    bg=BG, fg=TEXT, activebackground=BG,
    selectcolor=ENTRY_BG, font=("Segoe UI", 9),
    anchor="w"
).pack(fill="x", padx=20, pady=(0, 8))

warn_frame = tk.Frame(inner, bg=WARN_BG, pady=10)
warn_frame.pack(fill="x", padx=20, pady=(0, 12))
tk.Label(
    warn_frame,
    text="⚠  The Institute Sports Council reserves the right to cancel any turf\n"
         "booking at any time for valid reasons.",
    bg=WARN_BG, fg=WARN_FG,
    font=("Segoe UI", 8), justify="center", wraplength=380
).pack()

# Status 
status_lbl = tk.Label(inner, text="", bg=BG, fg=ACCENT,
                       font=("Segoe UI", 9), wraplength=400)
status_lbl.pack(pady=(0, 6))

#  BOOK BUTTON
def on_book():
    name        = entry_name.get().strip()
    roll_num    = entry_roll.get().strip()
    other_rolls = entry_other.get().strip()
    num_players = entry_players.get().strip()

    if not all([name, roll_num, other_rolls, num_players]):
        messagebox.showwarning("Missing Fields", "Please fill in all fields.")
        return
    if selected_slot["index"] is None:
        messagebox.showwarning("No Slot Selected", "Please select a time slot.")
        return
    if not terms_var.get():
        messagebox.showwarning("Terms & Conditions", "Please accept the Terms and Conditions.")
        return

    run_booking(name, roll_num, other_rolls, num_players, selected_slot["index"])


book_btn = tk.Button(
    inner, text="BOOK SLOT", command=on_book,
    bg=ACCENT, fg="#0d1117", font=F_BTN,
    relief="flat", cursor="hand2", pady=14,
    activebackground=ACCENT_DIM, activeforeground="#0d1117"
)
book_btn.pack(fill="x", padx=20, pady=(0, 24))

def set_initial_size():
    root.update_idletasks()
    content_w = inner.winfo_reqwidth() + scrollbar.winfo_reqwidth() + 4
    content_h = inner.winfo_reqheight() + 4
    screen_w  = root.winfo_screenwidth()
    screen_h  = root.winfo_screenheight()
    win_w = min(content_w, screen_w - 80)
    win_h = min(content_h, screen_h - 100)
    x = (screen_w - win_w) // 2
    y = (screen_h - win_h) // 2
    root.geometry(f"{win_w}x{win_h}+{x}+{y}")

root.after(60, set_initial_size)
root.mainloop()