# Общие библиотеки
import time, datetime

# Библиотеки для работы с дисплеем
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from luma.core.render import canvas
from PIL import Image, ImageFont

serial = i2c(port=0, address=0x3C)
device = sh1106(serial, rotate=0)

#count = 1

def loading():
    font = ImageFont.truetype("2.otf", 32) 
    with canvas(device) as draw:
        draw.text((0, 16), "Загрузка...", font=font, fill="white")
    device.show()

def oled_draw(dht11, ens160):
    #global count
    font = ImageFont.truetype("2.otf", 10) 
    current_time = datetime.datetime.now().strftime("%H:%M")
    with canvas(device) as draw:
        draw.text((5, 2), "Температура: {0:0.1f}°C".format(dht11.dataInfo.lastTemperature), font=font, fill="white")
        draw.text((5, 12), "Влажность: {0:0.1f} %".format(dht11.dataInfo.lastHumidity), font=font, fill="white")
        draw.text((5, 22), "Качество воздуха: {}".format(ens160.dataInfo.aq), font=font, fill="white")
        draw.text((5, 32), "Co2: {} ppm".format(ens160.dataInfo.co2), font=font, fill="white")
        draw.text((5, 42), "TVOC: {} ppb".format(ens160.dataInfo.tvoc), font=font, fill="white")
        draw.text((5, 52), "Время: {}".format(current_time), font=font, fill="white")
    #count+=1
    device.show()