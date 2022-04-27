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