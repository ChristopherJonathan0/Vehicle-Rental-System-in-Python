from abc import ABC, abstractmethod
from datetime import datetime


class Vehicle(ABC):
    def __init__(self, vehicle_id, brand, rate_per_hour):
        self.vehicle_id = vehicle_id
        self.brand = brand
        self.__rate_per_hour = rate_per_hour  

    # getter
    def get_rate_per_hour(self):
        return self.__rate_per_hour

    # setter
    def set_rate_per_hour(self, value):
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
        self.renter = renter
        self.hours = hours
        self.cost = cost
        self.datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def save_transactions(self, filename="transactionscar.txt"):
        try:
            with open(filename, "a") as f:
                f.write(f"{self.datetime} | {self.renter} | {self.vehicle.brand} | {self.hours} jam | Rp {self.cost}\n")
            print("✅ Transaksi berhasil disimpan!\n")
        except Exception as ex:
            print("Error saat menyimpan transaksi:", ex)



if __name__ == "__main__":
    while True:
        print("\n=== Sistem Penyewaan Kendaraan ===")
        print("1. Tambah Transaksi Baru")
        print("2. Lihat Semua Transaksi")
        print("3. Keluar")

        menu = input("Pilih menu: ")

        if menu == "1":
            renter = input("\nMasukkan nama penyewa: ")
            type = input("Jenis kendaraan (Car/Motorcycle/Truck): ")
            brand = input("Masukkan merek kendaraan: ")
            rate_per_hour = int(input("Masukkan tarif per jam (Rp): "))
            hours = int(input("Durasi sewa (jam): "))

            # Buat objek sesuai jenis kendaraan
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
                print("❌ Jenis kendaraan tidak valid.")
                continue

            cost = vehicle.calculate_rent(hours)
            print(f"\nTotal biaya sewa: Rp {cost}")

            transaksi = RentalSystem(vehicle, renter, hours, cost)
            transaksi.save_transactions()

        elif menu == "2":
            try:
                with open("transactionscar.txt", "r") as f:
                    print("\n=== DAFTAR TRANSAKSI ===")
                    print(f.read())
            except FileNotFoundError:
                print("Belum ada transaksi tersimpan.")

        elif menu == "3":
            print("Keluar dari sistem...")
            break
        else:
            print("Menu tidak valid, coba lagi.")
