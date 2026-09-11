# HEALTH TRACKER PROJECT (REALISTIC INPUT VERSION)
# Features:
# - User Profile
# - BMI Calculator
# - Goal Tracking
# - Realistic Inputs (Glasses + Activity Level)
# - Smart Feedback
# - Streak System
# - Weekly Summary

import csv
import os
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox

DATA_FILE = "health_data.csv"
GOAL_FILE = "goals.csv"
USER_FILE = "user.csv"

# ---------- INIT ----------
def init_files():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', newline='') as f:
            csv.writer(f).writerow(["Date", "Water(L)", "Sleep", "Steps"])

    if not os.path.exists(GOAL_FILE):
        with open(GOAL_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["WaterGoal", "SleepGoal", "StepsGoal"])
            writer.writerow([3, 7, 8000])

# ---------- USER PROFILE ----------
def save_user():
    with open(USER_FILE, 'w', newline='') as f:
        csv.writer(f).writerow([name_entry.get(), age_entry.get(), weight_entry.get(), height_entry.get()])
    messagebox.showinfo("Saved", "Profile Saved")

# ---------- BMI ----------
def calculate_bmi():
    try:
        w = float(weight_entry.get())
        h = float(height_entry.get()) / 100
        bmi = w / (h*h)

        status = "Normal"
        if bmi < 18.5:
            status = "Underweight"
        elif bmi >= 25:
            status = "Overweight"

        messagebox.showinfo("BMI", f"BMI: {bmi:.2f}\nStatus: {status}")
    except:
        messagebox.showerror("Error", "Invalid input")

# ---------- LOAD GOALS ----------
def load_goals():
    with open(GOAL_FILE, 'r') as f:
        return list(map(float, list(csv.reader(f))[1]))

# ---------- ADD ENTRY ----------
def add_entry():
    try:
        date = datetime.now().strftime("%Y-%m-%d")

        # Convert glasses → liters (1 glass ≈ 0.25L)
        glasses = int(water_entry.get())
        water_liters = glasses * 0.25

        sleep = float(sleep_entry.get())

        # Activity → steps mapping
        activity = activity_var.get()
        steps_map = {
            "Low": 2000,
            "Medium": 5000,
            "High": 9000
        }
        steps = steps_map.get(activity, 0)

        with open(DATA_FILE, 'a', newline='') as f:
            csv.writer(f).writerow([date, water_liters, sleep, steps])

        give_feedback(water_liters, sleep, steps)
        messagebox.showinfo("Success", "Entry Added")

    except:
        messagebox.showerror("Error", "Invalid input")

# ---------- FEEDBACK ----------
def give_feedback(w, s, st):
    gw, gs, gst = load_goals()

    msg = "\nFeedback:\n"
    msg += "\nWater: " + ("Good" if w >= gw else "Low")
    msg += "\nSleep: " + ("Good" if s >= gs else "Low")
    msg += "\nActivity: " + ("Good" if st >= gst else "Low")

    messagebox.showinfo("Feedback", msg)

# ---------- STREAK ----------
def show_streak():
    gw, gs, gst = load_goals()
    streak = 0

    with open(DATA_FILE, 'r') as f:
        rows = list(csv.DictReader(f))

    for row in reversed(rows):
        if float(row['Water(L)']) >= gw and float(row['Sleep']) >= gs and int(row['Steps']) >= gst:
            streak += 1
        else:
            break

    messagebox.showinfo("Streak", f"🔥 {streak} days")

# ---------- WEEKLY SUMMARY ----------
def weekly_summary():
    last_week = datetime.now() - timedelta(days=7)
    w = s = st = c = 0

    with open(DATA_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if datetime.strptime(row['Date'], "%Y-%m-%d") >= last_week:
                w += float(row['Water(L)'])
                s += float(row['Sleep'])
                st += int(row['Steps'])
                c += 1

    if c == 0:
        messagebox.showinfo("Summary", "No data")
        return

    msg = f"Last 7 Days:\nWater: {w/c:.2f}L\nSleep: {s/c:.2f}hrs\nSteps: {st//c}"
    messagebox.showinfo("Weekly Summary", msg)

# ---------- GUI ----------
root = tk.Tk()
root.title("Smart Health Tracker")
root.geometry("400x520")

init_files()

# PROFILE
tk.Label(root, text="Name").pack()
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Age").pack()
age_entry = tk.Entry(root)
age_entry.pack()

tk.Label(root, text="Weight (kg)").pack()
weight_entry = tk.Entry(root)
weight_entry.pack()

tk.Label(root, text="Height (cm)").pack()
height_entry = tk.Entry(root)
height_entry.pack()

tk.Button(root, text="Save Profile", command=save_user).pack()
tk.Button(root, text="Calculate BMI", command=calculate_bmi).pack()

# INPUTS
tk.Label(root, text="Water (No. of Glasses)").pack()
water_entry = tk.Entry(root)
water_entry.pack()

tk.Label(root, text="Sleep (hrs)").pack()
sleep_entry = tk.Entry(root)
sleep_entry.pack()

# Activity Dropdown
tk.Label(root, text="Activity Level").pack()
activity_var = tk.StringVar(value="Medium")
tk.OptionMenu(root, activity_var, "Low", "Medium", "High").pack()

tk.Button(root, text="Add Entry", command=add_entry).pack()

# FEATURES
tk.Button(root, text="Show Streak", command=show_streak).pack()
tk.Button(root, text="Weekly Summary", command=weekly_summary).pack()

tk.Button(root, text="Exit", command=root.quit).pack()

root.mainloop()