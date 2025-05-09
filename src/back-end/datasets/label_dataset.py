# This script loads a dataset from a specified file path and displays the first few rows of the dataset.

import matplotlib.pyplot as plt
import pandas as pd

# Load the dataset as a DataFrame
file_path = 'artificial_1h_data.csv'
df = pd.read_csv(file_path)

# Plot the data
df.plot(figsize=(15, 8))
plt.title('Label Dataset')
plt.xlabel('Time (minutes)')
plt.ylabel('Values')
plt.legend(loc='best')
plt.grid(True)
plt.show()
