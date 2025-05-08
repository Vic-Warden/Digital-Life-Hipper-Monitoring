import pandas as pd
import numpy as np
from datetime import datetime
import random

# Create a start and end time
start_time = datetime(1970, 2, 1, 18, 0)
end_time = datetime(1970, 2, 10, 0, 0)

# Generate timestamps at 1-minute intervals
timestamps = pd.date_range(start=start_time, end=end_time, freq='1T')

# Simulate gaps by randomly removing some timestamps (e.g. 20% inactivity)
timestamps = timestamps.delete(np.random.choice(
    len(timestamps), size=int(0.2 * len(timestamps)), replace=False))

# Generate random step and PAM Score values for the remaining timestamps
data = {
    "Timestamp": timestamps,
    "Steps": [random.choice([0, 0, 0, random.randint(1, 20)]) for _ in range(len(timestamps))],
    "PAM Score": [round(random.uniform(0.0, 2.0), 2) if random.random() > 0.3 else 0.0 for _ in range(len(timestamps))]
}

df = pd.DataFrame(data)
df.to_csv("artificial_movement_data.csv", index=False)
