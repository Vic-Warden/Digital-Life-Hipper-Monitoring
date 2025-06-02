In this file will be written all the information about the design of the database.

## ERD
This is the first version of the database.

![ERD](../assets/ERD_Hipper.png)

## ERD Guide

### Therapist
This table stores all therapist-related data. It is linked to the patient table through a many-to-many relationship, as each therapist can have multiple patients, and each patient can have multiple therapists.

### Patient
This table stores all patient-related data. It is linked to the therapist table through a many-to-many relationship, as each patient can have multiple therapists, and each therapist can have multiple patients.

### Goal
This table is used to store all the goals set for a patient. You have 3 type of goals daily, weekly and monthly. In this table also uses a boolean to see if the goals are reached or not.

### Device
This table is used to story all the data of the devices. Every patient will have one device. This device is labeled with a number.

### Data
This table stores all data collected by the device. It is linked to the device table via the device_id field, which identifies the source device for each data record.

### References
- Chatgpt to help with the designing of the MySQL Workbench ERD.