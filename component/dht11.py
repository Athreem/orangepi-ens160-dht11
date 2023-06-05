# Импорт сдантартных библиотек
import time, datetime

# Импорт библиотек для работы с GPIO на Orange PI
from pyA20.gpio import gpio
from pyA20.gpio import port

# Импорт библиотек датчика
from lib import dht

# GPIO адресс датчика
DHT11_ADDRESS = port.PA19
gpio.init()

# "Ссылка" для считывания информации с датчика DHT11
instance = dht.DHT(pin=DHT11_ADDRESS, sensor=11)

class dataInfo:
    refreshTime = 300
    refreshTimeValidate = 1.0
    lastTemperature = 0.0
    lastHumidity = 0.0
    lastCheckTime = 0.0

DHT11 = dataInfo

def read_dht11():
    # Запускаем цикл считывания показаний
    while True:

        # Считываем показания с датчика
        result = instance.read()

        # Проверка ответа от датчика
        if not result.is_valid():
            error_count = 1
            print("Не удалось получить данные с датчика DHT11.")
            while not result.is_valid():
                print(f"Попытка получить данные №{error_count}")
                error_count += 1
                result = instance.read()
                time.sleep(DHT11.refreshTimeValidate)

            DHT11.lastTemperature, DHT11.lastHumidity, DHT11.lastCheckTime = result.temperature, result.humidity, datetime.datetime.now()
        else:
            DHT11.lastTemperature, DHT11.lastHumidity, DHT11.lastCheckTime = result.temperature, result.humidity, datetime.datetime.now()

        print(f"Данные получены успешно: Temp - {result.temperature:0.1f}, Humidity - {result.humidity:0.1f}")
        time.sleep(DHT11.refreshTime)