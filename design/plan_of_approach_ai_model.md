# Plan of Approach for AI Model

### Dataset

The dataset for this project contains the following base data:

- Timestamp: `Datetime`
- Steps: `int`
- PAM Score: `float32`

Here is a simple example of what the data looks like:

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

?? What is the time between every entry ??

In order to prepare all the data for training, the data should be split up into multiple parts of (for example) 5 or 10 second parts. This gives each individual entry in the 

### AI Model

#### Clustering