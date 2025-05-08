# DataVisualizer

The `DataVisualizer` class provides a set of visualization tools for exploring time-series physical activity data, such as **PAM scores** and **step counts**.

## 📦 Constructor

```python
DataVisualizer(data)
```

- **data** (`pandas.DataFrame`): The input data must contain the following columns:
  - `'Timestamp'`: Datetime values representing time
  - `'PAM Score'`: Numeric values representing the physical activity metric
  - `'Steps'`: Numeric values representing step counts

---

## 📊 Methods

### `plot_pam_score_over_time()`

Plots the **PAM Score** over time using a Seaborn line plot.

- **X-axis**: Timestamp  
- **Y-axis**: PAM Score  
- **Style**: Whitegrid background with circular markers

---

### `plot_steps_over_time()`

Plots the **number of steps** over time using a Seaborn line plot.

- **X-axis**: Timestamp  
- **Y-axis**: Steps  
- **Style**: Whitegrid background with orange square markers

---

### `plot_dual_axis()`

Generates a **dual-axis plot** to visualize both Steps and PAM Score on the same time axis.

- **Left Y-axis**: Steps (green line)  
- **Right Y-axis**: PAM Score (blue line)  
- **X-axis**: Timestamp  
- **Overlay**: Two y-axes sharing the same x-axis

---

