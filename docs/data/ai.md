# AI
documentation about the AI here

## Clustering
In order to find out how many labels we want to use when labeling the data we used a clustering model to determine the optimal amount of labels inside the data.<br>
<br>
we used KMeans clustering and came out on 3 clusters.

the details of how this was achieved can be found inside the src/back-end/AI/DataClusterngAnalysis.ipynb notebook.<br>
<br><br>
but the main gist of it comes down to the following:<br><br>
multiple activity files were imported and then put into a single dataframe.<br>
the timestamps were dropped since we deemed those to not be representative of the target audience.<br>
nor did they provide a meaninguful impact on the data.<br>
<br>
a standard scaler was then used to normalize the data.<br>
after which a basic KMeans clustering model was used on the data.<br>
From the inertia plot you could see how the optimal number of clusters was 3.<br>
<br>for a more visual impact we also used the KMeans on multiple variables of clusters to see what the impact was, and since our data was only in 2 dimensions we could easilly visualise the plots along 2 axis.<br>

## Trainings data
the training data exists from the labels that came from the clustered data from the previous clustering work.<br>
these clusters were exported as a label inside of a trainings data .csv file.<br>

## The model
we have only 3 features we can use for predictions, 

## usage

### retraining the model

### making predictions
