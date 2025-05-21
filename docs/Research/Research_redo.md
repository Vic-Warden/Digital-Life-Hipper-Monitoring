# Old research
For working with the hipper device, we need to ensure that the data we get from the device is correct data that we can trust. The original developers for the device did some tests and had some problems with wearing 2 devices at the same time and getting different data from these devices. In their research they had a big difference in the PAM score and the amount of steps compared to the 2 devices. This should not happen because both made the same movements at the same time. This is something we have to fix, wich is why we need to do this research again. 

## The old research

## New results
These are the results of re doing the research

### Short term tests
We did a small test taping 2 devices together and doing a small walk of around 20-30minutes. These small term results with our code to pull the data gave us some very good results with not much difference in the results between the 2 devices. These results where mapped out in a [jupiter file](../../src/back-end/datasets/research/my_notebook.ipynb). The results were as follows:
![results](../assets/ResearchRedo/ShortTermResults.png)
The small differences seen in the PAM scores and steps could be due to that the devices only saves the data from entire minutes. These minutes can end at different moments on the devices because they are not reset at the exact same time. This means that their could be small differences. The rest of these results look pretty promissing with the results being almost the same. 

### long term tests