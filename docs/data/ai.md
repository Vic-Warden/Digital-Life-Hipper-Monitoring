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
we have only 3 features we can use for predictions,<br>
so a decision tree model was chosen for to use for the predictions since we are working with clusters that have clear borders between them.<br>
<br> exeriments with other models was done (random forest, SVM and logistic regression) but decision tree turned out to be the best one.<br>

## output:
the output of the labels can best be viewed using bar plots of the pam score throughout a day, the image below shows an example of this.<br>
![labeled_data_example.png](..%2Fassets%2Flabeled_data_example.png)
<br> in this example image of the labeled data you can see by the different colors where the device wearer was walking a lot, and when the device wearer was not walking a lot of sitting still for periods of time. 

## usage
there are 2 things you need to know about the AI model when trying to use the model.<br>
and that is how to run the re-training scripts, and how to use the model for predictions.<br>

##### - retraining the model
if you have new data, and thus want to retrain the model, do the following steps:<br>
run the full notebook located at ./src/back-end/AI/training_data/generate_training_data.ipynb<br>
and then in order to train a new model on the new dataset, run the full notebook located at train_model.ipynb<br>
you can then use the new AI model you have inside of the backend.

##### - making predictions
the file ./src/app/zone_classifier.py contains a class that loads the models with the init, and then has a function in order to do single predictions with the date.<br>
an example of what this could look like is given at the bottom of that python script.

# sources used:
Chatgtp was used in order to clean up and comment the python codes.