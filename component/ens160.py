import time
import smbus

# Адреса датчиков на I2C шине
ENS160_ADDRESS = 0x53
AHT21_ADDRESS = 0x38

# Инициализация I2C шины
bus = smbus.SMBus(0)

class dataInfo:
    refreshTime = 2.0
    aq = 0
    tvoc = 0
    co2 = 0

ENS160 = dataInfo

# Функция чтения данных с датчика ENS160
def read_ens160():
    bus.write_i2c_block_data(ENS160_ADDRESS, 0x10, [0x02])
    while True:
        try:
            # Чтение данных с датчика ENS160
            data = bus.read_i2c_block_data(ENS160_ADDRESS, 0x21, 5)

            air_quality_index = data[0] # AQ byte
            tvoc_concentration = (data[2] << 8) | data[1] # tvoc byte
            co2_concentration = (data[4] << 8) | data[3] # co2 byte

            print("Air Quality Index: ", air_quality_index)
            print("TVOC Concentration (ppb): ", tvoc_concentration)
            print("Equivalent CO2 Concentration (ppm): ", co2_concentration)

            ENS160.aq, ENS160.tvoc, ENS160.co2 = air_quality_index, tvoc_concentration, co2_concentration

        except IOError as e:
            print("Ошибка чтения данных с датчика ENS160: ", str(e))

        time.sleep(ENS160.refreshTime)