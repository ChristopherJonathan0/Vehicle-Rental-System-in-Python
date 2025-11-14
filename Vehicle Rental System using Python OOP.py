from abc import ABC, abstractmethod
from datetime import datetime
import random
from typing import Counter

class Vehicle(ABC):
    Counter = 0
    def __init__(self, vehicle_id, brand, rate_per_hour):
        Vehicle.Counter += 1
        self.vehicle_id = f"VH-{Vehicle.Counter:03d}"
        self.brand = brand
        self.__rate_per_hour = rate_per_hour  

    # getter
    def get_rate_per_hour(self):
        return self.__rate_per_hour

    # setter
    def set_rate_per_hour(self, value):
        value = float(str(value).replace(".", "").replace(",", "."))
        if value > 0:
            self.__rate_per_hour = value
        else:
            print("❌ Tarif harus lebih besar dari 0!")

    @abstractmethod
    def calculate_rent(self, hours):
        pass

    @abstractmethod
    def display_info(self):
        pass


class Car(Vehicle):
    def __init__(self, vehicle_id, brand, rate_per_hour, seats):
        super().__init__(vehicle_id, brand, rate_per_hour)
        self.seats = seats

    def calculate_rent(self, hours):
        return self.get_rate_per_hour() * hours

    def display_info(self):
        print(f"Mobil {self.brand} - {self.seats} kursi - Tarif: Rp {self.get_rate_per_hour()}/jam")


class Motorcycle(Vehicle):
    def __init__(self, vehicle_id, brand, rate_per_hour, helmet_included):
        super().__init__(vehicle_id, brand, rate_per_hour)
        self.helmet_included = helmet_included

    def calculate_rent(self, hours):
        return self.get_rate_per_hour() * hours

    def display_info(self):
        print(f"Motor {self.brand} - Helm termasuk: {self.helmet_included} - Tarif: Rp {self.get_rate_per_hour()}/jam")


class Truck(Vehicle):
    def __init__(self, vehicle_id, brand, rate_per_hour, capacity):
        super().__init__(vehicle_id, brand, rate_per_hour)
        self.capacity = capacity

    def calculate_rent(self, hours):
        return self.get_rate_per_hour() * hours

    def display_info(self):
        print(f"Truk {self.brand} - Kapasitas: {self.capacity} ton - Tarif: Rp {self.get_rate_per_hour()}/jam")



class RentalSystem:
    def __init__(self, vehicle, renter, hours, cost):
        self.vehicle = vehicle
        self.vehicle_id = f"VH-{Vehicle.Counter:03d}"
        self.renter = renter
        self.hours = hours
        self.cost = cost
        self.datetime = datetime.now().strftime("%Y,%m,%d")

    def save_transactions(self, filename="transactionscar.txt"):
        try:
            with open(filename, "a") as f:
                f.write(f"{self.datetime}|{self.vehicle_id}|{self.renter}|{self.vehicle.brand} | {self.hours} jam | Rp {self.cost:,.0f}\n".replace(",", "."))
            print("✅ Transaksi berhasil disimpan!\n")
        except Exception as ex:
            print("Error saat menyimpan transaksi:", ex)

class RentalError(Exception): 
    pass


def delete_transaction(filename="transactionscar.txt"):
    try:
        # Baca semua transaksi dari file
        with open(filename, "r") as f:
            lines = f.readlines()

        if not lines:
            print("❌ Tidak ada transaksi untuk dihapus.\n")
            return

        print("\n=== DAFTAR TRANSAKSI ===")
        for i, line in enumerate(lines, start=1):
            print(f"[{i}] {line.strip()}")

        hapus = int(input("\nMasukkan nomor transaksi yang ingin dihapus: ")) - 1

        if 0 <= hapus < len(lines):
            del lines[hapus]
            with open(filename, "w") as f:
                f.writelines(lines)
            print("✅ Transaksi berhasil dihapus!\n")
        else:
            print("❌ Nomor transaksi tidak valid.\n")

    except FileNotFoundError:
        print("❌ File transaksi belum ditemukan.\n")

