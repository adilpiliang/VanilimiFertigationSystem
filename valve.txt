import RPi.GPIO as GPIO
import time
import requests

channel1 = 16

# GPIO setup
GPIO.setmode(GPIO.BCM)

# GPIO.setup(channel0, GPIO.OUT)
GPIO.setup(channel1, GPIO.OUT)

def relay_off(pin):
    GPIO.output(pin, GPIO.HIGH)  

def relay_on(pin):
    GPIO.output(pin, GPIO.LOW)  

while True:
    url = 'https://vanilimi.web.id/sensor/get_data_valve'  # Ganti dengan URL API Anda

    try:
        # Mengirim permintaan GET ke API untuk mengambil data
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            # Menampilkan data
            for row in data:
                id = row['id']
                tanggal = row['tanggal']
                valve1_status = row['valve1_status']
                source_trigger = row['source_trigger']

                print("ID:", id)
                print("Tanggal:", tanggal)
                print("Valve 1 Status:", valve1_status)
                print("Source Trigger:", source_trigger)
                print("------------------------")

                # Periksa jika valve1_status adalah "initiate"
                if valve1_status == "initiate":
                    # Buat payload untuk pembaruan data
                    payload = {
                        'id': id,
                        'valve1_status': 'process'
                    }
                    update_url = 'https://vanilimi.web.id/sensor/update_valve1_status'  # Ganti dengan URL API untuk pembaruan valve1_status

                    # Mengirim permintaan POST ke API untuk melakukan pembaruan data
                    update_response = requests.post(update_url, data=payload)

                    if update_response.status_code == 200:
                        print("Pembaruan valve1_status berhasil.")
                        # Lakukan penyiraman
                        # tanda tanda
                        relay_off(channel1)
                        print("Turn Off")

                        relay_on(channel1)
                        print("Turn On")
                        time.sleep(180)
                        
                        relay_off(channel1)
                        print("Turn Off")

                        # Selesai melakukan penyiraman

                        # Buat payload untuk pembaruan data
                        payload = {
                            'id': id,
                            'valve1_status': 'finish'
                        }
                        update_url = 'https://vanilimi.web.id/sensor/update_valve1_status'  # Ganti dengan URL API untuk pembaruan valve1_status

                        # Mengirim permintaan POST ke API untuk melakukan pembaruan data
                        update_response = requests.post(update_url, data=payload)

                        if update_response.status_code == 200:
                            print("Pembaruan valve1_status berhasil.")
                        else:
                            print("Gagal melakukan pembaruan valve1_status.")
                    else:
                        print("Gagal melakukan pembaruan valve1_status.")
                else:
                    print("Tidak ada pembaruan valve1_status.")

        else:
            print("Gagal mengambil data. Status code:", response.status_code)

    except KeyboardInterrupt:
        GPIO.cleanup()
    
    except Exception as e:
        print("Terjadi kesalahan:", str(e))
    
    time.sleep(10)