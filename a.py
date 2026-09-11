

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
            writer = csv.writer(f)
            writer.writerow(["Date", "Water", "Sleep", "Steps"])

    if not os.path.exists(GOAL_FILE):
        with open(GOAL_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["WaterGoal", "SleepGoal", "StepsGoal"])
            writer.writerow([3, 7, 8000])

# ---------- USER PROFILE ----------
def save_user():
    with open(USER_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([name_entry.get(), age_entry.get(), weight_entry.get(), height_entry.get()])
    messagebox.showinfo("Saved", "User Profile Saved")

# ---------- BMI ----------
def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get()) / 100
        bmi = weight / (height * height)

        if bmi < 18.5:
            status = "Underweight"
        elif bmi < 25:
            status = "Normal"
        elif bmi < 30:
            status = "Overweight"
        else:
            status = "Obese"

        messagebox.showinfo("BMI", f"BMI: {bmi:.2f}\nStatus: {status}")
    except:
        messagebox.showerror("Error", "Enter valid weight/height")

# ---------- LOAD GOALS ----------
def load_goals():
    with open(GOAL_FILE, 'r') as f:
        data = list(csv.reader(f))
        return list(map(float, data[1]))

# ---------- UPDATE GOALS ----------
def update_goals():
    try:
        w = float(goal_water.get())
        s = float(goal_sleep.get())
        st = int(goal_steps.get())

        with open(GOAL_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["WaterGoal", "SleepGoal", "StepsGoal"])
            writer.writerow([w, s, st])

        messagebox.showinfo("Success", "Goals Updated")
    except:
        messagebox.showerror("Error", "Invalid goals")

# ---------- ADD ENTRY ----------
def add_entry():
    try:
        date = datetime.now().strftime("%Y-%m-%d")
        water = float(water_entry.get())
        sleep = float(sleep_entry.get())
        steps = int(steps_entry.get())

        with open(DATA_FILE, 'a', newline='') as f:
            csv.writer(f).writerow([date, water, sleep, steps])

        give_feedback(water, sleep, steps)
        messagebox.showinfo("Success", "Entry Added")

    except:
        messagebox.showerror("Error", "Invalid input")

# ---------- FEEDBACK ----------
def give_feedback(w, s, st):
    gw, gs, gst = load_goals()
    msg = "\nFeedback:\n"

    msg += "\nWater: " + ("Good" if w >= gw else "Low")
    msg += "\nSleep: " + ("Good" if s >= gs else "Low")
    msg += "\nSteps: " + ("Good" if st >= gst else "Low")

    messagebox.showinfo("Feedback", msg)

# ---------- STREAK ----------
def show_streak():
    gw, gs, gst = load_goals()
    streak = 0

    with open(DATA_FILE, 'r') as f:
        rows = list(csv.DictReader(f))

    for row in reversed(rows):
        if float(row['Water']) >= gw and float(row['Sleep']) >= gs and int(row['Steps']) >= gst:
            streak += 1
        else:
            break

    messagebox.showinfo("Streak", f"🔥 {streak} days")

# ---------- WEEKLY SUMMARY ----------
def weekly_summary():
    last_week = datetime.now() - timedelta(days=7)
    water = sleep = steps = count = 0

    with open(DATA_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if datetime.strptime(row['Date'], "%Y-%m-%d") >= last_week:
                water += float(row['Water'])
                sleep += float(row['Sleep'])
                steps += int(row['Steps'])
                count += 1

    if count == 0:
        messagebox.showinfo("Summary", "No recent data")
        return

    msg = f"Last 7 Days:\nWater Avg: {water/count:.2f}\nSleep Avg: {sleep/count:.2f}\nSteps Avg: {steps//count}"
    messagebox.showinfo("Weekly Summary", msg)

# ---------- GUI ----------
root = tk.Tk()
root.title("Smart Health Tracker")
root.geometry("400x500")

init_files()

# USER PROFILE
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

# ENTRY
tk.Label(root, text="Water").pack()
water_entry = tk.Entry(root)
water_entry.pack()

tk.Label(root, text="Sleep").pack()
sleep_entry = tk.Entry(root)
sleep_entry.pack()

tk.Label(root, text="Steps").pack()
steps_entry = tk.Entry(root)
steps_entry.pack()

tk.Button(root, text="Add Entry", command=add_entry).pack()

# GOALS
tk.Label(root, text="Set Goals").pack()
goal_water = tk.Entry(root)
goal_water.pack()
goal_sleep = tk.Entry(root)
goal_sleep.pack()
goal_steps = tk.Entry(root)
goal_steps.pack()

tk.Button(root, text="Update Goals", command=update_goals).pack()

# FEATURES
tk.Button(root, text="Show Streak", command=show_streak).pack()
tk.Button(root, text="Weekly Summary", command=weekly_summary).pack()

tk.Button(root, text="Exit", command=root.quit).pack()

root.mainloop()
