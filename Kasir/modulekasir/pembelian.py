import os 
import pandas as pd
import time #Import library atau module time

tanggal = time.strftime("%d/%m/%Y %H:%M:%S",time.localtime(time.time())) #variabel tanggal

def pembelian():
    os.system('cls')
    data_pengunjung = pd.read_csv("data/daftar_pengunjung.csv")#Baca data file csv daftar pengunjung
    daftar_no_order = set(data_pengunjung["No Order"].tolist())#Mengambil kolom nomor order, diubah ke bentuk list dan diubah lagi menjadi set
    current_data = pd.read_csv("data/data_menu.csv")#Membaca data menu
    data_menu = current_data.values.tolist()#Diubah ke bentuk list
    nama_menu,jenis_menu,harga = map(list,zip(*data_menu))# Zip memisahkan item per index dalam bentuk tuple. Map berfungsi mengubah tuple menjadi list.

    menu_beli = [] #Variabel yang menampung list input menu yang dibeli
    jumlah_beli = [] #Variabel untuk menampung jumlah menu yang dibeli
    nomor_order = len(daftar_no_order) #untuk menentukan nomor order
    total_bayar = 0 #Untuk menghitung total yang dibayar
    
    while True: #Perulangan
        os.system("cls")
        #Desain tabel menu yang dijual
        print("-"*54)
        print("|{:^4}|{:^15}|{:^15}|{:^15}|".format(
                    "No", "Nama Menu", "Jenis Menu", "Harga"))
        print("-"*54)
        for i in range(len(data_menu)):
            print("|{:^4}|{:^15}|{:^15}|{:>15}|".format(i,nama_menu[i],jenis_menu[i],harga[i]))#Menampilkan daftar menu menggunakan perulangan for 
        print("-"*54)
        menu,jumlah = input("Masukkan menu yg dibeli dengan format (NamaMenu,jumlah beli): ").split(",")#Input pembelian yang dipisah dengan koma
        if menu in nama_menu: #Mengecek apakah menu yang dibeli ada di database. Jika ada blok ini akan dijalankan
            menu_beli.append(menu) #Menambah menu yang dibeli ke list menu_beli
            jumlah_beli.append(int(jumlah)) #menambah jumlah yang dibeli ke list jumlah_beli
            tambah =  input("Tambah menu? [y/n] : ")#check kondisi apakah akan menambah menu yang dibeli atau tidak
            if (tambah == "N") or (tambah =="n"): #Jika N/ n perulangan akan berhenti
                break
        else: #Blok else akan dijalankan bila input menu tidak ada pada database
            print("Maaf, Menu tersebut tidak tersedia di restoran kami")
            print("Silahkan masukkan ulang ")
            input()
            pembelian() #Memanggil fungsi pembelian kembali
    
    #Blok ini line 44 - 48 untuk mengatasi input yang double. Maksudnya misal beli Indomie,2 trs input lagi Indomie,2. Pada program sebelumnya saat cetak output dihitung secara terpisah. Dengan blok ini program akan menghitung sekaligus. Indomie,2 + Indomie,2 = Indomie,4 
    menu_beli2 = list(dict.fromkeys(menu_beli))#Menghapus item duplicate pada list menu_beli
    menu_jumlah = dict.fromkeys(menu_beli,0)#membuat dictionary untuk menampung jumlah menu yang dibeli dan value 0
    for h in range(len(menu_beli)): #menghitung jumlah menu yang dibeli
        banyak = menu_jumlah[menu_beli[h]] + jumlah_beli[h]
        menu_jumlah[menu_beli[h]] = banyak

    nomor_order += 1 #Nomor order akan ditambah 1 tiap proses sebelumnya berhasil
    #desain untuk struk
    print("\n{:^61}".format("Struk Belanja"))
    print("-"*61)
    print("|{:^4}|{:^15}|{:^12}|{:^12}|{:^12}|".format("No","Nama Menu","Harga","Jumlah","Total"))
    print("-"*61)
    #perulangan for untuk menampilkan menu yang dibeli, jumlah, harga, total harga
    for k in range(len(menu_beli2)):
            index = nama_menu.index(menu_beli2[k])
            total_harga = menu_jumlah[menu_beli2[k]] * harga[index]
            print("|{:^4}|{:^15}|{:^12}|{:^12}|{:>12}|".format(k,menu_beli2[k],harga[index],menu_jumlah[menu_beli2[k]],total_harga))
            total_bayar += total_harga #Menghitung total bayar
            list_pembelian = [nomor_order,menu_beli2[k],harga[index],menu_jumlah[menu_beli2[k]],total_harga,tanggal] #Setiap penghitungan dimasukkan ke dalam list ini 
            save_data_pengunjung(list_pembelian) #memanggil fungsi save data untuk menyimpan setiap transaksi ke database
    print("-"*61)
    print("|{:^46}|{:>12}|".format("Total Pembayaran",total_bayar))#Menampilkan total pembayaran
    print("-"*61)
    input("Enter untuk lanjut")

def save_data_pengunjung(list_pembelian):
    read_data = pd.read_csv("data/daftar_pengunjung.csv")#Membaca file daftar pengunjung
    list_data_pengunjung = read_data.values.tolist()#Diubah ke bentuk list
    
    list_data_pengunjung.append(list_pembelian) #Menambah list pembelian ke dalam list data pengunjung

    saved_data = pd.DataFrame(list_data_pengunjung, columns=["No Order","Nama Menu","Harga","Jumlah","Total Harga","Tanggal"])
    saved_data.to_csv("data/daftar_pengunjung.csv",index=False) #disimpan ke dalam file csv sesuai kolom masing"