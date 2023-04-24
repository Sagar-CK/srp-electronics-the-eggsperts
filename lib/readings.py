import board
import busio
import adafruit_bmp280
import adafruit_mpu6050
import sdcardio
import storage

class Readings:

    def __init__(self):
        # Create two arrays to store the data of the BMP280 and MPU6050
        self.bmp280_data = []
        self.mpu6050_data = []

        # i2c = busio.I2C(board.SCL, board.SDA)

        # self.bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
        # self.bmp280.sea_level_pressure = 1013.25
        # self.mpu6050 = adafruit_mpu6050.MPU6050(i2c)
        print("Initializing SD card...")

        # Use the board's primary SPI bus
        # first one used to be board.SCK, board.MOSI, board.MISO
        # spi = busio.SPI(board.D13, MOSI=board.D11, MISO=board.D12)

        # # For breakout boards, you can choose any GPIO pin that's convenient:
        # cs = board.D10
        # sdcard = sdcardio.SDCard(spi, cs)
        # vfs = storage.VfsFat(sdcard)
        # storage.mount(vfs, "/sd")

    def log_all_measurements(self):
        self.log_bmp280_readings()
        self.log_mpu6050_readings()

    def write_measurements(self):
        self.write_bmp280_measurements()
        self.write_mpu6050_measurements()

    def write_bmp280_measurements(self):
        print("Writing BMP280 measurements to file")
        # with open("/sd/bmp280.txt", "a") as f:
        #     for measurement in self.bmp280_data:
        #         f.write(measurement)
        #         f.write("\n")


    def write_mpu6050_measurements(self):
        print("Writing MPU6050 measurements to file")
        # with open("/sd/mpu6050.txt", "a") as f:
        #     for measurement in self.mpu6050_data:
        #         f.write(measurement)
        #         f.write("\n")


    def log_bmp280_readings(self):
        print("bmp reading")
        # self.bmp280_data.append(self.bmp280.temperature, self.bmp280.pressure, self.bmp280.altitude)


    def log_mpu6050_readings(self):
        print("mpu reading")
        # self.mpu6050_data.append(self.mpu6050.acceleration, self.mpu6050.gyro, self.mpu6050.temperature)
      