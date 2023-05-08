import board
import busio
import adafruit_bmp280
import adafruit_mpu6050
import sdcardio
import storage
import time
import random
import buzzer

class Readings:
    def __init__(self):
        self.gyro_lowpass = 0.05
        self.acc_lowpass = 0.3
            
        self.rn = random.randrange(1000,9999)
        self.log_event("STARTING READINGS SET UP")


        # Create arrays to store data of each sensor and events
        self.bmp280_data = []
        self.mpu6050_data = []
        self.events_data = []
        
        self.alt_list = []
        self.current_altitude = 0
        self.max_altitude = 0

        try:
            self.i2c = board.I2C()
            self.bmp = adafruit_bmp280.Adafruit_BMP280_I2C(self.i2c, address=0x76)
            self.mpu = adafruit_mpu6050.MPU6050(self.i2c)
            self.mpu.accelerometer_range = adafruit_mpu6050.Range.RANGE_16_G
            self.log_event(f"SUCCESFULLY SET UP SENSORS")

        except OSError as e:
            print("Failed initial sensor setup", e)
            self.log_event(f"FAILED SET UP SENSORS: {e}")

        # Set up SD card
        print("Initializing SD card...")
        try:
            # Use the board's primary SPI bus
            # first one used to be board.SCK, board.MOSI, board.MISO
            spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

            # For breakout boards, you can choose any GPIO pin that's convenient (in this case digital 6)
            cs = board.D6

            sdcard = sdcardio.SDCard(spi, cs)
            vfs = storage.VfsFat(sdcard)
            storage.mount(vfs, "/sd")

            print("SD Initialized")
            self.log_event(f"SUCCESFULLY INITIALIZED SD")
        
        except OSError as e:
            print("Failed to initialize SD card:", e)
            self.log_event(f"FAILED TO INITIALIZE SD: {e}")

        # Take average of sensor data over time to set an accurate** 0 value
        print("Calibrating sensors...")
        
        try:
            # Calibrate BMP280
            self.avg_alt = 0.0
            self.delta_alt = 0.0
            
            pressures = []
            for i in range(1,20):
                pressures.append(self.bmp.pressure)
                time.sleep(0.1)
            self.bmp.sea_level_pressure = sum(pressures) / len(pressures)

            print("Succesfully calibrated sensors:", self.bmp.sea_level_pressure)
            self.log_event(f"SUCCESFULLY CALIBRATED SENSORS (SLP {self.bmp.sea_level_pressure})")
            
        except OSError as e:
            print("Failed to calibrate sensors:", e)
            self.log_event(f"FAILED TO CALIBRATE SENSORS: {e}")

    def baro_detect_apogee(self):
        # Get current altitude and compare to previous altitude (max) to see if we are still going up
        if self.current_altitude + 5 < self.max_altitude:
            return True
        return False

    def log_all_measurements(self):
        self.write_events()
        self.log_bmp280_readings()
        self.log_mpu6050_readings()

    def write_measurements(self):
        self.write_bmp280_measurements()
        self.write_mpu6050_measurements()
        self._queue_low_beep(50)
        
    def write_events(self):
        if len(self.events_data) > 0:
            print("Writing events to file")
            try:
                with open(f"/sd/events_{self.rn}.txt", "a") as f:
                    for event in self.events_data:
                        f.write("%s, %s\n" % (event))
                print("Succesfully wrote events")
                self.events_data = []

            except OSError as e:
                print("Error writing event:", e)
                self.log_event(f"FAILED TO WRITE EVENTS: {e}")
        return

    def write_bmp280_measurements(self):
        if len(self.bmp280_data) > 0:
            print("Writing BMP280 measurements to file")
            try:
                with open(f"/sd/bmp280_{self.rn}.txt", "a") as f:
                    for measurement in self.bmp280_data:
                        f.write("%s, %s, %s, %s\n" % (measurement))
                print("Succesfully wrote BMP data")
           
            except OSError as e:
                print("Error writing BMP data:", e)
                self.log_event(f"FAILED TO WRITE BMP DATA: {e}")
            self.bmp280_data = []
        return


    def write_mpu6050_measurements(self):
        if len(self.mpu6050_data) > 0:
            print("Writing MPU6050 measurements to file...")
            try:
                with open(f"/sd/mpu6050_{self.rn}.txt", "a") as f:
                    for measurement in self.mpu6050_data:
                        f.write("%s, %s, %s, %s\n" % (measurement))
                print("Succesfully wrote MPU data")
           
            except OSError as e:
                print("Error writing MPU data:", e)
                self.log_event(f"FAILED TO WRITE MPU DATA: {e}")
            self.mpu6050_data = []
        return
    
    def log_event(self, event: str):
        try:
            self.events_data.append((time.monotonic(), event))
        
        except OSError as e:
            print("Error occured logging events:", e)
            self.log_event(f"FAILED TO LOG EVENT: {e}")

    def log_bmp280_readings(self):
        self.current_altitude = self.bmp.altitude
        
        # Update max altitude
        if self.current_altitude >= self.max_altitude:
            self.max_altitude = self.current_altitude

        try:
            self.bmp280_data.append((time.monotonic(), self.bmp.temperature, self.bmp.pressure, self.bmp.altitude))
        except OSError as e:
            print("Error occured reading BMP280:", e)
            self.log_event(f"FAILED TO READ BMP DATA: {e}")


    def log_mpu6050_readings(self):
        try:
            self.mpu6050_data.append((time.monotonic(), self.mpu.acceleration, self.mpu.gyro, self.mpu.temperature))
        except OSError as e:
            print("Error occured reading MPU6050:", e)
            self.log_event(f"FAILED TO READ MPU DATA: {e}")

    def _queue_short_beep(self):
        buzzer.append_buzzer_note(2000, 100)
        buzzer.append_buzzer_wait(100)
        buzzer.append_buzzer_note(2000, 100)
        buzzer.append_buzzer_wait(100)

    def _queue_long_beep(self):
        buzzer.append_buzzer_note(2000, 1000)
        buzzer.append_buzzer_wait(1000)
        
    def _queue_low_beep(self, length: int):
        buzzer.append_buzzer_note(1500, length)
        buzzer.append_buzzer_wait(length)
        
    def _queue_high_beep(self, length: int):
        buzzer.append_buzzer_note(2500, length)
        buzzer.append_buzzer_wait(length)
