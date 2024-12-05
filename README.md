# Solar Monitoring

This project reads data from a solar inverter using Modbus and sends the data to an OM2M server. It also blinks the built-in LED on a Raspberry Pi to indicate that the script is running.

## Features

- Reads data from a solar inverter using Modbus protocol.
- Sends the collected data to an OM2M server.
- Blinks the built-in LED on a Raspberry Pi to show that the script is running.
- Configurable via a JSON configuration file.
- Can be run as a systemd service for continuous monitoring.

## Prerequisites

- Python 3.x
- Raspberry Pi with built-in LED (typically connected to GPIO 17)

## Configuration

The project uses a JSON configuration file to specify Modbus settings and parameters to read from the inverter. Below is an example `config.json` file:

```json
{
    "modbus_settings": {
        "port": "/dev/ttyUSB0",
        "baudrate": 9600,
        "parity": "N",
        "stopbits": 1,
        "timeout": 2,
        "node_address": 1
    },
    "parameters": {
        "Eac_today": {"register": [26, 27], "type": "input", "scaling": 0.1, "unit": "kWh"},
        "Eac_total": {"register": [28, 29], "type": "input", "scaling": 0.1, "unit": "kWh"},
        "ActivePower": {"register": [11, 12], "type": "input", "scaling": 0.1, "unit": "W"},
        "Frequency": {"register": [13], "type": "input", "scaling": 0.01, "unit": "Hz"},
        "Power Factor": {"register": [5], "type": "holding", "scaling": 0.0001, "unit": ""},
        "Voltage1": {"register": [14], "type": "input", "scaling": 0.1, "unit": "V"},
        "Current1": {"register": [15], "type": "input", "scaling": 0.1, "unit": "A"},
        "Power1": {"register": [16, 17], "type": "input", "scaling": 0.1, "unit": "W"},
        "Voltage2": {"register": [18], "type": "input", "scaling": 0.1, "unit": "V"},
        "Current2": {"register": [19], "type": "input", "scaling": 0.1, "unit": "A"},
        "Power2": {"register": [20, 21], "type": "input", "scaling": 0.1, "unit": "W"},
        "Voltage3": {"register": [22], "type": "input", "scaling": 0.1, "unit": "V"},
        "Current3": {"register": [23], "type": "input", "scaling": 0.1, "unit": "A"},
        "Power3": {"register": [24, 25], "type": "input", "scaling": 0.1, "unit": "W"},
        "PV1Voltage": {"register": [3], "type": "input", "scaling": 0.1, "unit": "V"},
        "PV1Current": {"register": [4], "type": "input", "scaling": 0.1, "unit": "A"},
        "PV1Power": {"register": [5, 6], "type": "input", "scaling": 0.1, "unit": "W"},
        "PV2Voltage": {"register": [7], "type": "input", "scaling": 0.1, "unit": "V"},
        "PV2Current": {"register": [8], "type": "input", "scaling": 0.1, "unit": "A"},
        "PV2Power": {"register": [9, 10], "type": "input", "scaling": 0.1, "unit": "W"}
    },
    "url": ""
}
```

## Environment Variables

The project uses the following environment variables for configuration:

- `DEV_USERNAME`: Username for the OM2M server.
- `DEV_PASSWORD`: Password for the OM2M server.
- `OM2M_URL`: URL of the OM2M server. 
> The OM2M_URL in the environment is just for testing not needed for production deployment 

### Installation & Setup

1. Clone the GitHub repository:

    ```bash
    git clone https://github.com/your-repo/solar-monitoring.git
    cd solar-monitoring
    ```

2. Create a Python3 virtual environment:

    ```bash
    python3 -m venv venv
    ```

3. Activate the virtual environment:

    ```bash
    source venv/bin/activate
    ```

4. Install the module and its dependencies:

    ```bash
    pip install .
    ````


## Running the Program

To run the program, use the following command:

```bash
solar-monitoring --config config.json
```
<!-- 
## Blinking LED

The built-in LED on the Raspberry Pi will blink to indicate that the script is running. This is achieved using the `gpiozero` library. -->

