# Learning Journal
This file contains the learning journal with the learning story's of Mike.

# Learning stories:

## As a student I want to learn how store a bunch of different hardcoded values and get them on demand when needed so that I can store important values separately 

I managed to get this working using a python dictionary which stores all the data.<br>
developers can easilly add new values to this by simply adding a new entry.

````python

def get_detailed_request(name: str) -> bytearray:
    detailed_requests = {
        "LAST_15_MIN":    bytearray([0x01, 0x80]),
        "LAST_30_MIN":    bytearray([0x02, 0x80]),
        "LAST_1_HOUR":    bytearray([0x04, 0x80]),
        "LAST_3_HOURS":   bytearray([0x0C, 0x80]),
        "LAST_6_HOURS":   bytearray([0x18, 0x80]),
        "LAST_12_HOURS":  bytearray([0x30, 0x80]),
        "LAST_15_HOURS":  bytearray([0x3C, 0x80]),
        "LAST_1_DAY":  bytearray([0x60, 0x80]),
        "LAST_3_DAYS":    bytearray([0x20, 0x81]),
        "LAST_7_DAYS":    bytearray([0xA0, 0x82]),
        "LAST_14_DAYS":   bytearray([0x40, 0x85]),
        "LAST_30_DAYS":   bytearray([0xC0, 0x8B]),
        "MAX":            bytearray([0x00, 0x8C]),
    }

    try:
        return detailed_requests[name.upper()]
    except KeyError:
        raise ValueError(f"Invalid request name '{name}'. Available options: {', '.join(detailed_requests.keys())}")


````

these values can't be changed from the end user's perspective but can easilly be fetched using the 'detailed_requests' function (if the wanted data exists)
````python
get_detailed_request("MAX")
````

## As a student I want to learn how to use the python bleak library so that I can make use of bluetooth communications in python code 

I learned that in order to make use of BLE communications you always need to start by making a bluetooth connection. this can be done by first scanning all bluetooth devices for a name in order to get the address of that device,
and from there it's easiest to just directly sent a message to the bluetooth device.

I learned that in order to send messages to the PAM device, you need to use this connection to send a command to that address using a uuid. this uuid then contains a few characters for the wanted action (specified by the documentation)
<br> in python this can be done with the bleak library as follows;

the connection to the PAM device using the bleak library can be made as follows;<br>
````python
print("Scanning for BLE devices...")
devices = await BleakScanner.discover(timeout=5)

pam_device = None
for device in devices:
    print(f"- {device.name} [{device.address}]")
    if device.name and "Pam" in device.name:
        pam_device = device
        break

if not pam_device:
    print("Pam sensor not found.")
    return

