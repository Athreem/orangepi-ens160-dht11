# Общие библиотеки
import time, threading, datetime, requests, json, sys
from collections import deque

#Библиотеки для запуска сервера
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit

# Модули датчиков
from component import dht11
from component import ens160

# Импорт модуля oled
from component import oled

data_list = deque(maxlen=50)

# Создаем Flask приложение
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template('index.html', temperature="{0:0.1f}".format(dht11.dataInfo.lastTemperature), humidity="{0:0.1f}".format(dht11.dataInfo.lastHumidity), current_time=str(dht11.dataInfo.lastCheckTime))

@app.route('/data.json')
def get_data():
    with open('data.json') as f:
        data = json.load(f)
    return jsonify(data)

def save_data():
    while True:
        while dht11.dataInfo.lastCheckTime == 0.0:
            time.sleep(2.0)

        data_list.append({
            "temperature": "{0:0.1f}".format(dht11.dataInfo.lastTemperature),
            "humidity": "{0:0.1f}".format(dht11.dataInfo.lastHumidity),
            "time": str(dht11.dataInfo.lastCheckTime)
        })
        try:
            with open("data.json", "w") as f:
                json.dump(list(data_list), f)
        finally:
            f.close()
        time.sleep(dht11.dataInfo.refreshTime)

def main():
    #Ожидание показаний от датчика DHT11
    while dht11.dataInfo.lastCheckTime == 0.0:
        print("Идёт загрузка показаний")
        time.sleep(1.0)

    if dht11.dataInfo.lastCheckTime != 0.0:
        while True:
            oled.oled_draw(dht11, ens160)
            time.sleep(4.0)

if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        argument = sys.argv[1]
        if argument == '-web':
            print('Запуск с web интерфейсом')
            web_thread = threading.Thread(target=socketio.run, args=(app,), kwargs={'host': '0.0.0.0', 'port': 8080, 'debug': True})
            web_thread.start()
        else:
            print('Запуск не удался, неверный аргумент')


    # Получение данных с датчика DHT11
    threading.Thread(target=oled.loading).start()
    threading.Thread(target=dht11.read_dht11).start()
    threading.Thread(target=ens160.read_ens160).start()
    threading.Thread(target=main).start()
    threading.Thread(target=save_data).start()
