import os 
import pandas as pd

# Fungsi simpan data
def save_data(sort_data_menu):
    saved_data = pd.DataFrame(sort_data_menu, columns=["nama_menu", "jenis_menu", "harga"])#data menu yang sudah di input dadi sortir diubah ke dalam bentuk dataframe. Dataframe adalah data yg berbentuk 2 dimensi 
    #variabel columns ["nama_menu","Jenis_menu"] berarti urutan data yang diinput akan dimasukkan ke masing-masing kolom
    saved_data.to_csv("data/data_menu.csv", index=False)#Data yang telah diubah ke bentuk dataframe akan disimpan ke file csv. Index = False membuat index tidak akan muncul/dimasukkan ke file csv

#Fungsi untuk membaca dan menambah data
def curr_data(new_data):
    current_data = pd.read_csv("data/data_menu.csv")#Membaca data pada file csv dan bertipe dataframe
    data_menu = current_data.values.tolist()#Diubah ke bentuk list karena 2 dimensi maka list yg terbentuk nested list

    data_menu.append(new_data)#Menambah data baru ke list

    #Blok program sorting
    for i in range(len(data_menu)):
        for j in range(len(data_menu)-i-1):
            if data_menu[j][1] > data_menu[j+1][1]:
                temp = data_menu[j]
                data_menu[j] = data_menu[j+1]
                data_menu[j+1] = temp

    sort_data_menu = data_menu
    save_data(sort_data_menu) #data yang sudah di sorting akan disimpan

#Fungsi untuk meminta user memasukkan menu
def add_data():
    nama_menu = input("Masukkan nama menu : ")
    jns_menu = input("Masukkan jenis [Makanan/Minuman] : ")
    harga = int(input("Masukkan harga menu : "))
    new_data = [nama_menu, jns_menu, harga] #menu yang diinput dimasukkan ke dalam list
    curr_data(new_data)#Memanggil fungsi curr_data untuk menyimpan input ke dalam file csv

#Fungsi untuk menampilkan data yang sudah disimpan
def show_data():
    current_data = pd.read_csv("data/data_menu.csv")
    data_menu = current_data.values.tolist()
    if data_menu == []: #Jika data masih kosong blok if akan dijalankan
        print("Tidak ada data")
        return "Tidak ada data" #Return string "Tidak ada data"
    else: #Jika terdapat data, maka data akan ditampilkan
        nama_menu,jenis_menu,harga = map(list,zip(*data_menu)) # Zip memisahkan item per index dalam bentuk tuple. Map berfungsi mengubah tuple menjadi list.

        #Desain Tabel
        print("-"*54)
        print("|{:^4}|{:^15}|{:^15}|{:^15}|".format(
            "No", "Nama Menu", "Jenis menu", "Harga"))
        print("-"*54)
        for i in range(len(data_menu)):
            print("|{:^4}|{:^15}|{:^15}|{:^15}|".format(i,nama_menu[i],jenis_menu[i],harga[i]))#Menampilkan output sesuai indeks 
        print("-"*54)

#Fungsi untuk mengubah harga
def update_harga():
    if show_data() == "Tidak ada data": #Cek apakah fungsi show_data me-return nilai. jika iya blok ini akan dijalankan
        print("Tidak ada data")
        print("Buat data terlebih dahulu!")
    else:
        try: #Menggunakan error handling agar program tidak berhenti saat user salah input
            current_data = pd.read_csv("data/data_menu.csv")
            data_menu = current_data.values.tolist()
            pilih = int(input("Pilih data yang mau di perbaharui : "))#memilih daftar menu yang akan diganti harganya
            upd_harga = int(input("Masukkan harga baru : "))#Input harga baru

            data_menu[pilih][2] = upd_harga #harga lama diganti dengan harga baru
            save_data(data_menu)#Save data

        except ValueError: #JIka input value salah, program akan meminta input ulang
            print("Input harus Integer!!!")
            update_harga()

#Fungsi untuk menghapus data
def delete_data():
    show_data()#Menampilkan data
    try:
        current_data = pd.read_csv("data/data_menu.csv")#baca file
        data_menu = current_data.values.tolist()
        pilih = int(input("Pilih data yang mau dihapus : "))#Input data yang dihapus
        data_menu.pop(pilih)
        print("Data berhasil dihapus!!")
        save_data(data_menu) #Simpan data
    except ValueError:
        print("Salah inputan")
        delete_data()# Meminta input kembali jika Value salah

#Menu
def menu_edit():
    while (True): #looping menu 
        os.system('cls')#Untuk clear terminal
        print("[1] Buat Data/Tambah Data")
        print("[2] Lihat Data")
        print("[3] Update Harga")
        print("[4] Hapus Data")
        print("[5] Menu Sebelumnya")
        pilih_menu = int(input("Pilih menu : "))
        if pilih_menu == 1:
            add_data()#Memanggil fungsi tambah data
        elif pilih_menu == 2:
            show_data()#Untuk melihat data
        elif pilih_menu == 3:
            update_harga()#Update harga menu
        elif pilih_menu == 4:
            delete_data()#Menghaous data
        elif pilih_menu == 5:
            break #Mengakhiri menu
        else:
            print("Salah input!") 
            menu_edit()

        #Mengecek apakah akan melanjutkan process atau pindah menu
        check_status = input("Next process?[Y/N] => ")
        if (check_status == "Y") or (check_status == "y"):
            menu_edit()
        else:
            break