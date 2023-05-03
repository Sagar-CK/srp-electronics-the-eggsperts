import board
import external
import time
import measure
import statemachine
import buzzer
import config
from readings import Readings

loop_times = 1000
write_every = 100
sleepy_time = 1/loop_times

# default config time -> .json
delay_pyro_miliseconds = config.get_deployment_timer()
baro_detect_miliseconds = config.get_baro_timer()
print(f'Read in a delay of {delay_pyro_miliseconds} ms and {baro_detect_miliseconds} ms from the config file')

# initialize readings (sd, mpu, baro)
r = Readings()

# states are defined for pyro not for servos
states = statemachine.Statemachine(r, PYRO_FIRE_DELAY_MS = delay_pyro_miliseconds, BARO_DETECT_AFTER_MS = baro_detect_miliseconds)

states._queue_low_beep(1000)

readings = 0
while True:
    if readings % 2:
        r.log_all_measurements()
    buzzer.buzzer_tick()
    states.tick()
    readings+=1

    if(readings == write_every):
        readings = 0
        r.write_measurements()

    time.sleep(sleepy_time)
