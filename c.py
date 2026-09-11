
import csv
import os
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox

DATA_FILE = "health_data.csv"
GOAL_FILE = "goals.csv"
USER_FILE = "user.csv"

def init_files():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', newline='') as f:
            csv.writer(f).writerow(["Date", "Water", "Sleep", "Steps"])
    else:
        # Fix header if old format exists
        with open(DATA_FILE, 'r') as f:
            first_line = f.readline().strip()
        if "Water" not in first_line:
            with open(DATA_FILE, 'w', newline='') as f:
                csv.writer(f).writerow(["Date", "Water", "Sleep", "Steps"])

    if not os.path.exists(GOAL_FILE):
        with open(GOAL_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["WaterGoal", "SleepGoal", "StepsGoal"])
            writer.writerow([3, 7, 8000])

def load_goals():
    with open(GOAL_FILE, 'r') as f:
        return list(map(float, list(csv.reader(f))[1]))


def save_user():
    with open(USER_FILE, 'w', newline='') as f:
        csv.writer(f).writerow([name_entry.get(), age_entry.get(), weight_entry.get(), height_entry.get()])
    messagebox.showinfo("Saved", "Profile Saved")


def calculate_bmi():
    try:
        w = float(weight_entry.get())
        h = float(height_entry.get()) / 100
        bmi = w / (h*h)
        messagebox.showinfo("BMI", f"BMI: {bmi:.2f}")
    except:
        messagebox.showerror("Error", "Invalid input")


def add_entry():
    try:
        date = datetime.now().strftime("%Y-%m-%d")
        glasses = int(water_entry.get())
        water = glasses * 0.25
        sleep = float(sleep_entry.get())

        activity_map = {"Low": 2000, "Medium": 5000, "High": 9000}
        steps = activity_map.get(activity_var.get(), 0)

        with open(DATA_FILE, 'a', newline='') as f:
            csv.writer(f).writerow([date, water, sleep, steps])

        messagebox.showinfo("Success", "Entry Added")
    except:
        messagebox.showerror("Error", "Invalid input")


def show_streak():
    gw, gs, gst = load_goals()
    streak = 0

    with open(DATA_FILE, 'r') as f:
        rows = list(csv.DictReader(f))

    for row in reversed(rows):
        try:
            if float(row.get('Water', 0)) >= gw and float(row.get('Sleep', 0)) >= gs and int(row.get('Steps', 0)) >= gst:
                streak += 1
            else:
                break
        except:
            break

    messagebox.showinfo("Streak", f"🔥 {streak} days")


def weekly_summary():
    last_week = datetime.now() - timedelta(days=7)
    w = s = st = c = 0

    with open(DATA_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                if datetime.strptime(row['Date'], "%Y-%m-%d") >= last_week:
                    w += float(row.get('Water', 0))
                    s += float(row.get('Sleep', 0))
                    st += int(row.get('Steps', 0))
                    c += 1
            except:
                continue

    if c == 0:
        messagebox.showinfo("Summary", "No data")
        return

    msg = f"Water: {w/c:.2f}L\nSleep: {s/c:.2f}hrs\nSteps: {st//c}"
    messagebox.showinfo("Weekly Summary", msg)

# ---------- GUI ----------
root = tk.Tk()
root.title("Smart Health Tracker")
root.geometry("420x550")
root.configure(bg="#f0f0f0")

init_files()

# PROFILE FRAME
profile_frame = tk.LabelFrame(root, text="User Profile", padx=10, pady=10)
profile_frame.pack(fill="x", padx=10, pady=5)

name_entry = tk.Entry(profile_frame)
age_entry = tk.Entry(profile_frame)
weight_entry = tk.Entry(profile_frame)
height_entry = tk.Entry(profile_frame)

labels = ["Name", "Age", "Weight", "Height"]
entries = [name_entry, age_entry, weight_entry, height_entry]

for i in range(4):
    tk.Label(profile_frame, text=labels[i]).grid(row=i, column=0, sticky="w")
    entries[i].grid(row=i, column=1)


tk.Button(profile_frame, text="Save", command=save_user).grid(row=4, column=0, pady=5)
tk.Button(profile_frame, text="BMI", command=calculate_bmi).grid(row=4, column=1)

# INPUT FRAME
input_frame = tk.LabelFrame(root, text="Daily Input", padx=10, pady=10)
input_frame.pack(fill="x", padx=10, pady=5)

water_entry = tk.Entry(input_frame)
sleep_entry = tk.Entry(input_frame)
activity_var = tk.StringVar(value="Medium")


tk.Label(input_frame, text="Water (glasses)").grid(row=0, column=0)
water_entry.grid(row=0, column=1)


tk.Label(input_frame, text="Sleep (hrs)").grid(row=1, column=0)
sleep_entry.grid(row=1, column=1)


tk.Label(input_frame, text="Activity").grid(row=2, column=0)
tk.OptionMenu(input_frame, activity_var, "Low", "Medium", "High").grid(row=2, column=1)


tk.Button(input_frame, text="Add Entry", command=add_entry).grid(row=3, columnspan=2, pady=5)

# ACTION FRAME
action_frame = tk.LabelFrame(root, text="Insights", padx=10, pady=10)
action_frame.pack(fill="x", padx=10, pady=5)


tk.Button(action_frame, text="Show Streak", width=20, command=show_streak).pack(pady=2)
tk.Button(action_frame, text="Weekly Summary", width=20, command=weekly_summary).pack(pady=2)

# EXIT

tk.Button(root, text="Exit", bg="red", fg="white", command=root.quit).pack(pady=10)

root.mainloop()