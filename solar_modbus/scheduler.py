import schedule
import time
from threading import Lock
from solar_modbus.logger import log_message
from solar_modbus.modbus_reader import read_inverter_data

lock = Lock()

def scheduled_read_inverter_data(modbus_settings, parameters, url):
    """Ensure thread-safe execution of inverter data reading."""
    if lock.locked():
        log_message("Previous execution still in progress. Skipping this cycle.")
        return
    with lock:
        read_inverter_data(modbus_settings, parameters, url)

def start_scheduler(modbus_settings, parameters, url):
    log_message("Starting scheduler...")
    schedule.every(60).seconds.do(scheduled_read_inverter_data, modbus_settings, parameters, url)
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)  # Prevent high CPU usage
    except KeyboardInterrupt:
        log_message("Scheduler stopped. Exiting program.")