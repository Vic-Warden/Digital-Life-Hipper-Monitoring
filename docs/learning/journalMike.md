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


