## Importing data locally with PowerBI

1. Open Power BI Desktop

Make sure you have Power BI Desktop installed.

2. Get Data from Folder

Click Home → Get Data → Folder.
Navigate to the folder on your computer where the .csv files are stored.
Click OK.

3. View Folder Contents

Power BI will display the files in the folder.
Click Combine & Transform Data.

4. Power Query Editor Launches

You'll now be inside Power Query Editor with a preview.
Power BI shows a sample file to use as a template for combining all others.

You can:
Remove unnecessary columns (like Source.Name if not needed).
Apply transformations (change column types, remove headers, etc.).

5. Transform Data (Optional)

In Power Query, you can clean or manipulate your data before loading it:
Remove unwanted rows (e.g., header rows in each file if repeated).
Change column names and types.

6. Load Data

Once done:
Click Close & Load.
Power BI will import and mash together all the .csv files from the folder into a single table.

7. Refresh Automatically

Each time you refresh the data:
Power BI will re-read the folder and automatically combine any new .csv files added there.