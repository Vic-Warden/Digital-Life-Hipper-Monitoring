### Dataset

>The dataset for this project contains the following base data:

- Timestamp: `Datetime`
- Steps: `int`
- PAM Score: `float32`

>Here is a simple example of what the data looks like:

```csv
Timestamp,Steps,PAM Score
1970-02-01 18:06:00+00:00,0,0.0
1970-02-01 19:46:00+00:00,0,0.0
1970-02-02 00:02:00+00:00,5,0.44
1970-02-02 04:18:00+00:00,17,1.56
1970-02-02 08:34:00+00:00,2,0.19
1970-02-01 02:43:00+00:00,0,0.0
1970-02-01 06:59:00+00:00,14,0.75
1970-02-01 11:15:00+00:00,8,1.44
1970-02-01 15:31:00+00:00,6,2.06
1970-02-01 19:47:00+00:00,7,2.12
```

>In order to prepare the data we first need to get rid of the timestamp
>Afterwards we are left with this data:

```csv
Steps,PAM Score
0,0.0
0,0.0
5,0.44
17,1.56
2,0.19
0,0.0
14,0.75
8,1.44
6,2.06
7,2.12
```

>In order to use this data accurately, we should normalize it.
>To normalize the data, we scale the values of each column to a range between 0 and 1.
>
>Normalization ensures that the data is scaled appropriately, preventing any single feature from dominating the model due to its magnitude. This step is crucial for algorithms like Logistic Regression and K-Nearest Neighbors, which are sensitive to the scale of input features.
>
>The normalized dataset is shown below:

```csv
Steps,PAM Score
0.00,0.00
0.00,0.00
0.29,0.21
1.00,0.74
0.12,0.09
0.00,0.00
0.82,0.36
0.47,0.68
0.35,0.98
0.41,1.00
```

>This should be the finished dataset for our model

### AI Model

>As we are working with numeric data and our goal is to figure out what class a certain type of movement belongs to, we are constrained to classification algorithms.
>
>A few algorithms designed for classification are:

| **Algorithm**              | **Description**                                                        | **Specialty**                                                     |
| -------------------------- | ---------------------------------------------------------------------- | ----------------------------------------------------------------- |
| **Logistic Regression**    | Models the probability of class membership using a logistic function.  | Simple, fast, and effective for linearly separable data.          |
| **K-Nearest Neighbors**    | Classifies based on the majority label of the _k_ nearest data points. | Easy to implement; works well with small, labeled datasets.       |
| **Decision Tree**          | Splits data into branches based on feature values to make decisions.   | Interpretable model; handles both numerical and categorical data. |
| **Naive Bayes**            | Uses Bayes’ Theorem assuming independence between features.            | Fast and efficient, especially with high-dimensional data.        |
| **Support Vector Machine** | Finds the best boundary (hyperplane) that separates different classes. | Effective in high-dimensional spaces and with clear margins.      |
>We will start with Logistic Regression and K-NearestNeighbors. These algorithms are simple to implement and do not require much training.