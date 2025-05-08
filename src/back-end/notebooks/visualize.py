import matplotlib.pyplot as plt
import seaborn as sns


class DataVisualizer:
    def __init__(self, data):
        self.data = data

    def plot_pam_score_over_time(self):
        sns.set(style="whitegrid")
        plt.figure(figsize=(12, 6))
        sns.lineplot(x=self.data['Timestamp'],
                     y=self.data['PAM Score'], marker='o')
        plt.title('PAM Score Over Time')
        plt.xlabel('Timestamp')
        plt.ylabel('PAM Score')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_steps_over_time(self):
        sns.set(style="whitegrid")
        plt.figure(figsize=(12, 6))
        sns.lineplot(x=self.data['Timestamp'],
                     y=self.data['Steps'], marker='s', color='orange')
        plt.title('Steps Over Time')
        plt.xlabel('Timestamp')
        plt.ylabel('Steps')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_dual_axis(self):
        fig, ax1 = plt.subplots(figsize=(12, 6))
        ax2 = ax1.twinx()
        ax1.plot(self.data['Timestamp'],
                 self.data['Steps'], 'g-', label='Steps')
        ax2.plot(self.data['Timestamp'],
                 self.data['PAM Score'], 'b-', label='PAM Score')

        ax1.set_xlabel('Timestamp')
        ax1.set_ylabel('Steps', color='g')
        ax2.set_ylabel('PAM Score', color='b')
        ax1.tick_params(axis='x', rotation=45)
        plt.title('Steps and PAM Score Over Time')
        fig.tight_layout()
        plt.show()
