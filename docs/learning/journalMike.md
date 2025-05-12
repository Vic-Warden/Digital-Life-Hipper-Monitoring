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