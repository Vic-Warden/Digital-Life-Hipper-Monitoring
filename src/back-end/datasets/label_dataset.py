import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import SpanSelector
import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv('artificial_1h_data.csv')
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df['Timestamp'] = df['Timestamp'].dt.strftime('%Y-%m-%d-%H-%M-%S')
df = df.sort_values('Timestamp')
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

        # Convert xmin and xmax from matplotlib float dates to datetime
        xmin_dt = pd.to_datetime(
            df['Timestamp'].iloc[0]) + pd.to_timedelta(xmin, 'D')
        xmax_dt = pd.to_datetime(
            df['Timestamp'].iloc[0]) + pd.to_timedelta(xmax, 'D')

        # Print the converted xmin and xmax for debugging
        print(f"xmin_dt: {xmin_dt}, xmax_dt: {xmax_dt}")

        # Create a mask for the DataFrame
        mask = (df_labeled['Timestamp'] >= xmin_dt) & (
            df_labeled['Timestamp'] <= xmax_dt)

        # Print the mask to debug
        print(mask)

        # Ensure that the 'Label' column is updated correctly for the selected region
        df_labeled.loc[mask, 'Label'] = label

        # Print the updated DataFrame for debugging
        print(df_labeled)

        # Highlight region on the plot
        ax1.axvspan(xmin, xmax, color='gray', alpha=0.3)

        # Add label text in the middle of the region
        x_center = xmin + (xmax - xmin) / 2
        y_max = df['Steps'].max()
        ax1.text(x_center, y_max * 0.95, label, color='black', ha='center',
                 fontsize=9, bbox=dict(facecolor='white', alpha=0.6, edgecolor='none'))

        # Redraw the canvas to update the plot with the new region
        canvas.draw()


assign_button = tk.Button(left_frame, text="Assign", command=assign_label)
assign_button.pack(pady=5)

# Export function


def export():
    # Export the updated labeled DataFrame to CSV
    df_labeled.to_csv("labeled_output.csv", index=False)
    print("Exported to labeled_output.csv")


# Export button
export_button = tk.Button(left_frame, text="Export to CSV", command=export)
export_button.pack(pady=5)

# Main plot area
fig, ax1 = plt.subplots(figsize=(10, 5))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

ax1.set_xlim(df['Timestamp'].min(), df['Timestamp'].max())

# Plot data
ax2 = ax1.twinx()
ax1.plot(df['Timestamp'], df['Steps'], label='Steps', color='blue')
ax2.plot(df['Timestamp'], df['PAM Score'],
         label='PAM Score', color='green')

# Labels and legend
ax1.set_xlabel("Time")
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
