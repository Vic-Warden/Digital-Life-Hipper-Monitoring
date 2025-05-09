import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import SpanSelector
import pandas as pd
import numpy as np

DATASET_PATH = 'artificial_1h_data.csv'

# Load dataset and convert timestamps to Unix time
df = pd.read_csv(DATASET_PATH)
df['Timestamp'] = pd.to_datetime(df['Timestamp'], utc=True, errors='coerce')
df['UnixTime'] = df['Timestamp'].astype(np.int64) // 10**9
df = df.sort_values('UnixTime')
df_labeled = df.copy()
df_labeled['Label'] = ""

# Store label assignments: (label, xmin, xmax)
assigned_regions = []

# GUI Window
root = tk.Tk()
root.title("PAM Label Assignment Tool")

# Left frame for controls
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, padx=10, pady=10)

# Label dropdown
label_var = tk.StringVar()
label_options = ["Walking", "Running", "Jumping", "Idle"]
label_dropdown = ttk.Combobox(
    left_frame, textvariable=label_var, values=label_options)
label_dropdown.current(0)
label_dropdown.pack(pady=5)

# Assign button


def assign_label():
    if selected_region:
        xmin, xmax = selected_region
        label = label_var.get()
        assigned_regions.append((label, xmin, xmax))

        # Create a mask for the Unix time range
        mask = (df_labeled['UnixTime'] >= xmin) & (
            df_labeled['UnixTime'] <= xmax)
        df_labeled.loc[mask, 'Label'] = label

        # Highlight region on the plot
        ax1.axvspan(xmin, xmax, color='gray', alpha=0.3)

        # Add label text in the middle of the region
        x_center = xmin + (xmax - xmin) / 2
        y_max = df['Steps'].max()
        ax1.text(x_center, y_max * 0.95, label, color='black', ha='center',
                 fontsize=9, bbox=dict(facecolor='white', alpha=0.6, edgecolor='none'))

        canvas.draw()


assign_button = tk.Button(left_frame, text="Assign", command=assign_label)
assign_button.pack(pady=5)

# Export function


def export():
    df_labeled.to_csv("labeled_output.csv", index=False)
    print("Exported to labeled_output.csv")


export_button = tk.Button(left_frame, text="Export to CSV", command=export)
export_button.pack(pady=5)

# Main plot area
fig, ax1 = plt.subplots(figsize=(10, 5))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Plot using Unix time
ax1.set_xlim(df['UnixTime'].min(), df['UnixTime'].max())
ax2 = ax1.twinx()
ax1.plot(df['UnixTime'], df['Steps'], label='Steps', color='blue')
ax2.plot(df['UnixTime'], df['PAM Score'], label='PAM Score', color='green')

# Labels and legend
ax1.set_xlabel("Unix Time")
ax1.set_ylabel("Steps", color='blue')
ax2.set_ylabel("PAM Score", color='green')
ax1.set_title("Select a region and assign a label")
ax1.grid(True)

# SpanSelector
selected_region = []


def onselect(xmin, xmax):
    selected_region.clear()
    selected_region.extend([xmin, xmax])


span = SpanSelector(ax1, onselect, 'horizontal', useblit=True,
                    props=dict(alpha=0.5, facecolor='red'), interactive=True)

root.mainloop()
