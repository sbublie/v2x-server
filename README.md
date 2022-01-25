# V2X Server

This is the repository of the V2X Server which can receive, decode and expose the C-ITS/V2X messages MAPEM and SPATEM.

Please note that the project is in a very early stage. This means essential parts like error handling, documentation/comments, logging and many other features are missing!

## Getting started

To avoid compatibility issues please create a new virtual environment for this project.

1. Clone this repository and open the terminal in the main folder.
2. Install the required packages with `pip install -r requirements.txt`.
3. Start the server with `python -m v2x_server`. In case you want to start the server in offline mode with sample data use `python -m v2x_server debug`. 
4. The GraphQL playground is now available at <http://localhost:5000/graphql>. API requests can be sent to this endpoint (POST request).  

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
GraphQL docs are available in the playground

## Features

- UDP message processing for receiving messages from [Cohda Mk5 OBU](https://www.cohdawireless.com/solutions/hardware/mk5-obu/).
- MAPEM/SPATEM message decoding using [asn1tools](https://github.com/eerimoq/asn1tools) and the [ASN specification](https://forge.etsi.org/rep/ITS/asn1/is_ts103301) provided by ETSI.
- GraphQL API server using [Flask](https://flask.palletsprojects.com/en/2.0.x/) and [Ariadne](https://ariadnegraphql.org/) for transmitting the data to clients.

## Missing Features

- Processing of all available data
- Realtime processing
- Performance 
