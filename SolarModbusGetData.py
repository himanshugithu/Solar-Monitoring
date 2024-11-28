from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.exceptions import ModbusIOException
import schedule
from threading import Lock
from datetime import datetime
import time
import logging
from om2m import create_cin

# Configure logging
logging.basicConfig(
    filename="inverter_data.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
_url = f"http://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-SL/SL-VN02-00/Data"

lock = Lock()

def log_message(message):
    """Log messages to both console and log file."""
    print(message)
    logging.info(message)

# Configurable Modbus settings
MODBUS_SETTINGS = {
    "port": "/dev/ttyUSB0",  # Replace with your Modbus port
    "baudrate": 9600,
    "parity": "N",
    "stopbits": 1,
    "timeout": 2,
    "node_address": 1  # Update with your device's node address
}

# Modbus parameters to read with their register type, scaling, and units
PARAMETERS = {
    "Eac_today": {"register": [26, 27], "type": "input", "scaling": 0.1, "unit": "kWh"},
    "Eac_total": {"register": [28, 29], "type": "input", "scaling": 0.1, "unit": "kWh"},
    "ActivePower": {"register": [11, 12], "type": "input", "scaling": 0.1, "unit": "W"},
    "Frequency": {"register": [13], "type": "input", "scaling": 0.01, "unit": "Hz"},
    "Power Factor": {"register": [5], "type": "holding", "scaling": 0.0001, "unit": ""},

    "Voltage1": {"register": [14], "type": "input", "scaling": 0.1, "unit": "V"},
    "Current1": {"register": [15], "type": "input", "scaling": 0.1, "unit": "A"},
    "Power1": {"register": [16,17], "type": "input", "scaling": 0.1, "unit": "W"},

    "Voltage2": {"register": [18], "type": "input", "scaling": 0.1, "unit": "V"},
    "Current2": {"register": [19], "type": "input", "scaling": 0.1, "unit": "A"},
    "Power2": {"register": [20,21], "type": "input", "scaling": 0.1, "unit": "W"},

    "Voltage3": {"register": [22], "type": "input", "scaling": 0.1, "unit": "V"},
    "Current3": {"register": [23], "type": "input", "scaling": 0.1, "unit": "A"},
    "Power3": {"register": [24,25], "type": "input", "scaling": 0.1, "unit":"W"},

    "PV1Voltage": {"register": [3], "type": "input", "scaling": 0.1, "unit": "V"},
    "PV1Current": {"register": [4], "type": "input", "scaling": 0.1, "unit": "A"},
    "PV1Power": {"register": [5, 6], "type": "input", "scaling": 0.1, "unit": "W"},

    "PV2Voltage": {"register": [7], "type": "input", "scaling": 0.1, "unit": "V"},
    "PV2Current": {"register": [8], "type": "input", "scaling": 0.1, "unit": "A"},
    "PV2Power": {"register": [9, 10], "type": "input", "scaling": 0.1, "unit": "W"},
    # Add additional parameters here as needed
}

def read_inverter_data():
    """Read data from the inverter using Modbus."""
    client = ModbusClient(
        method='rtu',
        port=MODBUS_SETTINGS["port"],
        baudrate=MODBUS_SETTINGS["baudrate"],
        parity=MODBUS_SETTINGS["parity"],
        stopbits=MODBUS_SETTINGS["stopbits"],
        timeout=MODBUS_SETTINGS["timeout"]
    )

    try:
        if not client.connect():
            log_message("Error: Unable to connect to the inverter.")
            return

        log_message("Connected to the inverter.")
        results = {"Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        
        for param_name, details in PARAMETERS.items():
            registers = details["register"]
            reg_type = details["type"]
            scaling = details["scaling"]
            unit = details["unit"]

            # Handle multi-register (e.g., 2-register values) and single-register parameters
            if len(registers) == 2:  # Multi-register parameter
                if reg_type == "input":
                    response_high = client.read_input_registers(registers[0], 1, unit=MODBUS_SETTINGS["node_address"])
                    response_low = client.read_input_registers(registers[1], 1, unit=MODBUS_SETTINGS["node_address"])
                elif reg_type == "holding":
                    response_high = client.read_holding_registers(registers[0], 1, unit=MODBUS_SETTINGS["node_address"])
                    response_low = client.read_holding_registers(registers[1], 1, unit=MODBUS_SETTINGS["node_address"])
                else:
                    results[param_name] = "Invalid register type"
                    continue

                if not response_high.isError() and not response_low.isError():
                    raw_value = (response_high.registers[0] << 16) + response_low.registers[0]
                    scaled_value = raw_value * scaling
                    results[param_name] = f"{scaled_value:.2f} {unit}"
                else:
                    results[param_name] = "Error reading value"
            else:  # Single-register parameter
                if reg_type == "input":
                    response = client.read_input_registers(registers[0], 1, unit=MODBUS_SETTINGS["node_address"])
                elif reg_type == "holding":
                    response = client.read_holding_registers(registers[0], 1, unit=MODBUS_SETTINGS["node_address"])
                else:
                    results[param_name] = "Invalid register type"
                    continue

                if not response.isError():
                    raw_value = response.registers[0]
                    scaled_value = raw_value * scaling
                    results[param_name] = f"{scaled_value:.2f} {unit}"
                else:
                    results[param_name] = "Error reading value"

        # Log the results
        data=[]
        for key, value in results.items():
            log_message(f"{key}: {value}")
            numeric_part  = ''.join([char for char in value if char.isdigit() or char == '.'])
            formatted_value = f"{float(numeric_part):.2f}"
            data.append(formatted_value)
        data[0] = (int(time.time()))  
        print(data)  
        create_cin(_url,data)    
        

    except Exception as e:
        log_message(f"Error: {e}")
    finally:
        client.close()
        log_message("Connection closed.")

def scheduled_read_inverter_data():
    """Ensure thread-safe execution of inverter data reading."""
    if lock.locked():
        log_message("Previous execution still in progress. Skipping this cycle.")
        return
    with lock:
        read_inverter_data()

if __name__ == "__main__":
    
    log_message("Starting scheduler...")
    schedule.every(60).seconds.do(scheduled_read_inverter_data)
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)  # Prevent high CPU usage
    except KeyboardInterrupt:
        log_message("Scheduler stopped. Exiting program.")