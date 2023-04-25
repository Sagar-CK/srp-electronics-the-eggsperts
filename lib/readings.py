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
        
        self.i2c = board.I2C()
        self.bmp = adafruit_bmp280.Adafruit_BMP280_I2C(self.i2c, address=0x76)
        self.mpu = adafruit_mpu6050.MPU6050(self.i2c)
        
        self.gyro_lowpass = 0.05
        self.acc_lowpass = 1
        
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        
        self.vx = 0.0
        self.vy = 0.0
        self.vz = 0.0
        
        self.ax0 = self.mpu.acceleration[0]
        self.ay0 = self.mpu.acceleration[1]
        self.az0 = self.mpu.acceleration[2]
        
        self.theta_x = 0.0
        self.theta_y = 0.0
        self.theta_z = 0.0
        
        self.omega_x0 = self.mpu.gyro[0]
        self.omega_y0 = self.mpu.gyro[1]
        self.omega_z0 = self.mpu.gyro[2]

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
        return
        # with open("/sd/bmp280.txt", "a") as f:
        #     for measurement in self.bmp280_data:
        #         f.write(measurement)
        #         f.write("\n")


    def write_mpu6050_measurements(self):
        print("Writing MPU6050 measurements to file (not)")
        return
        # with open("/sd/mpu6050.txt", "a") as f:
        #     for measurement in self.mpu6050_data:
        #         f.write(measurement)
        #         f.write("\n")


    def log_bmp280_readings(self):
        temp = self.bmp.temperature
        pressure = self.bmp.pressure
        altitude = self.bmp.altitude
        
        print((temp, pressure, altitude))
        # self.bmp280_data.append(self.bmp280.temperature, self.bmp280.pressure, self.bmp280.altitude)


    def log_mpu6050_readings(self):
        ax, ay, az = self.mpu.acceleration
        omega_x, omega_y, omega_z = self.mpu.gyro
        
        omega_x_filtered = omega_x if abs(omega_x) >= self.gyro_lowpass else 0.0
        omega_y_filtered = omega_y if abs(omega_y) >= self.gyro_lowpass else 0.0
        omega_z_filtered = omega_z if abs(omega_z) >= self.gyro_lowpass else 0.0
        
        ax_filtered = (ax - self.ax0) * (1/100) if abs(ax) >= self.acc_lowpass else 0.0
        ay_filtered = (ay - self.ay0) * (1/100) if abs(ay) >= self.acc_lowpass else 0.0
        az_filtered = (az - self.az0) * (1/100) if abs(az) >= self.acc_lowpass else 0.0
        
        self.vx += ax_filtered
        self.vy += ay_filtered
        self.vz += az_filtered
        
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz
        
        self.theta_x += omega_x_filtered
        self.theta_y += omega_y_filtered
        self.theta_z += omega_z_filtered
        
        # print((self.theta_x, self.theta_y, self.theta_z))
        # self.mpu6050_data.append(self.mpu6050.acceleration, self.mpu6050.gyro, self.mpu6050.temperature)
      