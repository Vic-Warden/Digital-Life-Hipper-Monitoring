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

