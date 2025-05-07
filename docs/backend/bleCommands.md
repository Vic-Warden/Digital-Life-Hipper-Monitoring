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