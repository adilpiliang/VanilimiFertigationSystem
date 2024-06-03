# Simple example of reading the MCP3008 analog input channels and printing
# them all out.

import time
import datetime
import pymysql
import requests

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))


print('Reading MCP3008 values, press Ctrl-C to quit...')
# Print nice channel column headers.
# print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*range(8)))
print('| {0:>4} | {1:>4} |'.format(*range(8)))
print('-' * 57)
# Main program loop.
while True:
    # connection database
    # conn = pymysql.connect(host="vanilimilenial.com", port=3306, user="vanilimi_master", password="m2mU_u9OyC~%", db="vanilimi_db", autocommit=True, use_unicode=True, charset="utf8")
    # cur = conn.cursor()
    print("************")
    print("Reading....")
    waktu_berjalan = datetime.datetime.now()
    print("Local Time : ", waktu_berjalan)
    print("===================================")

    # Read all the ADC channel values in a list.
    values = [0]*8
    percentage_values = [0]*8
    for i in range(8):
        # The read_adc function will get the value of the specified channel (0-7).
        values[i] = mcp.read_adc(i)
        percentage_values[i] = (1 / 6.43)*(1023 - values[i])

    print(waktu_berjalan)
    # Print the ADC values.
    print('-' * 57)
    print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))
    print("***************")
    print("soil_sensor1 = ", values[0], " , Percentage = ", percentage_values[0])
    print("soil_sensor2 = ", values[1], " , Percentage = ", percentage_values[1])
    # print("soil_sensor3 = ", values[2], " , Percentage = ", percentage_values[2])
    # print("soil_sensor4 = ", values[3], " , Percentage = ", percentage_values[3])
    # print("soil_sensor5 = ", values[4], " , Percentage = ", percentage_values[4])
    # print("rain_sensor1 = ", values[5], " , Percentage = ", percentage_values[5])
    # print("rain_sensor2 = ", values[6], " , Percentage = ", percentage_values[6]) #sensor sudah tidak digunakan
    # print("\nSaving data...")
    # cur.execute("INSERT INTO tb_kelembaban_tanah(tanggal, sensor1_soil, sensor2_soil, sensor3_soil, sensor4_soil, sensor5_soil) VALUES('%s', '%s', '%s', '%s', '%s', '%s')" % (waktu_berjalan, percentage_values[0], percentage_values[1], percentage_values[2], percentage_values[3], percentage_values[4]))
    # cur.execute("INSERT INTO tb_hujan(tanggal, sensor1_rain) VALUES('%s', '%s')" % (waktu_berjalan, percentage_values[5]))
    # print("Data saved!\n")
    
    average_soil = (percentage_values[0]+percentage_values[1]) / 2
    # average_rain = percentage_values[5]
    print("rata-rata kelembaban tanah = ", average_soil)
    # print("rata-rata tingkat curah hujan = ", average_rain)

    url = 'https://vanilimi.web.id/sensor/insert_data_sensor_kelembapan_tanah'  # URL API Anda
    data = {
        'value1_kelembapan_tanah': percentage_values[0],
        'value2_kelembapan_tanah': percentage_values[1]
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        print('Data berhasil diinsert')
    else:
        print('Gagal menginsert data')

    print("***************\n")
    print("Menunggu data berikutnya dalam waktu 0.5 jam...")
    print("===================================")
    # Pause for half a second.
    time.sleep(3600)