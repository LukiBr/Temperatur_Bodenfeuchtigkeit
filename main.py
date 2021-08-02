import csv
from datetime import datetime
import time

import serial

USB_0 = "/dev/ttyUSB0"
USB_1 = "/dev/ttyUSB1"

### DS18b20 Temperatursensoren
def readTempSensor(sensorName):
    """Aus dem Systembus lese ich die Temperatur der DS18B20 aus."""
    f = open(sensorName, 'r')
    lines = f.readlines()
    f.close()
    return lines


def readTempLines(sensorName):
    lines = readTempSensor(sensorName)
    # Solange nicht die Daten gelesen werden konnten, bin ich hier in einer Endlosschleife
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = readTempSensor(sensorName)
    temperaturStr = lines[1].find('t=')
    # Ich überprüfe ob die Temperatur gefunden wurde.
    if temperaturStr != -1:
        tempData = lines[1][temperaturStr + 2:]
        tempCelsius = float(tempData) / 1000.0

        return tempCelsius

def get_bodenfeuchtigkeit(usb_path):
    ser = serial.Serial(usb_path, 9600)
    ser.flushInput()
    ser.timeout = 1

    print("READING USB: %s" % usb_path)

    parser = True
    buffer_str = ""
    while parser == True:
        data = ser.readline()
        buffer_str = data.decode("utf-8")
        if("\r\n" in buffer_str):
            parser = False
        
        bodenfeuchtigkeit_data = buffer_str.rstrip()
        print(bodenfeuchtigkeit_data, end="")

    end_data = bodenfeuchtigkeit_data.split(",")
    
    bodenfeuchtigkeit_Arduino0 = [end_data[0],end_data[1],end_data[2], end_data[3], end_data[4]]
    
    return bodenfeuchtigkeit_Arduino0

    ser.close()


'''
### Bodenfeuchtigkeit
# Bodenfeuchtigkeit Arduino1
def bodenfeuchtigkeitArduino0():
    ser = serial.Serial("/dev/ttyUSB0", 9600)
    ser.flushInput()
    ser.timeout = 1

    parser = True
    buffer_str = ""
    while parser == True:
      data = ser.readline().strip()
      buffer_str = data.decode("utf-8")
      if("\r\n\0" in buffer_str):
        parser = False

      bodenfeuchtigkeit_data = buffer_str.rstrip()

    end_data = bodenfeuchtigkeit_data.split(",")
    #print(end_data)

    bodenfeuchtigkeit_Arduino0 = [end_data[0],end_data[1],end_data[2], end_data[3], end_data[4]]
    """
    bodenfeuchtigkeit_Arduino0 = [bodenfeuchtigkeit_data[1], bodenfeuchtigkeit_data[3], bodenfeuchtigkeit_data[5],
                                  bodenfeuchtigkeit_data[7], bodenfeuchtigkeit_data[9]]
    """

    return bodenfeuchtigkeit_Arduino0

    ser.close()


def bodenfeuchtigkeitArduino1():
    ser = serial.Serial("/dev/ttyUSB1", 9600)
    ser.flushInput()
    ser.timeout = 1

    data = ser.readline().strip()
    bodenfeuchtigkeit_data = data.decode("utf-8")

    end_data = bodenfeuchtigkeit_data.split(",",5)
    #print(end_data)

    bodenfeuchtigkeit_Arduino1 = [end_data[0],end_data[1],end_data[2], end_data[3], end_data[4]]

    """
    bodenfeuchtigkeit_Arduino1 = [bodenfeuchtigkeit_data[1], bodenfeuchtigkeit_data[3], bodenfeuchtigkeit_data[5],
                                      bodenfeuchtigkeit_data[7], bodenfeuchtigkeit_data[9]]
    """
    return bodenfeuchtigkeit_Arduino1

    ser.close()
'''

### Schreibe Daten zu CSV
def data_to_csv(datei, time, sensorname, temperatur, bodenfeuchtigkeit):
    append = [time, sensorname, temperatur, bodenfeuchtigkeit]
    # with open('sensor_output.csv', 'a') as csvFile:
    with open("data/"+datei, 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(append)
    csvFile.close()


def main():
    Temperatursensoren = ['/sys/bus/w1/devices/28-01206274ac39/w1_slave',
                          '/sys/bus/w1/devices/28-012063739aa0/w1_slave',
                          '/sys/bus/w1/devices/28-0120628e0543/w1_slave',
                          '/sys/bus/w1/devices/28-012063d91619/w1_slave',
                          '/sys/bus/w1/devices/28-012063c164f9/w1_slave',
                          '/sys/bus/w1/devices/28-0120639b1b8c/w1_slave',
                          '/sys/bus/w1/devices/28-01206387ed4a/w1_slave',
                          '/sys/bus/w1/devices/28-01206375876d/w1_slave',
                          '/sys/bus/w1/devices/28-012063bf32bb/w1_slave',
                          '/sys/bus/w1/devices/28-012062804b96/w1_slave']

    # DB-Sensorpfad/Dateinamen
    CSV_Datei = ["sensor1.csv",
                 "sensor2.csv",
                 "sensor3.csv",
                 "sensor4.csv",
                 "sensor5.csv",
                 "sensor6.csv",
                 "sensor7.csv",
                 "sensor8.csv",
                 "sensor9.csv",
                 "sensor10.csv"]

    # DB-Sensornames
    sensorname = ["Sensor1",
                  "Sensor2",
                  "Sensor3",
                  "Sensor4",
                  "Sensor5",
                  "Sensor6",
                  "Sensor7",
                  "Sensor8",
                  "Sensor9",
                  "Sensor10"]

    # Datum auslesen
    datum = datetime.now().strftime('%Y-%m-%d,%H:%M:%S,')

    # Array bodenfeuchtigkeit beinhaltet alle 10 Werte der zwei Arduinos (Arduino1 = [:4] Arduino2= [5:])
    bf_arr = get_bodenfeuchtigkeit(USB_0) + get_bodenfeuchtigkeit(USB_1)

    # Schreibe Werte in individuelle CSV-Dateien
    i = 0
    while i < 10:
        data_to_csv(CSV_Datei[i], datum, sensorname[i], str(readTempLines(Temperatursensoren[i])), bf_arr[i])
        print("Messung um " + time.strftime('%H:%M:%S') + " Sensor: " + sensorname[i] + " Temperatur: " + str(readTempLines(Temperatursensoren[i])) + " °C " + "Bodenfeuchtigkeit: " + bf_arr[i])
        i += 1




if __name__ == "__main__":
    main()
