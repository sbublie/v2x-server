import threading
from flask import Flask
from flask_cors import CORS
import logging

from message_service import MessageService
from udp_service import UdpService
from graphql_api import client


def main():

    # Create a new Flask app
    app = Flask(__name__)
    # Initialize CORS handling to avoid any preflight or cross reference errors
    CORS(app)

    # Initialize GraphQL client for request handling
    client.initialize(app, message_service)

    # Run the Flask app on localhost with port 5000
    app.run(host="0.0.0.0", port=5000)


if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    # The UdpService decodes the messages which can then be accessed by the MessageService
    udp_service = UdpService()
    message_service = MessageService(udp_service)

    # The idea here is to run the MAPEM/SPATEM message decoding and the web server on different threads
    # TODO: Optimize multithreding
    udp_thread = threading.Thread(
        target=udp_service.resolve_udp_packets, daemon=False)
    udp_thread.start()
    main()
