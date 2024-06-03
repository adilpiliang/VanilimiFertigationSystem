import requests
import time

while True:

    url = 'https://vanilimi.web.id/sensor/get_data_sensor_kelembapan_tanah'  # Ganti dengan URL API Anda

    try:
        # Mengirim permintaan GET ke API untuk mengambil data
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            # Menampilkan data
            for row in data:
                id_sensor_kelembapan_tanah = row['id']
                tanggal = row['tanggal']
                value1_kelembapan_tanah = row['value1_kelembapan_tanah']
                value2_kelembapan_tanah = row['value2_kelembapan_tanah']
                decission_process = row['decission_process']

                print("ID:", id_sensor_kelembapan_tanah)
                print("Tanggal:", tanggal)
                print("Value 1 Kelembapan Tanah:", value1_kelembapan_tanah)
                print("Value 2 Kelembapan Tanah:", value2_kelembapan_tanah)
                print("Decission Process:", decission_process)
                print("------------------------")

                # Periksa jika decission_process adalah "initiate"
                if decission_process == "initiate":
                    # Buat payload untuk pembaruan data
                    payload = {
                        'id': id_sensor_kelembapan_tanah,
                        'decission_process': 'process'
                    }
                    update_url = 'https://vanilimi.web.id/sensor/update_decission_process'  # Ganti dengan URL API untuk pembaruan decission_process

                    # Mengirim permintaan POST ke API untuk melakukan pembaruan data
                    update_response = requests.post(update_url, data=payload)

                    if update_response.status_code == 200:
                        print("Pembaruan decission_process berhasil.")
                        
                        average_kelembapan_tanah = (int(value1_kelembapan_tanah) + int(value2_kelembapan_tanah)) / 2

                        # tambahkan perintah untuk get_data_sensor_udara
                        # Ambil data terbaru dari tabel log_sensor_udara
                        sensor_udara_url = 'https://vanilimi.web.id/sensor/get_data_sensor_udara'  # Ganti dengan URL API Anda
                        sensor_udara_response = requests.get(sensor_udara_url)

                        if sensor_udara_response.status_code == 200:
                            sensor_udara_data = sensor_udara_response.json()

                            # Tampilkan data log_sensor_udara
                            for sensor_udara_row in sensor_udara_data:
                                id_sensor_udara = sensor_udara_row['id']
                                tanggal_air = sensor_udara_row['tanggal']
                                value_temprature = sensor_udara_row['value_temprature']
                                value_airhumidity = sensor_udara_row['value_airhumidity']
                                decission_process_air = sensor_udara_row['decission_process']

                                print("ID:", id_sensor_udara)
                                print("Tanggal:", tanggal_air)
                                print("Value Temprature:", value_temprature)
                                print("Value Air Humidity:", value_airhumidity)
                                print("Decission Process:", decission_process_air)
                                print("------------------------")

                                # Periksa jika decission_process adalah "initiate"
                                if decission_process_air == "initiate":
                                    # Buat payload untuk pembaruan data
                                    payload = {
                                        'id': id_sensor_udara,
                                        'decission_process': 'process'
                                    }
                                    update_url = 'https://vanilimi.web.id/sensor/update_decission_process_udara'  # Ganti dengan URL API untuk pembaruan decission_process

                                    # Mengirim permintaan POST ke API untuk melakukan pembaruan data
                                    update_response = requests.post(update_url, data=payload)

                                    if update_response.status_code == 200:
                                        print("Pembaruan decission_process berhasil.")
                                        if int(value_temprature) > 34 or int(value_airhumidity) < 70 or average_kelembapan_tanah < 70 :
                                            url = 'https://vanilimi.web.id/sensor/insert_data_valve'  # URL API Anda
                                            data_keputusan = {
                                                'valve1_status': "initiate",
                                                'source_trigger': "sensor"
                                            }

                                            response = requests.post(url, data=data_keputusan)

                                            if response.status_code == 200:
                                                print('Data berhasil diinsert')
                                                # done 1
                                                # Buat payload untuk pembaruan data
                                                payload = {
                                                    'id': id_sensor_kelembapan_tanah,
                                                    'decission_process': 'done'
                                                }
                                                update_url = 'https://vanilimi.web.id/sensor/update_decission_process'  # Ganti dengan URL API untuk pembaruan decission_process

                                                # Mengirim permintaan POST ke API untuk melakukan pembaruan data
                                                update_response = requests.post(update_url, data=payload)

                                                if update_response.status_code == 200:
                                                    print("Pembaruan decission_process berhasil.")
                                                else:
                                                    print("Gagal melakukan pembaruan decission_process sensor kelembapan tanah.")

                                                #done 2
                                                # Buat payload untuk pembaruan data
                                                payload = {
                                                    'id': id_sensor_udara,
                                                    'decission_process': 'done'
                                                }
                                                update_url = 'https://vanilimi.web.id/sensor/update_decission_process_udara'  # Ganti dengan URL API untuk pembaruan decission_process

                                                # Mengirim permintaan POST ke API untuk melakukan pembaruan data
                                                update_response = requests.post(update_url, data=payload)

                                                if update_response.status_code == 200:
                                                    print("Pembaruan decission_process berhasil.")
                                                else:
                                                    print("Gagal melakukan pembaruan decission_process sensor kelembapan tanah.")
                                            else:
                                                print('Gagal menginsert data')
                                        else:
                                            print("Tidak perlu melakukan penyiraman")
                                            # done 1
                                            # Buat payload untuk pembaruan data
                                            payload = {
                                                'id': id_sensor_kelembapan_tanah,
                                                'decission_process': 'done'
                                            }
                                            update_url = 'https://vanilimi.web.id/sensor/update_decission_process'  # Ganti dengan URL API untuk pembaruan decission_process

                                            # Mengirim permintaan POST ke API untuk melakukan pembaruan data
                                            update_response = requests.post(update_url, data=payload)

                                            if update_response.status_code == 200:
                                                print("Pembaruan decission_process berhasil.")
                                            else:
                                                print("Gagal melakukan pembaruan decission_process sensor kelembapan tanah.")

                                            #done 2
                                            # Buat payload untuk pembaruan data
                                            payload = {
                                                'id': id_sensor_udara,
                                                'decission_process': 'done'
                                            }
                                            update_url = 'https://vanilimi.web.id/sensor/update_decission_process_udara'  # Ganti dengan URL API untuk pembaruan decission_process

                                            # Mengirim permintaan POST ke API untuk melakukan pembaruan data
                                            update_response = requests.post(update_url, data=payload)

                                            if update_response.status_code == 200:
                                                print("Pembaruan decission_process berhasil.")
                                            else:
                                                print("Gagal melakukan pembaruan decission_process sensor kelembapan tanah.")

                                    else:
                                        print("Gagal melakukan pembaruan decission_process sensor udara.")
                                else:
                                    print("Tidak ada pembaruan decission_process sensor udara.")


                        else:
                            print("Gagal mengambil data log_sensor_udara. Status code:", sensor_udara_response.status_code)

                    else:
                        print("Gagal melakukan pembaruan decission_process sensor kelembapan tanah.")
                else:
                    print("Tidak ada pembaruan decission_process.")

        else:
            print("Gagal mengambil data. Status code:", response.status_code)

    except Exception as e:
        print("Terjadi kesalahan:", str(e))
    
    # Tunggu selama 5 menit sebelum mengulang proses
    time.sleep(60)  # 300 detik = 5 menit