import board
import busio
import adafruit_bmp280
import adafruit_mpu6050
import adafruit_sdcard
import storage

class Readings:
    def __init__(self):
        # i2c = busio.I2C(board.SCL, board.SDA)

        # self.bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
        # self.bmp280.sea_level_pressure = 1013.25
        # self.mpu6050 = adafruit_mpu6050.MPU6050(i2c)
        print("Initializing SD card...")

        # spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        # cs = board.D10
        # sdcard = adafruit_sdcard.SDCard(spia, cs)
        # vfs = storage.VfsFat(sdcard)
        # storage.mount(vfs, "/sd")

    def start_logging(self):
        print("Starting logging...")
        # self.log_bmp280_readings()
        # self.log_mpu6050_readings()


    def log_bmp280_readings(self):
        print("recording")
        # print("Temperature: %0.1f C" % self.bmp280.temperature)
        # print("Pressure: %0.1f hPa" % self.bmp280.pressure)
        # print("Altitude = %0.2f meters" % self.bmp280.altitude)

        # with open("bmp280.txt", "a") as f:
        #     f.write(f"Temperature: {self.bmp280.temperature} C\n")
        #     f.write(f"Pressure: {self.bmp280.pressure} hPa\n")
        #     f.write(f"Altitude: {self.bmp280.altitude} meters\n")

        # with open("/sd/bmp280.txt", "a") as f:
        #     f.write(f"Temperature: {self.bmp280.temperature} C\n")
        #     f.write(f"Pressure: {self.bmp280.pressure} hPa\n")
        #     f.write(f"Altitude: {self.bmp280.altitude} meters\n")

    def log_mpu6050_readings(self):
        print("recording")
        # print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % self.mpu6050.acceleration)
        # print("Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s" % self.mpu6050.gyro)
        # print("Temperature: %.2f C" % self.mpu6050.temperature)

        # with open("mpu6050.txt", "a") as f:
        #     accel_x, accel_y, accel_z = self.mpu6050.acceleration
        #     gyro_x, gyro_y, gyro_z = self.mpu6050.gyro

        #     f.write("Acceleration (m/s^2): ({0:.2f}, {1:.2f}, {2:.2f})\n".format(
        #         accel_x, accel_y, accel_z))
        #     f.write("Gyro (deg/s): ({0:.2f}, {1:.2f}, {2:.2f})\n".format(
        #         gyro_x, gyro_y, gyro_z))

        # with open("/sd/mpu6050.txt", "a") as f:
        #     accel_x, accel_y, accel_z = self.mpu6050.acceleration
        #     gyro_x, gyro_y, gyro_z = self.mpu6050.gyro

        #     f.write("Acceleration (m/s^2): ({0:.2f}, {1:.2f}, {2:.2f})\n".format(
        #         accel_x, accel_y, accel_z))
        #     f.write("Gyro (deg/s): ({0:.2f}, {1:.2f}, {2:.2f})\n".format(
        #         gyro_x, gyro_y, gyro_z))

