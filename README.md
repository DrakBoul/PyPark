# PyPark
## Introduction
PyPark is a smart parking web application, built using python 3.12 with flask for the web interface, and arduino for the hardware interface. It uses various modules from an arduino starter kit such as the ultrasonic sensor, RFID RC-522 card reader, power supply module, and a RGB LED. PyPark was initially created in the span of 24 hours for a hackathon submission, and is still currently being worked on.

## How It Works
Users can start by signing up on the website, during the signup process the user will be asked to enter the unique identification number associated with the RFID card they are going to be using to validate there parking. After the signup process, the user can book any parking stall that is in the "availiable" state online using the PyPark website, which sends serial data to the arduino to display a "reserved" state (RGB LED turns blue). The stall will remain in a reserved state until a vehicle is detected by the ultrasonic sensor, at which point the state of the parking stall changes from "reserved" to "occupied, but not verified" (RGB LED turns yellow). While the stall is in this state the RFID card reader will await a card to be presented. If the user presents the correct RFID card/tag to the reader the RGB LED will turn blue, signifying the user is validly parked in the stall, once the user leaves the parking space the state will return to "availiable". If the user presents an incorrect card then the RGB LED will turn red signifying the user is not validly parked, once the user leaves the stall the state will go back to "reserved". Other users may see the state of the availiable parking spaces on the homepage of the PyPark website which updates in real time with what parking spaces are currently booked or free.

For a quick demo of PyPark see my YouTube Channel!

Link: YouTube Demo coming soon!

## Parts and Data Sheets

__Note: The following parts and data sheets were the ones used specifically for the creators implementation.__

* ELEGOO UNO R3 Board (
[Data Sheet](https://epow0.org/~amki/car_kit/Datasheet/ELEGOO%20UNO%20R3%20Board.pdf))
* 3 x 220 Ohm Resistor ([Data Sheet](https://acrobat.adobe.com/link/track?uri=urn:aaid:scds:US:c906d8db-da1e-35cf-9b43-42f47f67a175))
* Common Cathode RGB LED ([Data Sheet](https://acrobat.adobe.com/id/urn:aaid:sc:VA6C2:0b488878-efd7-4155-b3ab-c87b0b19fe6f))
* RC522 RFID Module ([Data Sheet](https://acrobat.adobe.com/id/urn:aaid:sc:VA6C2:a0a71096-326a-4ac2-88fd-325143133633))
* Ultrasonic Sensor ([Data Sheet](https://acrobat.adobe.com/id/urn:aaid:sc:VA6C2:de3336d2-2dc3-4530-aea0-314efd47b140))
* Breadboard Power Supply Module ([Data Sheet](https://acrobat.adobe.com/id/urn:aaid:sc:VA6C2:caedbf4e-47a1-4bd0-a852-d53e7a3e5b3c))