def update_transaction(filename="transactionscar.txt"):
    with open(filename, "r") as f:
        lines = f.readlines()

    # tampilkan semua transaksi
    for i, line in enumerate(lines, start=1):
        print(f"[{i}] {line.strip()}")

    index = int(input("Pilih nomor transaksi yang ingin diedit: ")) - 1

    if 0 <= index < len(lines):
        data = lines[index].strip().split("|")

        print("\nPilih bagian yang ingin diubah:")
        print("1. Nama Penyewa")
        print("2. Merek Kendaraan")
        print("3. Durasi Sewa")
        print("4. Batalkan")

        pilihan = input("Masukkan pilihan: ")

        if pilihan == "1":
            data[2] = input("Nama penyewa baru: ")
        elif pilihan == "2":
            data[3] = " " + input("Merek kendaraan baru: ")
        elif pilihan == "3":
            data[4] = " " + input("Durasi baru (contoh: 10 jam): ")
        elif pilihan == "4":
            print("Edit dibatalkan.")
            return
        else:
            print("❌ Pilihan tidak valid.")
            return

        # simpan perubahan
        lines[index] = "|".join(data) + "\n"

        with open(filename, "w") as f:
            f.writelines(lines)

        print("✅ Transaksi berhasil diperbarui!\n")
    else:
        print("❌ Nomor transaksi tidak ditemukan.")

def menu_penyewa():
    renter = input("\nMasukkan nama penyewa: ")
    type = input("Jenis kendaraan (Car/Motorcycle/Truck): ")
    brand = input("Masukkan merek kendaraan: ")
    rate_per_hour = float(input("Masukkan tarif per jam (Rp): ").replace(".", "").replace(",", "."))
    hours = int(input("Durasi sewa (jam): "))

    try:
        if hours <= 0:
            raise RentalError("Durasi sewa harus lebih dari 0 jam!")
    except RentalError as e:
        print("Terjadi kesalahan:", e)
        return  # kembali ke menu utama

    # objek kendaraan
    if type.lower() == "car":
        seats = int(input("Jumlah kursi: "))
        vehicle = Car("AUTO001", brand, rate_per_hour, seats)

    elif type.lower() == "motorcycle":
        helmet = input("Apakah helm termasuk? (yes/no): ")
        vehicle = Motorcycle("MOTO001", brand, rate_per_hour, helmet.lower() == "yes")

    elif type.lower() == "truck":
        capacity = int(input("Kapasitas (ton): "))
        vehicle = Truck("TRUCK001", brand, rate_per_hour, capacity)

    else:
        print("Jenis kendaraan tidak valid.")
        return

    cost = vehicle.calculate_rent(hours)
    print(f"\nTotal biaya sewa: Rp {cost:,.0f}".replace(",", "."))

    transaksi = RentalSystem(vehicle, renter, hours, cost)
    transaksi.save_transactions()

def menu_admin():
    while True:
        print("\n=== MENU ADMIN ===")
        print("1. Tampilkan transaksi")
        print("2. Update transaksi")
        print("3. Delete transaksi")
        print("4. Kembali ke menu utama")

        pilihan = input("Pilih menu admin: ")

        if pilihan == "1":
            try:
                with open("transactionscar.txt", "r") as f:
                    print("\n=== DAFTAR TRANSAKSI ===")
                    print(f.read())
            except FileNotFoundError:
                print("Belum ada transaksi tersimpan.")

        elif pilihan == "2":
            update_transaction()

        elif pilihan == "3":
            delete_transaction()

        elif pilihan == "4":
            break

        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    while True:
        print("\n=== SISTEM PENYEWAAN KENDARAAN ===")
        print("1. Penyewa")
        print("2. Admin")
        print("3. Keluar")

        menu = input("Pilih menu: ")

        if menu == "1":
            menu_penyewa()

        elif menu == "2":
            menu_admin()

        elif menu == "3":
            print("Keluar dari sistem...")
            break

        else:
            print("Menu tidak valid, coba lagi.")
