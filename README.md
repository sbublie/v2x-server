# V2X-Server Smart Intersection Server

V2X-Server is the backend application for [V2X-Pilot](https://github.com/sbublie/v2x-pilot). It can decode and expose data received from smart intersections.

The app was developed to communicate with the smart intersections in Friedrichshafen. The current implementation is optimized for the [intersection 309](https://www.google.de/maps/@47.6551006,9.4819818,20.96z).

## Features

- UDP message processing for receiving messages from [Cohda Mk5 OBU](https://www.cohdawireless.com/solutions/hardware/mk5-obu/).
- MAPEM/SPATEM message decoding using [asn1tools](https://github.com/eerimoq/asn1tools) and the [ans.1 specification](https://forge.etsi.org/rep/ITS/asn1/is_ts103301) provided by ETSI.
- GraphQL API server using [Flask](https://flask.palletsprojects.com/en/2.0.x/) and [Ariadne](https://ariadnegraphql.org/) for exposing the data to clients.

## Getting started

To avoid compatibility issues please create a new virtual environment for this project.

1. Check your Python version with `python -V`. The app requires at least **Python 3.10**!
2. Clone the repository and open the terminal in the main folder.
3. Install the required packages with `pip install -r requirements.txt`.
4. Start the server with `python -m v2x_server`. In case you want to start the server in offline mode with sample data use `python -m v2x_server debug`.
5. The GraphQL playground is now available at <http://localhost:5000/graphql>. API requests can be sent to this endpoint (POST request). GraphQL schema and documentation are available on the right side of the playground application.

Example GraphQL query for requesting available messages and signal groups:

```graphql
query {
  available_messages {
    messages {
      intersection_id
      spat_available
      map_available
    }
  }
  intersection(intersectionId: 309) {
    item {
      name
      signal_groups {
        id
      }
    }
  }
}
```

# User Reference

### Required Hardware:

- Cohda Mk5 OBU with antenna and corresponding power cable
- 12V power supply for Cohda OBU (e.g. 12V battery)
- Raspberry Pi, SD card and power supply
- Ethernet cable
- PC for setup
- Client OBU (Windows or Android device)

### Raspberry Pi Configuration

- Wi-Fi SSID: _ITSRouter_
- Wi-Fi password: itsrouter
- IP address: 192.168.1.1
- SSH user: pi
- SSH password: raspberry

### Cohda OBU Configuration

- IP address: fe80::6e5:48ff:fe20:5b58%eth0
- SSH user: user
- SSH password: user

## Step-by-Step Setup Guide

### **Hardware Connection**

_Do not power on the Cohda OBU before connecting the antenna!_

**1.** Connect all three antenna cables to the Cohda OBU.

**2.** Connect the Raspberry Pi and the Cohda OBU using the Ethernet cable.

**3.** Power on the Raspberry Pi by using the micro USB power supply or a power bank.

**4.** Power on the Cohda OBU by connecting it to the power supply with the enclosed battery cable. Please check the polarity!

### **Raspberry Pi**

**1.** Connect the PC to the Raspberry Pi's Wi-Fi network. SSID: `ITSRouter` Password: `itsrouter`

**2.** Establish a ssh connection to the Raspberry Pi from the terminal:

```bash
ssh pi@192.168.1.1
```

Password: `raspberry`

**3.** Navigate to the subfolder with

```bash
cd ./v2x-server
```

**4.** Run the V2X-Server with:

```bash
python -m v2x_server
```

To start the server with sample data use:

```bash
python -m v2x_server debug
```

### **Cohda OBU**

**1.** Establish a ssh connection to the Raspberry Pi from the terminal:

```bash
ssh pi@192.168.1.1
```

Password: `raspberry`

**2.** Connect to the Cohda OBU using:

```bash
ssh user@fe80::6e5:48ff:fe20:5b58%eth0
```

Password: `user`

**3.** To initiate the UDP package redirection to the Raspberry Pi use:

```bash
/opt/cohda/test/runtest_monitor.sh 180 192.168.1.1 target
```

The program is now running and can be cancelled with _Ctrl + C_.

### **Client**

**1.** Connect the client device to the Raspberry Pi's Wi-Fi network.

**2.** Open the V2X-Pilot app. If the app asks for an IP address enter `192.168.1.1` and hit confirm.

# Create an executable

Use `pyinstaller` to create a `.exe` file for publishing the app.

A single file executable can be created with:

```bash
pyinstaller --onefile --add-data "rsc/etsi_mapem_spatem.asn;rsc" --add-data "graphql_api/schema.graphql;graphql_api" .\v2x_server.py
```

_Replace all `;` with `:` on Linux_

This creates a file in the `dist` folder. Make sure to provide the asn.1 file in `dist/rsc` and the GraphQL schema in `dist/graphql_api` before starting the app.
