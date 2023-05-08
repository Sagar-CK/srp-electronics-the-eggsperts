import time
import buzzer
import external
from measure import is_pyro_inserted, is_bw_inserted, is_armed, get_vbat_voltage

class States():
        SYSTEMS_CHECK = 0
        ERROR_MODE = 1
        IDLE_MODE = 2
        PREPERATION_MODE = 3
        ARMED_MODE = 4
        LAUNCHED_MODE = 5
        DEPLOYED_MODE = 6

class Statemachine:

        def __init__(self, readings, PYRO_FIRE_DELAY_MS=20000, BARO_DETECT_AFTER_MS=9000):
                self.state = States.SYSTEMS_CHECK
                self.last_in_state_action = round(time.monotonic()*1000)
                self.last_state_transition = round(time.monotonic()*1000)
                self.launched_time = 0
                self.do_state_action()
                self.STATE_ACTION_DELAY_MS = 5000
                self.MIN_STATE_DELAY_MS = 500
                self.PYRO_FIRE_DELAY_MS = PYRO_FIRE_DELAY_MS
                self.BARO_DETECT_AFTER_MS = BARO_DETECT_AFTER_MS
                self.LAUNCHED = False
                self.readings = readings

        def tick(self):
            if self.last_in_state_action + self.STATE_ACTION_DELAY_MS < round(time.monotonic()*1000):
                self.do_state_action()
                self.last_in_state_action = round(time.monotonic()*1000)
            if self.last_state_transition + self.MIN_STATE_DELAY_MS < round(time.monotonic()*1000):
                self.check_state_transition()

        def check_state_transition(self):
            if self.state == States.SYSTEMS_CHECK:
                if not is_pyro_inserted():
                    self.do_state_transition(States.ERROR_MODE)
                elif is_pyro_inserted() and self._battery_voltage_valid():
                    self.do_state_transition(States.IDLE_MODE)

            elif self.state == States.ERROR_MODE:
                if is_pyro_inserted() and not is_armed() and self._battery_voltage_valid():
                    self.do_state_transition(States.IDLE_MODE)

            elif self.state == States.IDLE_MODE:
                if is_armed():
                    self.do_state_transition(States.ERROR_MODE)
                elif is_bw_inserted():
                    self.do_state_transition(States.PREPERATION_MODE)

            elif self.state == States.PREPERATION_MODE:
                if is_armed() and not is_pyro_inserted():
                    self.do_state_transition(States.ERROR_MODE)
                elif is_armed() and is_pyro_inserted():
                    self.do_state_transition(States.ARMED_MODE)
                elif not is_bw_inserted():
                    self.do_state_transition(States.IDLE_MODE)

            elif self.state == States.ARMED_MODE:
                if not is_armed():
                    self.do_state_transition(States.PREPERATION_MODE)
                elif not is_bw_inserted():
                    self.do_state_transition(States.LAUNCHED_MODE)


            elif self.state == States.LAUNCHED_MODE:
                if self.check_if_pyro_should_be_fired():
                    self.do_state_transition(States.DEPLOYED_MODE)

            elif self.state == States.DEPLOYED_MODE:
                pass




        def do_state_action(self):
            if self.state == States.SYSTEMS_CHECK:
                external.neopixel_disable()
            elif self.state == States.ERROR_MODE:
                self._queue_long_beep()
                external.neopixel_set_rgb(255,0,0)
            elif self.state == States.IDLE_MODE:
                external.neopixel_set_rgb(0,0,255)
            elif self.state == States.PREPERATION_MODE:
                external.neopixel_set_rgb(255,255,0)
            elif self.state == States.ARMED_MODE:
                external.neopixel_set_rgb(255,100,0)
            elif self.state == States.LAUNCHED_MODE:
                self._queue_high_beep(250)
                external.neopixel_set_rgb(0,255,0)
            elif self.state == States.DEPLOYED_MODE:
                self._queue_scream_beep(1500)
                external.neopixel_set_rgb(255,30,70)
                external.PYRO_DETONATE()

        def do_state_transition(self, to_state):
            state_trans_has_happened = False
            
            if self.state == States.SYSTEMS_CHECK:
                if to_state == States.ERROR_MODE:
                    self.state = States.ERROR_MODE
                    state_trans_has_happened = True
                    self.readings.log_event("INIT TO ERROR")
                elif to_state == States.IDLE_MODE:
                    self.state = States.IDLE_MODE
                    self._queue_short_beep()
                    state_trans_has_happened = True
                    self.readings.log_event("INIT TO IDLE")

            elif self.state == States.IDLE_MODE:
                if to_state == States.PREPERATION_MODE:
                    self.state = States.PREPERATION_MODE
                    self._queue_short_beep()
                    state_trans_has_happened = True
                    self.readings.log_event("IDLE TO PREP")
                elif to_state == States.ERROR_MODE:
                    self.state = States.ERROR_MODE
                    state_trans_has_happened = True
                    self.readings.log_event("IDLE TO ERROR")

            elif self.state == States.PREPERATION_MODE:
                if to_state == States.ARMED_MODE:
                    self.state = States.ARMED_MODE
                    self._queue_high_beep(1000)
                    state_trans_has_happened = True
                    self.readings.log_event("PREP TO ARMED")
                elif to_state == States.IDLE_MODE:
                    self.state = States.IDLE_MODE
                    self._queue_long_beep()
                    state_trans_has_happened = True
                    self.readings.log_event("PREP TO IDLE")
                elif to_state == States.ERROR_MODE:
                    self.state = States.ERROR_MODE
                    state_trans_has_happened = True
                    self.readings.log_event("PREP TO ERROR")

            elif self.state == States.ARMED_MODE:
                if to_state == States.PREPERATION_MODE:
                    self.state = States.PREPERATION_MODE
                    self._queue_long_beep()
                    state_trans_has_happened = True
                    self.readings.log_event("ARMED TO PREP")
                elif to_state == States.LAUNCHED_MODE:
                    self.state = States.LAUNCHED_MODE
                    self.LAUNCHED = True
                    self.set_launched_time()
                    state_trans_has_happened = True
                    self._queue_high_beep(1000)
                    self.readings.log_event("LAUNCH MODE TRIGGERED!")

            elif self.state == States.LAUNCHED_MODE:
                if to_state == States.DEPLOYED_MODE:
                    self.state = States.DEPLOYED_MODE
                    state_trans_has_happened = True
                    self.readings.log_event("PARACHUTE DEPLOYMENT TRIGGERED!")

            elif self.state == States.ERROR_MODE:
                if to_state == States.IDLE_MODE:
                    self.state = States.IDLE_MODE
                    self._queue_short_beep()
                    state_trans_has_happened = True
                    self.readings.log_event("ERROR TO IDLE")


            if state_trans_has_happened:
                self.do_state_action()
                self._reset_state_timer()

        def check_if_pyro_should_be_fired(self):
            if self.state != States.LAUNCHED_MODE: # Not in launching state of the statediagram
                return False
            if self.LAUNCHED == False: # Has not launched yet
                return False
            if self.launched_time == 0: # The launchtimer has not been set yet
                return False
            if self.launched_time + self.PYRO_FIRE_DELAY_MS < round(time.monotonic()*1000) or\
                (self.readings.baro_detect_apogee() and self.launched_time + self.BARO_DETECT_AFTER_MS < round(time.monotonic()*1000)): # The amount of time has passed
                self.readings.log_event(f"PYRO DEPLOY TRIGGERED AT TIMESTEP {time.monotonic()*1000}ms AT {self.readings.current_altitude}m WITH APOGEE {self.readings.max_altitude}m")
                return True
            else:
                return False

        def set_launched_time(self):
            if self.LAUNCHED == True:
                self.launched_time = round(time.monotonic()*1000)

        def _reset_state_timer(self):
            self.last_state_transition = round(time.monotonic()*1000)

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
            buzzer.append_buzzer_note(2200, length)
            buzzer.append_buzzer_wait(length)
            
        def _queue_scream_beep(self, length: int):
            buzzer.append_buzzer_note(2500, length)
            buzzer.append_buzzer_wait(length)

        def _battery_voltage_valid(self): # Todo: Make it depend on the battery configuration
            if get_vbat_voltage() > 3.0:
                return True
            else:
                return False
