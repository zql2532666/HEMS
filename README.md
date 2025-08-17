# IoT Home Environment Monitoring System 

# Overview
HEMS is an IoT-based application designed to monitor and manage the physical conditions of indoor environments. It collects real-time sensor data—including temperature, humidity, and light levels—to help users track and maintain optimal environmental conditions.

In addition to environmental monitoring, HEMS integrates facial detection and recognition using a Raspberry Pi camera. Captured faces are automatically compared against authorized personnel images stored in an AWS S3 bucket to control and verify access.

The system is particularly targeted at small and medium-sized businesses that maintain on-site server rooms, offering them a cost-effective solution for both environmental monitoring and access control. With its easy-to-use interface and IoT-enabled features, HEMS provides an efficient way to ensure the safety and stability of critical IT infrastructure.

## 1.2 Final RPI Set-up
![Alt text](README-images/RPI-Setup.png?raw=true)

## 1.3 Web Application Screenshots
![Alt text](README-images/realtime_sensor.png?raw=true)
Dashboard – Real Time Sensor Values & Controlling of LED <br><br>

![Alt text](README-images/light_graph.png?raw=true)
Dashboard – Light Graph <br><br>

![Alt text](README-images/temperature_graph.png?raw=true)
Dashboard – Temperature Graph <br><br>

![Alt text](README-images/humidity_graph.png?raw=true)
Dashboard – Humidity Graph <br><br>

![Alt text](README-images/light_table.png?raw=true)
Tables Page  – Light Table <br><br>

![Alt text](README-images/temperature_humidity_table.png?raw=true)
Tables Page  – Temperature & Humidity Table <br><br>

![Alt text](README-images/access_checker.png?raw=true)
Facial Recognition Page – Acess Checker <br><br>

![Alt text](README-images/access_log_1.png?raw=true)
![Alt text](README-images/access_log_2.png?raw=true)
Facial Recognition Page – Acess Logs <br><br>

![Alt text](README-images/login.png?raw=true)
Login Page <br><br>

![Alt text](README-images/register.png?raw=true)
Register New User Page <br><br>

![Alt text](README-images/side_bar_hidden.png?raw=true) <br>
Side Bar – Hidden <br><br>

![Alt text](README-images/side_bar_revealed.png?raw=true) <br>
Side Bar – Revealed <br><br>

![Alt text](README-images/main_bar.png?raw=true) <br>
Main Bar  <br><br>

## 1.4 Email Notification Example
![Alt text](README-images/email.png?raw=true) <br>

## 1.5 System Architecture
![Alt text](README-images/arch.png?raw=true) <br>

# Section 2 Hardware requirements 
## 2.1 Hardware checklist
- Arduino
- Raspberry Pi
- PiCamera
- Buzzer
- DHT sensor
- LED
- LDR Sensor
- Button
- Two Breadboards
- Three 10k Ohms resistor (For DHT11, LDR sensor and Button)
- 330 Ohms resistor (for LED)

## 2.2 Hardware setup instructions
### 2.2.1 Connections for LDR to Arduino:

![Alt text](README-images/LDR+Arduino-setup.png?raw=true)


### 2.2.2 Connection for Arduino to Raspberry Pi:
#### Make sure that the USB connector for the Arduino is connected to the **top left** USB port in the Raspberry Pi
![Alt text](README-images/Arduino-RPI-setup.png?raw=true)


### 2.2.3 Connections for Button:

![Alt text](README-images/button-setup.png?raw=true)


### 2.2.4 Connections for LED:

![Alt text](README-images/led-setup.png?raw=true)


### 2.2.5 Connections for Buzzer:

![Alt text](README-images/buzzer-setup.png?raw=true)


### 2.2.6 Connections for DHT11 Sensor:

![Alt text](README-images/dht11-setup.png?raw=true)


## 2.2.7 Fritzing Diagram

![Alt text](README-images/fritzing-diagram.jpg?raw=true)



# Section 3 - Source Code Set Up

1. Fork the current repository and issue the "git clone" command, to clone the git repository to your raspberry pi. 

2. Place the AWS certificate, private key and root CA in "CA2/app/aws_certs"

3. In config.conf, change the configuration parameters if necessary. Configuration needed for sensors, raspberry pi and aws can be set here before running the program

    ![Alt text](README-images/config_file.png?raw=true)

4. Run the following command to install all the required python dependencies to run the application.
```
pip3 install -r requirements.txt
```

5. Directory structure of the code base should be as follows:

    ![Alt text](README-images/dir_struct.png?raw=true)


# Section 4 - Run Program

1. Login to your AWS Educate account and click on “Account Details”.

2. Copy over the AWS Credentials to clipboard

    ![Alt text](README-images/aws_creds.png?raw=true)

4. On both the Raspberry Pi and the EC2 instance, run the following commands:
```
rm ~/.aws/credentials
vi ~/.aws/credentials
```
5. Paste the credentials into the text editor and save. After saving, exit the terminal

6. Go to the cloned folder and run the following command to start the server:
```
python3 app/app.py
``` 




# Section 5 - References
https://github.com/xbwei/data-analysis-aws/tree/master/facial-recognition-raspberry-pi

https://www.youtube.com/watch?v=xFCK1-lYzqA

https://docs.aws.amazon.com/rekognition/latest/dg/API_CompareFaces.html

https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/set-time.html
