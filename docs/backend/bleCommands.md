# BLE commands<br>
Hipper ble commands documentation here

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

## 2103

this code can be used by importing the services file and using the ````ActivityDownload()```` function

it makes use of the 2102 command to request a file and then downloads it.
the data is sent in blocks of bytes, parsed using the following logic.

Skips block 0 (header), joins payloads in order, splits into 4-byte records, and extracts:
     - day offset (5 bits)
     - minute index (11 bits)
     - step count (1 byte)
     - raw score (1 byte ÷ 16)
