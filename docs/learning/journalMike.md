# Learning Journal
This file contains the learning journal with the learning story's of Mike.

# learning stories:

### As a student I want to learn how to use the python bleak library so that I can make use of bluetooth communications in python code 

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