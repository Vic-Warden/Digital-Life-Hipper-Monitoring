# This script loads a dataset from a specified file path and displays the first few rows of the dataset.

import matplotlib.pyplot as plt
import pandas as pd


class ActivityPlotter:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self._load_data()

    def _load_data(self):
        """Load and preprocess the CSV data."""
        self.df = pd.read_csv(self.file_path)
        self.df['Timestamp'] = pd.to_datetime(self.df['Timestamp'])
        self.df = self.df.sort_values('Timestamp')

    def plot(self):
        """Plot Steps and PAM Score with dual Y-axes."""
        fig, ax1 = plt.subplots(figsize=(15, 8))

        # Plot Steps (primary Y-axis)
        ax1.plot(self.df['Timestamp'], self.df['Steps'],
                 color='blue', label='Steps')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Steps', color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')

        # Plot PAM Score (secondary Y-axis)
        ax2 = ax1.twinx()
        ax2.plot(self.df['Timestamp'], self.df['PAM Score'],
                 color='green', label='PAM Score')
        ax2.set_ylabel('PAM Score', color='green')
        ax2.tick_params(axis='y', labelcolor='green')

        # Title and legend
        plt.title('Steps and PAM Score Over Time')
        ax1.grid(True)

        # Combine legends
        lines_1, labels_1 = ax1.get_legend_handles_labels()
        lines_2, labels_2 = ax2.get_legend_handles_labels()
        ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

        plt.tight_layout()
        plt.show()


plotter = ActivityPlotter('artificial_1h_data.csv')
plotter.plot()
