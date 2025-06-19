import pandas as pd
import joblib

class EntryPredictor:
    """
    A predictor class that loads a decision tree model and predicts a label for a single entry.
    Usage:
        predictor = EntryPredictor(model_path)
        single_label = predictor.predict_entry(timestamp, steps, pam_score)
    """

    def __init__(self, model_path: str):
        """
        Initialize the predictor by loading the trained model.

        Args:
            model_path: Path to the saved decision tree model (joblib file).
        """
        self.model = joblib.load(model_path)
        if hasattr(self.model, 'feature_names_in_'):
            self.features = list(self.model.feature_names_in_)
        else:
            self.features = None

    def predict_entry(self, timestamp: str, steps: int, pam_score: float):
        """
        Predict the label for a single data entry.

        Args:
            timestamp: ISO-format timestamp string, e.g. "2025-06-04 14:00:00".
            steps: Number of steps recorded at that timestamp.
            pam_score: The PAM Score recorded at that timestamp.

        Returns:
            The predicted label.
        """
        # Build a one-row DataFrame
        df_row = pd.DataFrame([{
            'Timestamp': timestamp,
            'Steps': steps,
            'PAM Score': pam_score
        }])

        # Select appropriate features
        if self.features is not None:
            X = df_row[self.features]
        else:
            X = df_row.select_dtypes(include='number')

        # Predict and return label
        return self.model.predict(X)[0]



# usage example:
predictor = EntryPredictor('./static/HipperLabeler.joblib')
label = predictor.predict_entry(
    timestamp='2025-06-04 14:00:00',
    steps=86,
    pam_score=6
)
print(label)