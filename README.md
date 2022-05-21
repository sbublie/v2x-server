# V2X-Server Smart Intersection Server

V2X-Server is a backend application for the [V2X-Pilot](https://github.com/sbublie/v2x-pilot) app. It can decode and expose data received from smart intersections.

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
query  {
  messages {
    messages {intersection_id, spat_available, map_available}
  }
  intersection(intersectionId: 309) {
    item {
      name, signal_groups {id}
    }
  }
}
```

## Create an executable

Use `pyinstaller` to create a `.exe` file for publishing the app.

A single file executable can be created with:
```bash
pyinstaller --onefile --add-data "rsc/etsi_mapem_spatem.asn;rsc" --add-data "graphql_api/schema.graphql;graphql_api" .\v2x_server.py
```
*Replace all `;` with `:` on Linux*

This creates a file in the `dist` folder. Make sure to provide the asn.1 file in `dist/rsc` and the GraphQL schema in `dist/graphql_api` before starting the app.

![image](https://user-images.githubusercontent.com/103438908/169650332-8917ca34-fa82-45a4-9208-b2a2c83380b4.png)

## User manual: set-up of Onboard unit :

1. Connect antenna to COHDA-device (blue box) & securely place it on the vehicle's roof. There are three connectors in total:  one blue connector with thinner cable for GPS reception and two green ones with thicker cable for establishing Wi-Fi connection. Please do not attempt to switch on COHDA-device without having first connected the antenna since it functions as terminating resistor. Otherwise, there would be an open line end which can cause the signal's total reflection in phase and thus result in doubling of power. This in turn might possibly lead to the destruction of electronics.
2. Connect Raspberry Pi to COHDA-device through Ethernet cable (here: yellow cable).
3. Switch on Raspberry Pi by connecting it to power supply (Power Bank) through USB cable.
4. Switch on COHDA device by connecting it to power supply (12V battery) with the enclosed battery cable (incl. choke filter). Please be careful to apply correct polarity!
5. Connect PC to the Raspberry Pi's Wi-Fi network (ITSRouter). The password is itsrouter.
6. Connect PC to Raspberry Pi by establishing ssh-connection (address: IP 192.168.1.1) --> username pi and password Raspberry
7. The ssh-connection is then used to connect with COHDA device through the Raspberry Pi's window displayed on PC --> address to be done and password user
8. To initiate data connection call /opt/cohda/test/runtest_monitor.sh 180 192.168.1.1 target, please note that the program is now running (it can be cancelled by Ctrl + C).
9. Open a second ssh-window directed to Raspberry Pi (see step 5).
10. Run command `cd v2x-server`
11. Run command `python -m v2x_server`
12. Connect designated client (e.g. Android tablet) with the Raspberry Pi's Wi-Fi network (ITSRouter).
13. Start V2X-Pilot app on the Android tablet or in your web browser.
