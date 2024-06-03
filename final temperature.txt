import time
import board
import adafruit_dht
import pymysql
import datetime
import requests

# Initial the dht device, with data pin connected to:
# dhtDevice = adafruit_dht.DHT22(board.D18)
# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.

dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)
while True:
    try:
        # connection database
        # conn = pymysql.connect(host="vanilimilenial.com", port=3306, user="vanilimi_master", password="m2mU_u9OyC~%", db="vanilimi_db", autocommit=True, use_unicode=True, charset="utf8")
        # cur = conn.cursor()

        waktu_berjalan = datetime.datetime.now()

        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        
        # turn off default print from documentation
        # print(
        #     "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
        #         temperature_f, temperature_c, humidity
        #     )
        # )

        print(waktu_berjalan, " Temp: ", temperature_c, " C, Humidity: ", humidity, " %")
        # print("Saving data...")
        # cur.execute("INSERT INTO tb_suhu_udara(tanggal, nilai_suhu_udara, nilai_kelembaban_udara) VALUES('%s', '%s', '%s')" % (waktu_berjalan, temperature_c, humidity))
        # print("Data saved!")
        url = 'https://vanilimi.web.id/sensor/insert_data_sensor_udara'  # URL API
        data = {
            'value_temprature': temperature_c,
            'value_airhumidity': humidity
        }

        response = requests.post(url, data=data)

        if response.status_code == 200:
            print('Data berhasil diinsert')
        else:
            print('Gagal menginsert data')

        print("********************")


    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        # print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error
    except KeyboardInterrupt:
        dhtDevice.exit()
        print('exiting script')

    time.sleep(3600)