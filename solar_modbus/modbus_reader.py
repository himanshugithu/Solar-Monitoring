from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.exceptions import ModbusIOException
from datetime import datetime
import time
from solar_modbus.logger import log_message
from solar_modbus.om2m import create_cin
import json

def read_inverter_data(modbus_settings, parameters, url):
    """Read data from the inverter using Modbus."""
    client = ModbusClient(
        method='rtu',
        port=modbus_settings["port"],
        baudrate=modbus_settings["baudrate"],
        parity=modbus_settings["parity"],
        stopbits=modbus_settings["stopbits"],
        timeout=modbus_settings["timeout"]
    )

    try:
        if not client.connect():
            log_message("Error: Unable to connect to the inverter.")
            return

        log_message("Connected to the inverter.")
        results = {"Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        
        for param_name, details in parameters.items():
            registers = details["register"]
            reg_type = details["type"]
            scaling = details["scaling"]
            unit = details["unit"]

            # Handle multi-register (e.g., 2-register values) and single-register parameters
            if len(registers) == 2:  # Multi-register parameter
                if reg_type == "input":
                    response_high = client.read_input_registers(registers[0], 1, unit=modbus_settings["node_address"])
                    response_low = client.read_input_registers(registers[1], 1, unit=modbus_settings["node_address"])
                elif reg_type == "holding":
                    response_high = client.read_holding_registers(registers[0], 1, unit=modbus_settings["node_address"])
                    response_low = client.read_holding_registers(registers[1], 1, unit=modbus_settings["node_address"])
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
                    response = client.read_input_registers(registers[0], 1, unit=modbus_settings["node_address"])
                elif reg_type == "holding":
                    response = client.read_holding_registers(registers[0], 1, unit=modbus_settings["node_address"])
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
        create_cin(url, data)    
        

    except Exception as e:
        log_message(f"Error: {e}")
    finally:
        client.close()
        log_message("Connection closed.")