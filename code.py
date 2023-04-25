import board
import external
import time
import measure
import statemachine
import buzzer
import config
from readings import Readings

# default config time -> .json
delay_pyro_miliseconds = config.get_deployment_timer()
print(f'Read in a delay of {delay_pyro_miliseconds} ms from the config file')

# states are defined for pyro not for servos
states = statemachine.Statemachine(PYRO_FIRE_DELAY_MS = delay_pyro_miliseconds)
r = Readings()

readings = 0

while True:
    
    r.log_all_measurements()
    buzzer.buzzer_tick()
    states.tick()
    readings+=1

    if(readings == 20):
        readings = 0
        r.write_measurements()
