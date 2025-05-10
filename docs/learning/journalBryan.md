# Learning Journal
This file contains the learning journal with the learning story's of Bryan van Riesen. 

## Learning story
As a student I want to learn how the communication with the hipper device functions and how that can be implemented, so that I can use this information to communicate with the hipper divce 

## Learned
To communicate with the Hipper device, I use Bluetooth Low Energy (BLE) protocols wich is specified in the [Pam BLE Specs file](../assets/Pam_BLE_Spec_V1_8.pdf). The device supports both standard and custom BLE services. This allows me to communicate with the device with a specific set of codes. 

The device has an activity service (UUID 0x2100) that provides data from the device's activity. To make sure this data is saved on the device, I send the 2102 command to the device. This prepares the data that can then be requested using the 2103 command. 

I implemented a part of this communication by making a BLE connection with the hipper device and then writing the 2102 command to make a request to the device. 

This implementation shows my understanding of the BLE communication with the hipper device and that I understand how to use the device. 