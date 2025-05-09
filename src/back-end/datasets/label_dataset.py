import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import SpanSelector
import pandas as pd
import numpy as np

# Load and prepare dataset
df = pd.read_csv('artificial_1h_data.csv')
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df = df.sort_values('Timestamp').reset_index(drop=True)
df['Label'] = ""  # New column to store assigned labels

# Track label regions
assigned_regions = []

# GUI setup
root = tk.Tk()
root.title("PAM Label Assignment Tool")

left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, padx=10, pady=10)

# Label dropdown
label_var = tk.StringVar()
label_options = ["Walking", "Running", "Jumping", "Idle"]
label_dropdown = ttk.Combobox(
    left_frame, textvariable=label_var, values=label_options)
label_dropdown.current(0)
label_dropdown.pack(pady=5)

# Plot area
fig, ax1 = plt.subplots(figsize=(10, 5))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Twin axis
ax2 = ax1.twinx()
ax1.plot(df['Timestamp'], df['Steps'], label='Steps', color='blue')
ax2.plot(df['Timestamp'], df['PAM Score'],
         label='PAM Score', color='green')

ax1.set_xlim(df['Timestamp'].min(), df['Timestamp'].max())

# Labels and grid
ax1.set_xlabel("Time")
ax1.set_ylabel("Steps", color='blue')
ax2.set_ylabel("PAM Score", color='green')
ax1.set_title("Select a region and assign a label")
ax1.grid(True)

# Region selector
selected_region = []


def onselect(xmin, xmax):
    selected_region.clear()
    selected_region.extend([xmin, xmax])

# Assign label to selected time region


def assign_label():
    if selected_region:
        xmin, xmax = selected_region
        label = label_var.get()

        # Assign to DataFrame
        mask = (df['Timestamp'] >= pd.to_datetime(xmin, unit='s')) & (
            df['Timestamp'] <= pd.to_datetime(xmax, unit='s'))
        df.loc[mask, 'Label'] = label

        # Draw region and label
        ax1.axvspan(pd.to_datetime(xmin, unit='s'), pd.to_datetime(
            xmax, unit='s'), color='gray', alpha=0.3)
        x_center = xmin + (xmax - xmin) / 2
        y_max = df['Steps'].max()
        ax1.text(pd.to_datetime(x_center, unit='s'), y_max * 0.95, label, color='black', ha='center', fontsize=9,
                 bbox=dict(facecolor='white', alpha=0.6, edgecolor='none'))

        canvas.draw()
        assigned_regions.append((label, xmin, xmax))


# Assign button
assign_button = tk.Button(left_frame, text="Assign", command=assign_label)
assign_button.pack(pady=5)

# Export labeled dataset


def export():
    df.to_csv("labeled_output.csv", index=False)
    print("Exported to labeled_output.csv")


export_button = tk.Button(left_frame, text="Export to CSV", command=export)
export_button.pack(pady=20)

# Enable span selector
span = SpanSelector(ax1, onselect, 'horizontal', useblit=True,
                    props=dict(alpha=0.5, facecolor='red'), interactive=True)

# Launch GUI
root.mainloop()
