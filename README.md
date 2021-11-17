# V2X Server

This is the repository of the V2X Server which can receive, decode and transmit the C-ITS messages MAPEM and SPATEM.

Please note that the project is a very early stage. This means essential parts like error handling, documentation/comments, logging and many other features are missing!

## Getting started

1. Clone repository and open terminal in main folder
2. Install packages with `pip install -r requirements.txt`
3. Start server with `python3 -m v2x_server`. In case you want to start the server with sample data use `python3 -m v2x_server debug`

## Features

- UDP message processing for receiving messages
- MAPEM/SPATEM message decoding using asn1tools and the ASN specification provided by ETSI
- GraphQL API server using Flask and Ariadne for transmitting the data to clients

## Missing Features

- All available data processed
- Realtime processing


