# Temperatur_Bodenfeuchtigkeit
Mit Hilfe des Projektes soll ermöglicht werden, die Temperatur und Bodenfeuchtigkeit aufzuzeichnen. Im Einsatz ist ein RaspberryPi, Arduino Nano, RTC3231, DS18b20 Temperatursensor sowie ein capacitive moisture soil sensor v1.2

Hardware:
- 1x Raspberry Pi 3b
- 2x Arduino Nano
- 1x RTC3231 Realtime Clock
- 10x DS18b20 Temperatursensor
- 10x Capacitive moisture soil sensor v1.2

Cronjob der es ermöglicht jede 15 Minuten eine Messung vorzunehmen:
crontab -e */15 * * * * python3 /home/pi/Temperatur_Bodenfeuchtigkeit/main.py