print(f"\nConnecting to {pam_device.name}...")
async with BleakClient(pam_device.address
````

and a message can then be sent to this BLE device using the following code;
````python
await client.write_gatt_char(self.ACTIVITY_FILE_UUID, self.REQUEST_AMOUNT_TYPE)
print("Requested activity file...")
````

In order to receive messages over BLE you python code needs to work as a client that waits untill it gets a message.<br>
in python code this works via a callback function that gets triggered when a message is received.<br>
````python
#callback for when a new block of bytes is received
def notification_handler(self, sender, data):
    block_number = int.from_bytes(data[:2], byteorder='little')
    payload = data[2:]
    self.received_blocks[block_number] = payload
    print(f"Received block #{block_number} with {len(payload)} bytes")

await client.start_notify(self.ACTIVITY_DOWNLOAD_UUID, self.notification_handler)
````

## As a student I want to learn how to parse the bytes that come in the download of the 2103 BLE command so that I can get usefull data from the device 
I learned that the data exists of multiple byte blocks of 100 bytes each containing 4 byte chunks for data.
these are in the following structure:
Each chunk is decoded into:

day_offset: days after the base date (5 bits).

minute_offset: minutes into that day (11 bits).

step_count: number of steps.

pam_score: score scaled down by dividing by 16.



I integrated this into the code as follows:
I first make one giant data package from all the blocks of 100 bytes and then I go over it in chunks of 4 and decode each as shown above.

````python
# Split into 4‑byte records and unpack
activity_records: list[tuple[int, int, int, float]] = []
record_size = 4
for offset in range(0, len(full_data_stream), record_size):
    record_bytes = full_data_stream[offset: offset + record_size]
    if len(record_bytes) < record_size:
        break  # incomplete tail, ignore

    # first two bytes: combined bitfields
    bitfield = int.from_bytes(record_bytes[0:2], byteorder='little')
    day_offset = bitfield & 0x1F  # lower 5 bits: days since base date
    minute_offset = (bitfield >> 5) & 0x7FF  # next 11 bits: minutes into that day

    # third byte: steps count
    step_count = record_bytes[2]

    # fourth byte: raw PAM score, must be divided by 16 for the actual value
    raw_pam_score = record_bytes[3]
    pam_score = raw_pam_score / 16.0

    activity_records.append((day_offset, minute_offset, step_count, pam_score))
````
## As a student I want to learn how to make a json to store adresses of pam devices so that I can easilly use them
I stored all the values I wanted into a JSON structure:
````json
{
  "label_90243": "C1:08:00:01:12:33",
  "label_90248": "C1:08:00:01:36:3A"
}
````
I learned that I can use the json library to then export this and make use of it inside a python script.<br>
I learned that I had to include error handling in order to make sure that the code wouldn't crash if you called the wrong value

````python

# checks the PAM_devices.json and returns the desired mac addres if asked for
def get_address_by_label(label_id = None, filename="PAM_devices.json"):
    if label_id is None:
        return None
    label_id = "label_" + str(label_id)
    try:
        with open(filename, "r") as f:
            labels = json.load(f)
        return labels.get(label_id, "Label ID not found.")
    except FileNotFoundError:
        return "File not found."
    except json.JSONDecodeError:
        return "Error decoding JSON."
````

#   As a student I want to learn how to correctly structure a front end file structure 

##### Web page file template
I learned that each web page should exist of a html, js and css file.
In order to correctly link the css and js files to the html file I need to include them into the header using the following structure

````html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Blank Page</title>
  <link rel="stylesheet" href="../static/css/home.css" />
</head>
<body>

  <!-- Content goes here -->

  <script src="../static/js/home.js"></script>
</body>
</html>

````

#####  File structures
I learned that the file structure is as follows:<br>

the templates folder had all the html files,<br>
the static folder has the css and js files in their folders as well as all the assets like fonts and images.

I learned this by asking it to my peers as well as form the following sources:
https://www.youtube.com/watch?v=tBep6Nhq5gc 

https://www.youtube.com/watch?v=aNt2s0sXltk 

![structure.png](..%2Fassets%2Fstructure.png)


# As a student I want to learn how to use AI models in order to predict labels 
<br>
I learned that for classifications taks like predicting labels I need certain model.<br>
In my case since the data was about dividing it I learned that I needed to use a simple model like Decision tree of Random forest.<br>
first the data has to be split up in train and test data, and after that the data can be used to train the model.<br>
In oder to find the best parameters for the AI model I learned to use a gridsearch option in order to finetune to the best parameters.<br>

````python
# =============================================================================
# 4) SET UP A PIPELINE: SCALER + RANDOM FOREST CLASSIFIER
# =============================================================================

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('rf', RandomForestClassifier(random_state=42, n_jobs=-1))
])

# =============================================================================
# 5) HYPERPARAMETER TUNING (OPTIONAL)
# =============================================================================

# Example grid for RandomForest parameters
param_grid = {
    'rf__n_estimators': [100, 200],
    'rf__max_depth': [None, 10, 20],
    'rf__min_samples_split': [2, 5],
    'rf__min_samples_leaf': [1, 2]
}

grid_search = GridSearchCV(
    estimator=pipeline,
    param_grid=param_grid,
    cv=5,
    scoring='accuracy',
    n_jobs=-1,
    verbose=1
)

print("Starting grid search for best hyperparameters...\n")
grid_search.fit(X_train, y_train)
print(f"Best CV score: {grid_search.best_score_:.4f}")
print("Best parameters:")
print(grid_search.best_params_, "\n")

# Use the best estimator from grid search
best_model = grid_search.best_estimator_
````





# As a student I want to learn how to use AI clustering in order to find clusters inside of data 
<br>
I learned how to use KMeans clustering in order to make clusters of the data.
<br>
I learned how to use an intertia plot in order to see how many clusteres there are based on where the inertia flattens out and stops finding new good clusters<br>

![inertia_clustering_learnings.png](..%2Fassets%2Finertia_clustering_learnings.png)

and then I used KMeansclustering to find the following clusters<br>

![Clustering_learnings_mike.png](..%2Fassets%2FClustering_learnings_mike.png)

<br>

I leared how to use the following code to achieve this.<br>
````python
kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(scaled_data)
````