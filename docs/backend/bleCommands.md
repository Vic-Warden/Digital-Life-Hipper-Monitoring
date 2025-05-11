# BLE commands<br>
Hipper ble commands documentation here

## 2001<br>
This command is used for synchronizing the current UTC time with the PAM device via BLE (UUID 2001).

This code scans for a PAM device, connects via Bluetooth, and writes the current timestamp as a 4-byte payload to the device.<br>
Structure based on PAM device BLE Interface Specification provided by Michel Oey:

Payload (4 bytes):<br>
Byte 0–3: Current UTC timestamp in seconds (uint32, little endian)

To use this command, the read_live_pam_data.py script runs the PAM_2001.run() function, which internally calls set_timestamp().<br>
The function scans for devices named "Pam", connects, and writes the time to the target characteristic. Progress is shown via console output.

## 2101<br>
this command is used for measuring the current data of the total value that is stored on the hipper device.

this code parses an 8-byte notification payload from the Pam Activity Data (UUID 2101).<br>
Structure based on PAM device BLE Interface Specification provided by Michel Oey:

Byte 0-1: Steps (uint16, little endian)<br>
Byte 2-3: Activity Score (uint16, little endian)<br>
Byte 4  : Lower 8 bits of Zone 3 (Sport)<br>
Byte 5  : Bit 0 = MSB of Zone 3<br>
          Bits 1-7 = Lower 7 bits of Zone 2 (Health)<br>
Byte 6  : Bits 0-3 = MSB of Zone 2<br>
          Bits 4-7 = Lower 4 bits of Zone 1 (Living)<br>
Byte 7  : MSB of Zone 1

to make use of this command the read_live_pam_data.py script is used to run the ActivityData() which is imported from the services file.

the function is used for making a client that receives data every few seconds from the PAM device which gets shown as a print statement into the console

## 2102<br>

This command is used to request the activity file from the PAM device. The command initiates the transfer of the stored activity data for a specified time period.

Command Format:

Byte 0: Low byte of file request command

Byte 1: High byte of file request command

The format of the request depends on the file being requested (e.g., day data file or 
detailed file). The requested data will be returned in the Activity Download characteristic. 
To start the data transfer, the Download notification must be enabled before sending the request.

To use this command, the read_pam_data.py script runs the ActivityFile() function, 
imported from the services file. This function sends the command to the device and provides 
simple feedback on whether the request was successful.
<br>
<br>
<br>
#### File duration size
in order to get a file we need to specify of how long we want data. sometimes we want to download the last hour of data, and sometimes we want to download the last
<br><br>
this code will mainly be used when data needs to be collected from a specified duration of time, in which case the time simply needs to be selected and then used while making a dataset.<br>
<br>
for the end user this code will mean that there could be a button added which makes use of this code to specifically show how much you scored (and in what ways) during the past hour or day
<br>
<br>
How to use the function:<br>
the code exists of a list that has a bunch of different byte values for different amounts of time indicators.<br>
<br>
<br>
What Identifier strings you can use:<br>
These can be accesed from the list using the get function as follows this (from src/back-end/pam):
````python
from PAM_2102 import get_detailed_request
get_detailed_request("MAX")
````


````
    last 15 min

    last 30 min

    last 1 hour

    last 3 hours

    last 6 hours

    last 12 hours

    last 15 hours

    last 24 hours

    last 3 days

    last 7 days

    last 14 days

    last 30 days

    max (full buffer)
````
Each of these identifiers is used to give a byte array of 2 bytes;<br>
Each two-byte command packs the number of 15-minute intervals you want (low byte + high byte’s lower 7 bits) in little-endian,
with the high byte’s MSB set to 1 to signal a detailed-file request.
<br>
these bytes were determined by the following logic from the PAM device documentation provided by Michel Oey from Hipper Therapeutics
<br><br>use this logic to add a new identifier to the list if needed

## 2103

this code can be used by importing the services file and using the ````ActivityDownload()```` function

it makes use of the 2102 command to request a file and then downloads it.
the data is sent in blocks of bytes, parsed using the following logic.

Skips block 0 (header), joins payloads in order, splits into 4-byte records, and extracts:
     - day offset (5 bits)
     - minute index (11 bits)
     - step count (1 byte)
     - raw score (1 byte ÷ 16)

#### storing as csv

the date data gets converted into seconds by multiplying by 86400.

the csv library is then used for writing the values into a csv file with the provided filename

then it gets stored using the following csv stucture:
Timestamp,Steps,PAM Score