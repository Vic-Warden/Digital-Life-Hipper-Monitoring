# Learning Journal
This file contains the learning journal with the learning story's of Bryan van Riesen. 

## Learning story 1
As a student I want to learn how the communication with the hipper device functions and how that can be implemented, so that I can use this information to communicate with the hipper divce 

### Learned
To communicate with the Hipper device, I use Bluetooth Low Energy (BLE) protocols wich is specified in the [Pam BLE Specs file](../assets/Pam_BLE_Spec_V1_8.pdf). The device supports both standard and custom BLE services. This allows me to communicate with the device with a specific set of codes. 

The device has an activity service (UUID 0x2100) that provides data from the device's activity. To make sure this data is saved on the device, I send the 2102 command to the device. This prepares the data that can then be requested using the 2103 command. 

I implemented a part of this communication by making a BLE connection with the hipper device and then writing the 2102 command to make a request to the device. 

This implementation shows my understanding of the BLE communication with the hipper device and that I understand how to use the device. 

## Learning story 2
As a student I want to learn how I can pull raw data from the hipper monitor so that we can create datasets using the raw accelerometer data.

### Learned
The code used for pulling raw data does not work with the regular hipper monitor and its software that it has. The device can only make use of the standard communication with sending the steps and regular data it is supposed to send. Looking at the code that was sent by the developer that he used to pull raw data, he uses different bits to communicate with the device. Using some simple test code written in open_ble_services.py, we can see that the device has the following services:
<pre>
Service 00001801-0000-1000-8000-00805f9b34fb:
  Characteristic 00002a05-0000-1000-8000-00805f9b34fb, properties: ['indicate']
  Characteristic 00002b29-0000-1000-8000-00805f9b34fb, properties: ['read', 'write']
  Characteristic 00002b2a-0000-1000-8000-00805f9b34fb, properties: ['read']
Service 00001800-0000-1000-8000-00805f9b34fb:
  Characteristic 00002a00-0000-1000-8000-00805f9b34fb, properties: ['read']
  Characteristic 00002a01-0000-1000-8000-00805f9b34fb, properties: ['read']
  Characteristic 00002a04-0000-1000-8000-00805f9b34fb, properties: ['read']
Service 0000180a-0000-1000-8000-00805f9b34fb:
  Characteristic 00002a23-0000-1000-8000-00805f9b34fb, properties: ['read']
  Characteristic 00002a24-0000-1000-8000-00805f9b34fb, properties: ['read']
  Characteristic 00002a25-0000-1000-8000-00805f9b34fb, properties: ['read']
  Characteristic 00002a26-0000-1000-8000-00805f9b34fb, properties: ['read']
  Characteristic 00002a27-0000-1000-8000-00805f9b34fb, properties: ['read']
  Characteristic 00002a28-0000-1000-8000-00805f9b34fb, properties: ['read']
  Characteristic 00002a29-0000-1000-8000-00805f9b34fb, properties: ['read']
  Characteristic 00002a2a-0000-1000-8000-00805f9b34fb, properties: ['read']
  Characteristic 00002a50-0000-1000-8000-00805f9b34fb, properties: ['read']
Service 0000180f-0000-1000-8000-00805f9b34fb:
  Characteristic 00002a19-0000-1000-8000-00805f9b34fb, properties: ['read', 'notify']
Service 99db2000-ac2d-11e3-a5e2-0800200c9a66:
  Characteristic 99db2001-ac2d-11e3-a5e2-0800200c9a66, properties: ['read', 'write']
  Characteristic 99db2002-ac2d-11e3-a5e2-0800200c9a66, properties: ['read', 'write']
  Characteristic 99db2003-ac2d-11e3-a5e2-0800200c9a66, properties: ['read', 'write']
Service 99db2100-ac2d-11e3-a5e2-0800200c9a66:
  Characteristic 99db2101-ac2d-11e3-a5e2-0800200c9a66, properties: ['notify']
  Characteristic 99db2102-ac2d-11e3-a5e2-0800200c9a66, properties: ['write']
  Characteristic 99db2103-ac2d-11e3-a5e2-0800200c9a66, properties: ['notify']
</pre>

The services used in the code we got from the developer uses the following services:
```python
# Define your service and characteristic UUIDs here
self.TIME_DATE_UUID = "99DB1001-AC2D-11E3-A5E2-0800200C9A66"
self.SETUP_UUID = "99DB1002-AC2D-11E3-A5E2-0800200C9A66"
self.COMMAND_UUID = "99DB1003-AC2D-11E3-A5E2-0800200C9A66"
self.DRIVING_BEHAVIOR_UUID = "99DB1005-AC2D-11E3-A5E2-0800200C9A66"
self.DRIVING_BEHAVIOR_SETTINGS_UUID = "99DB1006-AC2D-11E3-A5E2-0800200C9A66"
self.DATA_DOWNLOAD_UUID = "99DB1007-AC2D-11E3-A5E2-0800200C9A66"

self.FIRMWARE_UUID = "00002A26-0000-1000-8000-00805F9B34FB"
self.BATTERY_UUID = "00002A19-0000-1000-8000-00805F9B34FB"
self.SYSTEM_ID_UUID = "00002A23-0000-1000-8000-00805F9B34FB"
self.DEVICE_NAME_UUID = "00002A00-0000-1000-8000-00805F9B34FB"

self.ACC_ENABLER_UUID = "033AFFA1-6778-4112-AC5C-15265F21ED94"
self.ACC_RANGE_UUID = "033AFFA2-6778-4112-AC5C-15265F21ED94"
self.RAW_DATA_UUID = "033AFFAD-6778-4112-AC5C-15265F21ED94"
self.MEASUREMENT_PERIOD_UUID = "033AFFAE-6778-4112-AC5C-15265F21ED94"
```
These are ofcourse a lot different then what we use and are able to use at this point in time, wich means that I can conclude that we need the other software that is used by the developer to be able to read out the raw sensor data. This sensor we will get somewhere this week so that we can continue testing and make use of this raw sensor data. 